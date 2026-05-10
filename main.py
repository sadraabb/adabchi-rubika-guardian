# ==============================================
# ================== LIBRARIES ==================
# ==============================================
from rubka import Robot, Message,filters
from rubka.button import ChatKeypadBuilder,InlineBuilder
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from datetime import datetime
# ==============================================
# ================ LOCAL FILES =================
# ==============================================
from database import (
    add_user, add_group,
      increment_messages,
        get_stats,
        get_stats_message,
        add_special_group,
        remove_special_group,
        is_special_group,
        add_ticket,
        get_pending_tickets,
        get_all_tickets,
        answer_ticket,
        get_ticket
        
        )
from answer_list import start_message , about_me , help_bot , bot_say
from config import TOKEN,ADMIN_ID,ADMIN_USER_NAME,commands_list
from fun_setting import hafez,joke_create,get_bio
from web_services import get_currency , ask_ai



# ========== تنظیمات لاگ ==========
# ایجاد پوشه logs (اگه وجود نداشت)
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

# تنظیم لاگر اصلی
log_file = log_dir / "bot_errors.log"

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

# هندلر فایل (با چرخش)
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=5*1024*1024,  # 5 مگابایت
    backupCount=5,
    encoding='utf-8'
)
file_handler.setLevel(logging.ERROR)

# گرفتن لاگر اصلی
logger = logging.getLogger()
logger.addHandler(file_handler)

# ==================== BOT INITIALIZATION ====================
# مقداردهی اولیه ربات با استفاده از توکن
bot = Robot(TOKEN)

# ==================== ADMIN CONFIG ====================
# آیدی عددی ادمین
admin_id = ADMIN_ID
# یوزر نیم ادمین
admin_user_name = ADMIN_USER_NAME

# ==================== DATA ====================
get_hafez = hafez.get_fal_bot()
joke_get = joke_create.get_joke_bot()

waiting_for_ticket = set()

# ==============================================
# ==================== KEYPADS ====================
# ==============================================

# تعریف کی‌پد (صفحه کلید) اصلی ربات با دکمه‌های کاربردی
# این کی‌پد برای تعاملات عمومی کاربران استفاده می‌شود

# ---------- Main Menu Keypad ----------
chat_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="help_bot", text="راهنما"),
        ChatKeypadBuilder().button(id="about_me", text="درباره ما"),
        ChatKeypadBuilder().button(id="add_group",text="➕ افزودن به گروه"),
        ChatKeypadBuilder().button(id="sargarmi_menu",text="🎮 سرگرمی")
    )
    .row(
        ChatKeypadBuilder().button(id="support_menu",text="📞 پشتیبانی")
    )
    .build()
)

# ---------- Entertainment Menu Keypad ----------
sargarmi_menu_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="fal_hafez_get",text="🍃 فال حافظ"),
        ChatKeypadBuilder().button(id="joke_get_button",text="😂 جوک")
    )
    .build()
)


# ---------- Admin Panel Keypad ----------
# کیبورد پنل ادمین - فقط برای مدیر ربات قابل دسترسی است
admin_panel_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="bot_status",text="خاموش/روشن"),
        ChatKeypadBuilder().button(id="amar_bot",text="📊 آمار ربات"),
        ChatKeypadBuilder().button(id="list_ticket",text="لیست تیکت"),
        ChatKeypadBuilder().button(id="help_admin_panel",text="راهنمای پنل مدیریت")
    )
    .build()
)


# ---------- Support Menu Keypad ----------
# کیبورد بخش پشتیبانی - نمایش داده می‌شود پس از کلیک روی دکمه "ارتباط با پشتیبانی"



# تعریف کی‌پد برای بخش پشتیبانی که شامل دو گزینه ارتباط است
# این کی‌پد پس از فشردن دکمه "ارتباط با پشتیبانی" نمایش داده می‌شود
support_button_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(
            id= 'support_id',
            text="ارسال پیام به پشتیبانی👤"
        ),
        ChatKeypadBuilder().button(
            id="submit_ticket",
            text="ثبت تیکت"
        )
    )
    .build()
)


