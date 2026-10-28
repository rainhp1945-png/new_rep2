# servers/models.py
"""Factory-классы для управления инфраструктурой БД."""


class DatabaseServer:
    def __init__(self, name: str, ip_address: str):
        self.name = name
        self.ip_address = ip_address

    def get_info(self) -> str:
        raise NotImplementedError()


class PostgreSQLServer(DatabaseServer):
    def get_info(self) -> str:
        return f"PostgreSQL: {self.name} ({self.ip_address}:5432)"


class MySQLServer(DatabaseServer):
    def get_info(self) -> str:
        return f"MySQL: {self.name} ({self.ip_address}:3306)"


class OracleServer(DatabaseServer):
    def get_info(self) -> str:
        return f"Oracle: {self.name} ({self.ip_address}:1521)"


class ServerFactory:
    _registry = {
        "postgresql": PostgreSQLServer,
        "mysql": MySQLServer,
        "oracle": OracleServer,
    }

    @classmethod
    def create_server(cls, server_type: str, name: str, ip: str) -> DatabaseServer:
        server_type = server_type.lower()
        if server_type not in cls._registry:
            raise ValueError(f"Неизвестный тип сервера: {server_type}. "
                             f"Доступные: {list(cls._registry.keys())}")
        return cls._registry[server_type](name, ip)

    @classmethod
    def get_available_types(cls) -> list:
        return list(cls._registry.keys())

class SchemaChange:
    def __init__(self, table_name: str, details: str):
        self.table_name = table_name
        self.details = details

    def execute(self) -> str:
        raise NotImplementedError()


class AlterChange(SchemaChange):
    def execute(self) -> str:
        return f"ALTER TABLE {self.table_name}: {self.details}"


class CreateChange(SchemaChange):
    def execute(self) -> str:
        return f"CREATE TABLE {self.table_name}: {self.details}"


class DropChange(SchemaChange):
    def execute(self) -> str:
        return f"DROP TABLE {self.table_name}: {self.details}"


class RenameChange(SchemaChange):
    def execute(self) -> str:
        return f"RENAME TABLE {self.table_name}: {self.details}"


class ChangeFactory:
    _registry = {
        "alter": AlterChange,
        "create": CreateChange,
        "drop": DropChange,
        "rename": RenameChange,
    }

    @classmethod
    def create_change(cls, change_type: str, table_name: str, details: str) -> SchemaChange:
        change_type = change_type.lower()
        if change_type not in cls._registry:
            raise ValueError(f"Неизвестный тип изменения: {change_type}. "
                             f"Доступные: {list(cls._registry.keys())}")
        return cls._registry[change_type](table_name, details)

    @classmethod
    def get_available_types(cls) -> list:
        return list(cls._registry.keys())


class DatabaseUser:
    def __init__(self, username: str):
        self.username = username

    def get_info(self) -> str:
        raise NotImplementedError()


class AdminUser(DatabaseUser):
    def get_info(self) -> str:
        return f"Admin: {self.username} (полный доступ)"


class DBAUser(DatabaseUser):
    def get_info(self) -> str:
        return f"DBA: {self.username} (управление БД)"


class DeveloperUser(DatabaseUser):
    def get_info(self) -> str:
        return f"Developer: {self.username} (чтение/запись)"


class ReadonlyUser(DatabaseUser):
    def get_info(self) -> str:
        return f"Readonly: {self.username} (только чтение)"


class UserFactory:
    _registry = {
        "admin": AdminUser,
        "dba": DBAUser,
        "developer": DeveloperUser,
        "readonly": ReadonlyUser,
    }

    @classmethod
    def create_user(cls, user_type: str, username: str) -> DatabaseUser:
        user_type = user_type.lower()
        if user_type not in cls._registry:
            raise ValueError(f"Неизвестный тип пользователя: {user_type}. "
                             f"Доступные: {list(cls._registry.keys())}")
        return cls._registry[user_type](username)

    @classmethod
    def get_available_types(cls) -> list:
        return list(cls._registry.keys())


class ReplicationStatus:
    def __init__(self, node: str, delay: float = 0.0):
        self.node = node
        self.delay = delay

    def get_info(self) -> str:
        raise NotImplementedError()


class MasterStatus(ReplicationStatus):
    def get_info(self) -> str:
        return f"MASTER: {self.node} (источник репликации)"


class SlaveStatus(ReplicationStatus):
    def get_info(self) -> str:
        return f"SLAVE: {self.node} (задержка {self.delay} сек)"


class DelayedStatus(ReplicationStatus):
    def get_info(self) -> str:
        return f"DELAYED: {self.node} (критическая задержка {self.delay} сек)"


class ReplicationStatusFactory:
    _registry = {
        "master": MasterStatus,
        "slave": SlaveStatus,
        "delayed": DelayedStatus,
    }

    @classmethod
    def create_status(cls, status_type: str, node: str, delay: float = 0.0) -> ReplicationStatus:
        status_type = status_type.lower()
        if status_type not in cls._registry:
            raise ValueError(f"Неизвестный статус: {status_type}. "
                             f"Доступные: {list(cls._registry.keys())}")
        # Master не принимает delay, поэтому создаём с проверкой
        if status_type == "master":
            return cls._registry[status_type](node)
        return cls._registry[status_type](node, delay)

    @classmethod
    def get_available_types(cls) -> list:
        return list(cls._registry.keys())


class StoredProcedure:
    def __init__(self, name: str):
        self.name = name

    def get_info(self) -> str:
        raise NotImplementedError()


class FunctionProcedure(StoredProcedure):
    def get_info(self) -> str:
        return f"FUNCTION: {self.name}()"


class TriggerProcedure(StoredProcedure):
    def get_info(self) -> str:
        return f"TRIGGER: {self.name} ON TABLE"


class ViewProcedure(StoredProcedure):
    def get_info(self) -> str:
        return f"VIEW: {self.name}"


class ProcedureFactory:
    _registry = {
        "function": FunctionProcedure,
        "trigger": TriggerProcedure,
        "view": ViewProcedure,
    }

    @classmethod
    def create_procedure(cls, proc_type: str, name: str) -> StoredProcedure:
        proc_type = proc_type.lower()
        if proc_type not in cls._registry:
            raise ValueError(f"Неизвестный тип процедуры: {proc_type}. "
                             f"Доступные: {list(cls._registry.keys())}")
        return cls._registry[proc_type](name)

    @classmethod
    def get_available_types(cls) -> list:
        return list(cls._registry.keys())