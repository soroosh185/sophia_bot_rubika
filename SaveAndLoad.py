import os
import json
import sqlite3
import threading
import atexit
from pathlib import Path
from contextlib import contextmanager

DB_PATH = "database.db"
_db_lock = threading.Lock()
_pending_threads = []
_threads_lock = threading.Lock()


def _wait_all_saves():
    with _threads_lock:
        threads = list(_pending_threads)
    for t in threads:
        if t.is_alive():
            t.join(timeout=5)

atexit.register(_wait_all_saves)


def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bot_data (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.commit()


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15.0)
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
    finally:
        conn.close()


def save_json_async(key, data):
    try:
        json_data = json.dumps(
            data,
            default=lambda o: getattr(o, "__dict__", str(o)),
            ensure_ascii=False,
            separators=(",", ":")
        )
    except Exception as e:
        print(f"❌ خطا در تبدیل داده به JSON برای {key}: {e}")
        return

    def job():
        try:
            init_db()
            with _db_lock:
                with get_db_connection() as conn:
                    conn.execute(
                        "INSERT OR REPLACE INTO bot_data (key, value) VALUES (?, ?)",
                        (key, json_data)
                    )
                    conn.commit()
        except Exception as e:
            print(f"❌ خطا در ذخیره داده '{key}': {e}")
        finally:
            with _threads_lock:
                if t in _pending_threads:
                    _pending_threads.remove(t)

    
    t = threading.Thread(target=job, daemon=False)
    with _threads_lock:
        _pending_threads.append(t)
    t.start()


def save_json_sync(key, data):
    try:
        init_db()
        json_data = json.dumps(
            data,
            default=lambda o: getattr(o, "__dict__", str(o)),
            ensure_ascii=False,
            separators=(",", ":")
        )
        with _db_lock:
            with get_db_connection() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO bot_data (key, value) VALUES (?, ?)",
                    (key, json_data)
                )
                conn.commit()
        return True
    except Exception as e:
        print(f"❌ خطا در ذخیره همزمان '{key}': {e}")
        return False


def load_json(key, default_value=None):
    try:
        init_db()
        with get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT value FROM bot_data WHERE key = ?", (key,)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
    except Exception as e:
        print(f"❌ خطا در خواندن داده '{key}': {e}")
    return default_value


def migrate_old_data():
    old_files = {
        "data.json": "data",
        "all_data.json": "all_data",
        "group_all_dont_save.json": "group_all_dont_save"
    }
    init_db()
    for filename, key in old_files.items():
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                save_json_sync(key, data)
                backup_name = f"{filename}.backup"
                os.rename(filename, backup_name)
                print(f"✅ {filename} به SQLite منتقل شد → {backup_name}")
            except Exception as e:
                print(f"❌ خطا در انتقال {filename}: {e}")
    print("✅ Migration کامل شد!")



def load_json_asl(default_value=None):
    try:
        with open("all_data.json", encoding="utf8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("❌ فایل all_data.json یافت نشد.")
        return default_value
    except json.JSONDecodeError:
        print("❌ خطا در تجزیه JSON از فایل all_data.json.")
        return default_value
    except Exception as e:
        print(f"❌ خطای غیرمنتظره در خواندن داده: {e}")
        return default_value