# بخش کامنت شده: کی‌پد شیشه‌ای (Inline) برای پشتیبانی
# این بخش ممکن است در آینده فعال شود یا به عنوان یک رویکرد جایگزین در نظر گرفته شده باشد
# support_inline_keypad = (
#     InlineBuilder()
#     .row(
#     # دکمه برای ارسال پیام مستقیم به پشتیبانی از طریق چت
#     InlineBuilder().button_open_chat(
#         id = "support_chat",
#         text="ارسال پیام به پشتیبانی👤",
#         object_guid= "psychohkill", # شناسه کاربری یا گروه پشتیبانی
#         object_type="user"
#     ),
#     # دکمه برای ثبت تیکت از طریق وارد کردن متن
#     InlineBuilder().button_textbox(
#         id="ticket",
#         title="ثبت تیکت",
#         type_line="SingleLine",
#         type_keypad="String",
#         place_holder="لطفا پیامی را که میخواهید به عنوان تیکت ثبت کنید رو بنویسید"
#     )
#     )
#     .build()
# )



#-------------MAIN-MENU-BOT---------#
@bot.on_message_text(commands=['start'])
async def welcome_message(bot: Robot, message: Message):
    user_id = str(message.sender_id)
    add_user(user_id)  # ثبت کاربر
    print(f"پیام جدید: {message.text}")
    await message.reply(start_message(),chat_keypad=chat_keypad)
    await bot.set_commands(commands_list)



@bot.callback_query(button_id="about_me")
async def about_bot(bot:Robot,message:Message):
    await message.answer(about_me())



@bot.callback_query(button_id="support_menu")
async def contact_support(bot:Robot,message:Message):
    try:
        await message.reply(
            "کدام یک از روش های زیر را ترجیح میدهید برای ارتباط؟",
            chat_keypad = support_button_keypad
            )
    except:
        await message.answer(
            "لطفا بعدا امتحان کنید ، مشکلی پیش آمده است"
        )


@bot.callback_query(button_id="support_id")
async def support_pv(bot:Robot,message:Message):
    await message.reply(f"برای ارسال پیام به پشتیبانی با آیدی زیر در ارتباط باشید \n {admin_user_name}")



@bot.callback_query(button_id="submit_ticket")
async def submit_ticket(bot:Robot,message:Message):
    user_id = message.sender_id
    waiting_for_ticket.add(user_id)
    await message.reply(
    "لطفا پیامی را که میخواهید به ادمین ارسال شود را بفرستید\n\n"
    "(پشتیبانی در اسرع وقت پاسخ خواهد داد)"
    )


#----------------------Help command and Button -------------#
@bot.callback_query(button_id="help_bot")
async def help_bot_callback(bot:Robot,message:Message):
    await message.answer(
        help_bot()
    )
#---------------------- FUN MENU -------------------------#
@bot.callback_query(button_id="sargarmi_menu")
async def sargarmi_menu_buttons(bot:Robot,message:Message):
    try:
        await message.reply(
            "لطفا یکی از گزینه های زیر را انتخاب کنید!",
            chat_keypad = sargarmi_menu_keypad
        )
    except:
        await message.answer(
            "لطفا بعدا امتحان کنید ، مشکلی پیش آمده است"
        )

#------------------fal hafez------------------#


@bot.callback_query(button_id="fal_hafez_get")
async def get_fal_button(bot:Robot,message:Message):
    try:
        await message.answer(
            get_hafez
        )
    except Exception as e:
        await message.answer(
            "مشکلی پیش آمده"
        )
        logger.error(f"خطا در fal - کاربر: {message.sender_id} - خطا: {e}")    


