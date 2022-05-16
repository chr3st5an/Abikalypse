from typing import Callable, Coroutine
import re

from aiohttp.web_request import Request
from aiohttp import web

from ..database import MongoDB


def subdomain_access(mongodb: MongoDB) -> Coroutine:
    """|middleware_factory|

    Redirects the client when the site is requested
    with a subdomain. This allows `max-mustermann.domain.com`
    to be redirected to `domain.com/überlebende/12345678`.

    Parameters
    ----------
    mongodb : MongoDB
        Database of the main app. Used to retrieve
        students.

    Returns
    -------
    Coroutine
        The middleware
    """

    @web.middleware
    async def inner(request: Request, handler: Callable[[Request], Coroutine]) -> str:
        if subdomain := re.match(r'.+(?=\.[a-z]+\.[a-z]+)', request.host):
            subdomain = subdomain.group(0)
            domain    = request.host.replace(subdomain + '.', '')

            student_name = subdomain.replace('-', ' ')

            if not (student := mongodb.find_student_by_name(student_name)):
                return await handler(request)

            raise web.HTTPFound(f"http://{domain}/überlebende/{student._id}")

        return await handler(request)

    return inner
