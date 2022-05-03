from .DataBaseError import DataBaseError


class StudentExistsError(DataBaseError):
    """Given context can't be resolved to a student
    """
