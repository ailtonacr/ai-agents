from .base_dao import BaseDAO


def init_db():
    base = BaseDAO()
    conn = base.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            username VARCHAR(20) UNIQUE NOT NULL,
            hashed_password VARCHAR(256) NOT NULL,
            email VARCHAR(50) UNIQUE NULL,
            role VARCHAR(5) NOT NULL DEFAULT 'user',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
    '''
    )
    cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS sessions (
            id VARCHAR(36) PRIMARY KEY,
            username VARCHAR(20) NOT NULL,
            adk_session_id VARCHAR(100) UNIQUE NOT NULL,
            agent_name VARCHAR(30) NOT NULL,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
            )
    '''
    )
    cursor.execute(
        '''
           CREATE TABLE IF NOT EXISTS messages (
           id INTEGER PRIMARY KEY AUTO_INCREMENT,
           session_db_id VARCHAR(36) NOT NULL,
           role VARCHAR(5) NOT NULL,
           text TEXT NOT NULL,
           timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           FOREIGN KEY (session_db_id) REFERENCES sessions (id)
           )
    '''
    )
    conn.commit()
    conn.close()
