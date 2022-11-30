import datetime
import os

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards import user_keyboards as u_kb
from models.DBManager import BoatDB
from states import user_states

db = BoatDB(os.environ['database'])


async def back_to_filter_settings(message: Message, state: FSMContext):
    if await state.get_state() in [s.state for s in user_states.AddFilter.all_states]:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить выберите /apply или"
                             " /apply_and_save, чтобы сохранить этот фильтр.", reply_markup=u_kb.add_filter_kb)
        await user_states.AddFilter.AddFilterParam.set()
    else:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить жмите /save_filter",
                             reply_markup=u_kb.new_filter_kb)
        await user_states.NewFilter.AddFilterParam.set()


async def add_boat_name(message: Message, state: FSMContext):
    await message.answer("Введите название лодки:", reply_markup=u_kb.get_something_kb([]))
    if await state.get_state() == user_states.AddFilter.AddFilterParam.state:
        await user_states.AddFilter.SetBoatName.set()
    else:
        await user_states.NewFilter.SetBoatName.set()


async def set_boat_name(message: Message, state: FSMContext):
    await state.update_data({"boat_name": message.text})
    if await state.get_state() == user_states.AddFilter.SetBoatName.state:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить выберите /apply или"
                             " /apply_and_save, чтобы сохранить этот фильтр.", reply_markup=u_kb.add_filter_kb)
        await user_states.AddFilter.AddFilterParam.set()
    else:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить жмите /save_filter",
                             reply_markup=u_kb.new_filter_kb)
        await user_states.NewFilter.AddFilterParam.set()


async def add_location(message: Message, state: FSMContext):
    await message.answer("Введите название локации:", reply_markup=u_kb.get_something_kb([]))
    if await state.get_state() == user_states.AddFilter.AddFilterParam.state:
        await user_states.AddFilter.SetLocation.set()
    else:
        await user_states.NewFilter.SetLocation.set()


async def set_location(message: Message, state: FSMContext):
    await state.update_data({"location": message.text})
    if await state.get_state() == user_states.AddFilter.SetLocation.state:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить выберите /apply или"
                             " /apply_and_save, чтобы сохранить этот фильтр.", reply_markup=u_kb.add_filter_kb)
        await user_states.AddFilter.AddFilterParam.set()
    else:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить жмите /save_filter",
                             reply_markup=u_kb.new_filter_kb)
        await user_states.NewFilter.AddFilterParam.set()


async def add_price(message: Message, state: FSMContext):
    await message.answer("Установите минимальную и максимальную цены.",
                         reply_markup=u_kb.price_kb)
    if await state.get_state() == user_states.AddFilter.AddFilterParam.state:
        await user_states.AddFilter.AddPrice.set()
    else:
        await user_states.NewFilter.AddPrice.set()


async def set_price(message: Message, state: FSMContext):
    if message.text == "/min_price":
        await message.answer("Введите минимальную цену(число):")
        if await state.get_state() == user_states.AddFilter.AddPrice.state:
            await user_states.AddFilter.SetMinPrice.set()
        else:
            await user_states.NewFilter.SetMinPrice.set()
    elif message.text == "/max_price":
        await message.answer("Введите максимальную цену(число):")
        if await state.get_state() == user_states.AddFilter.AddPrice.state:
            await user_states.AddFilter.SetMaxPrice.set()
        else:
            await user_states.NewFilter.SetMaxPrice.set()
    else:
        await message.delete()

        await message.answer(f"Установите минимальную и максимальную цены.",
                             reply_markup=u_kb.price_kb)


async def set_min_price(message: Message, state: FSMContext):
    try:
        min_price = float(message.text)
        min_price = 0.0 if min_price < 0 else min_price
    except ValueError:
        min_price = 0.0
    await state.update_data({"min_price": min_price})
    if await state.get_state() == user_states.AddFilter.SetMinPrice.state:
        await user_states.AddFilter.AddPrice.set()
    else:
        await user_states.NewFilter.AddPrice.set()
    await message.answer("Минимальная цена установлена!", reply_markup=u_kb.price_kb)


async def set_max_price(message: Message, state: FSMContext):
    try:
        max_price = float(message.text)
        max_price = 10000000 if max_price < 0 else max_price
    except ValueError:
        max_price = 10000000
    await state.update_data({"max_price": max_price})
    if await state.get_state() == user_states.AddFilter.SetMaxPrice.state:
        await user_states.AddFilter.AddPrice.set()
    else:
        await user_states.NewFilter.AddPrice.set()
    await message.answer("Максимальная цена установлена!", reply_markup=u_kb.price_kb)


async def add_hull_material(message: Message, state: FSMContext):
    materials = db.get_something_distinct("hull_material")
    if len(materials) > 0:
        await message.answer("Выберите материал корпуса:",
                             reply_markup=u_kb.get_something_kb(materials))
    else:
        await message.answer("Введите интересующий вас материал корпуса:")
    if await state.get_state() == user_states.AddFilter.AddFilterParam.state:
        await user_states.AddFilter.SetHullMaterial.set()
    else:
        await user_states.NewFilter.SetHullMaterial.set()


