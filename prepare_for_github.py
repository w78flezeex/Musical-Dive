#!/usr/bin/env python3
"""
Скрипт подготовки проекта для загрузки на GitHub
"""

import os
import shutil

print("=" * 60)
print("🚀 Подготовка проекта для GitHub")
print("=" * 60)
print()

# 1. Переименовываем README_GITHUB.md в README.md
if os.path.exists('README_GITHUB.md'):
    if os.path.exists('README.md'):
        # Делаем бэкап старого README
        shutil.copy2('README.md', 'README_OLD.md')
        print("📄 Старый README.md сохранен как README_OLD.md")
    
    shutil.copy2('README_GITHUB.md', 'README.md')
    print("✅ README_GITHUB.md → README.md")
else:
    print("❌ README_GITHUB.md не найден!")

print()

# 2. Проверяем .gitignore
if os.path.exists('.gitignore'):
    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()
    
    required = ['config.py', '*.db', '__pycache__']
    missing = [r for r in required if r not in gitignore_content]
    
    if missing:
        print(f"⚠️ В .gitignore отсутствуют: {', '.join(missing)}")
    else:
        print("✅ .gitignore настроен правильно")
else:
    print("❌ .gitignore не найден!")

print()

# 3. Проверяем наличие config.py (не должен быть добавлен)
if os.path.exists('config.py'):
    print("⚠️ config.py существует - убедись что он в .gitignore!")
else:
    print("✅ config.py не найден (это ОК для GitHub)")

print()

# 4. Список файлов для GitHub
github_files = [
    'README.md',
    'INSTALL.md',
    'GITHUB_GUIDE.md',
    'bot.py',
    'database.py',
    'keyboards.py',
    'utils.py',
    'backup.py',
    'config.example.py',
    'requirements.txt',
    '.gitignore'
]

print("📦 Файлы для загрузки на GitHub:")
print()

total_size = 0
for filename in github_files:
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        total_size += size
        size_kb = size / 1024
        print(f"   ✅ {filename:<30} ({size_kb:.1f} KB)")
    else:
        print(f"   ❌ {filename:<30} (НЕ НАЙДЕН)")

print()
print(f"📊 Общий размер: {total_size / 1024:.1f} KB")
print()

# 5. Предупреждения
print("=" * 60)
print("⚠️  ВАЖНО ПЕРЕД ЗАГРУЗКОЙ:")
print("=" * 60)
print("1. НЕ загружай config.py с токенами!")
print("2. НЕ загружай users.db с личными данными!")
print("3. Проверь что .gitignore работает")
print()

print("🚀 Команды для загрузки на GitHub:")
print("=" * 60)
print("git init")
print("git add .")
print('git commit -m "Initial commit: Music Davinchi Bot"')
print("git remote add origin https://github.com/USERNAME/REPO.git")
print("git branch -M main")
print("git push -u origin main")
print("=" * 60)
print()

print("✅ Готово! Проект подготовлен для GitHub")

