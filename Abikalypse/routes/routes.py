"""Implements the routes for the app
"""

import re
import os

from aiohttp.web import Request, RouteTableDef
from aiohttp import web
import aiohttp_jinja2

from Abikalypse import database


mongodb = database.MongoDB()
routes  = RouteTableDef()


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def index(request: Request) -> None:
    """Represents the homepage
    """


@routes.get('/überlebende')
@aiohttp_jinja2.template('survivors/index.html')
async def student_index(request: Request) -> dict:
    """Represents the index page of all survivors
    """

    return {
        'students': mongodb.fetch_all_students()
    }


@routes.get('/überlebende/{id:\d{8}}')
@aiohttp_jinja2.template('survivors/profile.html')
async def student_page(request: Request) -> dict:
    """Represents the unique profile page of a student
    """

    student = mongodb.find_student(int(request.match_info.get('id')))

    if not student:
        return web.Response(status=400)

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
        return web.Response(status=400)

    if not re.match(r'[a-zA-Z]\w+', username):
        return  web.Response(status=400)

    try:
        mongodb.insert_guestbook_entry(int(request.match_info.get('id')), data['username'], data['content'])
    except database.StudentExistsError:
        return  web.Response(status=400)

    if data.get('context-url') and re.search(rf'{request.host}.*?%C3%BCberlebende\/\d+', data['context-url']):
        raise web.HTTPFound(data['context-url'] + '#guest-book')

    raise web.HTTPFound('/überlebende')


@routes.get('/fotos')
@aiohttp_jinja2.template('photos/index.html')
async def photo_index(request: Request) -> None:
    """Index page of the photos
    """

    return {
        'files': os.listdir('./img/group_photos/')
    }


@routes.get('/robots.txt')
async def robots(request) -> None:
    with open('../robots.txt') as f:
        return web.Response(text=f.read())