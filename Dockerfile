# استخدام أحدث نسخة مستقرة من صورة ماين كرافت المدعومة بجافا
FROM itzg/minecraft-server:latest

# الموافقة على شروط اتفاقية الاستخدام EULA (مطلوب لتشغيل السيرفر)
ENV EULA=TRUE

# تحديد نوع السيرفر (ينصح بـ PAPER لضمان أفضل أداء لمنع الـ Lag في سيرفرات SMP)
ENV TYPE=PAPER

# تحديد إصدار اللعبة (LATEST يعتمد أحدث إصدار مستقر تلقائياً)
ENV VERSION=LATEST

# نص رسالة الترحيب التي تظهر للاعبين في القائمة (MOTD) مع ألوان مخصصة
ENV MOTD="§6§lNovaSMP §7- §bOfficial Java Survival Server"

# فتح المنفذ الافتراضي لماين كرافت جافا
EXPOSE 25565
