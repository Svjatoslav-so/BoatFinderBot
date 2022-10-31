from aiogram.dispatcher.filters.state import StatesGroup, State


class ApplyFilter(StatesGroup):
    SetFilter = State()


class AddFilter(StatesGroup):
    AddFilterParam = State()
    SetBoatName = State()
    SetFilterName = State()
    SetLocation = State()
    # Price
    AddPrice = State()
    SetMinPrice = State()
    SetMaxPrice = State()

    SetHullMaterial = State()
    SetCategory = State()
    SetFuelType = State()
    SetBoatType = State()
    # Length
    AddLength = State()
    SetMinLength = State()
    SetMaxLength = State()
    # Year
    AddYear = State()
    SetMinYear = State()
    SetMaxYear = State()


class NewFilter(StatesGroup):
    AddFilterParam = State()
    SetBoatName = State()
    SetFilterName = State()
    SetLocation = State()
    # Price
    AddPrice = State()
    SetMinPrice = State()
    SetMaxPrice = State()

    SetHullMaterial = State()
    SetCategory = State()
    SetFuelType = State()
    SetBoatType = State()
    # Length
    AddLength = State()
    SetMinLength = State()
    SetMaxLength = State()
    # Year
    AddYear = State()
    SetMinYear = State()
    SetMaxYear = State()


class ShowBoats(StatesGroup):
    Next = State()
