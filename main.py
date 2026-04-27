from rubka import Robot, Message
from rubka.button import ChatKeypadBuilder,InlineBuilder
from answer_list import start_message , about_me
from config import TOKEN,ADMIN_ID,ADMIN_USER_NAME,commands_list

# مقداردهی اولیه ربات با استفاده از توکن
bot = Robot(TOKEN)
#آیدی عددی ادمین
admin_id = ADMIN_ID
admin_user_name = ADMIN_USER_NAME

# تعریف کی‌پد (صفحه کلید) اصلی ربات با دکمه‌های کاربردی
# این کی‌پد برای تعاملات عمومی کاربران استفاده می‌شود
chat_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="help_bot", text="راهنما"),
        ChatKeypadBuilder().button(id="about_me", text="درباره ما"),
        ChatKeypadBuilder().button(id="add_group",text="➕ افزودن به گروه")
    )
    .row(
        ChatKeypadBuilder().button(id="support_menu",text="ارتباط با پشتیبانی👤")
    )
    .build()
)

# تعریف کی‌پد پنل ادمین
# این کی‌پد فقط برای ادمین قابل دسترس است و شامل ابزارهای مدیریتی ربات می‌شود
admin_panel_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="bot_status",text="خاموش/روشن"),
        ChatKeypadBuilder().button(id="amar_bot",text="📊 آمار ربات"),
        ChatKeypadBuilder().button(id="list_ticket",text="لیست تیکت")
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

#-------------MAIN-MENU-BOT---------#
@bot.on_message(commands=['start'])
async def welcome_message(bot: Robot, message: Message):
    print(f"پیام جدید: {message.text}")
    await message.reply(start_message(),chat_keypad=chat_keypad)
    await bot.set_commands(commands_list)



@bot.callback_query("about_me")
async def about_bot(bot:Robot,message:Message):
    await message.answer(about_me())

@bot.callback_query("support_menu")
async def contact_support(bot:Robot,message:Message):
    await message.reply(
        "کدام یک از روش های زیر را ترجیح میدهید برای ارتباط؟",
        chat_keypad = support_button_keypad
        )


@bot.callback_query(button_id="support_id")
async def support_pv(bot:Robot,message:Message):
    await message.reply(f"برای ارسال پیام به پشتیبانی با آیدی زیر در ارتباط باشید \n {admin_user_name}")



@bot.callback_query("submit_ticket")
async def submit_ticket(bot:Robot,message:Message):
    await message.reply(
        "لطفا پیامی را که میخواهید به ادمین ارسال شود را بفرستید"
    )
    


#----------------ADMIN-PANEL----------------#
# تعریف رویداد برای دستور '/panel'
# این تابع دسترسی به پنل ادمین را کنترل می‌کند
@bot.on_message(commands=['panel'])
async def admin_panel(bot:Robot,message:Message):
    # دریافت آیدی عددی کابری که دستور را ارسال کرده
    sender_id = message.sender_id
    # شرط بررسی برابر بودن آیدی عددی فرستاده پیام و ادمین
    if sender_id == admin_id:
        # اگر ادمین بود، پیام خوش‌آمدگویی و پنل ادمین را ارسال می‌کند
        await message.answer("سلام ادمین خوش آمدی",chat_keypad=admin_panel_keypad)
    else:
        # اگر کاربر ادمین نبود، پیام عدم دسترسی را ارسال می‌کند
        await message.reply("شما ادمین نیستید")


#--------------------CREATOR-COMMAND--------#
@bot.on_message(commands=['creator', 'dev', 'admin_info', 'developer'])
async def show_creator_info(bot: Robot, message: Message):
    await message.reply("این ربات توسط [yourname] توسعه داده شده است.\nآیدی روبیکا: @your_user_name\nگیت‌هاب: https://github.com/your_github")


# اجرای ربات
# این خط باید در انتهای فایل قرار گیرد تا ربات اجرا شود
bot.run()
