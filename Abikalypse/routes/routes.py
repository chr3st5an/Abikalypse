"""Implements the routes for the app
"""

from typing import Any, Dict, List
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
async def student_index(request: Request) -> Dict[str, List[database.Student]]:
    """Represents the index page of all survivors
    """

    return {
        'students': mongodb.fetch_all_students()
    }


@routes.get('/überlebende/{id:\d{8}}')
@aiohttp_jinja2.template('survivors/profile.html')
async def student_page(request: Request) -> Dict[str, Any]:
    """Represents the unique profile page of a student
    """

    student = mongodb.find_student(int(request.match_info.get('id')))

    if not student:
        return web.Response(status=400)

    return {
        'student': student,
        'request': request
    }


@routes.post('/überlebende/{id:\d{8}}')
async def create_comment(request: Request) -> web.Response:
    """Creates a guestbook entry
    """

    data = await request.post()

    username, content = data.get('username', ''), data.get('content', '')

    if not ((3 <= len(username) <= 16) and (4 <= len(content) <= 128)):
        return web.Response(status=400)

    if not re.match(r'[a-zA-Z]\w+', username):
        return web.Response(status=400)

    try:
        entry = mongodb.insert_guestbook_entry(int(request.match_info.get('id')), data['username'], data['content'])
    except database.StudentExistsError:
        return web.Response(status=400)

    return aiohttp_jinja2.render_template(
        template_name='survivors/comment.html',
        request=request,
        context={'comment': entry},
        status=201
    )


@routes.get('/fotos')
@aiohttp_jinja2.template('photos/index.html')
async def photo_index(request: Request) -> Dict[str, List[str]]:
    """Index page of the photos
    """

    return {
        'files': os.listdir('./img/group_photos/')
    }


@routes.get('/robots.txt')
async def robots(request: Request) -> web.Response:
    """Return robots.txt for web crawlers
    """

    with open('../robots.txt') as f:
        return web.Response(text=f.read())
