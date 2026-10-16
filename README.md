# Genisys — جدار حماية متكامل وDPI لنظام Linux (مرجعي)

ملخّص
Genisys مشروع مرجعي مكتوب بـ Python يقوم بإدارة واجهة TUN، تحليل الحزم، اعتراض طلبات DNS وإعادة توجيهها عبر DoH، وواجهة تفتيش حية للمراقبة. هذه النسخة مبدئية ومصممة للاستخدام المحلي والدفاع عن الجهاز.

تحذير قانوني
لا تستخدم هذه الأداة على أنظمة أو شبكات لا تملك إذنًا صريحًا عليها. المؤلف غير مسؤول عن سوء الاستخدام.

الخطوات السريعة للتجربة (كمستخدم محلي)
1. انسخ المشروع إلى `/opt/genisys` أو مجلد عمل.
2. أنشئ venv وتثبّت المتطلبات:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
3. أنشئ ملف dummy (للوصول لحجم الأرشيف المطلوب):
   python3 tools/generate_dummy_data.py --out samples/dummy.bin --mb 120
4. ابنِ أرشيف التوزيع:
   python3 tools/build_zip.py --src . --out genisys_linux_studio.zip
5. إعداد واجهة TUN (مطلوب صلاحيات):
   sudo ip tuntap add dev genisys0 mode tun
   sudo ip addr add 10.0.0.1/24 dev genisys0
   sudo ip link set dev genisys0 up
6. لتشغيل محليًا:
   source venv/bin/activate
   python -m genisys.core

تشغيل كخدمة systemd (مُقترح للاستخدام الدائم)
1. انسخ ملفات المشروع إلى /opt/genisys
2. ضع unit file في /etc/systemd/system/genisys.service
3. sudo systemctl daemon-reload
4. sudo systemctl enable --now genisys.service

المزيد
- الشيفرة المرفقة تعد نقطة انطلاق؛ لتحسين الأداء قد نضيف pooling متقدم للـ bytearrays، native extensions، وWebSocket UI لعرض الحزم مباشرة في المتصفح.