@bot.on_message_group(filters=filters.text_equals("فال"))
async def fal_gap(bot:Robot,message:Message):
    group_id = str(message.chat_id)
    try:
        add_group(group_id)
        await message.answer(
            get_hafez
        )
    except Exception as e:
        add_group(group_id)
        await message.answer(
            "مشکلی پیش آمده"
        )
        logger.error(f"خطا در fal_gap - کاربر: {message.sender_id} - خطا: {e}")    


@bot.on_message_group(commands=['fal'])
async def fal_gap_cmd(bot:Robot,message:Message):
    group_id = str(message.chat_id)
    try:
        add_group(group_id)
        await message.answer(
            get_hafez
        )
    except Exception as e:
        add_group(group_id)
        await message.answer(
            "مشکلی پیش آمده"
        )
        logger.error(f"خطا در fal_gap - کاربر: {message.sender_id} - خطا: {e}")        

#------------------Joke ------------------------#

@bot.callback_query(button_id='joke_get_button')
async def joke_get_callback(bot:Robot,message:Message):
    try:
        await message.answer(
            joke_get
        )
    except Exception as e:
        await message.answer(
            "مشکلی پیش آمده"
        )
        logger.error(f"خطا در joke - کاربر: {message.sender_id} - خطا: {e}")
@bot.on_message_group(filters=filters.text_equals("جوک"))
async def joke_gap(bot:Robot,message:Message):
    group_id = str(message.chat_id)
    try:
        add_group(group_id)
        await message.answer(
            joke_get
        )
    except Exception as e:
        add_group(group_id)
        await message.answer(
            "مشکلی پیش آمده"
        )
        logger.error(f"خطا در joke_gap - کاربر: {message.sender_id} - خطا: {e}")
@bot.on_message_group(commands=['joke'])
async def cmd_joke_gap(bot:Robot,message:Message):
    group_id = str(message.chat_id)
    try:
        add_group(group_id)
        await message.answer(
            joke_get
        )
    except Exception as e:
        add_group(group_id)
        await message.answer(
            "مشکلی پیش آمده"
        )
        logger.error(f"خطا در joke_gap - کاربر: {message.sender_id} - خطا: {e}")
#------------------> currency price <-----------------#
@bot.on_message_group(filters=filters.text_equals("نرخ ارز"))
async def currency_gap(bot:Robot,message:Message):
    group_id = str(message.chat_id)
    try:
        add_group(group_id)
        await message.answer(
            get_currency()
        )
    except Exception as e:
        add_group(group_id)
        await message.answer(
            "مشکلی پیش آمده"
        )
        logger.error(f"خطا در currency_gap  - کاربر: {message.sender_id} - خطا: {e}")
        
@bot.on_message_group(commands=['currency'])
async def cmd_currency_gap(bot:Robot,message:Message):
    group_id = str(message.chat_id)
    try:
        add_group(group_id)
        await message.answer(
            get_currency()
        )
    except Exception as e:
        add_group(group_id)
        await message.answer(
            "مشکلی پیش آمده"
        )
        logger.error(f"خطا در currency_gap  - کاربر: {message.sender_id} - خطا: {e}")
    
#----------------------------> Bio Get <-----------------#
@bot.on_message_group(filters= filters.text_equals('بیو'))
async def random_bio(bot:Robot,message:Message):
    try:
        await message.answer(
            get_bio()
        )
    except:
        await message.answer(
            "مشکلی پیش آمده"
        )

#---------------------------- > Say Bot <----------------------#
@bot.on_message_group(filters=lambda m: m.text in ["ربات", "بات", "هوش مصنوعی"])
async def say_bot(bot:Robot,message:Message):
    group_id = str(message.chat_id)
    try:
        add_group(group_id)
        await message.answer(
            bot_say()
        )
    except Exception as e:
        add_group(group_id)
        await message.answer(
            "مشکلی پیش آمده"
        )
        logger.error(f"خطا در say_bot - کاربر: {message.sender_id} - خطا: {e}")


