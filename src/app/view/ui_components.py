import streamlit as st
from infrastructure.session_dao import SessionDAO
from model.chat_session import ChatSession
from model.user import User
import html


def display_chat_message(role: str, text: str, is_typing_placeholder=False) -> None:
    align_class = 'user-message' if role == 'user' else 'agent-message'
    if is_typing_placeholder:
        align_class = 'typing-indicator'

    safe_text = html.escape(text)
    st.markdown(
        f'''<div class="chat-message-container {align_class}">
            <div class="chat-bubble">{safe_text}</div>
        </div>''',
        unsafe_allow_html=True,
    )


def display_sidebar_chat_history(session_dao: SessionDAO, user: User, current_session_db_id: str | None) -> None:
    st.sidebar.markdown('---')
    st.sidebar.markdown('<h2 class="sidebar-section-header">Histórico de Chats</h2>', unsafe_allow_html=True)

    if not user:
        st.sidebar.warning('Usuário não identificado para carregar histórico.')
        return

    sessions = session_dao.get_sessions_for_user(user)

    if not sessions:
        st.sidebar.caption('Nenhum chat encontrado.')
        return

    for session in sessions:
        session_id_db = session.db_id
        summary = session.summary if session.summary else f'Chat com {session.agent_name}'
        summary_display = summary[:30] + '...' if len(summary) > 30 else summary

        button_key = f'session_select_{session_id_db}'

        is_selected = session_id_db == current_session_db_id

        button_label = f'▶  {summary_display}' if is_selected else summary_display

        if st.sidebar.button(
            button_label,
            key=button_key,
            help=f'Agente: {session.agent_name}\nCriado em: {session.created_at}',
            use_container_width=True,
        ):
            if st.session_state.current_session_db_id != session_id_db:
                st.session_state.current_session_db_id = session_id_db
                st.session_state.active_chat_messages = []
                session_details = session_dao.get_session_details(session_id_db)
                if session_details:
                    st.session_state.current_adk_session_id = session_details.adk_session_id
                    st.session_state.active_chat_agent_name = session_details.agent_name
            st.rerun()
