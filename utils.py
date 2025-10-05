import re
import requests
import logging
from database import get_db_connection

def escape_md(text: str) -> str:
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def format_profile(profile_data: dict) -> str:
    gender_icon = "🙋‍♂️" if profile_data['gender'] == 'male' else "🙋‍♀️"
    instrument_icons = {
        'vocalist': '🎤',
        'guitarist': '🎸',
        'drummer': '🥁',
        'bassist': '🪕',
        'keyboardist': '🎹',
        'violinist': '🎻',
        'saxophonist': '🎷',
        'trumpeter': '🎺',
        'accordionist': '🪗',
        'other': '🎵'
    }
    instrument_icon = instrument_icons.get(profile_data['instrument'], '🎵')
    
    instrument_display_map = {
        'vocalist': 'Я вокалист',
        'guitarist': 'Я гитарист',
        'drummer': 'Я барабанщик',
        'bassist': 'Я басист',
        'keyboardist': 'Я клавишник',
        'violinist': 'Я скрипач',
        'saxophonist': 'Я саксофонист',
        'trumpeter': 'Я трубач',
        'accordionist': 'Я баянист',
    }
    instrument_display = instrument_display_map.get(profile_data['instrument'], profile_data.get('instrument', 'Не указан'))
    
    text = (
        f"{gender_icon} *{escape_md(profile_data['full_name'])}*, {profile_data['age']} лет\n"
        f"{instrument_icon} Инструмент: {escape_md(instrument_display)}\n"
        f"📍 Город: {escape_md(profile_data['city'])}\n\n"
        f"{escape_md(profile_data['about'])}"
    )
    return text

def find_cities_geonames(query: str, max_rows=10):
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'format': 'json',
            'addressdetails': 1,
            'countrycodes': 'RU',
            'accept-language': 'ru',
            'limit': max_rows
        }
        headers = {
            'User-Agent': 'JamHunterBot/1.0 (https://t.me/jamhunterbot)'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        cities = []
        
        for item in data:
            place_type = item.get('type', '')
            address = item.get('address', {})
            
            if place_type in ['city', 'town', 'village'] or \
               address.get('city') or address.get('town') or address.get('village'):
                
                city_name = address.get('city') or address.get('town') or address.get('village') or item.get('display_name')
                
                if city_name and city_name not in cities:
                    city_clean = city_name.split(',')[0].strip()
                    if city_clean not in cities:
                        cities.append(city_clean)
        
        return cities[:max_rows] if cities else [query]
        
    except Exception as e:
        print(f"Ошибка API: {e}")
        return [query]

def contains_links(text: str) -> bool:
    if not text:
        return False
    
    patterns = [
        r'https?://[^\s]+',
        r'www\.[^\s]+',
        r'@[a-zA-Z0-9_]{5,32}',
        r't\.me/[^\s]+',
        r'telegram\.me/[^\s]+'
    ]
    
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def get_link_warnings(user_id: int) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT warning_count FROM link_warnings WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result['warning_count'] if result else 0

def add_link_warning(user_id: int) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT warning_count FROM link_warnings WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        new_count = result['warning_count'] + 1
        cursor.execute("""
            UPDATE link_warnings 
            SET warning_count = ?, last_warning = CURRENT_TIMESTAMP 
            WHERE user_id = ?
            INSERT INTO link_warnings (user_id, warning_count) 
            VALUES (?, ?)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM blacklist WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None