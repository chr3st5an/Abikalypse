import os
import re

from aiohttp.web_request import Request
from jinja2 import FileSystemLoader
from aiohttp import web
import aiohttp_jinja2

from . import database


__all__ = ['app']

app     = web.Application()
mongodb = database.MongoDB()
path    = os.path.realpath(os.path.dirname(__file__))
routes  = web.RouteTableDef()

aiohttp_jinja2.setup(app, loader=FileSystemLoader(path + '/templates'))


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def index(request: Request) -> None:
    """Represents the homepage
    """


@routes.get('/überlebende')
@aiohttp_jinja2.template('survivors/index.html')
async def student_index(request: Request) -> dict:
    """Represents the index pages of all survivors
    """

    return {
        "students" : mongodb.fetch_all_students()
    }


@routes.get('/überlebende/{id:\d{8}}')
@aiohttp_jinja2.template('survivors/profile.html')
async def student_page(request: Request) -> dict:
    """Represents the unique profile page of a student
    """

    student = mongodb.find_student(int(request.match_info.get('id')))

    if not student:
        return web.Response(text='400: Student doesn\'t exist', status=400)

    return {
        'student' : student,
        'request' : request
    }


@routes.post('/create-comment/{id:\d{8}}')
async def create_comment(request: Request):
    """Creates a guestbook entry
    """

    data = await request.post()

    username, content = data.get('username', ''), data.get('content', '')

    if not ((3 <= len(username) <= 16) and (4 <= len(content) <= 128)):
        return aiohttp_jinja2.render_template('err/400.html', request, None, status=400)

    if not re.match(r'[a-zA-Z]\w+', username):
        return aiohttp_jinja2.render_template('err/400.html', request, None, status=400)

    try:
        mongodb.insert_guestbook_entry(int(request.match_info.get('id')), data['username'], data['content'])
    except database.StudentExistsError:
        return aiohttp_jinja2.render_template('err/400.html', request, None, status=400)

    if data.get('context-url') and re.search(rf'{request.host}.*?%C3%BCberlebende\/\d+', data['context-url']):
        raise web.HTTPFound(data['context-url'] + '#guest-book')

    raise web.HTTPFound('/überlebende')


@routes.get('/fotos')
@aiohttp_jinja2.template('photos/index.html')
async def photo_index(request: Request) -> None:
    """Index page of the photos
    """

    return {
        'files': os.listdir(path + '/img/group_photos/')
    }


def init() -> None:
    """Adds all routes to the app
    """

    routes.static('/css', path + '/static/css')
    routes.static('/js', path + '/static/js')
    routes.static('/img', path + '/img')

    app.router.add_routes(routes)


init()


if __name__ == '__main__':
    web.run_app(app)
