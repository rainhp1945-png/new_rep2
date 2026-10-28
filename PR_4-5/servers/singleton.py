# servers/singleton.py

class DatabaseConnectionManager:
    """Singleton: управляет подключениями к разным СУБД."""
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connections = {}
        return cls._instance
    def get_connection(self, db_type: str) -> str:
        if db_type not in self.connections:
            self.connections[db_type] = f"Connection to {db_type}"
        return self.connections[db_type]
    def get_all_connections(self) -> dict:
        return self.connections
    def clear(self):
        self.connections.clear()

class SchemaChangeLogger:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log_change(self, change_type: str, table_name: str, details: str) -> str:
        entry = f"[{change_type.upper()}] {table_name} | {details}"
        self.logs.append(entry)
        return entry

    def get_all_logs(self) -> list:
        return self.logs

    def clear(self):
        self.logs.clear()


class UserSessionManager:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.sessions = {}
        return cls._instance

    def login(self, username: str, role: str) -> str:
        session_id = f"SESS-{len(self.sessions) + 1:03d}"
        self.sessions[session_id] = {"username": username, "role": role}
        return session_id

    def get_sessions(self) -> dict:
        return self.sessions

    def logout(self, session_id: str):
        self.sessions.pop(session_id, None)

    def clear(self):
        self.sessions.clear()


class ReplicationMonitor:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.statuses = []
        return cls._instance

    def add_status(self, node: str, status: str, delay: float = 0.0) -> str:
        entry = f"{node}: {status} (задержка {delay} сек)"
        self.statuses.append(entry)
        return entry

    def get_all_statuses(self) -> list:
        return self.statuses

    def clear(self):
        self.statuses.clear()


class ProcedureRegistry:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.procedures = []
        return cls._instance

    def register(self, name: str, proc_type: str) -> str:
        entry = f"{proc_type}: {name}"
        self.procedures.append(entry)
        return entry

    def get_all_procedures(self) -> list:
        return self.procedures

    def clear(self):
        self.procedures.clear()