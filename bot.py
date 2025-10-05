import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from config import TOKEN, CHANNEL_ID, ADMINS, BOT_USERNAME, CHANNEL_USERNAME
from database import init_db, get_db_connection
from keyboards import *
from utils import escape_md, format_profile, find_cities_geonames, contains_links, add_link_warning

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_gender = State()
    waiting_for_instrument = State()
    waiting_for_other_instrument = State()
    waiting_for_about = State()
    waiting_for_video = State()
    waiting_for_location = State()
    waiting_for_city_input = State()

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT reason FROM blacklist WHERE user_id = ?", (user_id,))
    ban = cursor.fetchone()
    if ban:
        await message.answer(f"🚫 Вы заблокированы.\nПричина: {ban['reason']}")
        conn.close()
        return
    
    cursor.execute("SELECT is_registered FROM users WHERE tg_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute(
            "INSERT OR IGNORE INTO users (tg_id, username, full_name) VALUES (?, ?, ?)",
            (user_id, username, full_name)
        )
        conn.commit()
        conn.close()
        if not await is_subscribed(user_id):
            await message.answer(
                "👋 Привет! Чтобы начать, подпишись на наш канал!",
                reply_markup=get_subscription_keyboard(CHANNEL_USERNAME)
            )
            return
        else:
            await start_registration(message, state)
    else:
        conn.close()
        if not user['is_registered']:
            if not await is_subscribed(user_id):
                await message.answer(
                    "👋 Привет! Чтобы начать, подпишись на наш канал!",
                    reply_markup=get_subscription_keyboard(CHANNEL_USERNAME)
                )
                return
            else:
                await start_registration(message, state)
        else:
            await show_main_menu(message)

@dp.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if await is_subscribed(user_id):
        await callback.message.delete()
        await start_registration(callback.message, state)
    else:
        await callback.answer("❌ Вы еще не подписались на канал.", show_alert=True)

async def start_registration(message: Message, state: FSMContext):
    await state.set_state(Registration.waiting_for_name)
    await message.answer("👤 Как тебя зовут?")

@dp.message(Registration.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.waiting_for_age)
    await message.answer("🔢 Сколько тебе лет?")

