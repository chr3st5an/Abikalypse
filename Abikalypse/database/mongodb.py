from typing import Any, Dict, List, NoReturn, Optional
from datetime import datetime, timedelta
from random import randint
from os import PathLike
import functools
import asyncio
import copy
import os

from pymongo import MongoClient
from dotenv import load_dotenv

from .exceptions import *
from .models import *


__all__ = ['MongoDB']

load_dotenv()

DATABASE   = os.getenv('DATABASE')
MONGO_HOST = os.getenv('MONGO_HOST')


class MongoDB(object):
    """Interaction endpoint with MongoDB

    Author
    ------
    @chr3st5an
    """

    def __init__(self, host: str = MONGO_HOST, database: str = DATABASE) -> None:
        """Establish a connection with MongoDB

        Also create all necessary collections

        Parameters
        ----------
        host : str, optional
            Host URL, by default MONGO_HOST
        database : str, optional
            Name of the database to connect to,
            by default DATABASE
        """

        self.__conn = MongoClient(host)[database]

        required_collections  = ['students']
        available_collections = self.__conn.list_collection_names()

        for collection_name in required_collections:
            if collection_name not in available_collections:
                self.__conn.create_collection(collection_name)

    def __find(self, collection: str, key: Any, value: Any) -> Optional[Any]:
        if not (collection and key):
            return None

        return self.__conn[collection].find_one({key: value})

    def __init_student(self, data: Dict[str, Any]) -> Student:
        data = copy.deepcopy(data)

        if data.get('photo'):
            data['photo'] = Photo(**data['photo'])

        return Student(**data)

    def find_student(self, _id: Optional[int]) -> Optional[Student]:
        """Find a student by its unique identifier

        Parameters
        ----------
        _id : int, optional
            Unique identifier of the student

        Returns
        -------
        Student, optional
            the student if found or None
        """

        if not (student := self.__find('students', '_id', _id)):
            return None

        return self.__init_student(student)

    def find_student_by_name(self, name: Optional[str]) -> Optional[Student]:
        """Find a student by its name and return the first match

        Parameters
        ----------
        name : str, optional
            The name of the student to look up

        Returns
        -------
        Student, optional
            the student if found or None

        Note
        ----
        Can be inaccurate if multiple students
        have the exact same name
        """

        if not (student := self.__find('students', 'name', name.lower())):
            return None

        return self.__init_student(student)

    @functools.cache
    def fetch_all_students(self) -> List[Student]:
        """Return a list with all students
        """

        return [self.__init_student(data) for data in self.__conn['students'].find()]

    def list_student_names(self) -> List[str]:
        """Retrieve a list containing the names of every student
        that is currently in the database

        Returns
        -------
        List[str]
            list of names
        """

        return [data['name'] for data in self.fetch_all_students()]

    def insert_student(self, name: str, about: Dict[str, Any], photo: Optional[PathLike] = None) -> Student:
        """Create and insert a student into the database

        Parameters
        ----------
        name : str
            The name of the student, e.g. "Max Mustermann"
        about : Dict[str, Any]
            A dict containing data about the student.
            Should be structured like `{"Birthday": <obj>}`
        photo : PathLike, optional
            Path to a valid image file, by default None

        Returns
        -------
        Student
            the student that just got created
        """

        _id = randint(11111111, 99999999)

        # Ensure that the id is unique
        if self.find_student(_id):
            return self.insert_student(name, about, photo)

        student = Student(_id, name, about, Photo.from_path(photo))

        self.__conn['students'].insert_one(student.as_dict())

        return student

    def insert_guestbook_entry(self, target_student_id: int, author: str, content: str) -> dict[str, str]:
        """Create a guest book entry

        Parameters
        ----------
        target_student_id : int
            Unique identifier of the student whose guest book
            is tried to be edited
        author : str
            The author of the message that is tried to be added
        content : str
            The message that is tried to be added

        Returns
        -------
        dict[str, str]
            A dict representing the entry that got inserted

        Raises
        ------
        StudentExistsError
            Student whose guest book is tried to be edited
            does not exist
        """

        if not (student := self.find_student(target_student_id)):
            raise StudentExistsError("mongodb: student doesn't exist")

        entry = {
            'author'       : author,
            'content'      : content,
            'creation_date': datetime.now().strftime('%d/%m/%Y')
        }

        student.guest_book.append(entry)

        self.__conn['students'].update_one({'_id': target_student_id},
            {'$set': {'guest_book': copy.deepcopy(student.guest_book)}}
        )

        return entry

    async def loop_clear_cache(self, hours: int = 12) -> NoReturn:
        """|coro|

        Start a loop which constantly clears the
        cache.

        >>> asyncio.create_task(mongodb.loop_clear_cache())

        Parameters
        ----------
        hours : int
            Set the interval between every clearing
            event, e.g. clear the cache
            every `n` hours, by default 12
        """

        start_time = datetime.now() + timedelta(hours=hours)

        while True:
            if datetime.now() >= start_time and (start_time := datetime.now() + timedelta(hours=hours)):
                await self.clear_cache()

            await asyncio.sleep(30)

    async def clear_cache(self) -> None:
        """|coro|

        Clear the cache
        """

        for attr in dir(self):
            if isinstance(attr := getattr(self, attr), functools._lru_cache_wrapper):
               attr.cache_clear()

            await asyncio.sleep(0)
