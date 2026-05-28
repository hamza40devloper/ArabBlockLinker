#!/bin/bash
# الانتقال لمجلد السيرفر
cd "$(dirname "$0")"

# الرابط المباشر لتحديث Paper المختار من قبلك
PAPER_URL="https://fill-data.papermc.io/v1/objects/2c2af90d6ef0e823c272e7059873e3b7a24e07674e56e3b8d6c63ebff03cf827/paper-26.1.2-66.jar"

# التحقق من وجود ملف السيرفر، إذا لم يكن موجوداً يتم تحميله تلقائياً
if [ ! -f "server.jar" ]; then
    echo "[-] Paper jar not found. Downloading your specified version..."
    curl -L -o server.jar "$PAPER_URL"
fi

# تشغيل السيرفر بالإعدادات الاحترافية ونظام الحماية من الانهيار
exec java -Xmx4G -Xms4G \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:+AlwaysPreTouch \
  -XX:G1NewSizePercent=30 \
  -XX:G1MaxNewSizePercent=40 \
  -XX:G1HeapRegionSize=8m \
  -XX:G1ReservePercent=15 \
  -XX:G1HeapWastePercent=5 \
  -XX:G1MixedGCCountTarget=4 \
  -XX:InitiatingHeapOccupancyPercent=15 \
  -XX:G1MixedGCLiveThresholdPercent=90 \
  -XX:G1RSetUpdatingPauseTimePercent=5 \
  -XX:SurvivorRatio=32 \
  -XX:+PerfDisableSharedMem \
  -XX:MaxTenuringThreshold=1 \
  -Dusing.aikars.flags=https://mcflags.emc.gs \
  -Daikars.new.flags=true \
  -jar server.jar nogui
