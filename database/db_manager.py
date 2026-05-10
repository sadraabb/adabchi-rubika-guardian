import sqlite3
from pathlib import Path
from datetime import datetime

# مسیر دیتابیس
DB_PATH = Path(__file__).parent / "adabchi.db"
TICKETS_DB_PATH = Path(__file__).parent / "tickets.db"


def create_tables():
    """ایجاد جدول‌های مورد نیاز"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bot_stats (
                id INTEGER PRIMARY KEY,
                total_users INTEGER DEFAULT 0,
                total_groups INTEGER DEFAULT 0,
                total_messages INTEGER DEFAULT 0,
                last_update DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_active DATETIME
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id TEXT PRIMARY KEY,
                first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_active DATETIME
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS special_groups (
                group_id TEXT PRIMARY KEY,
                group_name TEXT,
                group_type TEXT DEFAULT 'vip',
                added_by TEXT,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        # اگر رکوردی در bot_stats نیست، یک رکورد خالی بساز
        cursor = conn.execute("SELECT COUNT(*) FROM bot_stats")
        if cursor.fetchone()[0] == 0:
            conn.execute("INSERT INTO bot_stats (total_users, total_groups) VALUES (0, 0)")

def add_user(user_id):
    """افزودن کاربر جدید"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone()
        
        if not exists:
            conn.execute("INSERT INTO users (user_id, last_active) VALUES (?, ?)", (user_id, datetime.now()))
            conn.execute("UPDATE bot_stats SET total_users = total_users + 1, last_update = ?", (datetime.now(),))
        else:
            conn.execute("UPDATE users SET last_active = ? WHERE user_id = ?", (datetime.now(), user_id))

def add_group(group_id):
    """افزودن گروه جدید"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT group_id FROM groups WHERE group_id = ?", (group_id,))
        exists = cursor.fetchone()
        
        if not exists:
            conn.execute("INSERT INTO groups (group_id, last_active) VALUES (?, ?)", (group_id, datetime.now()))
            conn.execute("UPDATE bot_stats SET total_groups = total_groups + 1, last_update = ?", (datetime.now(),))
        else:
            conn.execute("UPDATE groups SET last_active = ? WHERE group_id = ?", (datetime.now(), group_id))




def add_special_group(group_id, group_name="", group_type="vip", added_by=""):
    """افزودن گروه ویژه (نامحدود)"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR REPLACE INTO special_groups (group_id, group_name, group_type, added_by, is_active)
            VALUES (?, ?, ?, ?, 1)
        """, (group_id, group_name, group_type, added_by))
    

def is_special_group(group_id, group_type=None):
    """بررسی گروه ویژه بودن (بدون محدودیت زمانی)"""
    with sqlite3.connect(DB_PATH) as conn:
        if group_type:
            cursor = conn.execute("""
                SELECT group_id FROM special_groups 
                WHERE group_id = ? AND group_type = ? AND is_active = 1
            """, (group_id, group_type))
        else:
            cursor = conn.execute("""
                SELECT group_id FROM special_groups 
                WHERE group_id = ? AND is_active = 1
            """, (group_id,))
        
        return cursor.fetchone() is not None



def remove_special_group(group_id):
    """حذف گروه ویژه (غیرفعال کردن)"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE special_groups SET is_active = 0 WHERE group_id = ?", (group_id,))

def increment_messages():
    """افزایش تعداد پیام‌های پردازش شده"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE bot_stats SET total_messages = total_messages + 1, last_update = ?", (datetime.now(),))

def get_stats():
    """دریافت آمار کامل ربات"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT total_users, total_groups, total_messages, last_update FROM bot_stats LIMIT 1")
        stats = cursor.fetchone()
        
        # تعداد کاربران فعال (در 24 ساعت اخیر)
        cursor = conn.execute("""
            SELECT COUNT(*) FROM users 
            WHERE last_active >= datetime('now', '-1 day')
        """)
        active_users = cursor.fetchone()[0]
        
        return {
            "total_users": stats[0] if stats else 0,
            "total_groups": stats[1] if stats else 0,
            "total_messages": stats[2] if stats else 0,
            "active_users": active_users,
            "last_update": stats[3] if stats else None
        }

def get_stats_message():
    """دریافت آمار ربات به صورت متن آماده برای ارسال"""
    stats = get_stats()
    
    return f"""
📊 آمار ربات ادب‌چی

━━━━━━━━━━━━━━━━━━━━━━

👥 کل کاربران: {stats['total_users']}
🟢 کاربران فعال (۲۴ ساعت): {stats['active_users']}
👥 گروه‌ها: {stats['total_groups']}
💬 کل پیام‌ها: {stats['total_messages']}

━━━━━━━━━━━━━━━━━━━━━━
📅 آخرین به‌روزرسانی: {stats['last_update']}
"""

# ایجاد جدول‌ها هنگام import
create_tables()




def create_tickets_table():
    """ایجاد جدول تیکت‌ها"""
    with sqlite3.connect(TICKETS_DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                user_name TEXT,
                message TEXT,
                status TEXT DEFAULT 'pending',
                created_at DATETIME,
                answer TEXT,
                answered_at DATETIME
            )
        """)

def add_ticket(user_id, user_name, message):
    """ثبت تیکت جدید"""
    with sqlite3.connect(TICKETS_DB_PATH) as conn:
        cursor = conn.execute("""
            INSERT INTO tickets (user_id, user_name, message, created_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, user_name, message, datetime.now()))
        return cursor.lastrowid

def get_pending_tickets():
    """دریافت تیکت‌های در انتظار"""
    with sqlite3.connect(TICKETS_DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT id, user_id, user_name, message, created_at 
            FROM tickets 
            WHERE status = 'pending'
            ORDER BY created_at ASC
        """)
        return cursor.fetchall()

def get_all_tickets():
    """دریافت همه تیکت‌ها"""
    with sqlite3.connect(TICKETS_DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT id, user_id, user_name, message, status, created_at, answered_at
            FROM tickets 
            ORDER BY created_at DESC
        """)
        return cursor.fetchall()

def answer_ticket(ticket_id, answer):
    """پاسخ به تیکت"""
    with sqlite3.connect(TICKETS_DB_PATH) as conn:
        conn.execute("""
            UPDATE tickets 
            SET status = 'answered', answer = ?, answered_at = ?
            WHERE id = ?
        """, (answer, datetime.now(), ticket_id))

def get_ticket(ticket_id):
    """دریافت اطلاعات یک تیکت"""
    with sqlite3.connect(TICKETS_DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT id, user_id, user_name, message, status, created_at 
            FROM tickets 
            WHERE id = ?
        """, (ticket_id,))
        return cursor.fetchone()

def delete_old_tickets(days=30):
    """حذف تیکت‌های قدیمی (بیش از ۳۰ روز)"""
    with sqlite3.connect(TICKETS_DB_PATH) as conn:
        conn.execute("""
            DELETE FROM tickets 
            WHERE created_at <= datetime('now', ?)
        """, (f'-{days} days',))

# ایجاد جدول هنگام import
create_tickets_table()