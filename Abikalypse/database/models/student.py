from typing import Any, Dict, List, Optional
from copy import deepcopy

from .photo import Photo


class Student(object):
    """Represent a student

    This class is mainly intended for view-only purposes
    and hence does not offer large functionality.

    Attributes
    ----------
    _id : int
        Unique identifier of the student. No other
        student should have the same identifier.
    name : str
        The full name of the student, e.g. "Max Wahnhausen"
    about : Dict[str, str]
        Data about the student structured like
        `{'Hates': 'I hate art', ...}` which gets displayed
        on their profile page.
    photo : database.models.Photo
        Photo of the student
    guest_book : List[Dict[str, str]]
        List containing guest book entries. Should be
        structured like `[{'author': '', 'content': '', 'creation_date': ''}, ...]`

    Properties
    ----------
    forename : str
        The forename of the student
    surname : str
        The surname of the student
    has_photo : bool
        If a photo of the student is available

    Methods
    -------
    as_dict() -> Dict[str, Any]
        Return a dict representing the student

    Supported Operations
    --------------------
    `str(obj)`
        Return a str representation of the student
    `int(obj)`
        Return the identifier of the student

    Author
    ------
    @chr3st5an
    """

    def __init__(self,
        _id: int,
        name: str,
        about: Dict[str, str],
        photo: Optional[Photo] = None,
        guest_book: Optional[List[Dict[str, str]]] = None
    ) -> None:
        """Create a student instance

        Parameters
        ----------
        _id : int
            Unique identifier of the student. Should be
            unique among all other objects.
        name : str
            The name of the studen, e.g. "Max Wahnhausen"
        about : Dict[str, str]
            Data about the student structured like
            `{'Hates': 'I hate art', ...}` which gets displayed
            on their profile page.
        photo : Optional[Photo], optional
            Photo of the student, by default None
        guest_book : Optional[List[Dict[str, str]]], optional
            List containing guest book entries. Should be
            structured like `[{'author': '', 'content': '', 'creation_date': ''}, ...]`,
            by default None
        """

        self._id        = _id
        self.name       = name
        self.about      = deepcopy(about)
        self.photo      = photo
        self.guest_book = deepcopy(guest_book) if guest_book else []

    def __str__(self) -> str:
        return f'<{self.__class__.__qualname__}(id={self._id}, name=\'{self.name}\')>'

    def __int__(self) -> int:
        return self._id

    @property
    def forename(self) -> str:
        return self.name.split()[0].title()

    @property
    def surname(self) -> str:
        return self.name.split()[1].title()

    @property
    def has_photo(self) -> bool:
        return bool(self.photo)

    def as_dict(self) -> Dict[str, Any]:
        """Return a dict representing the student
        """

        data = {}

        for k, v in self.__dict__.items():
            if hasattr(v, 'as_dict'):
                data[k] = v.as_dict()
            else:
                data[k] = v

        return data
