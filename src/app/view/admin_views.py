import streamlit as st
from model.user import User
from model.email import Email
from infrastructure.user_dao import UserDAO


def user_menu_popover() -> None:
    _, col_menu = st.columns([10, 0.95])
    with col_menu:
        user = st.session_state.logged_in_user
        if user:
            with st.popover(f'👤 {user.name}', use_container_width=False):
                st.markdown(f'Logado como: **{user.name}** ({getattr(user, 'role', None)})')
                if getattr(user, 'role', None) == 'admin':
                    if st.button('Painel Admin', use_container_width=True, key=f'popover_admin_panel_{user.name}'):
                        st.session_state.current_view = 'admin_panel'
                        st.rerun()
                if st.button('Logout', use_container_width=True, key=f'popover_logout_{user.name}'):
                    for key in [
                        'logged_in_user',
                        'user_role',
                        'current_session_db_id',
                        'active_chat_messages',
                        'user_id_for_adk',
                    ]:
                        st.session_state[key] = None
                    st.session_state.current_view = 'login'
                    st.success('Logout realizado com sucesso!')
                    st.rerun()


def admin_panel_view(user_dao: UserDAO) -> None:
    st.title('👑 Painel de Administração')
    if st.button('← Voltar para o Chat'):
        st.session_state.current_view = 'app'
        st.rerun()

    st.subheader('Gerenciar Usuários')
    users = user_dao.get_all_users()

    if not users:
        st.info('Nenhum usuário encontrado (além de você, se for o único).')
        return

    user_data_for_editor = []
    for u in users:
        user_data_for_editor.append(
            {
                'Usuário': u.name,
                'Email': u.email,
                'Role': u.role,
                'Ativo': 'Ativo' if u.is_active else 'Inativo',
            }
        )

    st.data_editor(
        user_data_for_editor,
        disabled=['Usuário', 'Email', 'Role', 'Ativo'],
        num_rows='dynamic',
        key='admin_user_editor',
    )

    st.caption(
        'Para alterar Role ou status Ativo, modifique na tabela e use os botões abaixo para confirmar ações mais complexas.'
    )

    st.subheader('Ações nos Usuários')
    selected_username = st.selectbox('Selecione o usuário para Ações:', options=[u.name for u in users])

    if selected_username:
        selected_user = next((u for u in users if u.name == selected_username), None)

        if not selected_user:
            st.error('Usuário selecionado não encontrado.')
            st.stop()

        st.subheader(f'Editando: {selected_user.name}')

        col1, col2 = st.columns(2)

        with col1:
            selected_user.name = st.text_input('Nome de Usuário', value=selected_user.name, key='username_input')
            email_input = st.text_input('Email', value=selected_user.email, key='email_input')
            selected_user.password = st.text_input('Nova Senha', key='new_password', type='password')

        with col2:
            role = st.selectbox(
                'Role',
                ['user', 'admin'],
                index=['user', 'admin'].index(selected_user.role),
                key='role_select',
            )
            is_active_str = st.selectbox(
                'Usuário Ativo',
                options=['Ativo', 'Inativo'],
                index=0 if selected_user.is_active else 1,
                key='active_toggle',
            )
            is_active = True if is_active_str == 'Ativo' else False
            confirm_new_password = st.text_input(
                'Confirme sua nova Senha', key='confirm_new_password', type='password'
            )
        st.divider()

        # ============ Action buttons =============
        action_col1, action_col2, _ = st.columns([1, 1, 2])

        if action_col1.button('✓ Salvar Alterações', type='primary', use_container_width=True):
            st.session_state.confirm_action = 'update'

        if action_col2.button('🗑️ Deletar Usuário', type='secondary', use_container_width=True):
            st.session_state.confirm_action = 'delete'

        if st.session_state.get('confirm_action') == 'update':
            st.warning(f'**Tem certeza que deseja SALVAR as alterações para o usuário {selected_username}?**')

            confirm_col1, confirm_col2, _ = st.columns([1, 1, 2])
            if confirm_col1.button('Sim, salvar', key='confirm_update_yes'):
                logged_in_user_name = getattr(st.session_state.logged_in_user, 'name', None)

                if selected_username == logged_in_user_name and role != 'admin':
                    st.error('Você não pode remover seu próprio status de admin.')
                elif selected_username == logged_in_user_name and not is_active:
                    st.error('Você não pode desativar sua própria conta.')
                elif selected_user.password is not None and selected_user.password != confirm_new_password:
                    st.warning('As senhas devem ser iguais, por favor, verifique e tente novamente.')
                else:
                    try:
                        selected_user.email = Email(email_input)
                        user_dao.update_user(selected_user)
                        st.success(f'Usuário {selected_username} atualizado com sucesso!')
                        del st.session_state.confirm_action
                        st.rerun()
                    except Exception as e:
                        st.error(f'Falha ao atualizar o usuário {selected_username}: {e}')

            if confirm_col2.button('Não, cancelar', key='confirm_update_no'):
                del st.session_state.confirm_action
                st.rerun()

        if st.session_state.get('confirm_action') == 'delete':
            st.warning(f'**Tem certeza que deseja DELETAR o usuário {selected_username}? Esta ação é irreversível.**')

            confirm_col1, confirm_col2, _ = st.columns([1, 1, 2])
            if confirm_col1.button('Sim, deletar', key='confirm_delete_yes', type='primary'):
                if selected_username == getattr(st.session_state.logged_in_user, 'name', None):
                    st.error('Você não pode deletar sua própria conta.')
                else:
                    try:
                        user_dao.delete_user(selected_username)
                        st.success(f'Usuário {selected_username} deletado com sucesso.')
                        del st.session_state.confirm_action
                        st.rerun()
                    except Exception as e:
                        st.error(f'Falha ao deletar o usuário: {e}')

            if confirm_col2.button('Não, cancelar', key='confirm_delete_no'):
                del st.session_state.confirm_action
                st.rerun()
