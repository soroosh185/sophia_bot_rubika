<div dir="rtl">

# 🤖 سوفیا — ربات مدیریت هوشمند روبیکا

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Rubika-purple)](https://rubika.ir)
[![Version](https://img.shields.io/badge/Version-3.0.0-green)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

سوفیا یک ربات مدیریت حرفه‌ای و هوشمند برای گروه‌های **روبیکا** است که با Python نوشته شده و امکانات گسترده‌ای برای مدیریت، سرگرمی و نظم‌دهی به گروه فراهم می‌کند.

---

## ✨ ویژگی‌های اصلی

### 🛡️ مدیریت گروه
- تشخیص و حذف خودکار پیام‌های اسپم، لینک، آیدی، فوروارد، متادیتا و کدهای مخرب
- سیستم اخطار (ectart) با تعداد قابل تنظیم
- بن خودکار با قابلیت بن بی‌صدا
- فیلترهای سفارشی کلمات ممنوع
- پشتیبانی از انواع پیام: عکس، ویدیو، صدا، ویس، فایل، آرشیو، نظرسنجی، لوکیشن و ...
- سیستم سطح‌بندی کاربران (مالک، ادمین، مدیر، معاف، ساکت و ...)

### 🎭 سرگرمی و قابلیت‌های اجتماعی
- **فونت‌ساز** فارسی (۱۰ استایل) و انگلیسی (۸ استایل)
- جوک، داستان، شعر (سعدی، حافظ، مولوی، فردوسی، شهریار، نظامی)
- فال، چیستان، انگیزشی، دیالوگ، چالش، حدیث، آیه
- شانس، تاس، سنگ‌کاغذقیچی
- آب‌وهوا، ساعت، تاریخ (شمسی / میلادی / هجری / عبری)
- اوقات شرعی، تاریخ تولد، اطلاعات ستاره‌شناسی
- دانلود پست و استوری روبینو
- هوش مصنوعی، ارز دیجیتال، گیف‌ساز

### 📊 آمار و گزارش
- ثبت آمار کامل پیام‌های هر کاربر در گروه
- پنل مدیریت مرکزی با دکمه‌های شیشه‌ای
- ارسال همگانی به کاربران و گروه‌ها
- گزارش پینگ و وضعیت ربات

### 💾 ذخیره‌سازی
- پایگاه داده SQLite با قابلیت WAL
- ذخیره async و sync
- مهاجرت خودکار از فایل‌های JSON قدیمی

---

## 📁 ساختار پروژه

```
├── main.py              # هسته اصلی ربات و هندلرهای پیام
├── defalts.py           # تنظیمات پیش‌فرض گروه‌ها
├── get_type.py          # تشخیص نوع پیام و نوع کاربر
├── font.py              # استایل‌های فونت فارسی و انگلیسی
├── SaveAndLoad.py       # مدیریت پایگاه داده SQLite
├── translate.py         # جداول ترجمه فارسی ↔ انگلیسی
├── text_get.py          # متون ثابت و پیام‌های ربات
├── fosh.py              # لیست کلمات فیلتر
└── all_data.json        # داده‌های استاتیک محتوا
```

---

## ⚙️ نصب و راه‌اندازی

### پیش‌نیازها

```bash
git clone https://github.com/soroush185/sophia_bot_rubika.git
```

```bash
cd sophia_bot_rubika
```

```bash
pip install rubka aiohttp httpx jdatetime hijridate convertdate pytz
```

### اجرا

1. در فایل `main.py` مقدار `Token` را با توکن ربات خود جایگزین کنید:
   ```python
   Token = "توکن_ربات_شما"
   ```
2. ربات را اجرا کنید:
   ```bash
   python main.py
   ```
3. ربات را به گروه اضافه کنید، ادمین کامل بدهید، سپس در گروه بنویسید: **فعال**

---

## 📢 لینک‌های مفید

- کانال رسمی: `@sophia_bot_rubika`
- راهنما و آموزش: `@help_sophia`
---

## 📜 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

</div>

---
---

<div dir="ltr">

# 🤖 Sophia — Smart Rubika Group Management Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Rubika-purple)](https://rubika.ir)
[![Version](https://img.shields.io/badge/Version-3.0.0-green)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

Sophia is a professional, feature-rich group management bot for the **Rubika** messaging platform, written in Python. It provides powerful tools for moderation, entertainment, and group organization.

---

## ✨ Key Features

### 🛡️ Group Moderation
- Auto-detection and deletion of spam, links, user IDs, forwarded messages, metadata, and malicious code patterns
- Configurable warning (ectart) system before banning
- Auto-ban with optional silent ban mode
- Custom word filters
- Handles all message types: photo, video, audio, voice, document, archive, poll, location, and more
- Multi-level user roles: owner, admin, manager, exempt, silent, blacklisted, and more

### 🎭 Entertainment & Social Features
- **Font styler** — 10 Persian styles & 8 English font variants
- Jokes, stories, poems (Saadi, Hafez, Rumi, Ferdowsi, Shahryar, Nezami)
- Fortune telling, riddles, motivational quotes, dialogues, challenges, hadiths, Quran verses
- Luck meter, dice, rock-paper-scissors
- Weather, clock, date (Shamsi / Gregorian / Hijri / Hebrew)
- Prayer times, birthday info, astrological data
- Rubino post & story downloader
- AI assistant, crypto prices, GIF maker

### 📊 Stats & Reporting
- Per-user message statistics tracked per group
- Central admin panel with inline keyboard buttons
- Broadcast messages to users or groups
- Ping and bot status reporting

### 💾 Data Persistence
- SQLite database with WAL (Write-Ahead Logging) mode
- Async and sync save operations
- Automatic migration from legacy JSON files

---

## 📁 Project Structure

```
├── main.py              # Bot core — message & callback handlers
├── defalts.py           # Default settings for new groups
├── get_type.py          # Message type & user role detection
├── font.py              # Persian & English font styling
├── SaveAndLoad.py       # SQLite database management
├── translate.py         # Persian ↔ English translation tables
├── text_get.py          # Static texts and bot messages
├── fosh.py              # Word filter lists
└── all_data.json        # Static content data
```

---

## ⚙️ Installation & Setup

### Requirements

```bash
git clone https://github.com/soroush185/sophia_bot_rubika.git
```

```bash
cd sophia_bot_rubika
```

```bash
pip install rubka aiohttp httpx jdatetime hijridate convertdate pytz
```

### Running the Bot

1. Open `main.py` and replace the `Token` variable with your bot token:
   ```python
   Token = "your_bot_token_here"
   ```
2. Run the bot:
   ```bash
   python main.py
   ```
3. Add the bot to your group, grant it full admin permissions, then type **فعال** (activate) inside the group.

---

## 🔧 Configuration

Group settings are initialized from `defalts.py` and stored in the SQLite database. Each group can independently configure:

- Which message types to allow or filter
- Warning thresholds and ban behavior
- Entertainment features to enable/disable
- User roles and permissions

---

## 🔗 Links

- Official Channel: `@sophia_bot_rubika`
- Help & Tutorials: `@help_sophia`

---

## 📜 License

This project is released under the MIT License.

</div>
