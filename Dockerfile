# استخدام نسخة جافا كاملة ومستقرة مبنية على Ubuntu لمنع مشاكل الانهيار
FROM eclipse-temurin:17-jre

# تثبيت أداة curl فقط لأن الـ bash مدمج تلقائياً
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# تحديد مجلد العمل
WORKDIR /minecraft

# نسخ الملفات
COPY . .

# إعطاء صلاحية تشغيل لسكربت البداية
RUN chmod +x start.sh

# فتح المنفذ
EXPOSE 25565

# أمر التشغيل
CMD ["./start.sh"]
