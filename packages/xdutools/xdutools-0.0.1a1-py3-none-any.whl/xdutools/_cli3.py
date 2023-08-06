from asgiref.sync import async_to_sync as a2s
from typer import Argument, Option, Typer, get_app_dir, prompt, Context

from xdutools.state import COOKIES_PATH
from httpx import AsyncClient

from xdutools.auth import ids
from xdutools.auth import cookies
from xdutools.auth.utils import create_client

STATE = {}


app = Typer()


def log_in_ids(ctx: Context, username: str, password: str = None) -> "AsyncClient":
    cookie_path = COOKIES_PATH / username
    jar = cookies.load_cookies_from_file(cookie_path)
    client = create_client(cookies=jar)
    if jar:
        u = a2s(ids.get_logged_in_user)(client)
        if u == username:
            ctx.obj["client"] = client
            return client
    password: str = password or prompt("密码")
    a2s(ids.log_in)(username, password, client)
    cookies.save_cookies_to_file(client.cookies)
    ctx.obj["client"] = client


@app.command()
def schedule(client: AsyncClient = Option(..., callback=log_in_ids)):
    from xdutools.apps.schedule import get_lessons, save_lessons_as_wake_up

    return save_lessons_as_wake_up(a2s(get_lessons)(client))


if __name__ == "__main__":
    app()
