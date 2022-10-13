from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def get_filters_kb(btn_name_list: list[str]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.insert(add_filter_btn)
    for btn in btn_name_list:
        new_btn = KeyboardButton(str(btn[0]))
        kb.insert(new_btn)
    return kb


search_btn = KeyboardButton("/search")
add_filter_btn = KeyboardButton("/add_filter")
settings_btn = KeyboardButton("/settings")

year_btn = KeyboardButton("/year")
boat_name_btn = KeyboardButton("/boat_name")
price_btn = KeyboardButton("/price")
location_btn = KeyboardButton("/location")
length_btn = KeyboardButton("/length")
draft_btn = KeyboardButton("/draft")
hull_material_btn = KeyboardButton("/hull_material")
fuel_type_btn = KeyboardButton("/fuel_type")
category_btn = KeyboardButton("/category")
boat_type_btn = KeyboardButton("/boat_type")
apply_btn = KeyboardButton("/apply")
apply_and_save_btn = KeyboardButton("/apply_and_save")

menu_btn = KeyboardButton("/menu")
new_filter_btn = KeyboardButton("/new_filter")
my_filters_btn = KeyboardButton("/my_filters")
edit_filter_btn = KeyboardButton("/edit_filter")

save_filter_btn = KeyboardButton("/save_filter")

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.row(search_btn, settings_btn)

search_kb_1 = ReplyKeyboardMarkup(resize_keyboard=True)
search_kb_1.row(add_filter_btn)

search_kb_2 = ReplyKeyboardMarkup(resize_keyboard=True)
search_kb_2.row()

add_filter_kb = ReplyKeyboardMarkup(resize_keyboard=True)
add_filter_kb.row(boat_name_btn, category_btn, boat_type_btn)
add_filter_kb.row(location_btn, year_btn, hull_material_btn)
add_filter_kb.row(length_btn, draft_btn, fuel_type_btn)
add_filter_kb.row(price_btn)
add_filter_kb.row(apply_btn, apply_and_save_btn)

new_filter_kb = ReplyKeyboardMarkup(resize_keyboard=True)
new_filter_kb.row(boat_name_btn, category_btn, boat_type_btn)
new_filter_kb.row(location_btn, year_btn, hull_material_btn)
new_filter_kb.row(length_btn, draft_btn, fuel_type_btn)
new_filter_kb.row(price_btn)
new_filter_kb.row(save_filter_btn)

settings_kb = ReplyKeyboardMarkup(resize_keyboard=True)
settings_kb.row(menu_btn, new_filter_btn)
settings_kb.row(my_filters_btn, edit_filter_btn)


def get_my_filters_kb(filters):
    kb = InlineKeyboardMarkup(row_width=3)
    for f in filters:
        btn = InlineKeyboardButton(str(f[0]), callback_data=str(f[0]))
        kb.insert(btn)
    return kb
