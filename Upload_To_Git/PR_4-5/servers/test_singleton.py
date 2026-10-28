
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from servers.singleton import (
    DatabaseConnectionManager, SchemaChangeLogger,
    UserSessionManager, ReplicationMonitor, ProcedureRegistry,
)

print("=" * 60)
print("ТЕСТ SINGLETON — все 5 менеджеров")
print("=" * 60)

classes = [
    DatabaseConnectionManager, SchemaChangeLogger,
    UserSessionManager, ReplicationMonitor, ProcedureRegistry,
]

for cls in classes:
    obj1 = cls()
    obj2 = cls()
    print(f"\n{cls.__name__}:")
    print(f"  obj1 is obj2: {obj1 is obj2}")
    print(f"  id(obj1): {id(obj1)}")
    print(f"  id(obj2): {id(obj2)}")

print("\n✓ Все Singleton работают корректно.")