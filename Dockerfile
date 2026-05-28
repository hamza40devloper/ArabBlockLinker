FROM eclipse-temurin:25-jre
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /minecraft
COPY . .
RUN echo "eula=true" > eula.txt

# تحميل نسخة الـ Paper المطلوبة
RUN curl -L -o server.jar "https://fill-data.papermc.io/v1/objects/2c2af90d6ef0e823c272e7059873e3b7a24e07674e56e3b8d6c63ebff03cf827/paper-26.1.2-66.jar"

# فتح المنفذ الافتراضي
EXPOSE 25565

# تشغيل السيرفر مع تعطيل قراءة الـ Terminal وإلغاء نظام إعادة التشغيل التلقائي من الجافا
CMD ["java", "-Xmx4G", "-Xms4G", "-Dcom.mojang.eula.agree=true", "-Dterminal.jline=false", "-Dterminal.ansi=false", "-Djava.awt.headless=true", "-jar", "server.jar", "--nogui"]
