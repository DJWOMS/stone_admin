#!/usr/bin/env python
import os
import sys
from edgy import Migrate
from esmerald import Esmerald, Include, Pluggable, conf, Gateway

from admin_test.src.apps.account.admin import UserAdmin
from admin_test.src.apps.account.v1.urls import route_patterns
from admin_test.src.apps.price.admin import PriceAdmin
from admin_test.src.apps.price.models import Price
from admin_test.src.configs.db_connection import get_db_connection, get_db_connection_edgy

from admin_test.src.apps.account.models import User
from admin_test.src.configs.settings import AppSettings
from core import StoneAdmin
from extension import StoneAdminExtension


def build_path():
    """
    Builds the path of the project and project root.
    """
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

    if SITE_ROOT not in sys.path:
        sys.path.append(SITE_ROOT)
        sys.path.append(os.path.join(SITE_ROOT, "apps"))


def get_application():
    """
    This is optional. The function is only used for organisation purposes.
    """
    build_path()

    database, registry = get_db_connection_edgy()

    admin = StoneAdmin()
    admin.add_view(UserAdmin(User))
    admin.add_view(PriceAdmin(Price))

    app = Esmerald(
        routes=route_patterns,
        pluggables={
            "stone_admin": Pluggable(
                StoneAdminExtension,
                path="/admin",
                admin=admin
            )
        },
        on_startup=[database.connect],
        on_shutdown=[database.disconnect],
        debug=True
    )

    Migrate(
        app,
        registry,
        # model_apps={
        #     "accounts": "accounts.models",
        #     "price": "price.models",
        # },
    )

    return app


app = get_application()
