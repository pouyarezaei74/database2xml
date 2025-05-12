# Android SMS & Call Log to XML Converter

ابزاری ساده برای تبدیل فایل‌های `mmssms.db` و `calllog.db` (بازیابی شده از گوشی‌های اندرویدی) به فایل XML سازگار با برنامه‌های **SMS Backup & Restore**.

## ویژگی‌ها

- تبدیل پیامک‌ها از `mmssms.db` به `sms-YYYYMMDDHHMMSS.xml`
- تبدیل تاریخچه تماس از `calllog.db` به `calllog-YYYYMMDDHHMMSS.xml`
- کاملاً سازگار با Python 3
- بدون نیاز به نصب پکیج اضافی

## نحوه استفاده

### برای پیامک‌ها:
```bash
python convert_calllog_db_to_xml.py mmssms.db
```

### برای تماس‌ها:
```bash
python calllog2xml.py calllog.db
```

فایل XML تولیدشده در مسیر اجرای اسکریپت ذخیره می‌شود. کافی‌ست آن را در فولدر `SMSBackupRestore` روی حافظه گوشی بریزید و از طریق اپلیکیشن **SMS Backup & Restore** ریستور کنید.
