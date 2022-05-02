from __future__ import annotations

from typing import Any, Dict, Optional, Union
from os import PathLike
import base64
import sys
import re


class Photo(object):
    """Represent an image

    Stores raw image data encoded in base64

    Classmethods
    ------------
    cls.from_path(Optional[Union[PathLike, str]])
        Reads the data of the image specified by the
        given path and returns an instance of this class

    Attributes
    ----------
    file_type : str
        The file type of the image such as 'jpg' or 'png'
    ext : str
        Alias for file_type
    size : float
        The size of the raw data in MB
    data : bytes
        Actual image data encoded in base64

    Methods
    -------
    obj.decode()
        Decodes the image data in utf-8
    obj.as_dict()
        Returns a dict representing the object

    Supported Operations
    --------------------
    `str(obj)`
        Returns the str representation of the object

    Author
    ------
    @chr3st5an
    """

    @classmethod
    def from_path(cls, path: Optional[Union[PathLike, str]]) -> Optional[Photo]:
        """Create an Photo instance from an image

        Parameters
        ----------
        path : Union[PathLike, str], optional
            Absolute or relative path that specifies
            the location of an image which is going to
            be represented by this instance

        Returns
        -------
        Photo, optional
            The just created instance or None if path was
            None
        """

        if path is None:
            return None

        file_type = re.findall(r'\.(\w+?)$', path)[0]

        with open(path, 'rb') as img:
            data = base64.b64encode(img.read())

        return cls(file_type, data)

    def __init__(self, file_type: str, data: bytes) -> None:
        """Create a Photo object

        Parameters
        ----------
        file_type : str
            The file type of the given image
        data : bytes
            base64 encoded bytes that represent the image
        """

        if not isinstance(file_type, str):
            raise TypeError(f'excpected type \'str\' instead of \'{file_type.__class__.__qualname__}\'')

        if not isinstance(data, bytes):
            raise TypeError(f'expected type \'bytes\' instead of \'{data.__class__.__qualname__}\'')

        self.__file_type = file_type
        self.__data      = data

    def __str__(self) -> str:
        return f'<{self.__class__.__qualname__}(file_type=\'{self.__file_type}\', data={self.__data[:15] + b"..."})>'

    @property
    def file_type(self):
        """The file type of the image such as `jpg`
        """

        return self.__file_type

    @property
    def ext(self):
        """Alias for file_type
        """

        return self.file_type

    @property
    def data(self) -> bytes:
        """Returns the raw data of the image in base64 encoding
        """

        return self.__data

    @property
    def size(self) -> float:
        """Returns the size of the image in MB
        """

        return sys.getsizeof(self.__data) / 1_000_000

    def decode(self) -> str:
        """Decodes the raw data to utf-8

        Returns
        -------
        str
            Utf-8 decoded image-data str
        """

        return self.data.decode('utf-8')

    def as_dict(self) -> Dict[str, Any]:
        """Retrieve a dict representing this object
        """

        return {
            'file_type': self.ext,
            'data' : self.data
        }
