import streamlit as st
from .ui_components import display_chat_message, display_sidebar_chat_history
from .admin_views import user_menu_popover
from infrastructure.session_dao import SessionDAO
from controller.chat_controller import ChatController
from model.message import Message


def main_app_view(chat_controller: ChatController, session_dao: SessionDAO) -> None:
    user_menu_popover()
    with st.sidebar:
        st.markdown(f'## 🧠 ADK Chat UI')
        st.markdown('---')
        if st.button('💬 Novo Chat', use_container_width=True, type='primary'):
            st.session_state.show_agent_selector = not st.session_state.show_agent_selector
            if not st.session_state.available_agents:
                st.session_state.available_agents = chat_controller.adk_client.get_available_agents()
        if st.session_state.show_agent_selector:
            if not st.session_state.available_agents:
                st.caption('Buscando agentes...')
                st.session_state.available_agents = chat_controller.adk_client.get_available_agents()
            if st.session_state.available_agents:
                selected_agent = st.selectbox(
                    '🤖 Escolha o Agente para o Novo Chat:',
                    options=[""] + st.session_state.available_agents,
                    index=0,
                    key='new_chat_agent_selector_main_app',
                )
                if selected_agent:
                    chat_controller.start_new_chat_session(selected_agent)
            else:
                st.warning('Nenhum agente disponível.')
        display_sidebar_chat_history(
            session_dao, st.session_state.logged_in_user, st.session_state.current_session_db_id
        )
    if not st.session_state.current_session_db_id:
        st.info('👈 Selecione um chat existente ou clique em "💬 Novo Chat" na barra lateral para começar.')
    else:
        if not st.session_state.active_chat_messages and st.session_state.current_session_db_id:
            chat_controller.load_chat_messages_from_db(st.session_state.current_session_db_id)
        st.subheader(f'Chat com: {st.session_state.active_chat_agent_name}')
        st.markdown('---')
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.active_chat_messages:
                display_chat_message(msg.role, msg.text)
        user_input = st.chat_input(
            'Digite sua mensagem...', key=f'chat_input_{st.session_state.chat_input_key_counter}'
        )
        if user_input:
            new_msg = Message(role='user', text=user_input)
            st.session_state.active_chat_messages.append(new_msg)
            chat_controller.message_dao.add_message(st.session_state.current_session_db_id, new_msg)
            with chat_container:
                display_chat_message('user', user_input)
            with st.spinner(f'{st.session_state.active_chat_agent_name} está digitando...'):
                agent_responses = chat_controller.adk_client.send_message_to_adk(
                    st.session_state.active_chat_agent_name,
                    st.session_state.user_id_for_adk,
                    st.session_state.current_adk_session_id,
                    user_input,
                )
            for resp in agent_responses:
                agent_msg = Message(role=resp['role'], text=resp['text'])
                st.session_state.active_chat_messages.append(agent_msg)
                chat_controller.message_dao.add_message(st.session_state.current_session_db_id, agent_msg)
            st.rerun()
