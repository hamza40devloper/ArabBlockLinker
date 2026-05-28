# 1. ترقية الجافا إلى إصدار 25 المطلوب للتحديث الجديد
FROM eclipse-temurin:25-jre

# 2. تثبيت أداة تحميل الملفات من الإنترنت
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 3. تحديد مجلد العمل داخل الاستضافة
WORKDIR /minecraft

# 4. نسخ الملفات والموافقة التلقائية على شروط ماين كرافت
COPY . .
RUN echo "eula=true" > eula.txt

# 5. تحميل نسخة Paper التي اخترتها وتسميتها server.jar مباشرة
RUN curl -L -o server.jar "https://fill-data.papermc.io/v1/objects/2c2af90d6ef0e823c272e7059873e3b7a24e07674e56e3b8d6c63ebff03cf827/paper-26.1.2-66.jar"

# 6. فتح المنفذ وتشغيل السيرفر بذاكرة 4 جيجابايت
EXPOSE 25565
CMD ["java", "-Xmx4G", "-Xms4G", "-jar", "server.jar", "nogui"]
