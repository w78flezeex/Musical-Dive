# 📦 Установка

## Шаг 1: Клонируй репозиторий

```bash
git clone https://github.com/твой-username/music-bot.git
cd music-bot
```

## Шаг 2: Создай бота

1. Открой [@BotFather](https://t.me/BotFather)
2. Напиши `/newbot`
3. Придумай имя и username
4. Скопируй токен

## Шаг 3: Создай канал

1. Создай публичный канал
2. Добавь бота в админы
3. Получи ID канала через [@userinfobot](https://t.me/userinfobot)

## Шаг 4: Установи зависимости

```bash
pip install -r requirements.txt
```

Или с виртуальным окружением:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## Шаг 5: Настрой config.py

```bash
# Скопируй пример
cp config.example.py config.py

# Отредактируй config.py
```

Заполни:
```python
TOKEN = "1234567890:ABCdef..."  # От @BotFather
CHANNEL_ID = -1001234567890  # ID канала
ADMINS = [123456789]  # Твой ID от @userinfobot
```

## Шаг 6: Запусти

```bash
python bot.py
```

## ✅ Готово!

Найди бота в Telegram и отправь `/start`

---

## 🆘 Проблемы

### ModuleNotFoundError: No module named 'aiogram'
```bash
pip install aiogram==3.4.1
```

### Бот не отвечает
- Проверь токен в config.py
- Убедись что бот запущен

### Подписка не работает
- Добавь бота в администраторы канала
- Проверь CHANNEL_ID (должен начинаться с -100)

---

**Нужна помощь?** Проверь [README_GITHUB.md](README_GITHUB.md)