async def set_hull_material(message: Message, state: FSMContext):
    await state.update_data({"hull_material": message.text})
    if await state.get_state() == user_states.AddFilter.SetHullMaterial.state:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить выберите /apply или"
                             " /apply_and_save, чтобы сохранить этот фильтр.", reply_markup=u_kb.add_filter_kb)
        await user_states.AddFilter.AddFilterParam.set()
    else:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить жмите /save_filter",
                             reply_markup=u_kb.new_filter_kb)
        await user_states.NewFilter.AddFilterParam.set()


async def add_category(message: Message, state: FSMContext):
    categories = db.get_something_distinct("category")
    if len(categories) > 0:
        await message.answer("Выберите категорию:",
                             reply_markup=u_kb.get_something_kb(categories))
    else:
        await message.answer("Введите интересующую вас категорию:")
    if await state.get_state() == user_states.AddFilter.AddFilterParam.state:
        await user_states.AddFilter.SetCategory.set()
    else:
        await user_states.NewFilter.SetCategory.set()


async def set_category(message: Message, state: FSMContext):
    await state.update_data({"category": message.text})
    if await state.get_state() == user_states.AddFilter.SetCategory.state:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить выберите /apply или"
                             " /apply_and_save, чтобы сохранить этот фильтр.", reply_markup=u_kb.add_filter_kb)
        await user_states.AddFilter.AddFilterParam.set()
    else:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить жмите /save_filter",
                             reply_markup=u_kb.new_filter_kb)
        await user_states.NewFilter.AddFilterParam.set()


async def add_fuel_type(message: Message, state: FSMContext):
    fuel_types = db.get_something_distinct("fuel_type")
    if len(fuel_types) > 0:
        await message.answer("Выберите топливо:",
                             reply_markup=u_kb.get_something_kb(fuel_types))
    else:
        await message.answer("Введите интересующее вас топливо:")
    if await state.get_state() == user_states.AddFilter.AddFilterParam.state:
        await user_states.AddFilter.SetFuelType.set()
    else:
        await user_states.NewFilter.SetFuelType.set()


async def set_fuel_type(message: Message, state: FSMContext):
    await state.update_data({"fuel_type": message.text})
    if await state.get_state() == user_states.AddFilter.SetFuelType.state:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить выберите /apply или"
                             " /apply_and_save, чтобы сохранить этот фильтр.", reply_markup=u_kb.add_filter_kb)
        await user_states.AddFilter.AddFilterParam.set()
    else:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить жмите /save_filter",
                             reply_markup=u_kb.new_filter_kb)
        await user_states.NewFilter.AddFilterParam.set()


async def add_boat_type(message: Message, state: FSMContext):
    boat_types = db.get_boat_type()
    if len(boat_types) > 0:
        await message.answer("Выберите тип лодки:",
                             reply_markup=u_kb.get_something_kb(boat_types))
    else:
        await message.answer("Введите интересующее вас тип лодки:")
    if await state.get_state() == user_states.AddFilter.AddFilterParam.state:
        await user_states.AddFilter.SetBoatType.set()
    else:
        await user_states.NewFilter.SetBoatType.set()


async def set_boat_type(message: Message, state: FSMContext):
    await state.update_data({"type": message.text})
    if await state.get_state() == user_states.AddFilter.SetBoatType.state:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить выберите /apply или"
                             " /apply_and_save, чтобы сохранить этот фильтр.", reply_markup=u_kb.add_filter_kb)
        await user_states.AddFilter.AddFilterParam.set()
    else:
        await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить жмите /save_filter",
                             reply_markup=u_kb.new_filter_kb)
        await user_states.NewFilter.AddFilterParam.set()


async def add_length(message: Message, state: FSMContext):
    await message.answer("Установите минимальную и максимальную длину корпуса.",
                         reply_markup=u_kb.length_kb)
    if await state.get_state() == user_states.AddFilter.AddFilterParam.state:
        await user_states.AddFilter.AddLength.set()
    else:
        await user_states.NewFilter.AddLength.set()


async def set_length(message: Message, state: FSMContext):
    if message.text == "/min_length":
        await message.answer("Введите минимальную длину(число):")
        if await state.get_state() == user_states.AddFilter.AddLength.state:
            await user_states.AddFilter.SetMinLength.set()
        else:
            await user_states.NewFilter.SetMinLength.set()
    elif message.text == "/max_length":
        await message.answer("Введите максимальную длину(число):")
        if await state.get_state() == user_states.AddFilter.AddLength.state:
            await user_states.AddFilter.SetMaxLength.set()
        else:
            await user_states.NewFilter.SetMaxLength.set()
    else:
        await message.delete()
        await message.answer("Установите минимальную и максимальную длины.",
                             reply_markup=u_kb.length_kb)


async def set_min_length(message: Message, state: FSMContext):
    try:
        min_length = float(message.text)
        min_length = 0.0 if min_length < 0 else min_length
    except ValueError:
        min_length = 0.0
    await state.update_data({"min_length": min_length})
    if await state.get_state() == user_states.AddFilter.SetMinLength.state:
        await user_states.AddFilter.AddLength.set()
    else:
        await user_states.NewFilter.AddLength.set()
    await message.answer("Минимальная длина установлена!", reply_markup=u_kb.length_kb)


