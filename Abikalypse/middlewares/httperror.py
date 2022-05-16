from typing import Callable, Coroutine

from aiohttp.web_request import Request
from aiohttp import web
import aiohttp_jinja2


def error_handler(jinja2: aiohttp_jinja2) -> Coroutine:
    """|middleware_factory|

    Return a custom error page when a handler
    returns the code `4xx`

    Parameters
    ----------
    jinja2 : Module(aiohttp_jinja2)
        The aiohttp_jinja2 module used by the main
        app. Used for rendering the error template.

    Returns
    -------
    Coroutine
        The middleware
    """

    @web.middleware
    async def inner(request: Request, handler: Callable[[Request], Coroutine]) -> str:
        resp = await handler(request)

        if str(resp.status).startswith('4'):
            return jinja2.render_template('err/error.html', request, {'status': resp.status}, status=resp.status)

        return resp

    return inner