@dp.message(Registration.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введи возраст числом.")
        return
    await state.update_data(age=int(message.text))
    await state.set_state(Registration.waiting_for_gender)
    await message.answer("⚧ Твой пол:", reply_markup=get_gender_keyboard())

@dp.callback_query(F.data.startswith("gender_"))
async def process_gender(callback: CallbackQuery, state: FSMContext):
    gender = callback.data.split("_")[1]
    await state.update_data(gender=gender)
    await state.set_state(Registration.waiting_for_instrument)
    await callback.message.edit_text("🎵 На каком инструменте играешь?", reply_markup=get_instrument_keyboard())

@dp.callback_query(F.data.startswith("instrument_"))
async def process_instrument(callback: CallbackQuery, state: FSMContext):
    instrument = callback.data.split("_")[1]
    if instrument == "other":
        await state.set_state(Registration.waiting_for_other_instrument)
        await callback.message.edit_text("🎵 Введи название своего инструмента:")
    else:
        await state.update_data(instrument=instrument)
        await state.set_state(Registration.waiting_for_about)
        await callback.message.edit_text("📝 Напиши немного о себе:")

@dp.message(Registration.waiting_for_other_instrument)
async def process_other_instrument(message: Message, state: FSMContext):
    await state.update_data(instrument=message.text.lower())
    await state.set_state(Registration.waiting_for_about)
    await message.answer("📝 Напиши немного о себе:")

@dp.message(Registration.waiting_for_about)
async def process_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await state.set_state(Registration.waiting_for_video)
    await message.answer(
        "🎥 Хочешь добавить видео к анкете?\n\n"
        "⚠️ Видео должно быть не длиннее 15 секунд и не больше 25 МБ.\n\n"
        "Отправь видео или нажми 'Пропустить'.",
        reply_markup=get_video_keyboard()
    )

@dp.message(Registration.waiting_for_video, F.content_type.in_([ContentType.VIDEO, ContentType.VIDEO_NOTE]))
async def process_video(message: Message, state: FSMContext):
    video = message.video or message.video_note
    
    if video.duration and video.duration > 15:
        await message.answer("❌ Видео слишком длинное! Максимальная длина - 15 секунд.")
        return
    
    if video.file_size and video.file_size > 26214400:
        await message.answer("❌ Видео слишком большое! Максимальный размер - 25 МБ.")
        return
    
    await state.update_data(video_file_id=video.file_id, video_type=message.content_type)
    await state.set_state(Registration.waiting_for_location)
    await message.answer("✅ Видео добавлено!\n\n🌍 Теперь поделись локацией, чтобы я искал анкеты поблизости.", reply_markup=get_location_keyboard())

@dp.message(Registration.waiting_for_video)
async def process_video_text(message: Message, state: FSMContext):
    await message.answer(
        "❌ Пожалуйста, отправь видео или нажми кнопку 'Пропустить'.\n\n"
        "⚠️ Видео должно быть не длиннее 15 секунд и не больше 25 МБ.",
        reply_markup=get_video_keyboard()
    )

@dp.callback_query(F.data == "skip_video")
async def skip_video(callback: CallbackQuery, state: FSMContext):
    await state.update_data(video_file_id=None)
    await state.set_state(Registration.waiting_for_location)
    await callback.message.edit_text("🌍 Поделись локацией, чтобы я искал анкеты поблизости.", reply_markup=get_location_keyboard())

@dp.callback_query(F.data == "specify_city")
async def specify_city(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.waiting_for_city_input)
    await callback.message.edit_text("🏙 Введи название своего города:")

@dp.message(Registration.waiting_for_city_input)
async def process_city_input(message: Message, state: FSMContext):
    query = message.text
    cities = find_cities_geonames(query)
    if not cities:
        await message.answer("❌ Города не найдены. Попробуйте другое название.")
        return
    await state.update_data(cities=cities)
    await message.answer("Выбери свой город:", reply_markup=get_city_suggestions_keyboard(cities))

@dp.callback_query(F.data.startswith("city_"))
async def select_city(callback: CallbackQuery, state: FSMContext):
    city = callback.data.split("_", 1)[1]
    await state.update_data(city=city)
    await finish_registration(callback.message, state, callback.from_user)

@dp.callback_query(F.data == "retry_city_search")
async def retry_city_search(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.waiting_for_city_input)
    await callback.message.edit_text("🏙 Введи название своего города:")

@dp.callback_query(F.data == "skip_location")
async def skip_location(callback: CallbackQuery, state: FSMContext):
    await state.update_data(city="Не указан")
    await finish_registration(callback.message, state, callback.from_user)

async def finish_registration(message: Message, state: FSMContext, user):
    user_data = await state.get_data()
    
    profile_text_for_check = (
        f"{user_data.get('name', '')} "
        f"{user_data.get('about', '')} "
        f"{user_data.get('city', '')}"
    )
    
    if contains_links(profile_text_for_check):
        warning_count = add_link_warning(user.id)
        
        if warning_count >= 3:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO blacklist (user_id, reason, banned_by)
                VALUES (?, '3 предупреждения за ссылки', ?)
        SELECT 
            CASE 
                WHEN c.from_user_id = ? THEN c.to_user_id 
                ELSE c.from_user_id 
            END as matched_user_id,
            c.created_at
        FROM connections c
        WHERE (c.from_user_id = ? OR c.to_user_id = ?) 
            AND c.status = 'accepted'
        ORDER BY c.created_at DESC
        LIMIT 10
        CREATE TABLE IF NOT EXISTS viewed_profiles (
            viewer_id INTEGER,
            viewed_id INTEGER,
            viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (viewer_id, viewed_id)
        )
        SELECT u.* FROM users u
        JOIN profiles p ON u.tg_id = p.user_id
        WHERE u.tg_id != ? 
            AND u.city = ? 
            AND u.is_registered = 1
            AND u.tg_id NOT IN (
                SELECT reported_user_id FROM complaints 
                WHERE reporter_id = ? AND status = 'pending'
            )
            AND u.tg_id NOT IN (
                SELECT viewed_id FROM viewed_profiles 
                WHERE viewer_id = ?
            )
        ORDER BY RANDOM()
        LIMIT 1
            SELECT u.* FROM users u
            JOIN profiles p ON u.tg_id = p.user_id
            WHERE u.tg_id != ? 
                AND u.is_registered = 1
                AND u.tg_id NOT IN (
                    SELECT reported_user_id FROM complaints 
                    WHERE reporter_id = ? AND status = 'pending'
                )
                AND u.tg_id NOT IN (
                    SELECT viewed_id FROM viewed_profiles 
                    WHERE viewer_id = ?
                )
            ORDER BY RANDOM()
            LIMIT 1
            SELECT u.* FROM users u
            JOIN profiles p ON u.tg_id = p.user_id
            WHERE u.tg_id != ? 
                AND u.is_registered = 1
                AND u.tg_id NOT IN (
                    SELECT reported_user_id FROM complaints 
                    WHERE reporter_id = ? AND status = 'pending'
                )
            ORDER BY RANDOM()
            LIMIT 1
        INSERT OR IGNORE INTO viewed_profiles (viewer_id, viewed_id)
        VALUES (?, ?)
        SELECT * FROM connections
        WHERE (from_user_id = ? AND to_user_id = ?) OR (from_user_id = ? AND to_user_id = ?)
        INSERT INTO connections (from_user_id, to_user_id) VALUES (?, ?)
        SELECT from_user_id, to_user_id FROM connections WHERE id = ? AND to_user_id = ?
        SELECT from_user_id FROM connections WHERE id = ? AND to_user_id = ?
        SELECT COUNT(*) as cnt FROM complaints
        WHERE reporter_id = ? AND timestamp > {one_hour_ago}
        INSERT INTO complaints (reporter_id, reported_user_id, message_id)
        VALUES (?, ?, ?)
        INSERT OR IGNORE INTO blacklist (user_id, reason, banned_by)
        VALUES (?, 'Жалоба от пользователя', ?)
            UPDATE profile_moderation 
            SET status = 'approved', moderator_id = ?, moderated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            INSERT INTO profile_moderation (user_id, status, moderator_id, moderated_at)
            VALUES (?, 'approved', ?, CURRENT_TIMESTAMP)
        INSERT OR IGNORE INTO blacklist (user_id, reason, banned_by)
        VALUES (?, 'Забанен модератором', ?)
            UPDATE profile_moderation 
            SET status = 'rejected', moderator_id = ?, moderated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            INSERT INTO profile_moderation (user_id, status, moderator_id, moderated_at)
            VALUES (?, 'rejected', ?, CURRENT_TIMESTAMP)
