from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_gender_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🙋‍♂️Парень", callback_data="gender_male")],
        [InlineKeyboardButton(text="🙋‍♀️Девушка", callback_data="gender_female")]
    ])
    return keyboard

def get_instrument_keyboard():
    instruments = [
        ("🎤Я вокалист", "vocalist"),
        ("🎸Я гитарист", "guitarist"),
        ("🥁Я барабанщик", "drummer"),
        ("🪕Я басист", "bassist"),
        ("🎹Я клавишник", "keyboardist"),
        ("🎻Я скрипач", "violinist"),
        ("🎷Я саксофонист", "saxophonist"),
        ("🎺Я трубач", "trumpeter"),
        ("🪗Я баянист", "accordionist"),
        ("Другое", "other")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=f"instrument_{data}")] for text, data in instruments
    ])
    return keyboard

def get_profile_buttons(profile_tg_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🤝 Связаться", callback_data=f"connect_{profile_tg_id}"),
            InlineKeyboardButton(text="⏭ Пропустить", callback_data="skip_profile")
        ],
        [InlineKeyboardButton(text="⚠️ Пожаловаться", callback_data=f"complain_{profile_tg_id}")]
    ])
    return keyboard

def get_connection_response_buttons(connection_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_{connection_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{connection_id}")
        ]
    ])
    return keyboard

def get_complaint_admin_buttons(complaint_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚫 Забанить", callback_data=f"ban_{complaint_id}"),
            InlineKeyboardButton(text="✅ Ложная тревога", callback_data=f"dismiss_{complaint_id}")
        ]
    ])
    return keyboard

def get_location_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗺️ Уточнить город", callback_data="specify_city")],
        [InlineKeyboardButton(text="❌ Не хочу", callback_data="skip_location")]
    ])
    return keyboard

def get_city_suggestions_keyboard(cities, callback_prefix="city"):
    keyboard = []
    for city in cities[:5]:
        keyboard.append([InlineKeyboardButton(text=city, callback_data=f"{callback_prefix}_{city}")])
    keyboard.append([InlineKeyboardButton(text="🔄 Попробовать другое", callback_data="retry_city_search")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_subscription_keyboard(channel_username):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Перейти на канал", url=f"https://t.me/{channel_username}")],
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subscription")]
    ])
    return keyboard

def get_moderation_buttons(user_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Разрешить", callback_data=f"mod_approve_{user_id}"),
            InlineKeyboardButton(text="🚫 Забанить", callback_data=f"mod_ban_{user_id}")
        ]
    ])
    return keyboard

def get_video_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏭ Пропустить", callback_data="skip_video")]
    ])
    return keyboard

def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="◀️ Назад"),
                KeyboardButton(text="🏠 Главное меню"),
                KeyboardButton(text="👤 Мой профиль")
            ]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard

def remove_reply_keyboard():
    from aiogram.types import ReplyKeyboardRemove
    return ReplyKeyboardRemove()