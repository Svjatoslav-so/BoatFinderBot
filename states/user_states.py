from aiogram.dispatcher.filters.state import StatesGroup, State


class ApplyFilter(StatesGroup):
    SetFilter = State()


class AddFilter(StatesGroup):
    AddFilterParam = State()
    SetBoatName = State()
    SetFilterName = State()
    SetLocation = State()


class NewFilter(StatesGroup):
    AddFilterParam = State()
    SetBoatName = State()
    SetFilterName = State()
    SetLocation = State()