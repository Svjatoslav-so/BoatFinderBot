import datetime


class Status:
    ACTIVE = "ACTIVE"
    DELETE = "DELETE"


class Record:
    __record_status: str
    __date: datetime.datetime

    def __init__(self):
        self.__record_status = Status.ACTIVE
        self.__date = datetime.datetime.now()

    def delete(self) -> str:
        self.__record_status = Status.DELETE
        return self.__record_status

    def to_db(self) -> tuple:
        return self.__record_status, str(self.__date)
