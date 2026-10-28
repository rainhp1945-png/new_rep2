from django.shortcuts import render

# Create your views here.
# servers/views.py
from django.http import HttpResponse
from .singleton import (
    DatabaseConnectionManager,
    SchemaChangeLogger,
    UserSessionManager,
    ReplicationMonitor,
    ProcedureRegistry,
)
from .models import (
    ServerFactory,
    ChangeFactory,
    UserFactory,
    ReplicationStatusFactory,
    ProcedureFactory,
)


def index(request):


    conn1 = DatabaseConnectionManager()
    conn2 = DatabaseConnectionManager()
    conn1.get_connection("postgresql")
    conn1.get_connection("mysql")

    logger1 = SchemaChangeLogger()
    logger2 = SchemaChangeLogger()
    logger1.log_change("create", "users", "Создана таблица пользователей")
    logger1.log_change("alter", "orders", "Добавлено поле status")

    session1 = UserSessionManager()
    session2 = UserSessionManager()
    sid = session1.login("admin_ivan", "admin")
    session1.login("dev_petr", "developer")

    monitor1 = ReplicationMonitor()
    monitor2 = ReplicationMonitor()
    monitor1.add_status("db-master", "master")
    monitor1.add_status("db-slave-1", "slave", 0.5)

    registry1 = ProcedureRegistry()
    registry2 = ProcedureRegistry()
    registry1.register("calculate_total", "function")
    registry1.register("update_timestamp", "trigger")

    try:
        servers = [
            ServerFactory.create_server("postgresql", "prod-db", "192.168.1.10"),
            ServerFactory.create_server("mysql", "dev-db", "192.168.1.20"),
            ServerFactory.create_server("oracle", "fin-db", "192.168.1.30"),
        ]
        server_info = [s.get_info() for s in servers]
    except ValueError as e:
        server_info = [f"Ошибка: {e}"]

    try:
        changes = [
            ChangeFactory.create_change("create", "audit", "Таблица аудита"),
            ChangeFactory.create_change("alter", "products", "ADD COLUMN price"),
            ChangeFactory.create_change("drop", "temp", "Удаление"),
            ChangeFactory.create_change("rename", "old", "TO new"),
        ]
        change_info = [c.execute() for c in changes]
    except ValueError as e:
        change_info = [f"Ошибка: {e}"]

    try:
        users = [
            UserFactory.create_user("admin", "admin_ivan"),
            UserFactory.create_user("dba", "dba_petr"),
            UserFactory.create_user("developer", "dev_anna"),
            UserFactory.create_user("readonly", "report_bot"),
        ]
        user_info = [u.get_info() for u in users]
    except ValueError as e:
        user_info = [f"Ошибка: {e}"]

    try:
        repl = [
            ReplicationStatusFactory.create_status("master", "db-master"),
            ReplicationStatusFactory.create_status("slave", "db-slave-1", 0.5),
            ReplicationStatusFactory.create_status("delayed", "db-slave-2", 120.0),
        ]
        repl_info = [r.get_info() for r in repl]
    except ValueError as e:
        repl_info = [f"Ошибка: {e}"]

    try:
        procs = [
            ProcedureFactory.create_procedure("function", "calculate_total"),
            ProcedureFactory.create_procedure("trigger", "update_timestamp"),
            ProcedureFactory.create_procedure("view", "active_users"),
        ]
        proc_info = [p.get_info() for p in procs]
    except ValueError as e:
        proc_info = [f"Ошибка: {e}"]

    html = "<h1>Управление инфраструктурой БД</h1>"


    # Singleton
    html += "<h2>Singleton (id совпадают)</h2><ul>"
    html += f"<li>DatabaseConnectionManager: {conn1 is conn2} (id={id(conn1)})</li>"
    html += f"<li>SchemaChangeLogger: {logger1 is logger2} (id={id(logger1)})</li>"
    html += f"<li>UserSessionManager: {session1 is session2} (id={id(session1)})</li>"
    html += f"<li>ReplicationMonitor: {monitor1 is monitor2} (id={id(monitor1)})</li>"
    html += f"<li>ProcedureRegistry: {registry1 is registry2} (id={id(registry1)})</li>"
    html += "</ul>"

    # Factory
    html += "<h2>Factory (разные типы)</h2>"

    html += "<h3>ServerFactory</h3><ul>"
    for info in server_info:
        html += f"<li>{info}</li>"
    html += f"<li>Доступные: {ServerFactory.get_available_types()}</li></ul>"

    html += "<h3>ChangeFactory</h3><ul>"
    for info in change_info:
        html += f"<li>{info}</li>"
    html += f"<li>Доступные: {ChangeFactory.get_available_types()}</li></ul>"

    html += "<h3>UserFactory</h3><ul>"
    for info in user_info:
        html += f"<li>{info}</li>"
    html += f"<li>Доступные: {UserFactory.get_available_types()}</li></ul>"

    html += "<h3>ReplicationStatusFactory</h3><ul>"
    for info in repl_info:
        html += f"<li>{info}</li>"
    html += f"<li>Доступные: {ReplicationStatusFactory.get_available_types()}</li></ul>"

    html += "<h3>ProcedureFactory</h3><ul>"
    for info in proc_info:
        html += f"<li>{info}</li>"
    html += f"<li>Доступные: {ProcedureFactory.get_available_types()}</li></ul>"

    conn1.clear()
    logger1.clear()
    session1.clear()
    monitor1.clear()
    registry1.clear()

    return HttpResponse(html)


def changes_list(request):

    logger = SchemaChangeLogger()
    logger.log_change("create", "audit_log", "Создана таблица аудита")
    logger.log_change("alter", "users", "Добавлено поле email")

    logs = logger.get_all_logs()
    html = "<h1>Журнал изменений схем БД</h1><ul>"
    for log in logs:
        html += f"<li>{log}</li>"
    html += "</ul><p><a href='/servers/'>На главную</a></p>"
    logger.clear()
    return HttpResponse(html)
