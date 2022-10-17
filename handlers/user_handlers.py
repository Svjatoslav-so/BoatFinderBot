import os
import time

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from keyboards import user_keyboards as u_kb
from models.Boat import Boat
from models.DBManager import BoatDB
from models.Filter import Filter
from states import user_states

db = BoatDB(os.environ['database'])


async def start(message: Message, state: FSMContext):
    db.add_user((message.from_user.id,
                 message.from_user.first_name,
                 message.from_user.last_name,
                 message.from_user.username, None, None, None))
    await message.answer("Приветствую!\nИ так сразу к делу ; )\nЖми /search чтобы начать поиск.\n"
                         "Если тебе нужны настройки тогда переходи в /settings.",
                         reply_markup=u_kb.start_kb)
    await state.finish()


async def search(message: Message):
    filters = db.get_filters(message.from_user.id, columns="filter_name")
    if len(filters) <= 0:
        await message.answer("У вас пока нет никаких фильтров. Для того чтобы создать фильтр жми /add_filter.",
                             reply_markup=u_kb.search_kb_1)
    else:
        await message.answer("Выберите фильтр чтобы начать поиск", reply_markup=u_kb.get_filters_kb(filters))
        await user_states.ApplyFilter.SetFilter.set()


async def find(message: Message, state: FSMContext):
    boat_filters = db.get_filters(message.from_user.id, message.text)
    if len(boat_filters) > 0:
        await message.answer("Начнем!", reply_markup=ReplyKeyboardRemove())
        for boat in db.get_boats(Filter.filter_to_dict(boat_filters[0])):
            time.sleep(1.5)
            await message.answer(Boat.show(boat), parse_mode="HTML", reply_markup=u_kb.boat_kb)
        await message.answer("Кажись все)", reply_markup=u_kb.start_kb)
        await state.finish()
    else:
        await message.answer(f'У вас нет фильтра с названием "{message.text}".\n Выберите другой фильтр.')


async def add_filter(message: Message):
    await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить выберите"
                         " /apply или /apply_and_save, чтобы сохранить этот фильтр.", reply_markup=u_kb.add_filter_kb)
    await user_states.AddFilter.AddFilterParam.set()


async def new_filter(message: Message):
    await message.answer("Выберите какие параметры вы хотите настроить. Чтобы сохранить нажмите /save_filter",
                         reply_markup=u_kb.new_filter_kb)
    await user_states.NewFilter.AddFilterParam.set()


async def add_boat_name(message: Message, state: FSMContext):
    await message.answer("Введите название лодки:")
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
    await message.answer("Введите название локации:")
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


async def apply(message: Message, state: FSMContext):
    boat_filter = await state.get_data()
    await message.answer("Начнем!", reply_markup=ReplyKeyboardRemove())
    for boat in db.get_boats(boat_filter):
        time.sleep(1.5)
        await message.answer(Boat.show(boat), parse_mode="HTML", reply_markup=u_kb.boat_kb)
    await message.answer("Кажись все)", reply_markup=u_kb.start_kb)
    await state.finish()


async def add_filter_name(message: Message, state: FSMContext):
    await message.answer("Введите название фильтра:")
    await user_states.AddFilter.SetFilterName.set()


async def apply_and_save(message: Message, state: FSMContext):
    await state.update_data({"filter_name": message.text})
    await state.update_data({"user_id": message.from_user.id})
    boat_filter = await state.get_data()
    db.add_filter(boat_filter)
    await message.answer("Фильтр успешно сохранен!")
    await message.answer("Начнем!", reply_markup=ReplyKeyboardRemove())
    for boat in db.get_boats(boat_filter):
        time.sleep(1.5)
        await message.answer(Boat.show(boat), parse_mode="HTML", reply_markup=u_kb.boat_kb)
    await message.answer("Кажись все)", reply_markup=u_kb.start_kb)
    await state.finish()


async def new_filter_name(message: Message, state: FSMContext):
    await message.answer("Введите название фильтра:")
    await user_states.NewFilter.SetFilterName.set()


async def save_filter(message: Message, state: FSMContext):
    await state.update_data({"filter_name": message.text})
    await state.update_data({"user_id": message.from_user.id})
    boat_filter = await state.get_data()
    db.add_filter(boat_filter)
    await message.answer("Фильтр успешно сохранен!", reply_markup=u_kb.settings_kb)
    await state.finish()