@bot.on_message_group(commands=['ai', 'هوش'])
async def ai_command(bot: Robot, message: Message):
    question = message.text.replace("/ai", "").replace("/هوش", "").strip()
    group_id = str(message.chat_id)
    if is_special_group(group_id):
        if not question:
            await message.reply("❌ سوال خود را بنویس:\n/ai آسمان چرا آبی است؟")
            return
        
        await message.reply("🤔 لحظه...")
        answer = ask_ai(question)
        await message.reply(answer)
    else:
        await message.answer("گروه شما ویژه نیست")

#----------------ADMIN-PANEL----------------#
# تعریف رویداد برای دستور '/panel'
# این تابع دسترسی به پنل ادمین را کنترل می‌کند
@bot.on_message_text(commands=['panel'])
async def admin_panel(bot:Robot,message:Message):
    # دریافت آیدی عددی کابری که دستور را ارسال کرده
    sender_id = message.sender_id
    # شرط بررسی برابر بودن آیدی عددی فرستاده پیام و ادمین
    if sender_id == admin_id:
        try :
            # اگر ادمین بود، پیام خوش‌آمدگویی و پنل ادمین را ارسال می‌کند
            await message.answer("سلام ادمین خوش آمدی",chat_keypad=admin_panel_keypad)
        except:
            await message.answer("ادمین عزیز مشکلی در بخش پنل ادمین به وجود آمده لطفا کد رو بررسی کنید!")
    else:
        # اگر کاربر ادمین نبود، پیام عدم دسترسی را ارسال می‌کند
        await message.reply("شما ادمین نیستید")





@bot.callback_query(button_id="amar_bot")
async def amar_bot(bot: Robot, message: Message):
    user_id = message.sender_id
    if user_id == admin_id:
        await message.answer(get_stats_message())
    else:
        await message.answer("شما ادمین نیستید!")


@bot.on_message_group(filters= lambda m : m.text in ['امار ربات','وضعیت ربات','نصب شو',"آمار ربات","ویژه کن"])
async def admin_group_commands(bot:Robot,message:Message):
    user_id = message.sender_id
    if user_id == admin_id:
        if message.text == "امار ربات":
            await message.answer(get_stats_message())
        elif message.text == "نصب شو":
            pass
        elif message.text =="ویژه کن":
            group_id = str(message.chat_id)
            group_name = "بدون نام"
            if is_special_group(group_id):
                await message.answer(f"❌ گروه قبلاً ویژه شده است!")
                return
            add_special_group(group_id, group_name, "vip", str(admin_id))
            await message.answer(f"""
✅ گروه ویژه شد!

📋 اطلاعات گروه:
🏷️ نام: {group_name}
👑 نوع: VIP
📅 تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎁 *مزایای گروه ویژه:*
• امکانات ویژه
• پشتیبانی اولویت‌دار
• دسترسی زودهنگام به امکانات جدید
• تگ مخصوص VIP در گروه

🚫 *دسترسی محدود:* گروه‌های عادی فقط امکانات پایه را دارند.

🌟 از امکانات ویژه لذت ببرید!
            """)
    else:
        await message.answer("شما ادمین ربات نیستید!")

#--------------------CREATOR-COMMAND--------#
@bot.on_message_text(commands=['creator', 'dev', 'admin_info', 'developer'])
async def show_creator_info(bot: Robot, message: Message):
    await message.reply("این ربات توسط (نام شما) توسعه داده شده است.\nآیدی روبیکا: @YOUR-ID\nگیت‌هاب: https://github.com/your-github-user-name و \n میتوانید سورس کد من را در گیت هاب مشاهده کنید! \n https://github.com/sadraabb/adabchi-rubika-guardian")


# اجرای ربات
# این خط باید در انتهای فایل قرار گیرد تا ربات اجرا شود
bot.run()
