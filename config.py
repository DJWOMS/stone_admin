from esmerald import settings
from esmerald.conf.global_settings import EsmeraldAPISettings
from esmerald_simple_jwt.config import SimpleJWT


class StoneSettings(EsmeraldAPISettings):

    @property
    def simple_jwt(self) -> SimpleJWT:
        from contrib.auth.backends import BackendAuthentication, RefreshAuthentication

        return SimpleJWT(
            signing_key=settings.secret_key,
            backend_authentication=BackendAuthentication,
            backend_refresh=RefreshAuthentication,
        )
