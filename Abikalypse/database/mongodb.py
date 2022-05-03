from typing import Any, Dict, List, Optional
from datetime import datetime
from random import randint
from os import PathLike
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

        Create all necessary collections

        Parameters
        ----------
        host : str, optional
            Host URL, by default MONGO_HOST
        database : str, optional
            Name of the database to connect to,
            by default DATABASE
        """

        self.__conn = MongoClient(host)[database]

        required_collections = [
            'students',
            'photos'
        ]

        available_collections = self.__conn.list_collection_names()

        for collection_name in required_collections:
            if collection_name not in available_collections:
                self.__conn.create_collection(collection_name)

    def __find(self, collection: str, key: Any, value: Any) -> Optional[Any]:
        if not (collection and key):
            return None

        return self.__conn[collection].find_one({key: value})

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

        student = self.__find('students', '_id', _id)

        if student is None:
            return None

        if student['photo'] is not None:
            student['photo'] = Photo(**student['photo'])

        return Student(**student) if student else None

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

        student = self.__find('students', 'name', name)

        if student['photo'] is not None:
            student['photo'] = Photo(**student['photo'])

        return Student(**student) if student else None

    def list_student_names(self) -> List[str]:
        """Retrieve a list containing the names of every student
        that is currently in the database

        Returns
        -------
        List[str]
            list of names
        """

        return list(map(lambda data: data['name'], self.__conn['students'].find()))

    def fetch_all_students(self):
        return self.__conn['students'].find()

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
            the student that just got inserted
        """

        _id = randint(11111111, 99999999)

        #> Ensure that the id is unique
        if self.find_student(_id):
            return self.insert_student(name, about, photo)

        student = Student(_id, name, about, Photo.from_path(photo))

        self.__conn['students'].insert_one(student.as_dict())

        return student

    def insert_guestbook_entry(self, _id: int, author: str, content: str) -> None:
        student = self.find_student(_id)

        if not student:
            raise StudentExistsError("mongodb: student doesn't exist")

        entry = {
            'author': author,
            'content': content,
            'creation_date': datetime.now().strftime('%d/%m/%Y')
        }

        #> Adding the entry to the guest book
        student.guest_book.append(entry)

        self.__conn['students'].update_one({'_id': _id},
            {'$set': {'guest_book': copy.deepcopy(student.guest_book)}}
        )
