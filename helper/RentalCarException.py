class RentalCarException (Exception):
    """child of Exception class to be used for exceptions"""
    pass

class DatabaseException (RentalCarException):
    """child of Exception class to be used for exceptions"""
    pass

class NoDataException (RentalCarException):
    """child of Exception class to be used for exceptions"""
    pass