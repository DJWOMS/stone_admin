import edgy
# from esmerald.conf import settings
from admin_test.src.configs.db_connection import get_db_connection, get_db_connection_edgy

_, registry = get_db_connection_edgy()

# from admin_test.src.configs.settings import AppSettings
# database, registry = AppSettings().registry


class Price(edgy.Model):
    id: int = edgy.IntegerField(primary_key=True)
    name: str = edgy.CharField(max_length=255)
    description: str = edgy.CharField(max_length=255)
    is_active: bool = edgy.BooleanField(default=True)

    class Meta:
        registry = registry
