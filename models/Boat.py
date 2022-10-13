from typing import Optional

from models.Record import Record


class Boat(Record):
    __name: str  # headline
    __link: str  # link to boat page
    __price: str  # boat price
    __location: str  # boat location
    __year: Optional[int]  # year the boat was built
    __length: Optional[float]  # boat length
    __beam: Optional[float]  # boat width
    __draft: Optional[float]  # boat draft
    __hull_material: Optional[str]  # boat hull material
    __fuel_type: Optional[str]  # type of fuel the engine runs on
    __other_param: Optional[str]  # other characteristics of the boat
    __description: Optional[str]  # boat description
    __photo: Optional[int]  # boat photo
    __category: Optional[str]  # sailboat or motorboat
    __type: Optional[str]  # type of boat within a category

    def __init__(self, name: str, price: str, link: str, location: str = "", year: str = None, length: str = None,
                 beam: str = None, draft: str = None, hull_material: str = None, fuel_type: str = None,
                 other_param: str = None, description: str = None, photo: int = None, category: str = None,
                 boat_type: str = None):
        super().__init__()
        self.set_name(name)
        self.set_price(price)
        self.set_link(link)
        self.set_location(location)
        self.set_year(year)
        self.set_length(length)
        self.set_beam(beam)
        self.set_draft(draft)
        self.set_hull_material(hull_material)
        self.set_fuel_type(fuel_type)
        self.set_other_param(other_param)
        self.set_description(description)
        self.set_photo(photo)
        self.set_category(category)
        self.set_type(boat_type)

    def set_name(self, name: str):
        if type(name) == str:
            self.__name = name
        else:
            self.__name = "Default Name"

    def set_link(self, link: str):
        if type(link) == str:
            self.__link = link
        else:
            self.__link = "Default Link"

    def set_price(self, price: str):
        if type(price) == str:
            self.__price = price
        else:
            self.__price = "$ 0.0"

    def set_location(self, location: str):
        if type(location) == str:
            self.__location = location
        else:
            self.__location = "Default Location"

    def set_year(self, year: str):
        try:
            self.__year = int(year)
        except (ValueError, TypeError):
            self.__year = None

    def set_length(self, length: str):
        try:
            self.__length = float(length)
        except (ValueError, TypeError):
            self.__length = None

    def set_beam(self, beam: str):
        try:
            self.__beam = float(beam)
        except (ValueError, TypeError):
            self.__beam = None

    def set_draft(self, draft: str):
        try:
            self.__draft = float(draft)
        except (ValueError, TypeError):
            self.__draft = None

    def set_hull_material(self, hull_material: str):
        if type(hull_material) == str:
            self.__hull_material = hull_material
        else:
            self.__hull_material = None

    def set_fuel_type(self, fuel_type: str):
        if type(fuel_type) == str:
            self.__fuel_type = fuel_type
        else:
            self.__fuel_type = None

    def set_other_param(self, other_param: str):
        if type(other_param) == str:
            self.__other_param = other_param
        else:
            self.__other_param = None

    def set_description(self, description: str):
        if type(description) == str:
            self.__description = description
        else:
            self.__description = None

    def set_photo(self, photo: int):
        try:
            self.__photo = int(photo)
        except (ValueError, TypeError):
            self.__photo = None

    def set_category(self, category: str):
        if type(category) == str:
            self.__category = category
        else:
            self.__category = None

    def set_type(self, boat_type: str):
        if type(boat_type) == str:
            self.__type = boat_type
        else:
            self.__type = None

    def __str__(self):
        return f"{self.__name} Price {self.__price}\nLink {self.__link}\nLocation {self.__location}"

    def __repr__(self):
        return f"<{self.__name} Price: {self.__price} Link: {self.__link} Location: {self.__location}>"

    def to_db(self) -> tuple:
        return self.__name, self.__price, self.__link, self.__location, self.__year, self.__length, self.__beam, \
               self.__draft, self.__hull_material, self.__fuel_type, self.__other_param, self.__description, \
               self.__photo, self.__category, self.__type, *super().to_db()
