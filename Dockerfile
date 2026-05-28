FROM eclipse-temurin:25-jre
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /minecraft
COPY . .
RUN echo "eula=true" > eula.txt

# تحميل نسخة الـ Paper
RUN curl -L -o server.jar "https://fill-data.papermc.io/v1/objects/2c2af90d6ef0e823c272e7059873e3b7a24e07674e56e3b8d6c63ebff03cf827/paper-26.1.2-66.jar"

# فتح المنفذ
EXPOSE 25565

# تعديل أمر التشغيل لإيقاف تفاعل الـ Terminal الإجباري في السحاب
CMD ["java", "-Xmx4G", "-Xms4G", "-Dterminal.jline=false", "-Dterminal.ansi=true", "-jar", "server.jar", "--nogui"]
