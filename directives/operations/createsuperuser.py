import argparse
import random
import string
import asyncio
from typing import Any, Type

from esmerald.conf import settings
from esmerald.core.directives import BaseDirective
from esmerald.core.terminal import Print
from esmerald.utils.module_loading import import_string

User = import_string(settings.auth_user_model)

printer = Print()


class Directive(BaseDirective):
    help: str = "Creates a superuser"

    def add_arguments(self, parser: Type["argparse.ArgumentParser"]) -> Any:
        parser.add_argument("--first-name", dest="first_name", type=str, required=True)
        parser.add_argument("--last-name", dest="last_name", type=str, required=True)
        parser.add_argument("--username", dest="username", type=str, required=True)
        parser.add_argument("--email", dest="email", type=str, required=True)
        parser.add_argument("--password", dest="password", type=str, required=True)

    async def handle(self, *args: Any, **options: Any) -> Any:
        """
        Generates a superuser
        """
        first_name = options["first_name"]
        last_name = options["last_name"]
        username = options["username"]
        email = options["email"]
        password = options["password"]

        try:
            user = await User.query.create_superuser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
        except Exception as e:
            printer.write_error(f"User with email {email} already exists.")
            return

        printer.write_success(f"Superuser {user.email} created successfully.")
