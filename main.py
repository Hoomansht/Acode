from telegram import Updater, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# دیکشنری ساده برای ذخیره نقش کاربران
user_roles = {}

# دکمه‌های منو
role_keyboard = ReplyKeyboardMarkup([["من استاد هستم"], ["من شاگرد هستم"]], one_time_keyboard=True, resize_keyboard=True)
student_menu = ReplyKeyboardMarkup([["ثبت حضور", "دیدن جلسات من"]], resize_keyboard=True)
admin_menu = ReplyKeyboardMarkup([["ثبت جلسه (با وویس یا متن)", "لیست جلسات شاگردان"]], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! خوش اومدی به کلاس‌یار.\nنقشت رو انتخاب کن:",
        reply_markup=role_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # تنظیم نقش
    if text == "من استاد هستم":
        user_roles[user_id] = "admin"
        await update.message.reply_text("شما به عنوان استاد وارد شدید.", reply_markup=admin_menu)

    elif text == "من شاگرد هستم":
        user_roles[user_id] = "student"
        await update.message.reply_text("شما به عنوان شاگرد وارد شدید.", reply_markup=student_menu)

    # عملیات مربوط به استاد
    elif user_roles.get(user_id) == "admin":
        if "ثبت جلسه" in text:
            await update.message.reply_text("لطفاً وویس یا متن جلسه رو ارسال کنید.")
        elif "لیست جلسات" in text:
            await update.message.reply_text("در آینده لیست جلسات اینجا نمایش داده میشه.")

    # عملیات مربوط به شاگرد
    elif user_roles.get(user_id) == "student":
        if text == "ثبت حضور":
            await update.message.reply_text("حضور شما ثبت شد.")
        elif text == "دیدن جلسات من":
            await update.message.reply_text("در آینده لیست جلسات شما اینجا نمایش داده میشه.")

    else:
        await update.message.reply_text("لطفاً ابتدا نقش خود را انتخاب کنید با /start")

# اجرای برنامه
app = ApplicationBuilder().token("7803244136:AAFx0ET4NV2kq0EVNWnEZt-d6WkBc7xBj_Y").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("ربات در حال اجراست...")
app.run_polling()
