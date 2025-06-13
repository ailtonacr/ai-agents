import streamlit as st
import uuid

from controller.chat_controller import ChatController
from infrastructure.user_dao import UserDAO
from infrastructure.session_dao import SessionDAO
from infrastructure.message_dao import MessageDAO
from infrastructure.auth import AuthService
from infrastructure.adk_client import ADKClient
from infrastructure.schema_init import init_db
from view.styling import CHAT_STYLES
from view.admin_views import admin_panel_view
from view.auth_views import login_view, registration_view
from view.main_app_view import main_app_view

st.set_page_config(layout='wide', page_title='ADK Chat UI')
st.markdown(CHAT_STYLES, unsafe_allow_html=True)

adk_client = ADKClient()

init_db()

user_dao = UserDAO()
session_dao = SessionDAO()
message_dao = MessageDAO()

auth = AuthService(user_dao)


def init_session_state() -> None:
    defaults = {
        'logged_in_user': None,
        'user_role': None,
        'current_view': 'login',
        'available_agents': [],
        'selected_agent_for_new_chat': None,
        'current_session_db_id': None,
        'current_adk_session_id': None,
        'active_chat_agent_name': 'Agente',
        'active_chat_messages': [],
        'chat_input_key_counter': 0,
        'show_agent_selector': False,
        'user_id_for_adk': None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if user_dao.count_users() == 0 and st.session_state.current_view not in ['initial_setup', 'register']:
        st.session_state.current_view = 'initial_setup'


init_session_state()


def get_adk_user_id(username: str) -> str:
    return f'user-{uuid.uuid5(uuid.NAMESPACE_DNS, username)}'


chat_controller = ChatController(adk_client, session_dao, message_dao, get_adk_user_id)


if st.session_state.current_view == 'initial_setup':
    registration_view(auth, is_initial_setup=True)
elif st.session_state.current_view == 'login':
    login_view(auth, get_adk_user_id)
elif st.session_state.current_view == 'register':
    registration_view(auth)
elif st.session_state.current_view == 'app' and st.session_state.logged_in_user:
    main_app_view(chat_controller, session_dao)
elif st.session_state.current_view == 'admin_panel' and st.session_state.user_role == 'admin':
    admin_panel_view(user_dao)
else:
    st.session_state.current_view = 'login'
    st.rerun()