async def set_max_length(message: Message, state: FSMContext):
    try:
        max_length = float(message.text)
        max_length = 100 if max_length < 0 else max_length
    except ValueError:
        max_length = 100
    await state.update_data({"max_length": max_length})
    if await state.get_state() == user_states.AddFilter.SetMaxLength.state:
        await user_states.AddFilter.AddLength.set()
    else:
        await user_states.NewFilter.AddLength.set()
    await message.answer("Максимальная длина установлена!", reply_markup=u_kb.length_kb)


async def add_year(message: Message, state: FSMContext):
    await message.answer("Установите минимальный и максимальный год выпуска.",
                         reply_markup=u_kb.year_kb)
    if await state.get_state() == user_states.AddFilter.AddFilterParam.state:
        await user_states.AddFilter.AddYear.set()
    else:
        await user_states.NewFilter.AddYear.set()


async def set_year(message: Message, state: FSMContext):
    if message.text == "/min_year":
        await message.answer("Введите минимальный год выпуска(число):")
        if await state.get_state() == user_states.AddFilter.AddYear.state:
            await user_states.AddFilter.SetMinYear.set()
        else:
            await user_states.NewFilter.SetMinYear.set()
    elif message.text == "/max_year":
        await message.answer("Введите максимальный год выпуска(число):")
        if await state.get_state() == user_states.AddFilter.AddYear.state:
            await user_states.AddFilter.SetMaxYear.set()
        else:
            await user_states.NewFilter.SetMaxYear.set()
    else:
        await message.delete()
        await message.answer("Установите минимальный и максимальный год выпуска.",
                             reply_markup=u_kb.year_kb)


async def set_min_year(message: Message, state: FSMContext):
    try:
        min_year = int(message.text)
        min_year = 1900 if min_year < 1900 else min_year

    except ValueError:
        min_year = 1900
    await state.update_data({"min_year": min_year})
    if await state.get_state() == user_states.AddFilter.SetMinYear.state:
        await user_states.AddFilter.AddYear.set()
    else:
        await user_states.NewFilter.AddYear.set()
    await message.answer("Минимальный год выпуска установлен!", reply_markup=u_kb.year_kb)


async def set_max_year(message: Message, state: FSMContext):
    try:
        max_year = int(message.text)
        max_year = datetime.datetime.now().year if max_year < 1900 else max_year
    except ValueError:
        max_year = datetime.datetime.now().year
    await state.update_data({"max_year": max_year})
    if await state.get_state() == user_states.AddFilter.SetMaxYear.state:
        await user_states.AddFilter.AddYear.set()
    else:
        await user_states.NewFilter.AddYear.set()
    await message.answer("Максимальный год выпуска установлен!", reply_markup=u_kb.year_kb)


async def add_draft(message: Message, state: FSMContext):
    await message.answer("Установите минимальную и максимальную осадку.",
                         reply_markup=u_kb.draft_kb)
    if await state.get_state() == user_states.AddFilter.AddFilterParam.state:
        await user_states.AddFilter.AddDraft.set()
    else:
        await user_states.NewFilter.AddDraft.set()


async def set_draft(message: Message, state: FSMContext):
    if message.text == "/min_draft":
        await message.answer("Введите минимальную осадку(число):")
        if await state.get_state() == user_states.AddFilter.AddDraft.state:
            await user_states.AddFilter.SetMinDraft.set()
        else:
            await user_states.NewFilter.SetMinDraft.set()
    elif message.text == "/max_draft":
        await message.answer("Введите максимальную осадку(число):")
        if await state.get_state() == user_states.AddFilter.AddDraft.state:
            await user_states.AddFilter.SetMaxDraft.set()
        else:
            await user_states.NewFilter.SetMaxDraft.set()
    else:
        await message.delete()
        await message.answer("Установите минимальную и максимальную осадку.",
                             reply_markup=u_kb.length_kb)


async def set_min_draft(message: Message, state: FSMContext):
    try:
        min_draft = float(message.text)
        min_draft = 0.0 if min_draft < 0 else min_draft
    except ValueError:
        min_draft = 0.0
    await state.update_data({"min_draft": min_draft})
    if await state.get_state() == user_states.AddFilter.SetMinDraft.state:
        await user_states.AddFilter.AddDraft.set()
    else:
        await user_states.NewFilter.AddDraft.set()
    await message.answer("Минимальная осадка установлена!", reply_markup=u_kb.draft_kb)


async def set_max_draft(message: Message, state: FSMContext):
    try:
        max_draft = float(message.text)
        max_draft = 3 if max_draft < 0 else max_draft
    except ValueError:
        max_draft = 3
    await state.update_data({"max_draft": max_draft})
    if await state.get_state() == user_states.AddFilter.SetMaxDraft.state:
        await user_states.AddFilter.AddDraft.set()
    else:
        await user_states.NewFilter.AddDraft.set()
    await message.answer("Максимальная осадка установлена!", reply_markup=u_kb.draft_kb)
