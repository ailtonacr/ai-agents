import streamlit as st
from infrastructure.auth import AuthService
from model.email import Email


def login_view(auth: AuthService, get_adk_user_id: callable) -> None:
    st.subheader('Login existentes')
    with st.form('login_form'):
        username = st.text_input('Usuário').lower()
        password = st.text_input('Senha', type='password')
        submitted = st.form_submit_button('Login')

        if submitted:
            user = auth.authenticate_user(username, password)
            if user:
                st.session_state.logged_in_user = user
                st.session_state.user_role = getattr(user, 'role', None)
                st.session_state.user_id_for_adk = get_adk_user_id(user.name)
                st.session_state.current_view = 'app'
                st.session_state.current_session_db_id = None
                st.session_state.active_chat_messages = []
                st.rerun()
            else:
                st.error('Usuário ou senha inválidos, ou usuário inativo.')

    if st.button('Não tem uma conta? Cadastre-se'):
        st.session_state.current_view = 'register'
        st.rerun()


def registration_view(auth: AuthService, is_initial_setup: bool = False) -> None:
    st.subheader('Cadastro de Novo Usuário' if not is_initial_setup else 'Cadastro do Primeiro Usuário (Admin)')
    with st.form('registration_form'):
        username = st.text_input('Usuário (letras minúsculas, sem espaços)').lower()
        email_input = st.text_input('Email (opcional)')
        password = st.text_input('Senha (mínimo 6 caracteres)', type='password')
        confirm_password = st.text_input('Confirme a Senha', type='password')
        submitted = st.form_submit_button('Cadastrar')

        if submitted:
            if password != confirm_password:
                st.error('As senhas não coincidem.')
            else:
                try:
                    email = Email(email_input)
                    success, message = auth.register_user(username, password, email)
                    if success:
                        st.success(message)
                        st.session_state.current_view = 'login'
                        st.rerun()
                    else:
                        st.error(message)
                except Exception as e:
                    st.error(str(e))

    if not is_initial_setup:
        if st.button('Já tem uma conta? Faça Login'):
            st.session_state.current_view = 'login'
            st.rerun()
