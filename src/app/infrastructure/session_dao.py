from .base_dao import BaseDAO
from model.chat_session import ChatSession
from model.user import User
import datetime
from uuid import uuid5, NAMESPACE_DNS


class SessionDAO(BaseDAO):
    def create_chat_session_from_object(self, chat_session: ChatSession) -> str:
        query = 'INSERT INTO sessions (id, username, adk_session_id, agent_name, summary, created_at) VALUES (%s, %s, %s, %s, %s, %s)'
        params = (
            chat_session.db_id,
            chat_session.user_name,
            chat_session.adk_session_id,
            chat_session.agent_name,
            chat_session.summary,
            chat_session.created_at,
        )
        self.execute(query, params, commit=True)
        return chat_session.db_id

    def get_sessions_for_user(self, user: User) -> list[ChatSession]:
        rows = self.fetch_all(
            'SELECT id, adk_session_id, agent_name, summary, created_at FROM sessions WHERE username = %s ORDER BY created_at DESC',
            (user.name,),
        )
        return [
            ChatSession(
                db_id=row['id'],
                adk_session_id=row['adk_session_id'],
                user_name=user.name,
                agent_name=row['agent_name'],
                created_at=row['created_at'],
                summary=row['summary'] or f'Chat com {row['agent_name']}',
            )
            for row in rows
        ]

    def get_session_details(self, session_db_id: str) -> ChatSession | None:
        row = self.fetch_one(
            'SELECT id, username, adk_session_id, agent_name, summary, created_at FROM sessions WHERE id = %s',
            (session_db_id,),
        )
        if row:
            return ChatSession(
                db_id=row['id'],
                adk_session_id=row['adk_session_id'],
                user_name=row['username'],
                agent_name=row['agent_name'],
                created_at=row['created_at'],
                summary=row['summary'] or f'Chat com {row['agent_name']}',
            )
        return None
