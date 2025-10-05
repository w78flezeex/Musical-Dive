#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

DB_NAME = "users.db"
BACKUP_DIR = "backups"

def create_backup():
    if not os.path.exists(DB_NAME):
        print(f"❌ База данных {DB_NAME} не найдена!")
        return False
    
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"✅ Создана папка {BACKUP_DIR}/")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{BACKUP_DIR}/users_backup_{timestamp}.db"
    
    try:
        shutil.copy2(DB_NAME, backup_name)
        file_size = os.path.getsize(backup_name)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"✅ Резервная копия создана: {backup_name}")
        print(f"📊 Размер: {file_size_mb:.2f} МБ")
        
        backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.db')]
        print(f"📁 Всего бэкапов: {len(backups)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании резервной копии: {e}")
        return False

def list_backups():
    if not os.path.exists(BACKUP_DIR):
        print(f"❌ Папка {BACKUP_DIR}/ не найдена!")
        return
    
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.db')])
    
    if not backups:
        print(f"📁 В папке {BACKUP_DIR}/ нет бэкапов")
        return
    
    print(f"\n📁 Список резервных копий в {BACKUP_DIR}/:\n")
    for idx, backup in enumerate(backups, 1):
        filepath = os.path.join(BACKUP_DIR, backup)
        size = os.path.getsize(filepath) / (1024 * 1024)
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        print(f"{idx}. {backup}")
        print(f"   📊 Размер: {size:.2f} МБ")
        print(f"   📅 Дата: {mtime.strftime('%d.%m.%Y %H:%M:%S')}\n")

def cleanup_old_backups(keep_last=10):
    if not os.path.exists(BACKUP_DIR):
        return
    
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.db')])
    
    if len(backups) <= keep_last:
        print(f"✅ Всего бэкапов: {len(backups)}, очистка не требуется")
        return
    
    to_delete = backups[:-keep_last]
    
    for backup in to_delete:
        filepath = os.path.join(BACKUP_DIR, backup)
        try:
            os.remove(filepath)
            print(f"🗑️ Удален старый бэкап: {backup}")
        except Exception as e:
            print(f"❌ Не удалось удалить {backup}: {e}")
    
    print(f"✅ Оставлено {keep_last} последних бэкапов")

if __name__ == "__main__":
    print("=" * 50)
    print("🔄 Скрипт резервного копирования БД")
    print("=" * 50)
    print()
    
    if create_backup():
        print()
        list_backups()
        print()
        cleanup_old_backups(keep_last=10)
    
    print()
    print("=" * 50)
    print("Готово!")
    print("=" * 50)

