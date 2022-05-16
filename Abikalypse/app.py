import os

from jinja2 import FileSystemLoader
from aiohttp import web
import aiohttp_jinja2

from Abikalypse.routes import routes, mongodb
from Abikalypse import middlewares


os.chdir(os.path.realpath(os.path.dirname(__file__)))


def create_app() -> web.Application:
    app = web.Application(
        middlewares=[
            middlewares.error_handler(aiohttp_jinja2),
            middlewares.subdomain_access(mongodb)
        ]
    )

    routes.static('/css', './static/css')
    routes.static('/js',  './static/js')
    routes.static('/img', './img')

    app.router.add_routes(routes)

    aiohttp_jinja2.setup(app, loader=FileSystemLoader('./templates'))

    return app


app = create_app()
