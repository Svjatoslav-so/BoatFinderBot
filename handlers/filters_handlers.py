from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards import user_keyboards as u_kb
from states import user_states


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


async def add_price(message: Message, state: FSMContext):
    await message.answer("Установите минимальную и максимальную цены, чтобы завершить жмите /save_price",
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
    elif message.text == "/save_price":
        await message.answer("Цена сохранена!")
        if await state.get_state() == user_states.AddFilter.AddPrice.state:
            await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить выберите /apply или"
                                 " /apply_and_save, чтобы сохранить этот фильтр.", reply_markup=u_kb.add_filter_kb)
            await user_states.AddFilter.AddFilterParam.set()
        else:
            await message.answer("Выберите какие параметры вы хотите настроить. Чтобы применить жмите /save_filter",
                                 reply_markup=u_kb.new_filter_kb)
            await user_states.NewFilter.AddFilterParam.set()
    else:
        await message.delete()
        await message.answer("Установите минимальную и максимальную цены, чтобы завершить жмите /save_price",
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

