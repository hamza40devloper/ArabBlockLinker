# استخدام أفضل صورة Docker جاهزة لخوادم ماين كرافت
FROM itzg/minecraft-server:latest

# الموافقة الإلزامية على اتفاقية استخدام ماين كرافت (بدونها لن يعمل السيرفر)
ENV EULA=TRUE

# تعيين نوع السيرفر إلى Paper (أفضل بكثير من Vanilla من حيث الأداء ودعم الإضافات)
ENV TYPE=PAPER

# استخدام أحدث إصدار متوفر للعبة
ENV VERSION=LATEST

# تعيين اسم السيرفر كما طلبت
ENV SERVER_NAME="NovaSMP"

# رسالة الترحيب التي ستظهر للاعبين في قائمة السيرفرات (MOTD)
ENV MOTD="Welcome to NovaSMP Server!"

# تفعيل وضع النجاة (Survival) بما أنه سيرفر SMP
ENV MODE=survival

# تحديد المنفذ الافتراضي للعبة
EXPOSE 25565
