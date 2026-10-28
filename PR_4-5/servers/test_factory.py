
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from servers.models import (
    ServerFactory, ChangeFactory, UserFactory,
    ReplicationStatusFactory, ProcedureFactory,
)

print("=" * 60)
print("ТЕСТ FACTORY — все 5 фабрик")
print("=" * 60)

print("\n1. ServerFactory:")
for t in ServerFactory.get_available_types():
    s = ServerFactory.create_server(t, f"{t}-db", "10.0.0.1")
    print(f"  {s.get_info()}")

print("\n2. ChangeFactory:")
for t in ChangeFactory.get_available_types():
    c = ChangeFactory.create_change(t, "test_table", "детали")
    print(f"  {c.execute()}")

print("\n3. UserFactory:")
for t in UserFactory.get_available_types():
    u = UserFactory.create_user(t, f"user_{t}")
    print(f"  {u.get_info()}")

print("\n4. ReplicationStatusFactory:")
for t in ReplicationStatusFactory.get_available_types():
    r = ReplicationStatusFactory.create_status(t, f"node_{t}", 5.0)
    print(f"  {r.get_info()}")

print("\n5. ProcedureFactory:")
for t in ProcedureFactory.get_available_types():
    p = ProcedureFactory.create_procedure(t, f"proc_{t}")
    print(f"  {p.get_info()}")

print("\n6. Обработка ошибок:")
try:
    ServerFactory.create_server("mongodb", "x", "y")
except ValueError as e:
    print(f"  Ошибка перехвачена: {e}")

print("\n✓ Все Factory работают корректно.")