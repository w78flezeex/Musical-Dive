# 📘 Как загрузить проект на GitHub

## 1️⃣ Создай репозиторий на GitHub

1. Зайди на [github.com](https://github.com)
2. Нажми **New repository**
3. Название: `music-davinchi-bot` (или другое)
4. Описание: `Telegram bot for musicians to find each other`
5. **НЕ** ставь галочки "Add README" и ".gitignore"
6. Нажми **Create repository**

## 2️⃣ Подготовь проект

### Проверь .gitignore

Убедись что файл `.gitignore` есть и содержит:

```
*.db
config.py
__pycache__/
venv/
backups/
backups_code/
```

### Проверь, что НЕ будет загружено:

- ❌ `config.py` (с твоими токенами)
- ❌ `users.db` (база данных)
- ❌ папка `backups/`
- ✅ `config.example.py` (пример - ОК)

## 3️⃣ Инициализируй Git

В папке проекта выполни:

```bash
# Инициализация
git init

# Добавь файлы
git add .

# Первый коммит
git commit -m "Initial commit: Music Davinchi Bot v2.0"
```

## 4️⃣ Свяжи с GitHub

Замени `USERNAME` и `REPO` на свои:

```bash
git remote add origin https://github.com/USERNAME/REPO.git
git branch -M main
git push -u origin main
```

## 5️⃣ Готово! 🎉

Твой проект теперь на GitHub!

---

## 📝 Что загрузится

### Код (✅):
- bot.py
- database.py
- keyboards.py
- utils.py
- backup.py

### Документация (✅):
- README_GITHUB.md → переименуй в README.md
- INSTALL.md
- config.example.py
- requirements.txt

### НЕ загрузится (❌):
- config.py (токены)
- users.db (личные данные)
- backups/ (бэкапы)

---

## 🔄 Обновление

После изменений:

```bash
git add .
git commit -m "Описание изменений"
git push
```

---

## 📌 Переименуй README для GitHub

```bash
# Windows
ren README_GITHUB.md README.md

# Linux/Mac
mv README_GITHUB.md README.md
```

Или просто переименуй `README_GITHUB.md` → `README.md` в проводнике.

---

## 🎯 Итоговая структура на GitHub

```
твой-репозиторий/
├── README.md (главный)
├── INSTALL.md (инструкция)
├── bot.py
├── database.py
├── keyboards.py
├── utils.py
├── backup.py
├── config.example.py
├── requirements.txt
└── .gitignore
```

**Минималистично и понятно!** 🚀

