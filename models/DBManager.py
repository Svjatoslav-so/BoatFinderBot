import functools
import sqlite3
from sqlite3 import Cursor
from typing import Optional

from models.Boat import Boat


class BoatDB:
    _boats_table = "boats"  # название таблицы для хранения лодок
    _users_table = "users"  # название таблицы для хранения пользователей
    _filters_table = "filters"  # название таблицы для хранения фильтров пользователя
    _favorites_table = "favorites"  # название таблицы для хранения избранных объявлений пользователя
    _db_name: str  # название базы данных

    def __init__(self, db_name):
        self.set_db_name(db_name)

    def set_db_name(self, db_name: str):
        if db_name.endswith(".db"):
            self._db_name = db_name
        else:
            self._db_name = db_name + ".db"

    def get_boat_table_name(self):
        return self._boats_table

    def create_boats_table(self, cur: Cursor):
        """Данная функция создает в базе данных таблицу для хранения лодок."""
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self._boats_table}(
                        title TEXT NOT NULL,
                        price TEXT,
                        price_num REAL,
                        link TEXT PRIMARY KEY NOT NULL,
                        location TEXT,
                        year INTEGER,
                        length REAL,
                        beam REAL,
                        draft REAL,
                        hull_material TEXT,
                        fuel_type TEXT,
                        other_param TEXT,
                        description TEXT,
                        photo INTEGER,
                        category TEXT,
                        type TEXT,
                        ad_status TEXT,
                        date TEXT                        
                        )""")

    def create_users_table(self, cur: Cursor):
        """Данная функция создает в базе данных таблицу для хранения пользователей. """
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self._users_table}(
                        id INTEGER PRIMARY KEY NOT NULL,
                        first_name TEXT,
                        last_name TEXT,
                        username TEXT,
                        email TEXT,
                        phone TEXT,
                        location TEXT
                        );""")

    def create_filters_table(self, cur: Cursor):
        """Данная функция создает в базе данных таблицу для хранения пользовательских фильтров. """
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self._filters_table}(
                        user_id INTEGER NOT NULL,
                        filter_name TEXT NOT NULL,
                        boat_name TEXT,
                        min_price REAL,
                        max_price REAL,
                        location TEXT,
                        min_year INTEGER,
                        max_year INTEGER,
                        min_length REAL,
                        max_length REAL,
                        min_draft REAL,
                        max_draft REAL,
                        hull_material TEXT,
                        fuel_type TEXT,
                        category TEXT,
                        type TEXT,
                        PRIMARY KEY(user_id, filter_name)
                        FOREIGN KEY(user_id) REFERENCES {self._users_table} (id) ON DELETE CASCADE
                        );""")

    def create_favorites_table(self, cur: Cursor):
        """Данная функция создает в базе данных таблицу для хранения избранных объявлений пользователя."""
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self._favorites_table}(
                        user_id INTEGER NOT NULL,
                        link TEXT NOT NULL,
                        PRIMARY KEY(user_id, link)
                        FOREIGN KEY(user_id) REFERENCES {self._users_table} (id) ON DELETE CASCADE
                        );""")

    def create_db(self):
        """Данная функция создает базу данных и таблицы в ней. """
        con = sqlite3.connect(self._db_name)
        cur = con.cursor()
        self.create_boats_table(cur)
        self.create_users_table(cur)
        self.create_filters_table(cur)
        self.create_favorites_table(cur)
        con.close()

    def add_boats(self, boats: list[Boat]):
        """
        Данная функция добавляет лодки в таблицу лодок в базе данных.

        Args:
            boats: список кортежей(каждый кортеж описывает лодку).
                   Размерность кортежа должна совпадать с количеством столбцов в таблице лодок в базе данных.
                   Если какой-либо параметр для лодки не указан, то необходимо указать None.
        """
        con = sqlite3.connect(self._db_name)
        cur = con.cursor()
        placeholders = "?, " * (len(boats[0].to_db()) - 1) + "?"
        cur.executemany(f"""REPLACE INTO {self._boats_table} VALUES({placeholders})""", [b.to_db() for b in boats])
        con.commit()
        con.close()

    def add_user(self, user: tuple[int, str, str, str, Optional[str], Optional[str], Optional[str]]):
        """
        Данная функция добавляет пользователя в таблицу пользователей в базе данных.

        Args:
            user: кортеж описывающий пользователя. Размерность кортежа должна совпадать с количеством столбцов
                  в таблице пользователей в базе данных. Если какой-либо параметр для пользователя не указан,
                  то необходимо указать None.
        """
        con = sqlite3.connect(self._db_name)
        cur = con.cursor()
        placeholders = "?, " * (len(user) - 1) + "?"
        cur.execute(f"""REPLACE INTO {self._users_table} VALUES({placeholders})""", user)
        con.commit()
        con.close()

    def add_filter(self, boat_filter: dict):
        """
        Данная функция добавляет фильтр в таблицу пользовательских фильтров в базе данных.

        Args:
            boat_filter: словарь описывающий фильтр(ключи для словаря берутся из множества названий столбцов таблицы
                         фильтра в базе данных). В словаре указываются только те параметры
                         для которых установлены значения.
        """
        keys = list(boat_filter.keys())
        values = list(boat_filter.values())

        con = sqlite3.connect(self._db_name)
        cur = con.cursor()
        cur.execute(f"""REPLACE INTO {self._filters_table} 
                        ({functools.reduce(lambda x, y: x + y + ", ", keys, "")[:-2]})
                        VALUES({functools.reduce(lambda x, y: x + '"' + str(y) + '"' + ', ', values, "")[:-2]})""")
        con.commit()
        con.close()

    def add_favorites(self, user_id: int, link: str):
        """
            Данная функция добавляет избранное объявление пользователя в таблицу избранного в базе данных.

            Args:
                user_id: id пользователя.
                link: ссылка на объявление на сайте(т.к. это PRIMARY KEY таблицы лодок).
            """
        con = sqlite3.connect(self._db_name)
        cur = con.cursor()
        cur.execute(f"""REPLACE INTO {self._favorites_table} 
                    (user_id, link)
                    VALUES("{user_id}", "{link}")""")
        con.commit()
        con.close()

    def get_user(self, user_id: int, columns: str = "*") -> tuple | None:
        """
        Данная функция ищет пользователя по id в таблице позьзователей в базе данных.

        Args:
            user_id: id позьзователя которого мы ищем.
            columns: строка содержащая названия столбцов таблицы пользователей, значения которых мы хотим получить.
                     По умолчанию "*" - все столбцы.
        Returns:
            Функция возвращает кортеж со значениями столбцов указанных в columns.
        """
        try:
            con = sqlite3.connect(self._db_name)
            cur = con.cursor()
            res = cur.execute(f"""SELECT {columns} FROM {self._users_table} WHERE id = {str(user_id)}""")
            user = res.fetchone()
            con.close()
            return user
        except sqlite3.OperationalError as e:
            print(f"Error in function {self.get_user} ->", e)

    def get_filters(self, user_id: int, filter_name: str = None, columns: str = "*") -> list | None:
        """
        Данная функция ищет фильтр по id в таблице фильтров в базе данных.

        Args:
            user_id: id позьзователя фильтр которого мы ищем.
            filter_name: название фильтра который мы ищем.
            columns: строка содержащая названия столбцов таблицы фильтров, значения которых мы хотим получить.
                     По умолчанию "*" - все столбцы.
        Returns:
            Функция возвращает кортеж со значениями столбцов указанных в columns.
        """
        try:
            con = sqlite3.connect(self._db_name)
            cur = con.cursor()
            request = f"""SELECT {columns} FROM {self._filters_table} WHERE user_id = {str(user_id)}"""
            request += f""" AND filter_name = "{filter_name}" """ if not (filter_name is None) else ""
            print(request)
            res = cur.execute(request)
            u_filter = res.fetchall()
            con.close()
            return u_filter
        except sqlite3.OperationalError as e:
            print(f"Error in function {self.get_filters} ->", e)

    @staticmethod
    def __boat_name_filter(boat_filter: dict, filter_name: str = "boat_name", param_name: str = "title") -> str | None:
        """
        Вспомогательная функция, используется для добавления фильтрации поля boat_name таблицы лодок в SQL-запросы.

        Args:
            boat_filter: словарь, описывающий применяемый фильтр.
            filter_name: название параметра фильтра, который мы хотим преобразовать в SQL-фильтр.
                         Название должно быть из множества названий столбцов в таблице фильтра в базе данных.
            param_name:  название параметра лодки на который наклабывается фильтр. Название должно быть из множества
                         названий столбцов в таблице лодок в базе данных.

        Returns:
            Функция возвращает строку(часть SQL-запроса, отвечающую за фильтрацию иказанного параметра), если фильтр на
            указанный параметр есть в словаре boat_filter. Если его нет, тогда пустую строку.
        """
        if filter_name in boat_filter.keys():
            keyword_list = boat_filter[filter_name].split()
            pattern = ""
            for kw in keyword_list:
                pattern += f"% {kw} "
            return f"{param_name} LIKE '{pattern}%' AND "
        return ""

    @staticmethod
    def __location_filter(boat_filter: dict, filter_name: str = "location", param_name: str = "location") -> str | None:
        """
        Вспомогательная функция, используется для добавления фильтрации поля location таблицы лодок в SQL-запросы.

        Args:
            boat_filter: словарь, описывающий применяемый фильтр.
            filter_name: название параметра фильтра, который мы хотим преобразовать в SQL-фильтр.
                         Название должно быть из множества названий столбцов в таблице фильтра в базе данных.
            param_name:  название параметра лодки на который наклабывается фильтр. Название должно быть из множества
                         названий столбцов в таблице лодок в базе данных.

        Returns:
            Функция возвращает строку(часть SQL-запроса, отвечающую за фильтрацию иказанного параметра), если фильтр на
            указанный параметр есть в словаре boat_filter. Если его нет, тогда пустую строку.
        """
        if filter_name in boat_filter.keys():
            keyword_list = boat_filter[filter_name].split()
            pattern = ""
            for kw in keyword_list:
                pattern += f"%{kw}"
            return f"{param_name} LIKE '{pattern}%' AND "
        return ""

    @staticmethod
    def __text_filter(boat_filter: dict, filter_name: str, param_name: str) -> str | None:
        """
        Вспомогательная функция, используется для добавления фильтрации текстовых полей таблицы лодок в SQL-запросы.

        Args:
            boat_filter: словарь, описывающий применяемый фильтр.
            filter_name: название параметра фильтра, который мы хотим преобразовать в SQL-фильтр.
                         Название должно быть из множества названий столбцов в таблице фильтра в базе данных.
            param_name:  название параметра лодки на который наклабывается фильтр. Название должно быть из множества
                         названий столбцов в таблице лодок в базе данных.

        Returns:
            Функция возвращает строку(часть SQL-запроса, отвечающую за фильтрацию иказанного параметра), если фильтр на
            указанный параметр есть в словаре boat_filter. Если его нет, тогда пустую строку.
        """
        if filter_name in boat_filter.keys():
            return f"{param_name} LIKE '%{boat_filter[filter_name]}%' AND "
        return ""

    @staticmethod
    def __range_filter(boat_filter: dict, from_filter_name: str, to_filter_name: str, param_name: str):
        """
        Вспомогательная функция, добавляет диапазон фильтрации для числовых полей в таблице лодок в SQL-запросы.

        Args:
            boat_filter:      словарь, описывающий применяемый фильтр.
            from_filter_name: название параметра фильтра, который указывает начало диапазона для указанного параметра
                              лодки. Название должно быть из множества названий столбцов в таблице фильтра.
            to_filter_name:   название параметра фильтра, который указывает конец диапазона для указанного параметра
                              лодки. Название должно быть из множества названий столбцов в таблице фильтра.
            param_name:       название параметра лодки на который наклабывается фильтр. Название должно быть из
                              множества названий столбцов в таблице лодок в базе данных.

        Returns:
            Функция возвращает строку(часть SQL-запроса, отвечающую за фильтрацию иказанного параметра), если фильтр на
            указанный параметр есть в словаре boat_filter. Если его нет, тогда пустую строку.
        """
        keys = boat_filter.keys()
        if from_filter_name in keys and to_filter_name in keys:
            return f"{param_name} BETWEEN {boat_filter[from_filter_name]} AND {boat_filter[to_filter_name]} AND "
        if from_filter_name in keys:
            return f"{param_name} >= {boat_filter[from_filter_name]} AND "
        if to_filter_name in keys:
            return f"{param_name} <= {boat_filter[to_filter_name]} AND "
        return ""

    def get_boats(self, boat_filter: dict, columns: str = "*") -> list[dict]:
        """
        Данная функция ищет лодки удовлетворяющие фильтру в таблице лодок.

        Args:
            boat_filter: словарь, описывающий применяемый фильтр.
            columns: строка содержащая названия столбцов таблицы лодок, значения которых мы хотим получить.
                     По умолчанию "*" - все столбцы.
        Returns:
            Функция возвращает список словарей со значениями столбцов из таблицы лобок указанных в columns.
        """
        con = sqlite3.connect(self._db_name)
        cur = con.cursor()
        request = f"SELECT {columns} FROM {self._boats_table}"
        if len(boat_filter) > 0:
            request += " WHERE "

            request += self.__boat_name_filter(boat_filter, "boat_name", "title")
            request += self.__location_filter(boat_filter, "location", "location")
            request += self.__text_filter(boat_filter, "hull_material", "hull_material")
            request += self.__text_filter(boat_filter, "fuel_type", "fuel_type")
            request += self.__text_filter(boat_filter, "category", "category")
            request += self.__text_filter(boat_filter, "type", "type")
            request += self.__range_filter(boat_filter, "min_price", "max_price", "price_num")
            request += self.__range_filter(boat_filter, "min_year", "max_year", "year")
            request += self.__range_filter(boat_filter, "min_length", "max_length", "length")
            request += self.__range_filter(boat_filter, "min_draft", "max_draft", "draft")

            request = request[:-4]

        print(request)
        res = cur.execute(request)
        boats = res.fetchall()
        con.close()

        return self.boats_from_tuple_to_dict(boats, columns)

    def get_favorites(self, user_id: int, columns="*") -> list[dict]:
        con = sqlite3.connect(self._db_name)
        cur = con.cursor()
        request = f"""SELECT {columns} FROM {self._boats_table} WHERE link IN (SELECT link FROM {self._favorites_table} 
                   WHERE user_id = "{user_id}");"""
        res = cur.execute(request)
        boats = res.fetchall()
        con.close()
        return self.boats_from_tuple_to_dict(boats, columns)

    def delete_favorites(self, user_id: int, link: str):
        con = sqlite3.connect(self._db_name)
        cur = con.cursor()
        request = f"""DELETE FROM {self._favorites_table} WHERE user_id = "{user_id}" AND link = "{link}";"""
        cur.execute(request)
        con.commit()
        con.close()

    def delete_filter(self, user_id: int, filter_name: str):
        con = sqlite3.connect(self._db_name)
        cur = con.cursor()
        request = f"""DELETE FROM {self._filters_table} WHERE user_id = "{user_id}" AND filter_name = "{filter_name}";"""
        cur.execute(request)
        con.commit()
        con.close()

    @staticmethod
    def boats_from_tuple_to_dict(boats: list[tuple], columns: str) -> list[dict]:
        if columns == "*":
            keys = ["title", "price", "price_num", "link", "location", "year", "length", "beam", "draft",
                    "hull_material",
                    "fuel_type", "other_param", "description", "photo", "category", "type", "ad_status", "date"]
        else:
            keys = [i.replace(",", "") for i in columns.split()]
        boats_dict_list = []
        for boat in boats:
            boats_dict = {}
            for i in range(len(boat)):
                boats_dict.update({keys[i]: boat[i]})
            boats_dict_list.append(boats_dict)
        return boats_dict_list

    def get_something_distinct(self, column: str) -> list[str]:
        con = sqlite3.connect(self._db_name)
        cur = con.cursor()
        request = f"""SELECT DISTINCT {column} FROM {self._boats_table};"""
        res = cur.execute(request)
        result_list = res.fetchall()
        con.close()
        return [r[0] for r in result_list]

    def get_boat_type(self) -> set:
        types_list = self.get_something_distinct("type")
        types_set = set()
        for type_ in types_list:
            types_set.update([t.strip() for t in type_.split(",")])
        return types_set
