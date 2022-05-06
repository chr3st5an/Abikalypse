from aiohttp.web import run_app

from Abikalypse import app


if __name__ == '__main__':
    run_app(app, host="localhost")
