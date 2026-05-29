FROM itzg/minecraft-server:latest

ENV EULA=TRUE
ENV TYPE=PAPER
ENV VERSION=LATEST
ENV SERVER_NAME="NovaSMP"
ENV MOTD="§6§lNovaSMP §7- §bOfficial Java Survival Server"
ENV MODE=survival
EXPOSE 25565
ENV MEMORY="2G"
# --- إضافة البلوجنات ---
# هذا الأمر يقوم بنسخ الإضافات من مجلد plugins في GitHub 
# إلى المجلد المخصص داخل السيرفر قبل تشغيله
COPY ./plugins/ /plugins/
