from infrastructure.config import configure_streamlit
from infrastructure.app_factory import AppFactory
from infrastructure.session_manager import SessionManager
from controller.router import AppRouter


def main() -> None:
    configure_streamlit()
    
    app_factory = AppFactory()
    app_factory.initialize_database()
    
    session_manager = SessionManager(app_factory.user_dao)
    session_manager.init_session_state()
    
    router = AppRouter(app_factory)
    router.route()


if __name__ == "__main__":
    main()
