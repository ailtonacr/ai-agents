from .base_dao import BaseDAO
from model.message import Message


class MessageDAO(BaseDAO):
    def add_message(self, session_db_id: str, message: Message):
        query = 'INSERT INTO messages (session_db_id, role, text, timestamp) VALUES (%s, %s, %s, %s)'
        params = (session_db_id, message.role, message.text, message.timestamp)
        self.execute(query, params, commit=True)

    def get_messages_for_session(self, session_db_id: str) -> list[Message]:
        rows = self.fetch_all(
            'SELECT role, text, timestamp FROM messages WHERE session_db_id = %s ORDER BY timestamp ASC',
            (session_db_id,),
        )
        messages = []
        for row in rows:
            message = Message(role=row['role'], text=row['text'], timestamp=row['timestamp'])
            messages.append(message)
        return messages
