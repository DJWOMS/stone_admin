from esmerald import APIView, get, post, put, delete, Request, Response
from ..models import User


class AccountController(APIView):
    path = "/"

    @get()
    async def list(self, request: Request) -> Response:
        return Response({"status": "ok"})

    @post()
    async def post(self) -> Response:
        """
        Generates a superuser
        """
        first_name = "admin"
        last_name = "admin"
        username = "admin"
        email = "admin@localhost.com"
        password = "Test1234"
        name = "admin"

        try:
            await User.query.create_superuser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                name=name,
            )
        except Exception as e:
            return Response({"status": f"{e}"})

        return Response({"status": "ok"})