async def settings(message: Message):
    await message.answer("Чтобы вернуться обратно нажмите /menu.\n"
                         "Хотите сохранить новый фильтр жмите /new_filter.\n"
                         "Чтобы посмотреть свои фильтры жмите /my_filters.\n"
                         "Если хотите отредактировать фильтр жмите /edit_filter.", reply_markup=u_kb.settings_kb)


async def menu(message: Message, state: FSMContext):
    await message.answer("/search -  начать поиск.\n/settings - настройки.", reply_markup=u_kb.start_kb)
    await state.finish()


async def my_filters(message: Message):
    filters = db.get_filters(message.from_user.id, columns="filter_name")
    if len(filters) > 0:
        await message.answer("Ваши фильтры:", reply_markup=u_kb.get_my_filters_kb(filters))
    else:
        await message.answer("Вы еще не сохраняли фильтры")


async def my_favorites(message: Message):
    favorites = db.get_favorites(message.from_user.id)
    if len(favorites) > 0:
        await message.answer("Избранное:", reply_markup=u_kb.start_kb)
        for boat in favorites:
            time.sleep(1.5)
            await message.answer(Boat.show(boat), parse_mode="HTML", reply_markup=u_kb.favorites_kb)
        await message.answer("Кажись все)")
    else:
        await message.answer("Вы еще ничего не добавили в избранное")


async def show_filter(callback_query: CallbackQuery):
    raw_filters = db.get_filters(callback_query.from_user.id, callback_query.data)
    if len(raw_filters) > 0:
        boat_filter = Filter.filter_to_dict(raw_filters[0])
        await callback_query.answer(Filter.show(boat_filter), show_alert=True)
    else:
        await callback_query.answer()


async def add_to_favorites(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(u_kb.boat_kb_2)
    link = callback_query.message.entities[len(callback_query.message.entities) - 1].url
    user_id = callback_query.message.chat.id
    db.add_favorites(user_id, link)


async def cancel_favorites(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(u_kb.boat_kb)
    link = callback_query.message.entities[len(callback_query.message.entities) - 1].url
    user_id = callback_query.message.chat.id
    db.delete_favorites(user_id, link)


async def delete_from_favorites(callback_query: CallbackQuery):
    link = callback_query.message.entities[len(callback_query.message.entities) - 1].url
    user_id = callback_query.message.chat.id
    await callback_query.message.delete()
    db.delete_favorites(user_id, link)


async def delete_boat(callback_query: CallbackQuery):
    # print("delete")
    await callback_query.message.delete()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(search, commands="search")
    dp.register_message_handler(add_filter, commands="add_filter", state="*")
    dp.register_message_handler(find, state=user_states.ApplyFilter.SetFilter)
    dp.register_message_handler(add_boat_name, commands="boat_name",
                                state=(user_states.AddFilter.AddFilterParam, user_states.NewFilter.AddFilterParam))
    dp.register_message_handler(set_boat_name,
                                state=(user_states.AddFilter.SetBoatName, user_states.NewFilter.SetBoatName))
    dp.register_message_handler(add_location, commands="location",
                                state=(user_states.AddFilter.AddFilterParam, user_states.NewFilter.AddFilterParam))
    dp.register_message_handler(set_location,
                                state=(user_states.AddFilter.SetLocation, user_states.NewFilter.SetLocation))
    dp.register_message_handler(apply, commands="apply", state=user_states.AddFilter.AddFilterParam)
    dp.register_message_handler(add_filter_name, commands="apply_and_save", state=user_states.AddFilter.AddFilterParam)
    dp.register_message_handler(apply_and_save, state=user_states.AddFilter.SetFilterName)
    dp.register_message_handler(settings, commands="settings")
    dp.register_message_handler(menu, commands="menu")
    dp.register_message_handler(new_filter, commands="new_filter")
    dp.register_message_handler(new_filter_name, commands="save_filter", state=user_states.NewFilter.AddFilterParam)
    dp.register_message_handler(save_filter, state=user_states.NewFilter.SetFilterName)
    dp.register_message_handler(my_filters, commands="my_filters")
    dp.register_message_handler(my_favorites, commands="my_favorites")

    dp.register_callback_query_handler(add_to_favorites, lambda c: c.data == "add_to_favorites")
    dp.register_callback_query_handler(cancel_favorites, lambda c: c.data == "cancel_favorites")
    dp.register_callback_query_handler(delete_from_favorites, lambda c: c.data == "delete_from_favorites")
    dp.register_callback_query_handler(delete_boat, text="delete_boat")
    # ИЛИ МОЖНО ТАК dp.register_callback_query_handler(delete_boat, lambda c: c.data == "delete_boat")
    dp.register_callback_query_handler(show_filter)