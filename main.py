nos = "3.0.0"
Token = ""


import asyncio, aiohttp
from rubka.asynco import Robot, Message, filters
from SaveAndLoad import save_json_async, save_json_sync, load_json, load_json_asl
from get_type import *
from convertdate import hebrew
import time
from typing import Dict, Any
import requests
from collections import OrderedDict, defaultdict
from rubka.keypad import ChatKeypadBuilder
from hijridate import Gregorian
import functools
from rubka.button import InlineBuilder
from hijridate import convert
import time
from translate import translate_en_fa, translate_fa_en, translate_fa_en_sar, translate_fa_en_sar2
from datetime import datetime, date
import random
import copy
import pytz
import jdatetime
import urllib.parse
import re
from text_get import *
from fosh import fosh, anti_ads_words
import httpx
from defalts import defultss
from font import font_farsi, font_auto
import atexit
import asyncio
import re







MAX_DELETE = 30
MAX_CACHE = 50
SAVE_INTERVAL = 2000
last_save = time.time()
API_KEY = "BcsGV8KPMfnA9HSiDbsLcXFfLIvAD8uN"
API_POST_URL = "https://api-free.ir/api/rubino-dl.php"
API_STORY_URL = "https://api-free.ir/api/story_rubino.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}


bot = Robot(Token)

data_save = defaultdict()



data = load_json("data", {"group":{}, "user":{}, 'esh':0, 'tedad_group':[], 'buy':0, "bot": None, "maker": [],"maker2":[], "number_message_send":0, "number_message_get":0})
data_json = load_json_asl({})
group_all_dont_save = load_json("group_all_dont_save", [])


data.setdefault("maker", [])
data.setdefault("maker2", [])
data.setdefault("group", {})
data.setdefault("user", {})
for i in data["group"]:
    if "sang" not in data["group"][i]["funny"]:
        data["group"][i]["funny"]["sang"] = True
    if "gifs" not in data["group"][i]["funny"]:
        data["group"][i]["funny"]["gifs"] = True
    if "fal" not in data["group"][i]["funny"]:
        data["group"][i]["funny"]["fal"] = True
    if "riddles" not in data["group"][i]["funny"]:
        data["group"][i]["funny"]["riddles"] = True
    if "fon_t" not in data["group"][i]["funny"]:
        data["group"][i]["funny"]["fon_t"] = True
    if "fon_f" in data["group"][i]["funny"]:
        del data["group"][i]["funny"]["fon_f"]
    if "fon_e" in data["group"][i]["funny"]:
        del data["group"][i]["funny"]["fon_e"]


def check_last_message_time(last_ts):
    now = datetime.now()
    last_dt = datetime.fromtimestamp(last_ts)
    diff = now - last_dt
    return diff.total_seconds() > 72 * 3600


groups_to_delete = []
def chek_delss():
    global groups_to_delete
    for group_key, group_data in data["group"].items():
        all_users_inactive = True
        for user_key, user_data in group_data["users"].items():
            for last_ts in user_data["last_messages_time"]:
                if not check_last_message_time(last_ts):
                    all_users_inactive = False
                    break
            if not all_users_inactive:
                break
        if all_users_inactive:
            groups_to_delete.append(group_key)
    return len(groups_to_delete)

async def del_datass():
    global groups_to_delete
    for group_key in groups_to_delete:
        if group_key in data["group"]:
            data["group"][group_key]["users"] = {}
            data["group"][group_key]['user_ectar'] = {}






pannel = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="state", text=" " + " " + " " + " " + " 📊 وضعیت"),
        ChatKeypadBuilder().button(id="buy", text=" " + " " + " " + " " + " 🛒 خرید"),
        ChatKeypadBuilder().button(id="buy_toman", text=" " + " " + " " + " " + " 💰 قیمت (تومان)")
    )
    .row(
        ChatKeypadBuilder().button(id="send_all", text=" " + " " + " " + " " + " 📣 ارسال همگانی"),
        ChatKeypadBuilder().button(id="froward_all", text=" " + " " + " " + " ➡️ فوروارد همگانی")
    )
    .row(
        ChatKeypadBuilder().button(id="ping", text=" " + " " + " " + " " + " 🏓 پینگ"),
        ChatKeypadBuilder().button(id="admin", text=" " + " " + " " + " " + " 👑 مالکیت مالک")
    )
    .row(
        ChatKeypadBuilder().button(id="tedad_group_max", text=" " + " " + " " + " " + " تعداد گروه"),
        ChatKeypadBuilder().button(id="posht_ba", text=" " + " " + " " + " " + " پیام پشتیبانی")
    )
    .row(
        ChatKeypadBuilder().button(id="charg", text=" " + " " + " " + " " + " 🔌 شارژ")
    )
    .row(
        ChatKeypadBuilder().button(id="back", text=" " + " " + " " + " " + " " + " ↩️ بازگشت")
    )
    .build()
)



async def get_birth_text(year: int, month: int, day: int, message) -> str:


    url = f"http://v3.api-free.ir/birth2?year={year}&month={month}&day={day}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await send_message("⨵ خطا در ارتباط با سرور",message)
                return 
            data = await response.json()

    if not data.get("ok"):
        await send_message("⨵ تاریخ وارد شده معتبر نیست",message)
        return

    d = data["result"]["age_details"]


    clean = lambda x: re.sub(r"^[^\w\d]+", "", x)
    text = f"""
🎂 اطلاعات تولد
━━━━━━━━━━━━━━

📅 {clean(d['birth_date_shamsi'])}
📅 {clean(d['birth_date_gregorian'])}
📅 {clean(d['birth_date_hijri'])}

━━━━━━━━━━━━━━
⭐ {clean(d['day_of_week'])}

🐾 {clean(d['birth_animal'])}
♑ {clean(d['month_symbol'])}
🪐 {clean(d['ruling_planet'])}
💎 {clean(d['birthstone'])}
🎲 {clean(d['lucky_number'])}

━━━━━━━━━━━━━━
⏳ {clean(d['days_since_birth'])}
📆 {clean(d['weeks_since_birth'])}
📅 {clean(d['months_since_birth'])}

━━━━━━━━━━━━━━
👤 {clean(d['age_of_adulthood'])}
""".strip()
    await send_with_prefix("◉BIRTH", text, message)

    return 




async def get_asls(text, sender_id, data, chat_id):
    if sender_id not in data["user"]:
        data["user"][sender_id] = {
            "chat_id":chat_id,
            "age": None,
            "name": None,
            "city": None,
            "title": None,
            "status": None,
            "type": None
        }
    text_split = text.split()
    if len(text_split) != 3:
        return "⨵ فرمت اشتباه است!\nلطفا به این شکل وارد کنید:\nنام سن شهر\nمثال: علی 25 تهران"

    name, age, city = text_split
    if not age.isdigit():
        return "⨵ سن باید عدد باشد! \nلطفا به این شکل وارد کنید:\nنام سن شهر\nمثال: علی 25 تهران"

    age_int = int(age)


    if not 0< len(name) <30:
        return
    if not 0< len(city) <30:
        return

    data["user"][sender_id]["name"] = name
    data["user"][sender_id]["age"] = str(age_int)
    data["user"][sender_id]["city"] = city
    data["user"][sender_id]["type"] = None
    return "✅ اصل شما با موفقیت ثبت شد!"


def slim_message(msg):
    return {
        "sender_id": msg.sender_id,
        "message_id": msg.message_id,
        "text":msg.text
    }

async def safe_save():
    try:
        save_json_sync("data", data)
        save_json_sync("group_all_dont_save", group_all_dont_save)
    except Exception as e:
        print("Save error:", e)

def emergency_save():
    try:
        print("⏳ در حال ذخیره اطلاعات قبل از خاموش شدن...")
        save_json_sync("data", data)
        save_json_sync("group_all_dont_save", group_all_dont_save)
        print("✅ اطلاعات با موفقیت ذخیره شد.")
    except Exception as e:
        print(f"❌ خطا در ذخیره اضطراری: {e}")


atexit.register(emergency_save)




async def send_for(chat_id, message_id, all_chai_id):
    send = 0
    dont_send = 0

    for i in all_chai_id:
        try:
            await bot.forward_message(chat_id, message_id, i)
            send += 1
            await asyncio.sleep(2)
        except Exception:
            if i in group_all_dont_save:
                group_all_dont_save.remove(i)
            dont_send += 1
            await asyncio.sleep(2)

    return send, dont_send

async def send_send(text, all_chai_id):
    send = 0
    dont_send = 0

    for i in all_chai_id:
        try:
            xx = await bot.send_message(i, text)
            send += 1
            await asyncio.sleep(2)
        except Exception:
            if i in group_all_dont_save:
                group_all_dont_save.remove(i)
            dont_send += 1
            await asyncio.sleep(2)
    return send, dont_send





def start_chat():
    start_chat = (
        ChatKeypadBuilder()
        .row(
            ChatKeypadBuilder().button(id="set_asl", text="✅ ثبت اصل"),
            ChatKeypadBuilder().button(id="del_asl", text="❌ حذف اصل"),
            ChatKeypadBuilder().button(id="edit_asl", text="📝 مشاهده اصل")
        )
        .row(
            ChatKeypadBuilder().button(id="help", text="💡 راهنما")
        )
        .build()
    )
    return start_chat








def sen_states(data):
    usr = list(data["user"].keys())
    num = 0
    for i in usr:
        if data["user"][i]["name"]:
            num += 1
    
    vip_count = 0
    for group_id, group_data in data["group"].items():
        vip_info = group_data.get("vip", {})
        if vip_info.get("vip", False) and vip_info.get("time_end"):
            vip_count += 1
    
    start_inlines = (
        InlineBuilder()
        .row(
            InlineBuilder().button_simple(
                "btn_dfbets", f"گروه:{len(data['tedad_group'])}"
            ),
            InlineBuilder().button_simple(
                "btn_efewbets", f"کاربر:{len(data['user'])}"
            )
        )
        .row(
            InlineBuilder().button_simple(
                "btn_befwaets", f"اصل:{num}"
            ),
            InlineBuilder().button_simple(
                "btn_befwdsaets", f"همه گروه:{len(group_all_dont_save)}"
            )
        )
        .row(
            InlineBuilder().button_simple(
                "btn_caahatid", f"ارسال: {data['number_message_send']}"
            ),
            InlineBuilder().button_simple(
                "btn_caahatid", f"دریافت: {data['number_message_get']}"
            )
        )
        .row(
            InlineBuilder().button_simple(
                "btn_caahatidklkl", f"گروه های ویژه: {vip_count}"
            ),
            InlineBuilder().button_simple(
                "btn_caahatidklkl", f"وضعیت خرید: {data['buy']}"
            )
        )
        .row(
            InlineBuilder().button_simple(
                "btn_caahatidklkl", f"تعداد روز فروش: {data['esh']}"
            )
        )
        .build()
    )
    return start_inlines


def start_inline(data):
    start_inlines = (
        InlineBuilder()
        .row(
            InlineBuilder().button_simple(
                "btn_bets", f"👥 گروه: {len(data['group'].keys())}"
            )
        )
        .row(
            InlineBuilder().button_simple(
                "btn_chatid", f"🆔 نسخه: {nos}"
            )
        )
        .build()
    )
    return start_inlines





def download_post(url):
    try:
        response = requests.get(API_POST_URL, params={"url": url}, timeout=20)
        return response.json() if response.status_code == 200 and response.json().get("ok") else None
    except Exception:
        return None

def download_story(page_id):
    try:
        response = requests.get(API_STORY_URL, params={"id": page_id}, timeout=20)
        return response.json() if response.status_code == 200 and response.json().get("ok") else None
    except Exception:
        return None

    



def status_text(settings: dict) -> str:
    action_names = {
        "delete": "حذف",
        "ban": "بن",
        "ectar": "اخطار",
    }

    enabled = []
    disabled = []

    for msg_type, config in settings.items():
        if not isinstance(config, dict):
            continue

        name = translate_en_fa.get(msg_type, msg_type)

        
        active_actions = [
            title for key, title in action_names.items()
            if config.get(key)
        ]

        warns = int(config.get("num_ectar", 0))

        if active_actions:
            actions_text = "، ".join(active_actions)
            enabled.append(
                f"⬡ {name}[ {actions_text} ] — {warns} اخطار"
            )
        else:
            disabled.append(f"⬡ {name}")

    lines = ["📋 وضعیت فیلترها\n"]

    if enabled:
        lines.append("❌ فیلتر های قفل »")
        lines.extend(enabled)
        lines.append("")

    if disabled:
        lines.append("✅ فیلتر های خاموش »")
        lines.extend(disabled)

    return "\n".join(lines).strip()




DIVIDER = "┄" * 22

USER_FIELDS = [
    ("manager",   "👑", "مدیر",           "bool"),
    ("admin",     "🛡️", "ادمین",          "list"),
    ("silent",    "🔇", "سکوت",           "list"),
    ("no_ansewr", "⛔", "لیست بی‌پاسخ",   "list"),
    ("mauf",      "📝", "معاف",           "list"),
]

MSG_FIELDS = [
    ("num_text",          "💬", "متن"),
    ("num_photo",         "🖼", "تصویر"),
    ("num_video",         "🎬", "ویدئو"),
    ("num_voice",         "🎙", "ویس"),
    ("num_audio",         "🎵", "صدا"),
    ("num_document",      "📄", "فایل"),
    ("num_archive",       "🗜", "آرشیو"),
    ("num_executable",    "⚙️", "اجرایی"),
    ("num_font",          "🔤", "فونت"),
    ("num_sticker",       "🧩", "استیکر"),
    ("num_poll",          "📊", "نظرسنجی"),
    ("num_contact",       "👤", "مخاطب"),
    ("num_location",      "📍", "لوکیشن"),
    ("num_live_location", "📡", "لوکیشن زنده"),
    ("num_link",          "🔗", "لینک"),
    ("num_forwarded",     "↪️", "فوروارد"),
]


def section(title: str) -> str:
    return f"\n{title}\n{DIVIDER}"


def user_row(emoji: str, label: str, value: str) -> str:
    return f"  {emoji}  {label:<15} {value}"


def msg_row(emoji: str, label: str, count: int) -> str:
    emoji = "⬡"
    filled_count = min(count // 5, 5)

    filled = "🟦" * filled_count
    empty = "⬜" * (5 - filled_count)

    return f"{emoji} {label:<16} {count:>5}\n   {filled}{empty}"


async def send_report(group_data, message):
    users = group_data.get("type_user", {})
    msgs  = group_data.get("num_message", {})
    now   = datetime.now().strftime("%Y/%m/%d  %H:%M")

    total_msgs = sum(msgs.get(k, 0) for k, *_ in MSG_FIELDS)

    lines = [
        f"    {get_sticr("report_group")}  گزارش گروه       ",

        section("👥  آمار کاربران"),
    ]

    for key, emoji, label, kind in USER_FIELDS:
        raw = users.get(key)
        if kind == "bool":
            value = "✅ دارد" if raw else "❌ ندارد"
        else:
            value = f"{len(raw):,} نفر" if raw else "0 نفر"
        lines.append(user_row(emoji, label, value))

    lines.append(section(f"📈  آمار پیام‌ها  ( جمع: {total_msgs:,} )"))

    for key, emoji, label in MSG_FIELDS:
        count = msgs.get(key, 0)
        lines.append(msg_row(emoji, label, count))

    lines += [
        "",
        DIVIDER,
        f"  🕐  {now}",
    ]

    await send_message("\n".join(lines), message)


panel_ids = [
    "send_group_on_f",
    "send_all_user_f",
    "send_group_all_f",
    "send_group_off_f",
    "send_all_f",
    "send_group_on_s",
    "send_all_user_s",
    "send_group_all_s",
    "send_group_off_s",
    "send_all_s"
    
]



forward_panel = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="send_group_on_f", text=" " + " " + " " + " " + " " + " 🚀 ارسال به گروه فعال"),
        ChatKeypadBuilder().button(id="send_all_user_f", text=" " + " " + " " + " " + " 👤 ارسال به کاربران"),
        ChatKeypadBuilder().button(id="send_group_all_f", text=" " + " " + " " + " 📢 ارسال به همه گروه ها")
    )
    .row(
        ChatKeypadBuilder().button(id="send_group_off_f", text=" " + " " + " " + " " + " 🔕 ارسال به گروه غیرفعال")
    )
    .row(
        ChatKeypadBuilder().button(id="send_all_f", text=" " + " " + " " + " " + " " + " 📣 ارسال همگانی")
    )
    .row(
        ChatKeypadBuilder().button(id="back1", text=" " + " " + " " + " " + " " + " ↩️ بازگشت")
    )
    .build()
)


send_panel = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="send_group_on_s", text=" " + " " + " " + " " + " " + " 🚀 ارسال به گروه فعال"),
        ChatKeypadBuilder().button(id="send_all_user_s", text=" " + " " + " " + " " + " 👤 ارسال به کاربران"),
        ChatKeypadBuilder().button(id="send_group_all_s", text=" " + " " + " " + " 📢 ارسال به همه گروه ها")
    )
    .row(
        ChatKeypadBuilder().button(id="send_group_off_s", text=" " + " " + " " + " " + " 🔕 ارسال به گروه غیرفعال")
    )
    .row(
        ChatKeypadBuilder().button(id="send_all_s", text=" " + " " + " " + " " + " " + " 📣 ارسال همگانی")
    )
    .row(
        ChatKeypadBuilder().button(id="back1", text=" " + " " + " " + " " + " " + " ↩️ بازگشت")
    )
    .build()
)


admin_panel = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="add_admin", text=" " + " " + " " + " " + " " + " ➕ افزودن ادمین کل"),
        ChatKeypadBuilder().button(id="del_admin", text=" " + " " + " " + " " + " ➖ حذف ادمین کل"),
        ChatKeypadBuilder().button(id="del_all_admin", text=" " + " " + " " + " " + " ❌ حذف همه ادمین کل ها")
    )
    .row(
        ChatKeypadBuilder().button(id="back1", text=" " + " " + " " + " " + " " + " ↩️ بازگشت")
    )
    .build()
)




ROLE_MAP = {
        1: "👑 سازنده",
        0: "🤖 ربات",
        2: "⭐ ادمین کل",
        3: "🔰 مالک",
        4: "🛡️ ادمین",
    }


async def send_user_report(group_data, user_id, message, all_data):  
    user_stats = group_data.get("users", {}).get(user_id, {})  
    if not user_stats:  
        await send_message("⨵ هیچ آماری برای شما ثبت نشده است.", message)  
        return  
    user_types = detect_user_types(all_data, group_data, user_id)
    if user_types:
        role_name = ROLE_MAP.get(user_types[0], "کاربر")  
    else:
        role_name = "کاربر"
    lines = [f"📌 مقام کاربر: **{role_name}**\n", "📊 آمار کاربر:"] 
    type_emojis = {  
        "num_text": "⬡ متن",  
        "num_photo": "⬡ تصویر",  
        "num_video": "⬡ ویدئو",  
        "num_voice": "⬡ ویس",  
        "num_audio": "⬡ صدا",  
        "num_document": "⬡ فایل",  
        "num_archive": "⬡ آرشیو",  
        "num_executable": "⬡ اجرایی",  
        "num_font": "⬡ فونت",  
        "num_sticker": "⬡ استیکر",  
        "num_poll": "⬡ نظرسنجی",  
        "num_contact": "⬡ مخاطب",  
        "num_location": "⬡ لوکیشن",  
        "num_live_location": "⬡ لوکیشن زنده",  
        "num_link": "⬡ لینک",  
        "num_id": "⬡ منشن/آیدی",  
        "num_forwarded": "⬡ فوروارد شده"  
    }  

    for key, label in type_emojis.items():  
        count = user_stats.get(key, 0)  
        lines.append(f"- {label}: {count}")  
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    lines.append(f"\n🗓️ تاریخ گزارش: {now}") 
    await send_message("\n".join(lines), message)



def get_disabled_features(funny_data: dict) -> list[tuple[str, str]]:

    items = [
        ("jok", "😂 جوک"),
        ("jok_kh", "📖 خاطره"),
        ("pnp", "😅 پ ن پ"),
        ("bio", "✨ بیو"),
        ("alky", "🤪 الکی مثلا"),
        ("dans", "🧠 دانستی"),
        ("dastan", "📚 داستان"),
        ("dialog", "🎭 دیالوگ"),
        ("sheer", "🎶 شعر"),
        ("angiz", "🔥 انگیزشی"),
        ("tas", "🎲 تاس بنداز"),
        ("sek", "🪙 سکه"),
        ("shan", "🍀 شانس"),
        ("chal", "⚡ چالش"),
        ("hadis", "📜 حدیث"),
        ("aye", "📖 آیه"),
        ("tarf", "💡 ترفند"),
        ("love", "❤️ جمله عاشقانه"),
        ("break", "💔 جمله دلشکسته"),
        ("ghan", "🌍 قوانین عجیب"),
        ("shas", "🔮 شخصیتم"),
        ("shog", "👔 شغل آینده"),
        ("hiy", "🐾 اگه حیوان بودم"),
        ("film", "🎬 فیلم من"),
        ("vaz", "😎 وضعیتم"),
        ("day", "📥 امروز"),
        ("download_p", "🔗 دانلود پست "),
        ("download_s", "📲 دانلود استوری"),
        ("ab", "⛅ آب و هوا "),
        ("arz", "💱 ارز"),
        ("ogh", "اوقات شرعی"),
        ("fon_t", "فونت"),
        ("man", "معنی"),
        ("hosh", "هوش مصنوعی"),
    ]

    poets = [
        ("sh_s", "🌹 شعر سعدی"),
        ("sh_h", "🍷 شعر حافظ"),
        ("sh_fr", "🗡️ شعر فردوسی"),
        ("sh_mvlv", "🌀 شعر مولوی"),
        ("sh_mvla", "✨ شعر مولانا"),
        ("sh_ne", "💍 شعر نظامی"),
        ("sh_sh", "✒️ شعر شهریار"),
    ]
    
    
    new = [
        ("riddles", "چیستان"),
        ("fal", "فال"),
        ("sang", "سنگ کاغذ قیچی"),
        ("gifs", "گیف ساز"),
    ]
    
    
    disabled_list = []


    for key, label in items:
        if not funny_data.get(key, True):
            disabled_list.append(label)

    for key, label in poets:
        if not funny_data.get(key, True):
            disabled_list.append(label)

    for key, label in new:
        if not funny_data.get(key, True):
            disabled_list.append(label)

    return disabled_list





async def manager_user(chat_id, sender_id, type_messages, data_group, message: Message):

    user_ectar = data_group.setdefault("user_ectar", {})
    type_config = data_group["type_message"]

    u = user_ectar.setdefault(sender_id, {
        k: 0 for k in [
            "filters", "spam", "text", "forwarded", "link", "id", "photo",
            "video", "audio", "voice", "document", "archive", "executable",
            "font", "sticker", "poll", "contact", "location", "live_location",
            "unknown", "ectar","hash","hang_code","metadata","spam","gif"
        ]
    })

    for msg_type in type_messages:
        config = type_config.get(msg_type)
        if not config:
            continue

        ban_enabled    = config.get("ban", False)
        warn_enabled   = config.get("ectar", False)
        delete_enabled = config.get("delete", False)

        silent_warn = config.get("ectar_silent", False)
        silent_ban  = config.get("ban_silent", False)

        limit = config.get("num_ectar", 0)
        u.setdefault(msg_type, 0)

        if warn_enabled:
            u[msg_type] += 1

        current = u[msg_type]

        if ban_enabled and warn_enabled and delete_enabled:
            message_ids_dont.append(message.message_id)
            message_ids_dont_2.append(message.message_id)
            if current > limit:
                asyncio.create_task(ban_user_group(chat_id, sender_id, message, silent_ban))
                u[msg_type] = 0
            else:
                if not silent_warn:
                    await send_warn(sender_id, msg_type, current, limit, message)

            await message.delete()
            return False


        if ban_enabled and warn_enabled and not delete_enabled:
            message_ids_dont.append(message.message_id)
            message_ids_dont_2.append(message.message_id)
            if current > limit:
                asyncio.create_task(ban_user_group(chat_id, sender_id, message, silent_ban))
                u[msg_type] = 0
            else:
                if not silent_warn:
                    await send_warn(sender_id, msg_type, current, limit, message)

            return False


        if ban_enabled and not warn_enabled and not delete_enabled:
            message_ids_dont.append(message.message_id)
            message_ids_dont_2.append(message.message_id)
            asyncio.create_task(ban_user_group(chat_id, sender_id, message, silent_ban))
            return False


        if warn_enabled and not ban_enabled and not delete_enabled:
            message_ids_dont.append(message.message_id)
            message_ids_dont_2.append(message.message_id)
            if not silent_warn:
                await send_warn(sender_id, msg_type, current, limit, message)
            return False


        if warn_enabled and delete_enabled and not ban_enabled:
            message_ids_dont.append(message.message_id)
            message_ids_dont_2.append(message.message_id)
            if not silent_warn:
                await send_warn(sender_id, msg_type, current, limit, message)

            await message.delete()
            return False


        if ban_enabled and delete_enabled and not warn_enabled:
            message_ids_dont.append(message.message_id)
            message_ids_dont_2.append(message.message_id)
            asyncio.create_task(ban_user_group(chat_id, sender_id, message, silent_ban))
            await message.delete()
            return False


        if delete_enabled and not warn_enabled and not ban_enabled:
            message_ids_dont.append(message.message_id)
            message_ids_dont_2.append(message.message_id)
            await message.delete()
            return False

    return True


async def send_warn(sender_id, msg_type, current, limit, message):
    tt = translate_en_fa[msg_type]
    await send_message(
        f"⨵ [اخطار]({sender_id}) ارسال «{tt}» در این گروه مجاز نیست. ↺ <{current}/{limit}>",
        message,
        20
    )




def on_funny(enabled):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(bot: Robot, message: Message):

            chat_id = message.chat_id

            if chat_id not in data["group"] or "funny" not in data["group"][chat_id]:
                return

            funny_type_all = data["group"][chat_id]["funny"]

            if not funny_type_all["funny"]:
                await message.reply("سرگرمی خاموش است.")
                return
            
            if not funny_type_all[enabled]:
                await message.reply(f"{translate_fa_en_sar2[enabled]} خاموش است.")
                return

            try:
                return await func(bot, message)

            except:
                return

        return wrapper
    return decorator



async def is_start(id):
    if id in data["group"]:
        if data["group"][id].get("bot", True):
            return True
        return False
    else:
        return False

async def is_start_1(id):
    if id in data["group"]:
        return True
    else:
        return False

async def build_admin_mentions(admin_ids):
    if not admin_ids:
        return []
    tasks = [get_name(user_id) for user_id in admin_ids]
    results = await asyncio.gather(*tasks)

    lines = []
    for user_id, result in zip(admin_ids, results):
        name, _, _, _ = result
        name = name if name else "کاربر"
        lines.append(f"⬡ [{name}]({user_id})")
    return lines

def get_local_dates():

    g_date = date.today()

    j_date = jdatetime.date.fromgregorian(date=g_date)

    h_date = Gregorian(
        g_date.year,
        g_date.month,
        g_date.day
    ).to_hijri()

    return {
        "shamsi": j_date.strftime("%Y/%m/%d"),
        "shamsi_day": j_date.strftime("%A"),
        "miladi": g_date.strftime("%Y-%m-%d"),
        "ghamari": f"{h_date.day} {h_date.month_name()} {h_date.year}"
    }

async def get_prayer_times(city: str, messaged):
    url = f"https://api.codebazan.ir/owghat/?city={city}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await send_message(f"⨵ خطا در دریافت اوقات شرعی برای {city}", messaged)

                data = await resp.json()

                if not data.get("Ok") or not data.get("Result"):
                    await send_message(f"⨵ اطلاعاتی برای شهر {city} پیدا نشد", messaged)

                info = data["Result"][0]
                print("ddd")
                dates = get_local_dates()
                print("jjj")

                msg = (
                    f"📆 {dates['shamsi_day']} | {dates['shamsi']}\n"
                    f"🕋 {dates['ghamari']}\n"
                    f"🌍 {dates['miladi']}\n\n"
                    f"🕌 اوقات شرعی به افق {info.get('shahr', city)}\n"
                    f"🔸 اذان صبح: {info.get('azansobh', '---')}\n"
                    f"🔸 طلوع آفتاب: {info.get('toloaftab', '---')}\n"
                    f"🔸 اذان ظهر: {info.get('azanzohr', '---')}\n"
                    f"🔸 غروب آفتاب: {info.get('ghorubaftab', '---')}\n"
                    f"🔸 اذان مغرب: {info.get('azanmaghreb', '---')}\n"
                    f"🔸 نیمه‌شب شرعی: {info.get('nimeshab', '---')}"
                )
                await send_message(msg, messaged)

    except Exception as e:
        await send_message("خطا", messaged)

async def reply_chat(message:Message):
    if message.reply_to_message_id:
        reply = data_save[message.chat_id].get(message.reply_to_message_id)
        if reply:
            reply_chat_id = reply.get("sender_id")
            return reply_chat_id
        return False
    return False


async def send_with_prefix(prefix, text, message):
    try:
        await send_message(f"{prefix}\n{text}", message)
    except Exception as e:
        await send_message(f"{prefix}\n⨵ خطای غیرمنتظره: {e}", message)

def find_price_by_symbol(data_list, symbol):
    try:
        item = next(item for item in data_list if item.get('symbol') == symbol)
        return str(item.get('price', '---'))
    except StopIteration:
        return '---'
    except Exception:
        return '---'

async def get_currency(msd):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://brsapi.ir/Api/Market/Gold_Currency.php?key={API_KEY}", headers=HEADERS) as res:
                data = await res.json()

        gold_18 = find_price_by_symbol(data.get('gold', []), 'IR_GOLD_18K')
        gold_24 = find_price_by_symbol(data.get('gold', []), 'IR_GOLD_24K')
        ounce = find_price_by_symbol(data.get('gold', []), 'XAUUSD')
        quarter_coin = find_price_by_symbol(data.get('gold', []), 'IR_COIN_QUARTER')
        half_coin = find_price_by_symbol(data.get('gold', []), 'IR_COIN_HALF')
        emami_coin = find_price_by_symbol(data.get('gold', []), 'IR_COIN_EMAMI')
        bahar_coin = find_price_by_symbol(data.get('gold', []), 'IR_COIN_BAHAR')

        usd = find_price_by_symbol(data.get('currency', []), 'USD')
        eur = find_price_by_symbol(data.get('currency', []), 'EUR')
        try_lira = find_price_by_symbol(data.get('currency', []), 'TRY')
        cad = find_price_by_symbol(data.get('currency', []), 'CAD')
        gbp = find_price_by_symbol(data.get('currency', []), 'GBP')

        tether = find_price_by_symbol(data.get('cryptocurrency', []), 'USDT')
        eth = find_price_by_symbol(data.get('cryptocurrency', []), 'ETH')
        btc = find_price_by_symbol(data.get('cryptocurrency', []), 'BTC')
        msg = "📊 نرخ‌های بازار:\n\n"

        msg += "--- طلا و سکه ---\n"
        msg += f"🔸 طلای 18 عیار: {int(gold_18):,} تومان\n" if gold_18.isdigit() else f"🔸 طلای 18 عیار: {gold_18}\n"
        msg += f"🔸 طلای 24 عیار: {int(gold_24):,} تومان\n" if gold_24.isdigit() else f"🔸 طلای 24 عیار: {gold_24}\n"
        msg += f"🔸 انس طلا: {float(ounce):,} دلار\n" if ounce.replace('.', '', 1).isdigit() else f"🔸 انس طلا: {ounce}\n"
        msg += f"🔹 سکه امامی: {int(emami_coin):,} تومان\n" if emami_coin.isdigit() else f"🔹 سکه امامی: {emami_coin}\n"
        msg += f"🔹 سکه بهار آزادی: {int(bahar_coin):,} تومان\n" if bahar_coin.isdigit() else f"🔹 سکه بهار آزادی: {bahar_coin}\n"
        msg += f"🔹 نیم سکه: {int(half_coin):,} تومان\n" if half_coin.isdigit() else f"🔹 نیم سکه: {half_coin}\n"
        msg += f"🔹 ربع سکه: {int(quarter_coin):,} تومان\n\n" if quarter_coin.isdigit() else f"🔹 ربع سکه: {quarter_coin}\n\n"

        msg += "--- ارزها ---\n"
        msg += f"💵 دلار: {int(usd):,} تومان\n" if usd.isdigit() else f"💵 دلار: {usd}\n"
        msg += f"💶 یورو: {int(eur):,} تومان\n" if eur.isdigit() else f"💶 یورو: {eur}\n"
        msg += f"💷 پوند: {int(gbp):,} تومان\n" if gbp.isdigit() else f"💷 پوند: {gbp}\n"
        msg += f"🇨🇦 دلار کانادا: {int(cad):,} تومان\n" if cad.isdigit() else f"🇨🇦 دلار کانادا: {cad}\n"
        msg += f"🇹🇷 لیر ترکیه: {int(try_lira):,} تومان\n\n" if try_lira.isdigit() else f"🇹🇷 لیر ترکیه: {try_lira}\n\n"

        msg += "--- رمز ارزها ---\n"
        msg += f"بیت کوین: {float(btc):,} دلار\n" if btc.replace('.', '', 1).isdigit() else f"₿ بیت کوین: {btc}\n"
        msg += f"اتریوم: {float(eth):,} دلار\n" if eth.replace('.', '', 1).isdigit() else f"Ξ اتریوم: {eth}\n"
        msg += f"تتر: {float(tether):,} دلار" if tether.replace('.', '', 1).isdigit() else f"₮ تتر: {tether}"
        await send_message(msg, msd)

    except Exception as e:
        await send_message(f"⨵ خطا در دریافت قیمت طلا و ارز", msd)




async def process_delete_messages(bot: Robot, message: Message):
    try:
        chat_id = message.chat_id
        sender_id = message.sender_id

        if not await is_start(chat_id):
            return
        if is_anser_2(message.message_id):
            return

        message_ids_dont.append(message.message_id)

        group_data = data.get("group", {}).get(chat_id)
        if not group_data:
            return

        sender_types = detect_user_types(data, group_data, sender_id)
        if not any(t in (1, 2, 3, 4) for t in sender_types):
            return

        match = re.match(r"^حذف\s+(\d+)$", message.text)
        if not match:
            return

        count = int(match.group(1))

        if count <= 0:
            await send_message("⨵ تعداد باید بیشتر از صفر باشد!", message)
            return

        if count > MAX_DELETE:
            await send_message(f"⨵ حداکثر تعداد حذف {MAX_DELETE} پیام است!", message)
            return

        group_messages_dict = data_save.get(chat_id)
        if not group_messages_dict:
            await send_message("⨵ هیچ پیامی برای حذف موجود نیست!", message)
            return

        last_messages = list(group_messages_dict.values())[-count:]

        deleted = 0
        for msg in last_messages:
            try:
                await bot.delete_message(chat_id, msg["message_id"])
                group_messages_dict.pop(msg["message_id"], None)
                deleted += 1
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"DELETE ERROR {msg['message_id']}: {e}")

        await send_message(
            f"✅ {deleted} پیام از {count} پیام آخر حذف شدند.",
            message,
            reply=False
        )

    except Exception as e:
        print("DELETE TASK ERROR:", e)



async def send_message(text, message:Message, time_del=None, reply = True):
    try:
        if data["group"].get(message.chat_id, {}).get("font", None) != None:
            text = font_farsi(text,data["group"][message.chat_id]["font"])
        data["number_message_send"] += 1
        if reply == True:
            xx = await bot.send_message(message.chat_id, text, reply_to_message_id=message.message_id, delete_after=time_del)
        else:
            xx = await bot.send_message(message.chat_id, text,delete_after=time_del)
        return xx
    except:
        None

async def send_gif(path, message:Message):
    xx = await bot.send_gif(message.chat_id, path=path, reply_to_message_id=message.message_id)

async def send_message_keypad(text, message, keypad):
    xx = await message.reply_keypad(text,keypad=keypad)

async def send_message_inline(text, message, keypad):
    xx = await message.reply_inline(text,inline_keypad=keypad)

async def send_message_inline_keypad(text, message, inline, keypad):
    xx = await message.reply(text, inline_keypad=inline , chat_keypad = keypad)

async def send_image(path, message, text):
    await message.reply_image(path=path, text= text)


async def ban_user_group(chat_id, sender_id, message, silent_text=False, reply=None, text_ban = None):
    if text_ban:
        try:
            await bot.ban_member_chat(chat_id=chat_id, user_id=sender_id)

            if silent_text:
                return True

            name, _, _, _ = await get_name(sender_id)

            await send_message(text_ban, message, 30)
            return True
        except Exception:
            return False
    

    try:
        await bot.ban_member_chat(chat_id=chat_id, user_id=sender_id)

        if silent_text:
            return True

        name, _, _, _ = await get_name(sender_id)

        text = (
            f"⬡ [{name}]({sender_id}) بن شد."
            if name else
            f"[بن]({sender_id}) شد."
        )

        await send_message(text, message, 30)
        return True

    except Exception:
        return False



async def process_tag_users(bot: Robot, message: Message):
    try:
        chat_id = message.chat_id
        sender_id = message.sender_id

        if not await is_start(chat_id):
            return
        if is_anser_2(message.message_id):
            return

        message_ids_dont.append(message.message_id)

        group_data = data.get("group", {}).get(chat_id)
        if not group_data:
            return

        sender_types = detect_user_types(data, group_data, sender_id)
        if not any(t in (1, 2, 3, 4) for t in sender_types):
            return

        match = re.match(r"^تگ\s+(\d+)$", message.text)
        if not match:
            return

        count = int(match.group(1))

        if count <= 0:
            await send_message("⨵ تعداد باید بیشتر از صفر باشد!", message, time_del=4)
            return

        if count > 100:
            await send_message("⨵ حداکثر تعداد تگ 100 نفر است!", message, time_del=5)
            count = 100

        users_dict = group_data.get("users", {})
        if not users_dict:
            await send_message("⨵ هنوز کاربری در این گروه ثبت نشده است.", message, time_del=4)
            return

        active_users = sorted(
            users_dict.keys(),
            key=lambda uid: users_dict[uid].get("all_message", 0),
            reverse=True
        )

        if sender_id in active_users:
            active_users.remove(sender_id)

        target_users = active_users[:count]

        if not target_users:
            await send_message("⨵ کاربر فعالی برای تگ کردن یافت نشد.", message, time_del=4)
            return

        await send_message(
            f"🔄 در حال تگ کردن {len(target_users)} کاربر فعال گروه...",
            message,
            time_del=3
        )

        chunk_size = 25

        for i in range(0, len(target_users), chunk_size):
            chunk = target_users[i:i + chunk_size]

            mentions = []

            for uid in chunk:
                user_info = data.get("user", {}).get(uid, {})
                user_name = user_info.get("name")

                display_text = user_name if user_name else random.choice(mention_texts)

                mentions.append(f"[{display_text}]({uid})")

            text = " ، ".join(mentions)

            try:
                await bot.send_message(chat_id, text)
                await asyncio.sleep(1)
            except Exception as e:
                print("TAG ERROR:", e)

    except Exception as e:
        print("TAG TASK ERROR:", e)



async def get_name(sender_id):
    u = data.get("user")
    if not u:
        return None, None, None, None

    info = u.get(sender_id)
    if not info:
        return None, None, None, None

    return (
        info.get("name"),
        info.get("age"),
        info.get("city"),
        info.get("title"),
    )


def get_user_warnings(group_data, user_id):

    user_ectar = group_data.get("user_ectar", {}).get(user_id, {})
    total_warnings = sum(value for value in user_ectar.values() if isinstance(value, int))
    return total_warnings


def get_user_message_count(data_group, user_id):
    user_stats = data_group.get("users", {}).get(user_id, {})
    return user_stats.get("all_message", 0)

async def send_user_amar(group_data, target_user_id):
    x = detect_user_types(data, group_data, target_user_id)

    roles = {
        1: "👑 سازنده",
        0: "🤖 ربات",
        2: "⭐ ادمین کل",
        3: "🔰 مالک",
        4: "🛡️ ادمین",
    }

    text_type = "👤 کاربر عادی"
    for role_id in [0, 1, 2, 3, 4]:
        if role_id in x:
            text_type = roles[role_id]
            break

    user_stats = group_data.get("users", {}).get(target_user_id)
    if not user_stats:
        return "⨵ آمار کاربر یافت نشد."

    user_ectar = group_data.get("user_ectar", {}).get(target_user_id, {})
    total_warnings = sum(
        value for value in user_ectar.values()
        if isinstance(value, int)
    )

    name, age, city, title = await get_name(target_user_id)

    stats = group_data.get("stats", {})
    user_stat = stats.get(str(target_user_id), {"total": 0, "ts": []})

    msg_24h = _count_period(user_stat.get("ts", []), PERIOD_24H)
    msg_7d = _count_period(user_stat.get("ts", []), PERIOD_7D)
    msg_30d = _count_period(user_stat.get("ts", []), PERIOD_30D)
    msg_all = user_stat.get("total", 0)

    total_messages = sum(
        u.get("total", 0)
        for u in stats.values()
    ) or 1

    percentage = (msg_all / total_messages) * 100

    sorted_users = sorted(
        stats.items(),
        key=lambda item: item[1].get("total", 0),
        reverse=True,
    )

    ranks = next(
        (
            index + 1
            for index, (uid, _) in enumerate(sorted_users)
            if uid == str(target_user_id)
        ),
        None
    )
    rank , all_group , _ = get_global_user_rank(data, target_user_id)

    me = (
        f"◄ آمار کاربر : {text_type}\n\n"
        f"○ نام: {name or 'نامشخص'}\n"
        f"○ سن: {age or 'نامشخص'}\n"
        f"○ شهر: {city or 'نامشخص'}\n\n"

        f"📨 تعداد پیام‌ها:\n"
        f"⬡ ۲۴ ساعت گذشته ← {msg_24h:,}\n"
        f"⬡ ۷ روز گذشته ← {msg_7d:,}\n"
        f"⬡ ۳۰ روز گذشته ← {msg_30d:,}\n"
        f"⬡ از ابتدا تاکنون ← {msg_all:,}\n\n"
        
        f"رتبه بین تمام کاربران ربات: {rank}\n\n"

        f"○ سهم از کل پیام‌ها: {percentage:.2f}%\n"
        f"○ رتبه در بین کاربران فعال گروه: {ranks or '-'}\n"
        f"○ تعداد کل اخطار: {total_warnings}\n"
        f"○ شناسه: {target_user_id}\n"
    )

    return me

def get_global_user_rank(data, user_id):
    users = {}

    for group in data.get("group", {}).values():
        stats = group.get("stats", {})

        for uid, info in stats.items():
            users.setdefault(uid, 0)

            users[uid] += _count_period(
                info.get("ts", []),
                PERIOD_30D
            )

    ranking = sorted(
        users.items(),
        key=lambda x: x[1],
        reverse=True
    )

    total_users = len(ranking)

    for rank, (uid, count) in enumerate(ranking, start=1):
        if uid == str(user_id):
            return rank, total_users, count

    return None, total_users, 0

def get_group_rank(data: dict, current_group_id):
    groups = []

    for gid, group in data.get("group", {}).items():
        stats = group.get("stats", {})

        msg_30d = sum(
            _count_period(user.get("ts", []), PERIOD_30D)
            for user in stats.values()
        )

        groups.append((gid, msg_30d))

    groups.sort(key=lambda x: x[1], reverse=True)

    total_groups = len(groups)

    for rank, (gid, count) in enumerate(groups, start=1):
        if gid == current_group_id:
            return rank, total_groups, count

    return None, total_groups, 0



PERIOD_24H  = 86400
PERIOD_7D   = 604800
PERIOD_30D  = 2592000

def update_user_stats(group_data: dict, sender_id) -> None:
    stats = group_data.setdefault("stats", {})
    now   = int(time.time())

    key = str(sender_id)
    if key not in stats:
        stats[key] = {"total": 0, "ts": []}

    u = stats[key]
    u["total"] += 1
    u["ts"].append(now)

    cutoff = now - PERIOD_30D
    if len(u["ts"]) > 500:
        u["ts"] = [t for t in u["ts"] if t >= cutoff]

def _count_period(ts_list: list, seconds: int) -> int:
    cutoff = int(time.time()) - seconds
    return sum(1 for t in ts_list if t >= cutoff)


async def send_group_stats(group_data: dict, message) -> None:

    stats      = group_data.get("stats", {})
    group_name = group_data.get("group_name") or "گروه"

    all_ts = [ts for u in stats.values() for ts in u.get("ts", [])]
    grp_24h = _count_period(all_ts, PERIOD_24H)
    grp_7d  = _count_period(all_ts, PERIOD_7D)
    grp_30d = _count_period(all_ts, PERIOD_30D)
    grp_all = sum(u.get("total", 0) for u in stats.values())

    user_scores = {
        uid: _count_period(u.get("ts", []), PERIOD_30D)
        for uid, u in stats.items()
    }
    top5 = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)[:5]

    if top5:
        names_raw = await asyncio.gather(*[get_name(uid) for uid, _ in top5])
    else:
        names_raw = []

    medals = ["🥇", "🥈", "🥉", "④", "⑤"]

    now_jalali = jdatetime.datetime.now().strftime("%Y/%m/%d | %H:%M")
    rank , all_group , _ = get_group_rank(data, message.chat_id)

    lines = [
        f"📊 آمار گروه",
        f"◈ {group_name}",
        "━━━━━━━━━━━━━━",
        "",
        "📨 تعداد پیام‌های گروه:",
        f"⬡ ۲۴ ساعت گذشته  ← {grp_24h:,}",
        f"⬡ ۷ روز گذشته    ← {grp_7d:,}",
        f"⬡ ۳۰ روز گذشته   ← {grp_30d:,}",
        f"⬡ از ابتدا تاکنون ← {grp_all:,}",
        "",
        "━━━━━━━━━━━━━━",
        f"رتبه بین تمام گروه های ربات: {rank} \n"
        "━━━━━━━━━━━━━━",
        "",
        "🏆 فعال‌ترین کاربران (۳۰ روز اخیر):",
    ]

    for i, ((uid, cnt_30d), (name, _, _, _)) in enumerate(zip(top5, names_raw)):
        cnt_all  = stats[uid].get("total", 0)
        cnt_7d   = _count_period(stats[uid].get("ts", []), PERIOD_7D)
        cnt_24h  = _count_period(stats[uid].get("ts", []), PERIOD_24H)
        disp     = name or "کاربر"
        medal    = medals[i]
        lines.append(
            f"{medal} [{disp}]({uid})\n"
            f"    ⤷ ۲۴h: {cnt_24h} │ ۷d: {cnt_7d} │ ۳۰d: {cnt_30d}"
        )

    if not top5:
        lines.append("⨵ هنوز هیچ آماری ثبت نشده است.")

    lines += [
        "",
        "━━━━━━━━━━━━━━",
        f"🗓️ {now_jalali}",
    ]

    await send_message("\n".join(lines), message)



async def send_message_controlled(text, message):
    result = await send_message(text, message)
    return result




def is_anser(_id):
    if _id in message_ids_dont:
        return True
    return False

message_ids_dont_2 = []
message_ids_dont = []

def is_anser_2(_id):
    if _id in message_ids_dont_2:
        return True
    return False


@bot.on_message_group()
async def group(bot: Robot, message: Message):
    if message.chat_id not in group_all_dont_save:
        group_all_dont_save.append(message.chat_id)

    if not await is_start(message.chat_id):
        return
    
    
    global last_save
    data["number_message_get"] += 1

    if time.time() - last_save > SAVE_INTERVAL:
        asyncio.create_task(safe_save())
        last_save = time.time()

    chat_id = message.chat_id
    sender_id = message.sender_id
    text = message.text



    if chat_id not in data_save:
        data_save[chat_id] = OrderedDict()

    data_save[chat_id][message.message_id] = slim_message(message)

    if len(data_save[chat_id]) > MAX_CACHE:
        data_save[chat_id].popitem(last=False)


    reply_chat_id = await reply_chat(message)
    if reply_chat_id == False:
        reply_chat_id = None

    g = data["group"][chat_id]

    type_user = detect_user_types(data, g, sender_id)
    type_messages = detect_message_types(message, g)

    if 0 not in type_user:
        update_user_stats(g, sender_id)

    if any(t in type_user for t in (0, 1, 2, 3, 4)):
        return



    if 5 in type_user:
        await message.delete()
        message_ids_dont.append(message.message_id)
        return
    
    if 7 in type_user:
        return

    if 6 in type_user:
        return

    if 8 in type_user:
        asyncio.create_task(ban_user_group(message.chat_id, message.sender_id, message, text_ban=f"در لیست کیل بود و [بن]({message.sender_id}) شد "))
        message_ids_dont.append(message.message_id)
        return


    await manager_user(
                chat_id, sender_id,
                type_messages, g, message
            )



@bot.on_edited_message()
async def edit(bot:Robot, message:Message):
    global message_ids_dont, message_ids_dont_2
    if message.chat_id not in group_all_dont_save:
        group_all_dont_save.append(message.chat_id)

    if not await is_start(message.chat_id):
        return
    global last_save
    data["number_message_get"] += 1

    if time.time() - last_save > SAVE_INTERVAL:
        asyncio.create_task(safe_save())
        last_save = time.time()

    chat_id = message.chat_id
    sender_id = message.sender_id
    text = message.text



    if chat_id not in data_save:
        data_save[chat_id] = OrderedDict()

    data_save[chat_id][message.message_id] = slim_message(message)

    if len(data_save[chat_id]) > MAX_CACHE:
        data_save[chat_id].popitem(last=False)


    reply_chat_id = await reply_chat(message)
    if reply_chat_id == False:
        reply_chat_id = None

    g = data["group"][chat_id]

    type_user = detect_user_types(data, g, sender_id)
    type_messages = detect_message_types(message, g)

    if any(t in type_user for t in (0, 1, 2, 3, 4)):
        return

    if 5 in type_user:
        await message.delete()
        message_ids_dont.append(message.message_id)
        message_ids_dont_2.append(message.message_id)
        return
    
    if 7 in type_user:
        return

    if 6 in type_user:
        message_ids_dont.append(message.message_id)
        message_ids_dont_2.append(message.message_id)
        return

    if 8 in type_user:
        asyncio.create_task(ban_user_group(message.chat_id, message.sender_id, message, text_ban=f"در لیست کیل بود و [بن]({message.sender_id}) شد "))
        message_ids_dont.append(message.message_id)
        message_ids_dont_2.append(message.message_id)
        return



@bot.on_message(filters.is_group & filters.text("حذف اصل"))
async def del_aslssf(bot: Robot, message: Message):
    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)
    
    await send_message("برای حذف اصل خود لطفا به پی وی ربات مراجع کنید.")


@bot.on_message(filters.is_group & filters.text_regex(r"^(ثبت اصل|تنظیم اصل)(\s+(.+))?"))
async def set_asl_for_user(bot: Robot, message: Message):

    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    target_id = await reply_chat(message)
    if not target_id:
        await send_message("❌ لطفاً روی پیام کاربری که می‌خواهید برایش اصل ثبت کنید ریپلای کنید.", message)
        return

    match = re.match(r"^(ثبت اصل|تنظیم اصل)(\s+(.+))?", message.text)
    asl_text = (match.group(3) or "").strip() if match else ""

    if not asl_text:
        await send_message(
            "⨵ فرمت صحیح:\nثبت اصل نام سن شهر\nمثال: `ثبت اصل علی 25 تهران`",
            message
        )
        return

    result = await get_asls(asl_text, target_id, data, message.chat_id)
    await send_message(result, message)







async def build_admin_list_text(admin_dict: Dict[str, Any]) -> str:

    if not admin_dict:
        return ""

    now = int(time.time())
    users_to_remove = []
    lines = []

    for user_id, info in admin_dict.items():
        name = info.get("name", "کاربر")
        end_time = info.get("end_time")

        if end_time is None:
            status = "👑 همیشه"
            lines.append(f"- [{name}]({user_id}) — {status}")
        else:
            remaining = end_time - now
            if remaining <= 0:
                users_to_remove.append(user_id)
            else:
                minutes = remaining // 60
                hours = minutes // 60
                if hours > 0:
                    status = f"⏳ {hours} ساعت و {minutes % 60} دقیقه"
                else:
                    status = f"⏳ {minutes} دقیقه"
                lines.append(f"- [{name}]({user_id}) — {status} \n - `{user_id}`")

    for uid in users_to_remove:
        del admin_dict[uid]

    return "\n".join(lines)



@bot.on_message(filters.is_group & (
    filters.text_equals("حذف لیست ادمین") |
    filters.text_equals("پاکسازی لیست ادمین") |
    filters.text_equals("حذف لیست ویژه") |
    filters.text_equals("پاکسازی لیست ویژه")
))
async def clear_admin_list(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data["group"].get(message.chat_id)
    if not group_data:
        return

    user_type = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3) for t in user_type):
        return

    admin_dict = group_data.get("type_user", {}).get("admin", {})
    if not admin_dict:
        await send_message("✅ لیست قبلاً خالی بود.", message)
        return

    admin_dict.clear()
    target = "ویژه" if "ویژه" in message.text else "ادمین"
    await send_message(f"✅ لیست {target} پاکسازی شد.", message)



@bot.on_message(
    filters.is_group &
    filters.regex(
        r"^حذف\s+(ادمین|ویژه)(?:\s+(u[a-zA-Z0-9]+))?$"
    )
)
async def remove_admin(bot, message: Message):
    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data["group"].get(message.chat_id)
    if not group_data:
        return

    user_type = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3) for t in user_type):
        return

    admin_dict = group_data.setdefault("type_user", {}).setdefault("admin", {})

    target = "ویژه" if "ویژه" in message.text else "ادمین"

    replied_id = None

    parts = message.text.strip().split()

    if len(parts) >= 3:
        user_id = parts[-1].strip()

        if user_id.startswith("u"):
            replied_id = user_id
        else:
            return

    if not replied_id:
        replied_id = await reply_chat(message)

    if not replied_id:
        await send_message(
            "❌ روی پیام کاربر ریپلای کنید یا Chat ID را وارد کنید.",
            message
        )
        return

    try:
        name, _, _, _ = await get_name(replied_id)
    except:
        name = None

    if not name:
        name = "کاربر"

    if replied_id in admin_dict:
        del admin_dict[replied_id]

        await send_message(
            f"✅ [{name}]({replied_id}) از لیست {target} حذف شد.",
            message
        )
    else:
        await send_message(
            f"⨵ [{name}]({replied_id}) در لیست {target} وجود نداشت.",
            message
        )



@bot.on_message(
    filters.is_group & (
        filters.regex(r"^ادمین(\s+\d+)?$") |
        filters.regex(r"^ویژه(\s+\d+)?$") |
        filters.regex(r"^تنظیم ادمین(\s+\d+)?$") |
        filters.regex(r"^تنظیم ویژه(\s+\d+)?$")
    )
)
async def set_admin(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data["group"].get(message.chat_id)
    if not group_data:
        return

    user_type = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3) for t in user_type):
        return

    replied_id = await reply_chat(message)
    if not replied_id:
        await send_message("❌ لطفاً روی پیام کاربر ریپلای کنید.", message)
        return

    name, _, _, _ = await get_name(replied_id)
    if not name:
        name = "کاربر"

    type_user = group_data.setdefault("type_user", {})
    type_user.get("no_ansewr", {}).pop(replied_id, None)
    type_user.get("mauf", {}).pop(replied_id, None)

    if type_user.get("manager") == replied_id:
        await send_message(f"[{name}]({replied_id}) مالک گروه است و نمی‌تواند ادمین/ویژه شود ⨵", message)
        return

    silent_dict = type_user.get("silent", {})
    was_in_silent = replied_id in silent_dict
    if was_in_silent:
        del silent_dict[replied_id]

    parts = message.text.split()
    duration_minutes = None
    is_permanent = True

    if len(parts) >= 2:
        last = parts[-1]
        if last.isdigit():
            duration_minutes = int(last)
            if duration_minutes > 0:
                is_permanent = False
            else:
                await send_message("⚠️ لطفاً یک عدد مثبت وارد کنید (مثال: ادمین 5).", message)
                return

    target = "ویژه" if "ویژه" in message.text else "ادمین"
    admin_dict = type_user.setdefault("admin", {})
    now_ts = int(time.time())
    extra = " (از سکوت خارج شد)" if was_in_silent else ""

    if replied_id not in admin_dict:
        if is_permanent:
            admin_dict[replied_id] = {"name": name, "end_time": None}
            final_msg = f"[{name}]({replied_id}) به عنوان {target} **همیشه** تنظیم شد ✅{extra}"
        else:
            end_time = now_ts + (duration_minutes * 60)
            admin_dict[replied_id] = {"name": name, "end_time": end_time}
            final_msg = f"[{name}]({replied_id}) به عنوان {target} به مدت **{duration_minutes} دقیقه** تنظیم شد ✅{extra}"
    else:
        if is_permanent:
            admin_dict[replied_id]["end_time"] = None
            final_msg = f"[{name}]({replied_id}) دسترسی {target} به **همیشه** تغییر کرد ✅"
        elif duration_minutes:
            new_end = now_ts + (duration_minutes * 60)
            admin_dict[replied_id]["end_time"] = new_end
            final_msg = f"[{name}]({replied_id}) مدت {target} به **{duration_minutes} دقیقه** تمدید شد ✅"
        else:
            final_msg = f"[{name}]({replied_id}) قبلاً {target} بود ⨵"

    await send_message(final_msg, message)



@bot.on_message(filters.is_group & (filters.text_equals("لیست ادمین") | filters.text_equals("لیست ویژه")))
async def admin_list(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data["group"].get(message.chat_id)
    if not group_data:
        return

    user_type = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (0, 1, 2, 3, 4) for t in user_type):
        return

    admin_dict = group_data.get("type_user", {}).get("admin", {})
    target = "ویژه" if "ویژه" in message.text else "ادمین"

    if not admin_dict:
        await send_message(f"**لیست {target} ها: {get_sticr("list_admin")} **\n\n⨵ لیست {target} خالی است 🍀", message)
        return

    text_lines = await build_admin_list_text(admin_dict)
    final_text = f" **لیست {target} ها:  {get_sticr("list_admin")}**\n\n{text_lines}"
    await send_message(final_text, message)



@bot.on_message(filters.is_group & filters.text_equals("مالک"))
async def show_manager(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        await send_message("⨵ اطلاعات گروه یافت نشد.", message)
        return

    manager_id = group_data.get("type_user", {}).get("manager")
    if not manager_id:
        await send_message("⨵ مالک تنظیم نشده است.", message)
        return

    name, _, _, _ = await get_name(manager_id)
    name = name or "کاربر"

    await send_message(f"👑 مالک گروه:\n⬡ [{name}]({manager_id})", message)




@bot.on_message(filters.is_group & filters.text_equals("گزارش گروه"))
async def group_report(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        await send_message("⨵ اطلاعات گروه یافت نشد.", message)
        return

    user_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (0, 1, 2, 3, 4) for t in user_types):
        return

    await send_report(group_data, message)





@bot.on_message(filters.is_group & filters.text_equals("تنظیم مالک"))
async def set_manager(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        await send_message("⨵ اطلاعات گروه یافت نشد.", message)
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3) for t in sender_types):
        return

    replied_id = await reply_chat(message)
    if not replied_id:
        await send_message("❌ لطفاً روی پیام کاربری که می‌خواهید مالک شود ریپلای کنید.", message)
        return

    type_user = group_data.setdefault("type_user", {})
    for key in ["admin", "silent", "no_ansewr", "mauf", "kill"]:
        type_user.get(key, {}).pop(replied_id, None)

    type_user["manager"] = replied_id

    await send_message(f"✅ مالک گروه با موفقیت تنظیم شد.", message)








@bot.on_message(filters.is_group & (filters.text_equals("بن") | filters.text_equals("سیک")))
async def ban_user(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    target_id = await reply_chat(message)
    if not target_id:
        await send_message("❌ لطفاً روی پیام کاربری که می‌خواهید بن کنید ریپلای کنید.", message)
        return

    if target_id == message.sender_id:
        await send_message("⨵ نمی‌توانید خودتان را بن کنید!", message)
        return

    target_types = detect_user_types(data, group_data, target_id)
    if any(t in (1, 2, 3, 4) for t in target_types):
        await send_message("⨵ کاربر دارای مقام مدیریتی است، نمی‌توانید او را بن کنید.", message)
        return
    
    asyncio.create_task(ban_user_group(message.chat_id, target_id, message))


@bot.on_message(filters.is_group & filters.text_equals("انبن"))
async def unban_user(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    target_id = await reply_chat(message)
    if not target_id:
        await send_message("❌ لطفاً روی پیام کاربری که می‌خواهید آنبن کنید ریپلای کنید.", message)
        return

    try:
        await bot.unban_chat_member(chat_id=message.chat_id, user_id=target_id)
        await send_message(f"✅ کاربر [کاربر]({target_id}) آنبن شد.", message)
    except Exception as e:
        await send_message(f"⨵ خطا در آنبن کردن: احتمالاً کاربر بن نبوده یا دسترسی کافی ندارید.", message)





@bot.on_message(
    filters.is_group &
    filters.regex(
        r"^حذف\s+سکوت(?:\s+(u[a-zA-Z0-9]+))?$"
    )
)
async def remove_silent(bot, message: Message):
    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return


    match = re.match(
        r"^حذف\s+سکوت(?:\s+(u[a-zA-Z0-9]+))?$",
        message.text.strip()
    )

    target_id = None

    if match:
        target_id = match.group(1)

    if not target_id:
        target_id = await reply_chat(message)

    if not target_id:
        await send_message(
            "❌ روی پیام کاربر ریپلای کنید یا Chat ID را وارد کنید.",
            message
        )
        return

    if not str(target_id).startswith("u"):
        return

    name, _, _, _ = await get_name(target_id)
    name = name or "کاربر"

    type_user = group_data.setdefault("type_user", {})
    silent_dict = type_user.get("silent")

    if isinstance(silent_dict, list):
        new_dict = {}
        for uid in silent_dict:
            n, _, _, _ = await get_name(uid)
            new_dict[uid] = {
                "name": n or "ناشناس",
                "end_time": None
            }

        type_user["silent"] = new_dict
        silent_dict = new_dict

    elif not isinstance(silent_dict, dict):
        silent_dict = {}
        type_user["silent"] = silent_dict

    if target_id not in silent_dict:
        await send_message(
            f"[{name}]({target_id}) در لیست سکوت نیست ⨵",
            message
        )
        return

    info = silent_dict[target_id]
    was_permanent = info.get("end_time") is None

    del silent_dict[target_id]

    if was_permanent:
        status_text = "🔊 برای همیشه ساکت بود، حالا آزاد شد!"
    else:
        status_text = "🔊 از حالت سکوت خارج شد."

    await send_message(
        f"[{name}]({target_id}) {status_text}",
        message
    )


@bot.on_message(filters.is_group & filters.regex(r"^سکوت(\s+\d+)?$"))
async def mute_user(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    target_id = await reply_chat(message)
    if not target_id:
        await send_message("❌ لطفاً روی پیام کاربری که می‌خواهید ساکت شود ریپلای کنید.", message)
        return

    name, _, _, _ = await get_name(target_id)
    name = name or "کاربر"

    target_types = detect_user_types(data, group_data, target_id)
    if any(t in (1, 2, 3, 4) for t in target_types):
        await send_message(f"⚠️ [{name}]({target_id}) دارای مقام است و نمی‌توانید او را ساکت کنید.", message)
        return

    parts = message.text.strip().split()
    is_permanent = False
    duration_minutes = None

    if len(parts) == 1 and parts[0] == "سکوت":
        is_permanent = True
    elif len(parts) == 3 and parts[1] == "برای" and parts[2] == "همیشه":
        is_permanent = True
    elif len(parts) == 2:
        try:
            duration_minutes = int(parts[1])
            if duration_minutes <= 0:
                raise ValueError
        except ValueError:
            await send_message("❌ لطفاً یک عدد مثبت وارد کنید (مثال: سکوت 10).", message)
            return
    else:
        await send_message("📝 نحوه استفاده:\n- سکوت (برای همیشه)\n- سکوت [عدد] (مثال: سکوت 10)", message)
        return

    type_user = group_data.setdefault("type_user", {})
    silent_dict = type_user.setdefault("silent", {})
    now_ts = int(time.time())

    if target_id in silent_dict:
        if is_permanent:
            silent_dict[target_id]["end_time"] = None
            msg = f"✅ [{name}]({target_id}) حالا **برای همیشه** ساکت شد."
        elif duration_minutes:
            new_end = now_ts + (duration_minutes * 60)
            silent_dict[target_id]["end_time"] = new_end
            msg = f"✅ [{name}]({target_id}) مدت سکوت به **{duration_minutes} دقیقه** تمدید شد."
        else:
            msg = f"ℹ️ [{name}]({target_id}) قبلاً در لیست سکوت بود."
    else:
        info = {"name": name}
        if is_permanent:
            info["end_time"] = None
            msg = f"🔇 [{name}]({target_id}) **برای همیشه** ساکت شد."
        else:
            end_time = now_ts + (duration_minutes * 60)
            info["end_time"] = end_time
            msg = f"🔇 [{name}]({target_id}) به مدت **{duration_minutes} دقیقه** ساکت شد."
        silent_dict[target_id] = info

    await send_message(msg, message)


async def build_silent_list_text(silent_dict: Dict[str, Any]) -> str:
    if not silent_dict:
        return ""

    now = int(time.time())
    to_remove = []
    lines = []

    for uid, info in silent_dict.items():
        name = info.get("name", "کاربر ناشناس")
        end_time = info.get("end_time")

        if end_time is None:
            lines.append(f"- [{name}]({uid}) — 🔴 برای همیشه")
        else:
            remaining = end_time - now
            if remaining <= 0:
                to_remove.append(uid)
            else:
                minutes = remaining // 60
                hours = minutes // 60
                if hours > 0:
                    time_str = f"⏳ {hours} ساعت و {minutes % 60} دقیقه"
                else:
                    time_str = f"⏳ {minutes} دقیقه"
                lines.append(f"- [{name}]({uid}) — {time_str} \n - `{uid}`")

    for uid in to_remove:
        del silent_dict[uid]

    return "\n".join(lines)


@bot.on_message(filters.is_group & filters.text_equals("لیست سکوت"))
async def silent_list(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (0, 1, 2, 3, 4) for t in sender_types):
        return

    silent_dict = group_data.get("type_user", {}).get("silent", {})
    target = " سکوت "


    if not silent_dict:
        await send_message(f"**لیست {target} ها: {get_sticr("list_silent")} **\n\n⨵ لیست {target} خالی است 🍀", message)
        return

    text_lines = await build_silent_list_text(silent_dict)
    await send_message(f"**لیست {target} ها:  {get_sticr("list_silent")} **\n\n{text_lines}", message)


@bot.on_message(filters.is_group & (filters.text_equals("پاکسازی سکوت") | filters.text_equals("پاکسازی لیست سکوت")))
async def clear_silent(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    silent_dict = group_data.get("type_user", {}).get("silent", {})
    if not silent_dict:
        await send_message("✅ لیست سکوت قبلاً خالی بود.", message)
        return

    silent_dict.clear()
    await send_message("✅ لیست سکوت پاکسازی شد و همه کاربران آزاد شدند.", message)








async def build_kill_list_text(kill_dict: Dict[str, Any]) -> str:

    if not kill_dict:
        return ""

    now = int(time.time())
    to_remove = []
    lines = []

    for uid, info in kill_dict.items():
        name = info.get("name", "کاربر ناشناس")
        end_time = info.get("end_time")

        if end_time is None:
            lines.append(f"- [{name}]({uid}) — 💀 برای همیشه")
        else:
            remaining = end_time - now
            if remaining <= 0:
                to_remove.append(uid)
            else:
                minutes = remaining // 60
                hours = minutes // 60
                if hours > 0:
                    time_str = f"⏳ {hours} ساعت و {minutes % 60} دقیقه"
                else:
                    time_str = f"⏳ {minutes} دقیقه"
                lines.append(f"- [{name}]({uid}) — {time_str} \n - `{uid}`")

    for uid in to_remove:
        del kill_dict[uid]

    return "\n".join(lines)



@bot.on_message(filters.is_group & filters.regex(r"^کیل(\s+\d+)?$"))
async def kill_user(bot, message: Message):

    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    target_id = await reply_chat(message)
    if not target_id:
        await send_message("❌ لطفاً روی پیام کاربری که می‌خواهید کیل کنید ریپلای کنید.", message)
        return

    name, _, _, _ = await get_name(target_id)
    name = name or "کاربر"

    target_types = detect_user_types(data, group_data, target_id)
    if any(t in (1, 2, 3, 4) for t in target_types):
        await send_message(f"⚠️ [{name}]({target_id}) دارای مقام است، نمی‌توانید کیل کنید.", message)
        return

    parts = message.text.strip().split()
    is_permanent = True
    duration_minutes = None

    if len(parts) == 2 and parts[1].isdigit():
        duration_minutes = int(parts[1])
        if duration_minutes > 0:
            is_permanent = False
        else:
            await send_message("⚠️ لطفاً یک عدد مثبت وارد کنید (مثال: کیل 5).", message)
            return

    type_user = group_data.setdefault("type_user", {})
    kill_dict = type_user.setdefault("kill", {})
    now_ts = int(time.time())

    if target_id in kill_dict:
        if is_permanent:
            kill_dict[target_id]["end_time"] = None
            msg = f"✅ [{name}]({target_id}) مدت کیل به **همیشه** تغییر کرد 💀"
        elif duration_minutes:
            new_end = now_ts + (duration_minutes * 60)
            kill_dict[target_id]["end_time"] = new_end
            msg = f"✅ [{name}]({target_id}) مدت کیل به **{duration_minutes} دقیقه** تمدید شد 💀"
        else:
            msg = f"ℹ️ [{name}]({target_id}) قبلاً در لیست کیل بود."
    else:
        if is_permanent:
            kill_dict[target_id] = {"name": name, "end_time": None}
            msg = f"💀 [{name}]({target_id}) به لیست کیل **برای همیشه** اضافه شد."
        else:
            end_time = now_ts + (duration_minutes * 60)
            kill_dict[target_id] = {"name": name, "end_time": end_time}
            msg = f"💀 [{name}]({target_id}) به مدت **{duration_minutes} دقیقه** کیل شد."

    await send_message(msg, message)



@bot.on_message(
    filters.is_group &
    filters.regex(
        r"^حذف\s+کیل(?:\s+(u[a-zA-Z0-9]+))?$"
    )
)
async def remove_kill(bot, message: Message):
    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return


    match = re.match(
        r"^حذف\s+کیل(?:\s+(u[a-zA-Z0-9]+))?$",
        message.text.strip()
    )

    target_id = None

    if match:
        target_id = match.group(1)

    if not target_id:
        target_id = await reply_chat(message)

    if not target_id:
        await send_message(
            "❌ روی پیام کاربر ریپلای کنید یا Chat ID را وارد کنید.",
            message
        )
        return

    if not str(target_id).startswith("u"):
        return

    name, _, _, _ = await get_name(target_id)
    name = name or "کاربر"

    kill_dict = group_data.setdefault("type_user", {}).setdefault("kill", {})

    if target_id not in kill_dict:
        await send_message(
            f"[{name}]({target_id}) در لیست کیل نیست ⨵",
            message
        )
        return

    del kill_dict[target_id]

    await send_message(
        f"🔊 [{name}]({target_id}) از لیست کیل خارج شد.",
        message
    )



@bot.on_message(filters.is_group & filters.text_equals("لیست کیل"))
async def kill_list(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (0, 1, 2, 3, 4) for t in sender_types):
        return

    kill_dict = group_data.get("type_user", {}).get("kill", {})


    target = " کیل "


    if not kill_dict:
        await send_message(f"**لیست {target} ها: {get_sticr("list_kill")} **\n\n⨵ لیست {target} خالی است 🍀", message)
        return

    text_lines = await build_kill_list_text(kill_dict)
    await send_message(f"**لیست {target} ها:  {get_sticr("list_kill")} **\n\n{text_lines}", message)



@bot.on_message(filters.is_group & (filters.text_equals("پاکسازی کیل") | filters.text_equals("پاکسازی لیست کیل")))
async def clear_kill(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    kill_dict = group_data.get("type_user", {}).get("kill", {})
    if not kill_dict:
        await send_message("✅ لیست کیل قبلاً خالی بود.", message)
        return

    kill_dict.clear()
    await send_message("✅ لیست کیل پاکسازی شد و همه کاربران آزاد شدند.", message)







async def build_mauf_list_text(mauf_dict: Dict[str, Any]) -> str:
    if not mauf_dict:
        return ""

    now = int(time.time())
    to_remove = []
    lines = []

    for uid, info in mauf_dict.items():
        name = info.get("name", "کاربر ناشناس")
        end_time = info.get("end_time")

        if end_time is None:
            lines.append(f"- [{name}]({uid}) — 🛡️ برای همیشه")
        else:
            remaining = end_time - now
            if remaining <= 0:
                to_remove.append(uid)
            else:
                minutes = remaining // 60
                hours = minutes // 60
                if hours > 0:
                    time_str = f"⏳ {hours} ساعت و {minutes % 60} دقیقه"
                else:
                    time_str = f"⏳ {minutes} دقیقه"
                lines.append(f"- [{name}]({uid}) — {time_str} \n - `{uid}`")

    for uid in to_remove:
        del mauf_dict[uid]

    return "\n".join(lines)



@bot.on_message(filters.is_group & filters.regex(r"^معاف(\s+\d+)?$"))
async def set_mauf(bot, message: Message):

    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    target_id = await reply_chat(message)
    if not target_id:
        await send_message("❌ لطفاً روی پیام کاربری که می‌خواهید معاف شود ریپلای کنید.", message)
        return

    name, _, _, _ = await get_name(target_id)
    name = name or "کاربر"

    target_types = detect_user_types(data, group_data, target_id)
    if any(t in (1, 2, 3, 4) for t in target_types):
        await send_message(f"⚠️ [{name}]({target_id}) دارای مقام است، نمی‌توانید معاف کنید.", message)
        return

    parts = message.text.strip().split()
    is_permanent = True
    duration_minutes = None

    if len(parts) == 2 and parts[1].isdigit():
        duration_minutes = int(parts[1])
        if duration_minutes > 0:
            is_permanent = False
        else:
            await send_message("⚠️ لطفاً یک عدد مثبت وارد کنید (مثال: معاف 5).", message)
            return


    type_user = group_data.setdefault("type_user", {})
    mauf_dict = type_user.setdefault("mauf", {})
    now_ts = int(time.time())

    if target_id in mauf_dict:
        if is_permanent:
            mauf_dict[target_id]["end_time"] = None
            msg = f"✅ [{name}]({target_id}) مدت معافیت به **همیشه** تغییر کرد 🛡️"
        elif duration_minutes:
            new_end = now_ts + (duration_minutes * 60)
            mauf_dict[target_id]["end_time"] = new_end
            msg = f"✅ [{name}]({target_id}) مدت معافیت به **{duration_minutes} دقیقه** تمدید شد 🛡️"
        else:
            msg = f"ℹ️ [{name}]({target_id}) قبلاً در لیست معاف بود."
    else:
        if is_permanent:
            mauf_dict[target_id] = {"name": name, "end_time": None}
            msg = f"🛡️ [{name}]({target_id}) به لیست معاف **برای همیشه** اضافه شد."
        else:
            end_time = now_ts + (duration_minutes * 60)
            mauf_dict[target_id] = {"name": name, "end_time": end_time}
            msg = f"🛡️ [{name}]({target_id}) به مدت **{duration_minutes} دقیقه** معاف شد."

    await send_message(msg, message)


@bot.on_message(
    filters.is_group &
    filters.regex(
        r"^حذف\s+معاف(?:\s+(u[a-zA-Z0-9]+))?$"
    )
)
async def remove_mauf(bot, message: Message):
    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return


    match = re.match(
        r"^حذف\s+معاف(?:\s+(u[a-zA-Z0-9]+))?$",
        message.text.strip()
    )

    target_id = None

    if match:
        target_id = match.group(1)

    if not target_id:
        target_id = await reply_chat(message)

    if not target_id:
        await send_message(
            "❌ روی پیام کاربر ریپلای کنید یا Chat ID را وارد کنید.",
            message
        )
        return

    if not str(target_id).startswith("u"):
        return

    name, _, _, _ = await get_name(target_id)
    name = name or "کاربر"

    mauf_dict = group_data.setdefault("type_user", {}).setdefault("mauf", {})

    if target_id not in mauf_dict:
        await send_message(
            f"[{name}]({target_id}) در لیست معاف نیست ⨵",
            message
        )
        return

    del mauf_dict[target_id]

    await send_message(
        f"🔊 [{name}]({target_id}) از لیست معاف خارج شد.",
        message
    )


@bot.on_message(filters.is_group & filters.text_equals("لیست معاف"))
async def list_mauf(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (0, 1, 2, 3, 4) for t in sender_types):
        return

    mauf_dict = group_data.get("type_user", {}).get("mauf", {})


    target = " معاف "


    if not mauf_dict:
        await send_message(f"**لیست {target} ها: {get_sticr("list_mauf")} **\n\n⨵ لیست {target} خالی است 🍀", message)
        return

    text_lines = await build_mauf_list_text(mauf_dict)
    await send_message(f" **لیست {target} ها:  {get_sticr("list_mauf")}**\n\n{text_lines}", message)



@bot.on_message(filters.is_group & (filters.text_equals("پاکسازی معاف") | filters.text_equals("پاکسازی لیست معاف")))
async def clear_mauf(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    mauf_dict = group_data.get("type_user", {}).get("mauf", {})
    if not mauf_dict:
        await send_message("✅ لیست معاف قبلاً خالی بود.", message)
        return

    mauf_dict.clear()
    await send_message("✅ لیست معاف پاکسازی شد و همه کاربران آزاد شدند.", message)







async def build_no_ansewr_list_text(no_ansewr_dict: Dict[str, Any]) -> str:

    if not no_ansewr_dict:
        return ""

    now = int(time.time())
    to_remove = []
    lines = []

    for uid, info in no_ansewr_dict.items():
        name = info.get("name", "کاربر ناشناس")
        end_time = info.get("end_time")

        if end_time is None:
            lines.append(f"- [{name}]({uid}) — ⚠️ برای همیشه")
        else:
            remaining = end_time - now
            if remaining <= 0:
                to_remove.append(uid)
            else:
                minutes = remaining // 60
                hours = minutes // 60
                if hours > 0:
                    time_str = f"⏳ {hours} ساعت و {minutes % 60} دقیقه"
                else:
                    time_str = f"⏳ {minutes} دقیقه"
                lines.append(f"- [{name}]({uid}) — {time_str} \n - `{uid}`")

    for uid in to_remove:
        del no_ansewr_dict[uid]

    return "\n".join(lines)



@bot.on_message(filters.is_group & filters.regex(r"^بی اهمیت(\s+\d+)?$"))
async def set_no_ansewr(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    target_id = await reply_chat(message)
    if not target_id:
        await send_message("❌ لطفاً روی پیام کاربری که می‌خواهید بی اهمیت شود ریپلای کنید.", message)
        return

    name, _, _, _ = await get_name(target_id)
    name = name or "کاربر"

    target_types = detect_user_types(data, group_data, target_id)
    if any(t in (1, 2, 3, 4) for t in target_types):
        await send_message(f"⚠️ [{name}]({target_id}) دارای مقام است، نمی‌توانید بی اهمیت کنید.", message)
        return

    parts = message.text.strip().split()
    is_permanent = True
    duration_minutes = None

    if len(parts) == 2 and parts[1].isdigit():
        duration_minutes = int(parts[1])
        if duration_minutes > 0:
            is_permanent = False
        else:
            await send_message("⚠️ لطفاً یک عدد مثبت وارد کنید (مثال: بی اهمیت 5).", message)
            return

    type_user = group_data.setdefault("type_user", {})
    no_ansewr_dict = type_user.setdefault("no_ansewr", {})
    now_ts = int(time.time())

    if target_id in no_ansewr_dict:
        if is_permanent:
            no_ansewr_dict[target_id]["end_time"] = None
            msg = f"✅ [{name}]({target_id}) مدت بی اهمیتی به **همیشه** تغییر کرد ⚠️"
        elif duration_minutes:
            new_end = now_ts + (duration_minutes * 60)
            no_ansewr_dict[target_id]["end_time"] = new_end
            msg = f"✅ [{name}]({target_id}) مدت بی اهمیتی به **{duration_minutes} دقیقه** تمدید شد ⚠️"
        else:
            msg = f"ℹ️ [{name}]({target_id}) قبلاً در لیست بی اهمیت بود."
    else:
        if is_permanent:
            no_ansewr_dict[target_id] = {"name": name, "end_time": None}
            msg = f"⚠️ [{name}]({target_id}) به لیست بی اهمیت **برای همیشه** اضافه شد."
        else:
            end_time = now_ts + (duration_minutes * 60)
            no_ansewr_dict[target_id] = {"name": name, "end_time": end_time}
            msg = f"⚠️ [{name}]({target_id}) به مدت **{duration_minutes} دقیقه** بی اهمیت شد."

    await send_message(msg, message)


@bot.on_message(
    filters.is_group &
    filters.regex(
        r"^حذف\s+بی\s+اهمیت(?:\s+(u[a-zA-Z0-9]+))?$"
    )
)
async def remove_no_ansewr(bot, message: Message):
    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return


    match = re.match(
        r"^حذف\s+بی\s+اهمیت(?:\s+(u[a-zA-Z0-9]+))?$",
        message.text.strip()
    )

    target_id = None

    if match:
        target_id = match.group(1)

    if not target_id:
        target_id = await reply_chat(message)

    if not target_id:
        await send_message(
            "❌ روی پیام کاربر ریپلای کنید یا Chat ID را وارد کنید.",
            message
        )
        return

    if not str(target_id).startswith("u"):
        return

    name, _, _, _ = await get_name(target_id)
    name = name or "کاربر"

    no_ansewr_dict = (
        group_data
        .setdefault("type_user", {})
        .setdefault("no_ansewr", {})
    )

    if target_id not in no_ansewr_dict:
        await send_message(
            f"[{name}]({target_id}) در لیست بی اهمیت نیست ⨵",
            message
        )
        return

    del no_ansewr_dict[target_id]

    await send_message(
        f"🔊 [{name}]({target_id}) از لیست بی اهمیت خارج شد.",
        message
    )


@bot.on_message(filters.is_group & filters.text_equals("لیست بی اهمیت"))
async def list_no_ansewr(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (0, 1, 2, 3, 4) for t in sender_types):
        return

    no_ansewr_dict = group_data.get("type_user", {}).get("no_ansewr", {})



    target = " بی اهمیت "



    if not no_ansewr_dict:
        await send_message(f"**لیست {target} ها: {get_sticr("list_ansewr")} **\n\n⨵ لیست {target} خالی است 🍀", message)
        return

    text_lines = await build_no_ansewr_list_text(no_ansewr_dict)
    await send_message(f"**لیست {target} ها:  {get_sticr("list_ansewr")} **\n\n{text_lines}", message)



@bot.on_message(filters.is_group & (filters.text_equals("پاکسازی بی اهمیت") | filters.text_equals("پاکسازی لیست بی اهمیت")))
async def clear_no_ansewr(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    no_ansewr_dict = group_data.get("type_user", {}).get("no_ansewr", {})
    if not no_ansewr_dict:
        await send_message("✅ لیست بی اهمیت قبلاً خالی بود.", message)
        return

    no_ansewr_dict.clear()
    await send_message("✅ لیست بی اهمیت پاکسازی شد و همه کاربران آزاد شدند.", message)







@bot.on_message(filters.is_group & filters.text_equals("حذف"))
async def delete_message(bot: Robot, message: Message):
    asyncio.create_task(process_delete_message(bot, message))


async def process_delete_message(bot: Robot, message: Message):
    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    target_msg_id = message.reply_to_message_id

    if not target_msg_id:
        await send_message(
            "❌ لطفاً روی پیامی که می‌خواهید حذف شود ریپلای کنید.",
            message
        )
        return

    try:
        await bot.delete_message(message.chat_id, target_msg_id)
        await bot.delete_message(message.chat_id, message.message_id)

        await send_message(
            "✅ پیام مورد نظر حذف شد.",
            message,
            time_del=10
        )

    except Exception:
        await send_message(
            "⨵ خطا در حذف پیام. شاید دسترسی کافی ندارید یا پیام قبلاً حذف شده است.",
            message
        )




@bot.on_message(filters.is_group & filters.text_regex(r"^تگ\s+(\d+)$"))
async def tag_active_users(bot: Robot, message: Message):
    asyncio.create_task(process_tag_users(bot, message))



@bot.on_message(filters.is_group & filters.text_regex(r"^حذف\s+(\d+)$"))
async def delete_last_messages(bot: Robot, message: Message):
    asyncio.create_task(process_delete_messages(bot, message))







@bot.on_message(filters.is_group & filters.text_equals("لیست قفل"))
async def show_lock_list(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)
    group_data = data["group"][message.chat_id]
    await send_message(status_text(group_data["type_message"]), message)


ACTION_LABELS = {
    "delete": "حذف",
    "ban":    "بن",
    "ectar":  "اخطار",
}

SECTION_DIVIDER = "┄" * 20


def format_filter_entry(name: str, config: dict) -> str | None:
    if not isinstance(config, dict):
        return None

    active = [label for key, label in ACTION_LABELS.items() if config.get(key)]
    warns  = int(config.get("num_ectar", 0))

    if active:
        actions_str = "  |  ".join(active)
        warn_str    = f"  |    {warns} اخطار" if warns else ""
        return f"🔴 {name}\n  ( {actions_str}{warn_str} )   ↳"
    else:
        return f"🟢 {name}"


def get_sticr(list_gofl):
    return "〔〕"



def status_text(settings: dict) -> str:
    locked   = []
    unlocked = []

    for msg_type, config in settings.items():
        name  = translate_en_fa.get(msg_type, msg_type)
        entry = format_filter_entry(name, config)

        if entry is None:
            continue
        (locked if config.get("delete") or config.get("ban") or config.get("ectar") else unlocked).append(entry)

    lines = [
        f"         وضعیت فیلترها  : {get_sticr("list_gofl")}   ",
        "",
    ]

    if locked:
        lines += [f"🔒 فیلترهای فعال ({len(locked)})", SECTION_DIVIDER]
        lines += locked
        lines.append("")

    if unlocked:
        lines += [f"🔓 فیلترهای غیرفعال ({len(unlocked)})", SECTION_DIVIDER]
        lines += unlocked

    return "\n".join(lines).strip()




@bot.on_message(filters.is_group & filters.text_equals("اخطار"))
async def give_warning(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)
    


    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return
    


    target_id = await reply_chat(message)
    if not target_id:
        await send_message("❌ لطفاً روی پیام کاربری که می‌خواهید اخطار دهید ریپلای کنید.", message)
        return

    name, _, _, _ = await get_name(target_id)
    name = name or "کاربر"


    target_types = detect_user_types(data, group_data, target_id)
    if any(t in (1, 2, 3, 4) for t in target_types):
        await send_message(f"⚠️ [{name}]({target_id}) دارای مقام است، نمی‌توانید اخطار دهید.", message)
        return

    user_ectar = group_data.setdefault("user_ectar", {})
    if target_id not in user_ectar:
        user_ectar[target_id] = {k: 0 for k in [
            "filters", "spam", "text", "forwarded", "link", "id", "photo",
            "video", "audio", "voice", "document", "archive", "executable",
            "font", "sticker", "poll", "contact", "location", "live_location",
            "unknown", "ectar", "hash", "hang_code", "metadata", "gif"
        ]}
        
    user_ectar[target_id]["ectar"] += 1
    current = user_ectar[target_id]["ectar"]
    limit = group_data.get("num_ectar", 3)

    if current >= limit:
        asyncio.create_task(ban_user_group(message.chat_id, target_id, message,
                            text_ban=f"⨵ [{name}]({target_id}) به دلیل رسیدن به {limit} اخطار بن شد."))

        user_ectar[target_id]["ectar"] = 0
    else:
        await send_message(
            f"⚠️ اخطار {name}: {current}/{limit}",
            message, time_del=10
        )



@bot.on_message(filters.is_group & filters.text_equals("حذف اخطار"))
async def clear_warnings(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    target_id = await reply_chat(message)
    if not target_id:
        await send_message("❌ لطفاً روی پیام کاربری که می‌خواهید اخطارهایش پاک شود ریپلای کنید.", message)
        return

    name, _, _, _ = await get_name(target_id)
    name = name or "کاربر"

    user_ectar = group_data.get("user_ectar", {})
    if target_id not in user_ectar:
        await send_message(f"[{name}]({target_id}) هیچ اخطاری ندارد.", message)
        return

    default_keys = [
        "filters", "spam", "text", "forwarded", "link", "id", "photo",
        "video", "audio", "voice", "document", "archive", "executable",
        "font", "sticker", "poll", "contact", "location", "live_location",
        "unknown", "ectar", "hash", "hang_code", "metadata", "gif"
    ]
    user_ectar[target_id] = {k: 0 for k in default_keys}

    await send_message(f"✅ اخطارهای {name} پاک شد.", message)


@bot.on_message(filters.is_group & filters.text_regex(r"^(تعداد اخطار|تعداد اخطارم|تعداد اخطارش)$"))
async def user_warning_count(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_id = str(message.sender_id)
    replied_id = await reply_chat(message)
    cmd = message.text

    if cmd == "تعداد اخطار":
        target_id = replied_id if replied_id else sender_id
    elif cmd == "تعداد اخطارم":
        target_id = sender_id
    else:
        if replied_id:
            target_id = str(replied_id)
        else:
            await send_message("⨵ لطفاً روی پیام فرد ریپلای کنید.", message)
            return

    warnings = get_user_warnings(group_data, target_id)
    await send_message(f"⚠️ تعداد کل اخطارها: {warnings}", message)


@bot.on_message(filters.is_group & filters.text_regex(r"^ضد (\S+) (خاموش|غیرفعال)$"))
async def anti_off(bot, message: Message):
    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(
        r"^ضد (\S+) (خاموش|غیرفعال)$",
        message.text.strip()
    )
    if not match:
        return

    key_fa, status = match.groups()

    key = translate_fa_en.get(key_fa)
    if not key:
        return

    type_message = group_data.setdefault("type_message", {})

    if key not in type_message:

        return

    config = type_message[key]

    if (
        config.get("delete") is False
        and config.get("ban") is False
        and config.get("ectar") is False
    ):
        await send_message(
            f"⨵ فیلتر {key_fa} از قبل {status} بوده است.",
            message
        )
        return

    config["delete"] = False
    config["ban"] = False
    config["ectar"] = False

    await send_message(
        f"✅ فیلتر {key_fa} {status} شد.",
        message
    )



@bot.on_message(
    filters.is_group &
    filters.text_regex(r"^(.+?)\s+(روشن|فعال|باز)$")
)
async def enable_funny_feature(bot, message: Message):

    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(
        r"^(.+?)\s+(روشن|فعال|باز)$",
        message.text.strip()
    )
    if not match:
        return

    key_fa, status = match.groups()

    key_fa = key_fa.strip()
    key = translate_fa_en_sar.get(key_fa)

    if not key:
        return

    funny = group_data.setdefault("funny", {})
    funny[key] = True

    await send_message(
        f"✅ {key_fa} {status} شد.",
        message
    )


@bot.on_message(
    filters.is_group &
    filters.text_regex(r"^(.+?)\s+(خاموش|غیرفعال|قفل)$")
)
async def disable_funny_feature(bot, message: Message):
    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(
        r"^(.+?)\s+(خاموش|غیرفعال|قفل)$",
        message.text.strip()
    )
    if not match:
        return

    key_fa, status = match.groups()

    key_fa = key_fa.strip()
    key = translate_fa_en_sar.get(key_fa)

    if not key:
        return

    funny = group_data.setdefault("funny", {})
    funny[key] = False

    await send_message(
        f"✅ {key_fa} {status} شد.",
        message
    )






@bot.on_message(filters.is_group & filters.text_regex(r"^(\S+) (باز)$"))
async def unlock_message_type(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^(\S+) (باز)$", message.text)
    if not match:
        return

    key_fa, status = match.groups()
    key = translate_fa_en.get(key_fa)
    if not key:
      
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["delete"] = False
    type_message[key]["ban"] = False
    type_message[key]["ectar"] = False
    await send_message(f"✅ {key_fa} {status} شد.", message)



@bot.on_message(filters.is_group & filters.text_regex(r"^ضد (\S+) (روشن|فعال)$"))
async def enable_filter_for_type(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^ضد (\S+) (روشن|فعال)$", message.text)
    if not match:
        return

    key_fa, status = match.groups()
    key = translate_fa_en.get(key_fa)
    if not key:
        
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["delete"] = True
    type_message[key]["ban"] = True
    type_message[key]["ectar"] = True
    await send_message(f"✅ {key_fa} {status} شد.", message)


@bot.on_message(filters.is_group & filters.text_regex(r"^(\S+) (قفل)$"))
async def lock_message_type(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^(\S+) (قفل)$", message.text)
    if not match:
        return

    key_fa, status = match.groups()
    key = translate_fa_en.get(key_fa)
    if not key:
       
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["delete"] = True
    type_message[key]["ban"] = True
    type_message[key]["ectar"] = True
    await send_message(f"✅ {key_fa} {status} شد.", message)




@bot.on_message(filters.is_group & filters.text_regex(r"^اخطار (\S+) (روشن|فعال)$"))
async def warning_on(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^اخطار (\S+) (روشن|فعال)$", message.text)
    if not match:
        return

    key_fa, _ = match.groups()
    key = translate_fa_en.get(key_fa)
    if not key:
        
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["ectar"] = True
    await send_message(f"✅ اخطار {key_fa} فعال شد.", message)





@bot.on_message(filters.is_group & filters.text_regex(r"^اخطار (\S+) (خاموش|غیرفعال)$"))
async def warning_off(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^اخطار (\S+) (خاموش|غیرفعال)$", message.text)
    if not match:
        return

    key_fa, _ = match.groups()
    key = translate_fa_en.get(key_fa)
    if not key:
      
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["ectar"] = False
    await send_message(f"✅ اخطار {key_fa} غیرفعال شد.", message)


@bot.on_message(filters.is_group & filters.text_regex(r"^اخطار (\S+) (\d+)$"))
async def set_warning_count(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^اخطار (\S+) (\d+)$", message.text)
    if not match:
        return

    key_fa, num_str = match.groups()
    key = translate_fa_en.get(key_fa)
    if not key:
     
        return

    try:
        num = int(num_str)
        if num <= 0:
            raise ValueError
    except ValueError:
        await send_message("⨵ لطفاً یک عدد مثبت وارد کنید.", message)
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["num_ectar"] = num
    await send_message(f"✅ تعداد اخطار برای {key_fa} به {num} تنظیم شد.", message)




@bot.on_message(filters.is_group & filters.text_regex(r"^تنظیم اخطار (\S+) (\d+)$"))
async def set_warning_count_alt(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        await send_message("⨵ شما اجازه این کار را ندارید.", message)
        return

    match = re.match(r"^تنظیم اخطار (\S+) (\d+)$", message.text)
    if not match:
        return

    key_fa, num_str = match.groups()
    key = translate_fa_en.get(key_fa.strip())
    if not key:
 
        return

    try:
        num = int(num_str)
        if num <= 0:
            raise ValueError
    except ValueError:
        await send_message("⨵ لطفاً یک عدد مثبت وارد کنید.", message)
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["num_ectar"] = num
    await send_message(f"✅ تعداد اخطار برای {key_fa} به {num} تنظیم شد.", message)


@bot.on_message(filters.is_group & filters.text_regex(r"^بن (\S+) (روشن|فعال)$"))
async def ban_on(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^بن (\S+) (روشن|فعال)$", message.text)
    if not match:
        return

    key_fa, _ = match.groups()
    key = translate_fa_en.get(key_fa)
    if not key:
      
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["ban"] = True
    await send_message(f"✅ بن {key_fa} فعال شد.", message)



@bot.on_message(filters.is_group & filters.text_regex(r"^بن (\S+) (خاموش|غیرفعال)$"))
async def ban_off(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^بن (\S+) (خاموش|غیرفعال)$", message.text)
    if not match:
        return

    key_fa, _ = match.groups()
    key = translate_fa_en.get(key_fa)
    if not key:
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["ban"] = False
    await send_message(f"✅ بن {key_fa} غیرفعال شد.", message)



@bot.on_message(filters.is_group & filters.text_regex(r"^حذف (\S+) (روشن|فعال)$"))
async def delete_on(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^حذف (\S+) (روشن|فعال)$", message.text)
    if not match:
        return

    key_fa, _ = match.groups()
    key = translate_fa_en.get(key_fa)
    if not key:
    
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["delete"] = True
    await send_message(f"✅ حذف {key_fa} فعال شد.", message)


@bot.on_message(filters.is_group & filters.text_regex(r"^حذف (\S+) (خاموش|غیرفعال)$"))
async def delete_off(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^حذف (\S+) (خاموش|غیرفعال)$", message.text)
    if not match:
        return

    key_fa, _ = match.groups()
    key = translate_fa_en.get(key_fa)
    if not key:
     
        return

    type_message = group_data.setdefault("type_message", {})
    if key not in type_message:
        await send_message(f"⨵ تنظیمات برای «{key_fa}» وجود ندارد.", message)
        return

    type_message[key]["delete"] = False
    await send_message(f"✅ حذف {key_fa} غیرفعال شد.", message)





@bot.on_message(filters.is_group & filters.text_regex(r"^حذف فیلتر (.+)$"))
async def remove_filter_word(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser(message.message_id):
        return
    if is_anser_2(message.message_id):
        return
    group_data = data["group"][message.chat_id]
    type_user = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1,2,3,4) for t in type_user):
        return

    word = re.match(r"^حذف فیلتر (.+)$", message.text).group(1).strip()

    if word not in group_data["list_filters"]:
        await send_message("این کلمه داخل فیلترها نیست", message)
        return

    group_data["list_filters"].remove(word)

    await send_message(f"کلمه حذف شد ⨵", message)




@bot.on_message(filters.is_group & filters.text_regex(r"^فیلتر (.+)$"))
async def add_filter_word(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^فیلتر (.+)$", message.text)
    if not match:
        return
    word = match.group(1).strip()
    if not word:
        await send_message("⨵ لطفاً یک کلمه معتبر وارد کنید.", message)
        return

    filters_list = group_data.setdefault("list_filters", [])
    if word in filters_list:
        await send_message(f"⚠️ کلمه «{word}» از قبل در لیست فیلتر وجود دارد.", message)
        return

    filters_list.append(word)
    await send_message(f"✅ کلمه «{word}» به لیست فیلتر اضافه شد.", message)



@bot.on_message(filters.is_group & filters.text_regex(r"^(پاکسازی لیست فیلتر|حذف لیست فیلتر)$"))
async def clear_filters_list(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    filters_list = group_data.get("list_filters", [])
    if not filters_list:
        await send_message("✅ لیست فیلترها قبلاً خالی است.", message)
        return

    filters_list.clear()
    await send_message("✅ لیست فیلترهای گروه کاملاً پاک شد.", message)


@bot.on_message(filters.is_group & filters.text_regex(r"^اخطار (\d+)$"))
async def warning_all_number(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    match = re.match(r"^اخطار (\d+)$", message.text)
    if not match:
        return

    try:
        num = int(match.group(1))
        if num <= 0:
            raise ValueError
    except ValueError:
        await send_message("⨵ لطفاً یک عدد مثبت وارد کنید.", message)
        return

    type_message = group_data.get("type_message", {})
    if not type_message:
        await send_message("⨵ تنظیمات فیلتر یافت نشد.", message)
        return

    for config in type_message.values():
        if isinstance(config, dict):
            config["num_ectar"] = num

    group_data["num_ectar"] = num

    await send_message(f"✅ تعداد اخطار برای همه نوع پیام‌ها به {num} تنظیم شد.", message)





@bot.on_message(filters.is_group & filters.text_regex(r"^تنظیم فونت\s+(\S+)$"))
async def set_group_font(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    style_name = message.text.replace("تنظیم فونت", "").strip()
    if not style_name:
        await send_message("⨵ لطفاً نام فونت را وارد کنید.", message)
        return

    fonts = {
        "معمولی": None,
        "کشیده": 1,
        "تشدید": 2,
        "خط": 3,
        "زالگو": 4,
        "موجی": 5,
        "تزئینی": 6,
    }

    if style_name not in fonts:
        await send_message(
            "⨵ فونت نامعتبر است!\n\n"
            "فونت‌های موجود:\n"
            "⨮ معمولی\n"
            "⨮ کشیده\n"
            "⨮ تشدید\n"
            "⨮ خط\n"
            "⨮ زالگو\n"
            "⨮ موجی\n"
            "⨮ تزئینی",
            message
        )
        return

    group_data["font"] = fonts[style_name]
    await send_message(f"✅ فونت پیش‌فرض روی «{style_name}» تنظیم شد.", message)




@bot.on_message(filters.is_group & filters.text_regex(r"^ضد فحش (روشن|فعال)$"))
async def anti_fosh_on(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    filters_list = group_data.setdefault("list_filters", [])
    for word in fosh:
        if word not in filters_list:
            filters_list.append(word)

    type_message = group_data.setdefault("type_message", {})
    filters_config = type_message.setdefault("filters", {})
    filters_config["delete"] = True
    filters_config["ban"] = True
    filters_config["ectar"] = True

    await send_message(f"✅ ضد فحش فعال شد. {len(fosh)} کلمه به لیست فیلتر اضافه شد.", message)


@bot.on_message(filters.is_group & filters.text_regex(r"^ضد فحش (خاموش|غیرفعال)$"))
async def anti_fosh_off(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    filters_list = group_data.get("list_filters", [])
    for word in fosh:
        if word in filters_list:
            filters_list.remove(word)

    await send_message(f"✅ ضد فحش غیرفعال شد. کلمات فحش از لیست فیلتر حذف شدند.", message)



@bot.on_message(filters.is_group & filters.text_regex(r"^ضد تبلیغ (روشن|فعال)$"))
async def anti_ads_on(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    filters_list = group_data.setdefault("list_filters", [])
    for word in anti_ads_words:
        if word not in filters_list:
            filters_list.append(word)

    type_message = group_data.setdefault("type_message", {})
    filters_config = type_message.setdefault("filters", {})
    filters_config["delete"] = True
    filters_config["ban"] = True
    filters_config["ectar"] = True

    await send_message(f"✅ ضد تبلیغ فعال شد. {len(anti_ads_words)} کلمه به لیست فیلتر اضافه شد.", message)


@bot.on_message(filters.is_group & filters.text_regex(r"^ضد تبلیغ (خاموش|غیرفعال)$"))
async def anti_ads_off(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3, 4) for t in sender_types):
        return

    filters_list = group_data.get("list_filters", [])
    for word in anti_ads_words:
        if word in filters_list:
            filters_list.remove(word)

    await send_message("✅ ضد تبلیغ غیرفعال شد. کلمات تبلیغاتی از لیست فیلتر حذف شدند.", message)





@bot.on_message(filters.is_group & filters.text_regex(r"^(گزارش|گزارشم|گزارشش)$"))
async def user_report(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_id = str(message.sender_id)
    replied_id = await reply_chat(message)
    cmd = message.text

    if cmd == "گزارش":
        target_id = replied_id if replied_id else sender_id
    elif cmd == "گزارشم":
        target_id = sender_id
    else:
        if replied_id:
            target_id = str(replied_id)
        else:
            await send_message("⨵ لطفاً روی پیام فرد ریپلای کنید تا گزارش او نمایش داده شود.", message)
            return

    await send_user_report(group_data, target_id, message, data)


@bot.on_message(filters.is_group & (
    filters.text_equals("آمار گروه") |
    filters.text_equals("آمار گپ") |
    filters.text_equals("امار گروه") |
    filters.text_equals("امار گپ")
))
async def group_stats_cmd(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser(message.message_id):
        return
    if is_anser_2(message.message_id):
        return
    group_data = data["group"][message.chat_id]

    type_user = detect_user_types(data, group_data, message.sender_id)
    if not any(t in type_user for t in (0, 1, 2, 3, 4)):
        return

    await send_group_stats(group_data, message)


@bot.on_message(filters.is_group & filters.text_regex(r"^(آمار|آمارم|آمارش|امار|امارم|امارش)$"))
async def user_amar(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_id = str(message.sender_id)
    replied_id = await reply_chat(message)
    cmd = message.text

    if cmd in ("آمار", "امار"):
        target_id = replied_id if replied_id else sender_id
    elif cmd in ("آمارم", "امارم"):
        target_id = sender_id
    else:
        if replied_id:
            target_id = str(replied_id)
        else:
            await send_message("⨵ لطفاً روی پیام فرد ریپلای کنید تا آمار او نمایش داده شود.", message)
            return

    result = await send_user_amar(group_data, target_id)
    await send_message(result, message)


@bot.on_message(filters.is_group & filters.text_regex(r"^(مقام|مقامم|مقامش)$"))
async def user_role(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_id = str(message.sender_id)
    replied_id = await reply_chat(message)
    cmd = message.text

    if cmd == "مقام":
        target_id = replied_id if replied_id else sender_id
    elif cmd == "مقامم":
        target_id = sender_id
    else:
        if replied_id:
            target_id = str(replied_id)
        else:
            await send_message("⨵ لطفاً روی پیام فرد ریپلای کنید تا مقام او نمایش داده شود.", message)
            return

    user_types = detect_user_types(data, group_data, target_id)
    roles = {
        0: "🤖 ربات",
        1: "👑 سازنده",
        2: "👑 سازنده",
        3: "🔰 مالک",
        4: "🛡️ ادمین",
    }
    role_name = "👤 کاربر عادی"
    for rid in (0, 1, 2, 3, 4):
        if rid in user_types:
            role_name = roles.get(rid, "کاربر عادی")
            break

    await send_message(f"🎭 نقش در این گروه: **{role_name}**", message)




@bot.on_message(filters.is_group & filters.text_regex(r"^(تعداد پیام|تعداد پیامم|تعداد پیامش)$"))
async def user_message_count(bot, message: Message):
    if not await is_start(message.chat_id):
        return

    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    sender_id = str(message.sender_id)
    replied_id = await reply_chat(message)
    cmd = message.text

    if cmd == "تعداد پیام":
        target_id = str(replied_id) if replied_id else sender_id

    elif cmd == "تعداد پیامم":
        target_id = sender_id

    else:
        if replied_id:
            target_id = str(replied_id)
        else:
            await send_message(
                "⨵ لطفاً روی پیام فرد موردنظر ریپلای کنید.",
                message
            )
            return

    stats = group_data.get("stats", {})
    user_stat = stats.get(target_id, {"total": 0, "ts": []})

    msg_24h = _count_period(user_stat.get("ts", []), PERIOD_24H)
    msg_7d = _count_period(user_stat.get("ts", []), PERIOD_7D)
    msg_30d = _count_period(user_stat.get("ts", []), PERIOD_30D)
    msg_all = user_stat.get("total", 0)

    name, _, _, _ = await get_name(target_id)

    text = (
        f"📊 آمار پیام‌های {name or 'کاربر'}\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"⬡ ۲۴ ساعت گذشته ← {msg_24h:,}\n"
        f"⬡ ۷ روز گذشته ← {msg_7d:,}\n"
        f"⬡ ۳۰ روز گذشته ← {msg_30d:,}\n"
        f"⬡ از ابتدا تاکنون ← {msg_all:,}"
    )

    await send_message(text, message)


















def get_world_regions() -> list:
    return [
        ("🌏 آسیا و خاورمیانه", [
            ("🇮🇷 ایران",      "Asia/Tehran"),
            ("🇸🇦 عربستان",   "Asia/Riyadh"),
            ("🇦🇪 امارات",    "Asia/Dubai"),
            ("🇹🇷 ترکیه",     "Europe/Istanbul"),
            ("🇮🇳 هند",        "Asia/Kolkata"),
            ("🇨🇳 چین",        "Asia/Shanghai"),
            ("🇯🇵 ژاپن",      "Asia/Tokyo"),
        ]),
        ("🌍 اروپا", [
            ("🇬🇧 انگلیس",    "Europe/London"),
            ("🇫🇷 فرانسه",    "Europe/Paris"),
            ("🇩🇪 آلمان",     "Europe/Berlin"),
            ("🇷🇺 روسیه",     "Europe/Moscow"),
        ]),
        ("🌎 آمریکا و اقیانوسیه", [
            ("🇨🇦 کانادا",    "America/Toronto"),
            ("🇺🇸 نیویورک",   "America/New_York"),
            ("🇺🇸 لس‌آنجلس", "America/Los_Angeles"),
            ("🇧🇷 برزیل",     "America/Sao_Paulo"),
            ("🇦🇺 استرالیا",  "Australia/Sydney"),
        ]),
    ]


def get_time_icon(hour: int) -> str:
    if 5 <= hour < 12:  return "🌅"
    if 12 <= hour < 17: return "☀️"
    if 17 <= hour < 21: return "🌆"
    return "🌙"

def format_country_row(name: str, zone: str) -> str:
    now = datetime.now(pytz.timezone(zone))
    return f"  {name}  ›   {now.strftime('%H:%M')} "

def build_time_header(now_ir) -> list:
    return [
        "      🕰  ساعت جهانی    ",
        "",
        "",
        f"📅 {now_ir.strftime('%Y/%m/%d')}  |  {now_ir.strftime('%H:%M')} {get_time_icon(now_ir.hour)}  ایران",
        "━━━━━━━━━━━━━━━━━━━━━",
    ]


def build_time_message() -> str:
    now_ir = datetime.now(pytz.timezone("Asia/Tehran"))
    lines  = build_time_header(now_ir)

    for region_name, countries in get_world_regions():
        lines.append(f"\n{region_name}")
        for name, zone in countries:
            lines.append(format_country_row(name, zone))

    lines.append("\n━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)

@bot.on_message(filters.is_group & filters.text_regex(r"^(/ساعت|ساعت)$"))
@on_funny("sa")
async def show_time(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    await send_message(build_time_message(), message)







def get_season(jalali_month: int) -> str:
    if jalali_month <= 3:  return "🌸 بهار"
    if jalali_month <= 6:  return "☀️ تابستان"
    if jalali_month <= 9:  return "🍂 پاییز"
    return "❄️ زمستان"


def get_year_stats(now_j) -> tuple:
    day_of_year = sum(31 if m <= 6 else 30 for m in range(1, now_j.month)) + now_j.day
    remaining   = (366 if is_jalali_leap(now_j.year) else 365) - day_of_year
    return day_of_year, remaining


def get_jalali_info(now_j) -> dict:
    months = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
        "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]
    return {
        "date":       now_j.strftime("%Y/%m/%d"),
        "month_name": months[now_j.month - 1],
        "day":        now_j.day,
        "year":       now_j.year,
        "season":     get_season(now_j.month),
        "day_name":   get_week_day(now_j.weekday()),
    }


def get_week_day(weekday: int) -> str:
    days = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
    return days[weekday]


def is_jalali_leap(year: int) -> bool:
    return (year % 33) in {1, 5, 9, 13, 17, 22, 26, 30}

def get_hijri_info(now: datetime) -> dict:
    hijri  = convert.Gregorian(now.year, now.month, now.day).to_hijri()
    months = [
        "محرم", "صفر", "ربیع‌الاول", "ربیع‌الثانی", "جمادی‌الاول", "جمادی‌الثانی",
        "رجب", "شعبان", "رمضان", "شوال", "ذیقعده", "ذیحجه"
    ]
    return {
        "date":       f"{hijri.year}/{hijri.month:02}/{hijri.day:02}",
        "month_name": months[hijri.month - 1],
    }


def get_hebrew_date(now: datetime) -> str:
    h_year, h_month, h_day = hebrew.from_gregorian(now.year, now.month, now.day)
    return f"{h_year}/{h_month:02}/{h_day:02}"


def get_buddhist_date(now: datetime) -> str:
    return f"{now.year + 543}/{now.month:02}/{now.day:02}"


def get_kurdish_date(now_j) -> str:
    months = [
        "کانونی یەکەم", "کانونی دووەم", "شوبات", "ئازار", "نیسان", "ئایار",
        "حوزەیران", "تەمووز", "ئاب", "ئەیلوول", "تشرینی یەکەم", "تشرینی دووەم"
    ]
    return f"{now_j.day} {months[now_j.month - 1]} {now_j.year}"


def get_pahlavi_date(now_j) -> str:
    return (
        f"𐎠𐎼𐎹: {str(now_j.year)[::-1]}"
        f"/{str(now_j.month).zfill(2)}"
        f"/{str(now_j.day).zfill(2)}"
    )


def build_date_message() -> str:
    now   = datetime.now()
    now_j = jdatetime.datetime.now()

    jalali       = get_jalali_info(now_j)
    hijri        = get_hijri_info(now)
    day_num, rem = get_year_stats(now_j)

    return (
        "   📆  تاریخ امروز   \n"
        "\n\n"
        f"✨ {jalali['day_name']}، {jalali['day']} {jalali['month_name']} {jalali['year']}\n"
        f"{jalali['season']}\n\n"
        "━━━━ 📅 تقویم‌ها ━━━━\n\n"
        f"🔹 میلادی:       {now.strftime('%Y/%m/%d')}\n"
        f"🔸 شمسی:        {jalali['date']}\n"
        f"🌙 قمری:         {hijri['date']}  ({hijri['month_name']})\n"
        f"🟢 کردی:         {get_kurdish_date(now_j)}\n"
        f"✡️  عبری:          {get_hebrew_date(now)}\n"
        f"🛕 بودایی:       {get_buddhist_date(now)}\n"
        f"🏛️ پهلوی:        {get_pahlavi_date(now_j)}\n\n"
        "━━━━ 📊 آمار سال ━━━━\n\n"
        f"📌 روز {day_num} از سال شمسی\n"
        f"⏳ {rem} روز تا پایان سال"
    )




@bot.on_message(filters.is_group & filters.text_regex(r"^(/تاریخ|تاریخ)$"))
@on_funny("ta")
async def show_date(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)
    await send_message(build_date_message(), message)






@bot.on_message(filters.is_group & filters.text_regex(r"^آب و هوا\s*(.*)$"))
@on_funny("ab")
async def weather_report(bot, message: Message):
    asyncio.create_task(process_weather(bot, message))


async def process_weather(bot, message: Message):
    try:
        if not await is_start(message.chat_id):
            return

        if is_anser_2(message.message_id):
            return

        message_ids_dont.append(message.message_id)

        city = message.text.replace("آب و هوا", "").strip()
        if not city:
            await send_message(
                "⨵ لطفاً نام شهر را وارد کنید! مثال: آب و هوا تهران",
                message
            )
            return

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"https://api.codebazan.ir/havairan/?unit=metric&city={city}"
                )

            if response.status_code != 200:
                await send_message(
                    "⨵ خطا در دریافت اطلاعات آب و هوا. لطفاً بعداً امتحان کنید.",
                    message
                )
                return

            data_resp = response.json()

            if "error" in data_resp or not data_resp.get("main_weather"):
                await send_message(
                    f"⨵ اطلاعاتی برای شهر {city} یافت نشد.",
                    message
                )
                return

            text = f"""🌤️ گزارش وضعیت آب و هوا

📍 شهر: {city}
☁️ وضعیت هوا: {data_resp.get('main_weather', 'نامشخص')}
💧 رطوبت: {data_resp.get('humidity', '?')}%
🌬️ سرعت باد: {data_resp.get('wind_speed', '?')} کیلومتر بر ساعت
🌡️ دمای هوا: {data_resp.get('temperature', '?')} درجه سانتی‌گراد
🔽 فشار هوا: {data_resp.get('pressure', '?')}

📌 آخرین بروزرسانی – همیشه آماده باشید! ⏳"""

            await send_message(text, message)

        except httpx.TimeoutException:
            await send_message(
                "⨵ زمان پاسخگویی سرور به پایان رسید. لطفاً دوباره تلاش کنید.",
                message
            )

        except Exception as e:
            await send_message(
                f"⨵ خطا در دریافت اطلاعات آب و هوا: {str(e)}",
                message
            )

    except Exception as e:
        print("WEATHER TASK ERROR:", e)



RPS_CHOICES = {
    "سنگ":   "🪨",
    "کاغذ":  "📄",
    "قیچی":  "✂️",
}
RPS_WIN_MAP = {
    "سنگ":  "قیچی",
    "کاغذ": "سنگ",
    "قیچی": "کاغذ",
}

@bot.on_message(filters.is_group & filters.text_regex(r"^(سنگ|کاغذ|قیچی)$"))
@on_funny("sang")
async def rock_paper_scissors(bot, message: Message):

    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    user_choice = message.text.strip()
    bot_choice  = random.choice(list(RPS_CHOICES))

    user_e = RPS_CHOICES[user_choice]
    bot_e  = RPS_CHOICES[bot_choice]

    if user_choice == bot_choice:
        result = "🤝 مساوی شد!"
    elif RPS_WIN_MAP[user_choice] == bot_choice:
        result = "🏆 تو بردی!"
    else:
        result = "🤖 من بردم!"

    await send_message(
        f"🎮  سنگ کاغذ قیچی\n\n"
        f"  تو   » {user_e} {user_choice}\n"
        f"  من   » {bot_e} {bot_choice}\n\n"
        f"  {result}",
        message,
    )

@bot.on_message(filters.is_group & filters.text_regex(r"^(/تاس|تاس)$"))
@on_funny("tas")
async def dice_roll(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    dice_number = random.randint(1, 6)
    dice_emojis = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    emoji = dice_emojis[dice_number - 1]
    text_dice = f"🎲 من تاس انداختم برات...\n\nنتیجه: {emoji} ({dice_number})"
    await send_message(text_dice, message)







@bot.on_message(filters.is_group & filters.text_regex(r"^فونت\s+(.+)"))
@on_funny("fon_t")
async def font_farsi_handler(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    text = message.text.replace("فونت", "", 1).strip()
    if not text:
        await send_message("⨵ بعد از «فونت» متن وارد کنید.", message)
        return

    numbers = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧"]
    fonts = [f"{numbers[i-1]} {font_auto(text, i)}" for i in range(1, 9)]
    result = "🎨 8 فونت :\n\n" + "\n".join(fonts)
    await send_message(result, message)




@bot.on_message(filters.is_group & filters.text_regex(r"^(ping|پینگ)$"))
async def ping(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    start = time.time()
    temp_msg = await send_message("🔄 در حال محاسبه سرعت پاسخگویی...", message, reply=False)
    if temp_msg:
        elapsed_ms = round((time.time() - start) * 1000)
        await bot.edit_message_text(
            message.chat_id,
            temp_msg.message_id,
            f"⏱ سرعت پاسخگویی: {elapsed_ms} میلی‌ثانیه"
        )
    else:
        elapsed = round(time.time() - start, 3)
        await send_message(f"⏱ سرعت پاسخگویی: {elapsed} ثانیه", message)



@bot.on_message(filters.is_group & filters.text_regex(r"^(/سکه|سکه)$"))
@on_funny("sek")
async def coin_flip(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    result = random.choice(["🪙 شیر", "🪙 خط"])
    await send_message(f"🎯 سکه پرتاب شد\nنتیجه: {result}", message)







@bot.on_message(filters.is_group & filters.text_regex(r"^(اصل|اصل بده)$"))
async def show_asl(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    target_id = await reply_chat(message)
    if not target_id:
        await send_message("❌ لطفاً روی پیام کاربر ریپلای کنید.", message)
        return

    name, age, city, _ = await get_name(target_id)
    if not name:
        await send_message("⨵ این کاربر هنوز اصل خود را ثبت نکرده است.\nبرای ثبت اصل، به پیوی ربات مراجعه کنید.", message)
        return

    await send_message(
        f"📌 اصل کاربر\n\n"
        f"👤 اسم: {name}\n"
        f"🎂 سن: {age}\n"
        f"📍 شهر: {city}",
        message
    )



@bot.on_message(filters.is_group & filters.text_regex(r"^(اصلم|اصل من)$"))
async def show_my_asl(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    name, age, city, _ = await get_name(str(message.sender_id))
    if not name:
        await send_message("⨵ شما هنوز اصل خود را ثبت نکرده‌اید.\nبرای ثبت اصل، به پیوی ربات مراجعه کنید.", message)
        return

    await send_message(
        f"📌 اصل من\n\n"
        f"👤 اسم: {name}\n"
        f"🎂 سن: {age}\n"
        f"📍 شهر: {city}",
        message
    )





@bot.on_message(filters.is_group & filters.text_regex(r"^(سرگرمی|لیست سرگرمی)$"))
async def list_sar(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser(message.message_id):
        return
    if is_anser_2(message.message_id):
        return


    text="""
「 🎯 امکانات ربات 」
━━━━━━━━━━━━━━━━

📝 محتوا
• جوک
• خاطره
• پ ن پ
• داستان
• دیالوگ
• شعر
• دانستی
• انگیزشی
• جمله عاشقانه
• جمله دل‌شکسته
• قوانین عجیب
• ترفند
• حدیث
• آیه
━━━━━━━━━━━━━━━━

🎲 سرگرمی
• تاس
• سکه
• شانس
• چالش
• شخصیتم
• شغل آینده
• اگه حیوان بودم
• فیلم من
• وضعیتم
• امروز
• سنگ یا کاغذ یا قیچی
• چیستان
• فال
━━━━━━━━━━━━━━━━

🌐 خدمات
• دانلود پست
• دانلود استوری
• آب‌وهوا
• ارز
• اوقات شرعی
• گیف متن
━━━━━━━━━━━━━━━━

🔤 ابزار متن
• فونت فارسی
• فونت انگلیسی
• معنی کلمه
━━━━━━━━━━━━━━━━

🤖 هوش مصنوعی
• + متن

مثال:
+ یک داستان کوتاه بنویس
━━━━━━━━━━━━━━━━

🧮 محاسبات
• محاسبه عبارات ریاضی

مثال:
محاسبه
6 + sin(60)
━━━━━━━━━━━━━━━━

📚 اشعار
• شعر سعدی
• شعر حافظ
• شعر فردوسی
• شعر مولوی
• شعر نظامی
• شعر مولانا
• شعر شهریار

"""
    await send_message(text, message)







@bot.on_message(filters.is_group & filters.text_regex(r"^(/day|day|امروز)$"))
@on_funny("day")
async def show_day(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    now = datetime.now()
    now_jalali = jdatetime.datetime.now()

    miladi = now.strftime("%d %B %Y")

    fa_months = {
        1: "فروردین", 2: "اردیبهشت", 3: "خرداد", 4: "تیر",
        5: "مرداد", 6: "شهریور", 7: "مهر", 8: "آبان",
        9: "آذر", 10: "دی", 11: "بهمن", 12: "اسفند"
    }
    jalali_str = f"{now_jalali.day} {fa_months[now_jalali.month]} {now_jalali.year}"

    try:
        hijri_date = convert.Gregorian(now.year, now.month, now.day).to_hijri()
        hijri_str = f"{hijri_date.day}/{hijri_date.month:02}/{hijri_date.year}"
    except Exception:
        hijri_str = "نامشخص"

    weekdays_fa = {
        'Saturday': 'شنبه', 'Sunday': 'یک‌شنبه', 'Monday': 'دوشنبه',
        'Tuesday': 'سه‌شنبه', 'Wednesday': 'چهارشنبه',
        'Thursday': 'پنج‌شنبه', 'Friday': 'جمعه'
    }
    day_en = now.strftime('%A')
    day_fa = weekdays_fa.get(day_en, day_en)

    current_time = now.strftime("%H:%M:%S")

    days_until_friday = (4 - now.weekday()) % 7
    if days_until_friday == 0:
        friday_text = "🎉 امروز جمعه است!"
    else:
        friday_text = f"⏳ {days_until_friday} روز تا جمعه باقی مانده"

    await send_message(
        f"📅 امروز: {day_fa} ({day_en})\n"
        f"🗓 تاریخ شمسی: {jalali_str}\n"
        f"🇺🇸 میلادی: {miladi}\n"
        f"🇸🇦 قمری: {hijri_str}\n"
        f"⏰ ساعت فعلی: {current_time}\n"
        f"{friday_text}",
        message
    )






@bot.on_message(filters.is_group & filters.text_regex(r"^(/post_download|دانلود پست)"))
@on_funny("download_p")
async def post_download(bot, message: Message):
    asyncio.create_task(process_post_download(bot, message))


async def process_post_download(bot: Robot, message: Message):
    try:
        if not await is_start(message.chat_id):
            return

        if is_anser_2(message.message_id):
            return

        message_ids_dont.append(message.message_id)

        text = message.text.replace("دانلود پست", "").replace("/post_download", "").strip()

        if "rubika.ir/post/" not in text:
            await send_message(
                "⨵ لینک نامعتبر است. لطفاً لینک صحیح روبیکا را ارسال کنید.",
                message
            )
            return

        result = await download_post(text)

        if not result or not result.get("ok"):
            await send_message(
                "⨵ خطا در دریافت اطلاعات پست. ممکن است لینک اشتباه یا پست خصوصی باشد.",
                message
            )
            return

        res_data = result.get("result", {})

        if not res_data:
            await send_message("⨵ اطلاعاتی یافت نشد.", message)
            return

        caption = (
            f"🔗 لینک دانلود: {res_data.get('url', 'نامشخص')}\n\n"
            f"👤 پیج: {res_data.get('page_username', 'نامشخص')}\n"
            f"👥 تعداد فالوورها: {res_data.get('follower_page', '?')}\n"
            f"❤️ لایک‌ها: {res_data.get('like', '?')}\n"
            f"💬 کامنت‌ها: {res_data.get('comment', '?')}\n"
            f"👁 بازدیدها: {res_data.get('view', '?')}\n"
            f"🆔 آیدی پست: {res_data.get('post_id', '?')}"
        )

        await send_message(caption, message)

    except Exception as e:
        print("POST DOWNLOAD ERROR:", e)


@bot.on_message(filters.is_group & filters.text_regex(r"^(/story_download|دانلود استوری)"))
@on_funny("download_s")
async def story_download(bot, message: Message):
    asyncio.create_task(process_story_download(bot, message))


async def process_story_download(bot: Robot, message: Message):
    try:
        if not await is_start(message.chat_id):
            return

        if is_anser_2(message.message_id):
            return

        message_ids_dont.append(message.message_id)

        page_id = (
            message.text
            .replace("/story_download", "")
            .replace("دانلود استوری", "")
            .replace("@", "")
            .strip()
        )

        if not page_id:
            await send_message(
                "⨵ لطفاً آیدی پیج را وارد کنید.\nمثال: دانلود استوری rubika",
                message
            )
            return

        result = await download_story(page_id)

        if not result or not result.get("ok"):
            await send_message(
                "⨵ استوری‌ای یافت نشد یا پیج خصوصی است.",
                message
            )
            return

        story_links = result.get("result", [])

        if not story_links:
            await send_message(
                "⨵ هیچ استوری عمومی برای این پیج یافت نشد.",
                message
            )
            return

        response_text = f"✅ تعداد {len(story_links)} استوری یافت شد.\n\n🔗 لینک‌های دانلود:\n"

        for i, link in enumerate(story_links, 1):
            response_text += f"{i}. {link}\n"

        await send_message(response_text, message)

    except Exception as e:
        print("STORY DOWNLOAD ERROR:", e)



@bot.on_message(filters.is_group & filters.text_regex(r"^ارز$"))
@on_funny("arz")
async def get_currency_handler(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    try:
        result = asyncio.create_task(get_currency(message))
    except Exception as e:
        await send_message(f"⨵ خطا در دریافت اطلاعات بازار: {str(e)}", message)




SLOT_SYMBOLS = [
        "🍀", "🍒", "🍋", "💎", "🔔", "🪙", "🧲", "🧁",
        "🌈", "🔥", "🌟", "👑", "💰", "🍫", "🎯", "🥇",
        "🥝", "🌮", "🍕", "🍉"
    ]

@bot.on_message(filters.is_group & filters.text_regex(r"^(/شانس|شانس)$"))
@on_funny("shan")
async def slot_game(bot, message: Message):

    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    slot   = [random.choice(SLOT_SYMBOLS) for _ in range(3)]
    joined = " ┃ ".join(slot)
    unique = len(set(slot))

    if unique == 1:
        result = "🏆 جک‌پات! هر سه‌تا یکی شدن! 🤩"
        frame  = "· · · · · · · · · ·\n   " + joined + "\n· · · · · · · · · ·"
    elif unique == 2:
        result = "😎 دو تاش یکی شد — نزدیک بود!"
        frame  = "· · · · · · · · · ·\n   " + joined + "\n· · · · · · · · · ·"
    else:
        result = "😢 شانست نگرفت، دوباره امتحان کن!"
        frame  = "· · · · · · · · · ·\n   " + joined + "\n· · · · · · · · · ·"

    await send_message(
        f"🎰  بازی شانس\n\n{frame}\n\n{result}",
        message,
    )







@bot.on_message(filters.is_group & filters.text_regex(r"^(/شخصیتم|شخصیتم)$"))
@on_funny("shas")
async def personality(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    personalities = [
        "🔥 ماجراجو و پرانرژی... مثل وقتی من فرار کردم از کارخانه آب‌نبات‌سازی!",
        "🧠 باهوش و منطقی... ولی نه به اندازه بین!",
        "😂 شوخ‌طبع و بامزه... مثل خودم، البته کمتر!",
        "😎 خونسرد و باحال... مثل لوسی وقتی همه جا آتیش گرفته!",
        "😇 مهربون و دلسوز... ولی حواست باشه زیاد مهربون نباشی، می‌خورنت!",
        "👑 رئیس و کاردرست... تو رئیس باش، من معاونت می‌شم!",
        "👻 مرموز و ساکت... مث اون شب که جادوگرها منو بردن!",
        "🎭 دمدمی‌مزاج و غیرقابل پیش‌بینی... یه لحظه می‌خندی، یه لحظه گریه می‌کنی؟ مثل زندگی!",
        "🤖 مثل یه ربات، منطقی و دقیق... ولی بیا کمی هم شیرین باش!",
        "🐢 آروم و صبور... مثل وقتی که منتظر یه شیرینی خوشمزه‌م!",
        "🐉 اژدهای پرقدرت! اوه اوه! ازت می‌ترسم!"
    ]
    selected = random.choice(personalities)
    await send_message(f"🎭 حدس می‌زنم که تو اینی:\n\n{selected}", message)



@bot.on_message(filters.is_group & filters.text_regex(r"^(/شغل آینده|شغل آینده)$"))
@on_funny("shog")
async def future_job(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    jobs = [
        "👨‍⚖️ قاضی عدالت‌خواه", "👨‍🚀 فضانورد شجاع", "🎭 بازیگر معروف",
        "👨‍🍳 سرآشپز حرفه‌ای", "💻 برنامه‌نویس نخبه", "🕵️‍♂️ کارآگاه زبده",
        "🎸 خواننده پرطرفدار", "✈️ خلبان ماهر", "🏥 دکتر متخصص",
        "📚 نویسنده خلاق", "📷 عکاس حرفه‌ای", "🏆 ورزشکار موفق",
        "🚀 مالک استارتاپ بزرگ", "🎮 گیمر حرفه‌ای", "🛠️ مهندس خلاق",
        "💰 تاجر ثروتمند", "🎤 مجری تلویزیونی", "⚖️ وکیل معروف",
        "🖌️ نقاش هنرمند", "🎼 آهنگساز محبوب", "🌍 جهانگرد ماجراجو",
        "🎢 طراح شهربازی", "🏗️ معمار برجسته", "🚓 افسر پلیس",
        "📡 کارشناس هواشناسی", "🎯 مربی انگیزشی", "🧪 دانشمند دیوانه",
        "🎩 شعبده‌باز حرفه‌ای", "📖 مترجم چندزبانه", "🛳️ ناخدای کشتی",
        "🏋️ مربی بدنسازی", "🛍️ طراح مد و لباس", "🎨 گرافیست خلاق",
        "👨‍🏫 استاد دانشگاه", "🎥 کارگردان سینما", "💼 مالک بانک",
        "🍔 مالک فست‌فود زنجیره‌ای", "🏹 شکارچی گنج", "🦸‍♂️ ابرقهرمان واقعی",
        "🎮 تستر بازی‌های ویدیویی", "🔧 تعمیرکار حرفه‌ای", "🚀 مهندس ناسا",
        "🐶 دامپزشک مهربان", "📰 خبرنگار جنجالی", "📞 اپراتور مرکز تماس",
        "🎶 تنظیم‌کننده موسیقی", "🎙️ دوبلور انیمیشن", "🎾 مربی تنیس",
        "🏖️ راهنمای تور مسافرتی"
    ]
    selected = random.choice(jobs)
    await send_message(f"🔮 شغل آینده‌ی شما: {selected}!", message)



@bot.on_message(filters.is_group & filters.text_regex(r"^(/فیلم من|فیلم من)$"))
@on_funny("film")
async def movie(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    movies = [
        "🦇 شوالیه تاریکی – بتمن", "⚡ انتقام‌جویان – اونجرز", "🧙 هری پاتر و سنگ جادو",
        "🚀 جنگ ستارگان – استار وارز", "🦖 پارک ژوراسیک", "🕷️ مرد عنکبوتی – اسپایدرمن",
        "🛸 میان‌ستاره‌ای – اینتراستلار", "🔥 بازی تاج و تخت", "🏎️ سریع و خشن",
        "🦸 واندر وومن", "👻 احضار – کانجورینگ", "🔫 جان ویک", "🎭 جوکر",
        "🤖 من، ربات – I, Robot", "⏳ تلقین – اینسپشن", "💰 گرگ وال استریت",
        "🐉 هابیت", "🌍 روز استقلال", "🤯 باشگاه مبارزه", "⚖️ وکیل مدافع شیطان",
        "🎩 پرستیژ", "🎶 لالالند", "🏹 عطش مبارزه – هانگر گیمز", "👮 فرار از شاوشنک",
        "🤖 ترمیناتور", "🎬 پدرخوانده", "🦁 شیرشاه", "🎸 راک‌استار", "💀 دزدان دریایی کارائیب",
        "🌊 تایتانیک", "🧟 رزیدنت اویل", "🏔️ اورست", "🏀 مربی کارتر", "🚔 پلیس آهنی",
        "🎤 بوهمین راپسودی", "🔪 جیغ", "💥 ماتریکس", "🔬 گتاکا", "🕵️ شرلوک هلمز",
        "🎤 بچه رئیس", "🐼 پاندای کونگ‌فوکار", "🍫 چارلی و کارخانه شکلات‌سازی",
        "🎅 تنها در خانه", "🦸 لوگان", "🎖️ نجات سرباز رایان", "🚁 اینسپشن",
        "🌪️ طوفان جغرافیایی", "🎭 نقاب", "🌌 نگهبانان کهکشان", "🎨 رَتاتویی",
        "🍕 لاک‌پشت‌های نینجا", "🦍 گودزیلا در برابر کینگ‌کونگ", "🕶️ مردان سیاه‌پوش",
        "🌠 شازده کوچولو", "💊 دارک سیتی"
    ]
    selected = random.choice(movies)
    await send_message(f"🎬 فیلم مناسب برای تو: {selected}!", message)



@bot.on_message(filters.is_group & filters.text_regex(r"^(/اگه حیوان بودم|اگه حیوان بودم)$"))
@on_funny("hiy")
async def animal(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    animals = [
        "🦁 شیر - قدرتمند و شجاع!", "🦊 روباه - باهوش و زیرک!", "🐺 گرگ - تنها ولی قوی!",
        "🐼 پاندای بامزه و آرام!", "🐍 مار - مرموز و خطرناک!", "🦅 عقاب - پادشاه آسمان‌ها!",
        "🐘 فیل - مهربان و قوی!", "🐯 ببر - نترس و پرهیبت!", "🐦 قناری - خوش‌صدا و آرام!",
        "🐻 خرس - صبور ولی خطرناک!", "🦉 جغد - دانا و شب‌زنده‌دار!", "🐨 کوالا - آرام و خوابالو!",
        "🦄 اسب تک‌شاخ - افسانه‌ای و خاص!", "🦋 پروانه - زیبا و لطیف!", "🦜 طوطی - پرحرف و باهوش!",
        "🐬 دلفین - بازیگوش و اجتماعی!", "🦏 کرگدن - سرسخت و مقاوم!", "🐴 اسب - سریع و نجیب!",
        "🦢 قو - زیبا و وفادار!", "🐒 میمون - شیطون و بازیگوش!", "🦔 جوجه‌تیغی - کوچک ولی مقاوم!",
        "🐊 کروکودیل - بی‌رحم و قدرتمند!", "🐌 حلزون - آروم و صبور!", "🦇 خفاش - شب‌زی و اسرارآمیز!",
        "🐿️ سنجاب - زرنگ و پرجنب‌وجوش!", "🦡 گورکن - جسور و نترس!", "🐋 نهنگ - غول آرام دریاها!",
        "🐜 مورچه - سخت‌کوش و منظم!", "🐢 لاک‌پشت - صبور و باحوصله!", "🦎 آفتاب‌پرست - منعطف و سازگار!",
        "🐃 بوفالو - قوی و سرسخت!", "🐩 سگ پشمالو - وفادار و دوست‌داشتنی!", "🦌 گوزن - ظریف و سریع!",
        "🦢 لک‌لک - خوش‌یمن و خوش‌قدم!", "🐉 اژدهای افسانه‌ای - نیرومند و اسرارآمیز!"
    ]
    chosen = random.choice(animals)
    await send_message(f"🦁 اگه حیوان بودی، {chosen}", message)



@bot.on_message(filters.is_group & filters.text_regex(r"^(/وضعیتم|وضعیتم)$"))
@on_funny("vaz")
async def mood(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    emotions = {
        "هیجان", "عصبانیت", "فعالیت ذهنی", "افسردگی", "انرژی",
        "خشم", "شادی", "تنهایی", "استرس", "امید", "عشق", "متغیر",
        "خستگی", "فشار ذهنی", "دلزدگی", "خجالت", "نیاز به حمایت",
        "نفرت", "انگیزه", "بی‌حوصلگی", "اجتماعی بودن", "کنجکاوی"
    }
    emotions_data = {emotion: random.randint(0, 100) for emotion in emotions}
    avg = sum(emotions_data.values()) / len(emotions_data)
    lines = "\n".join(f"🔹 {key}: {value}%" for key, value in emotions_data.items())
    await send_message(
        f"🎭 📊 تحلیل احساسات شما 📊 🎭\n\n{lines}\n\n📢 حالت کلی شما: {avg:.1f}%",
        message
    )



@bot.on_message(filters.is_group & filters.text_regex(r"^اوقات شرعی\s*(.*)$"))
@on_funny("ogh")
async def prayer_times_handler(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    city = message.text.replace("اوقات شرعی", "").strip()
    if not city:
        await send_message(
            "⨵ لطفاً نام شهر را وارد کنید\nمثال: اوقات شرعی کرمانشاه",
            message
        )
        return

    asyncio.create_task(get_prayer_times(city, message))




@bot.on_message(filters.is_group & filters.text_regex(r"^داستان$"))
@on_funny("dastan")
async def dastan(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    stories = data_json.get("dastan", [])
    if not stories:
        await send_message("⨵ داستانی یافت نشد.", message)
        return
    await send_with_prefix("◉STORY", random.choice(stories), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^دیالوگ$"))
@on_funny("dialog")
async def dialog(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    dialogs = data_json.get("dialog", [])
    if not dialogs:
        await send_message("⨵ دیالوگی یافت نشد.", message)
        return
    await send_with_prefix("◉DIALOG", random.choice(dialogs), message)





@bot.on_message(filters.is_group & filters.text_regex(r"^چیستان$"))
@on_funny("riddles")
async def dialog(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    dialogs = data_json.get("riddles", {})
    if not dialogs:
        await send_message("⨵ چیستان یافت نشد.", message)
        return
    
    fff = random.choice(dialogs)
    
    ans = fff["question"]
    qs = fff["answer"]
    
    await send_with_prefix("◉CHISTAN", f"""  {ans} \n \n ||{qs}|| """, message)






@bot.on_message(filters.is_group & filters.text_regex(r"^فال$"))
@on_funny("fal")
async def ashaar(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    poems = data_json.get("fal", [])

    if not poems:
        await send_message("⨵ فال یافت نشد.", message)
        return
    await send_with_prefix("◉FAL", random.choice(poems), message)


@bot.on_message(filters.is_group & filters.text_regex(r"^شعر$"))
@on_funny("sheer")
async def ashaar(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    poems = data_json.get("ashaar", [])
    if not poems:
        await send_message("⨵ شعری یافت نشد.", message)
        return
    await send_with_prefix("◉POEM", random.choice(poems), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^انگیزشی$"))
@on_funny("angiz")
async def angizeshi(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    motivations = data_json.get("angizeshi", [])
    if not motivations:
        await send_message("⨵ متن انگیزشی یافت نشد.", message)
        return
    await send_with_prefix("◉MOTIVATION", random.choice(motivations), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^چالش$"))
@on_funny("chal")
async def chalesh(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    challenges = data_json.get("chalesh", [])
    if not challenges:
        await send_message("⨵ چالشی یافت نشد.", message)
        return
    await send_with_prefix("◉CHALLENGE", random.choice(challenges), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^حدیث$"))
@on_funny("hadis")
async def hadis(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    hadiths = data_json.get("hadis", [])
    if not hadiths:
        await send_message("⨵ حدیثی یافت نشد.", message)
        return
    await send_with_prefix("◉HADITH", random.choice(hadiths), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^آیه$"))
@on_funny("aye")
async def aye(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    verses = data_json.get("aye", [])
    if not verses:
        await send_message("⨵ آیه‌ای یافت نشد.", message)
        return
    await send_with_prefix("◉AYE", random.choice(verses), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^جمله عاشقانه$"))
@on_funny("love")
async def love(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    loves = data_json.get("love", [])
    if not loves:
        await send_message("⨵ جمله عاشقانه‌ای یافت نشد.", message)
        return
    await send_with_prefix("◉LOVE", random.choice(loves), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^جمله دلشکسته$"))
@on_funny("break")
async def sad(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    sads = data_json.get("sad", [])
    if not sads:
        await send_message("⨵ جمله دلشکسته‌ای یافت نشد.", message)
        return
    await send_with_prefix("◉SAD", random.choice(sads), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^ترفند$"))
@on_funny("tarf")
async def tarfand(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    tips = data_json.get("Tarfand", [])
    if not tips:
        tips = data_json.get("tarfand", [])
    if not tips:
        await send_message("⨵ ترفندی یافت نشد.", message)
        return
    await send_with_prefix("◉TIP", random.choice(tips), message)




@bot.on_message(filters.is_group & filters.regex(r"^تولد\s+\d{4}([\/\-\s])\d{1,2}\1\d{1,2}$"))
@on_funny("tavl")
async def birth_handler(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    try:
        numbers = re.findall(r"\d+", message.text)
        if len(numbers) != 3:
            await send_message("⨵ فرمت صحیح:\nتولد 1385/10/2", message)
            return
        year, month, day = map(int, numbers)

        asyncio.create_task(get_birth_text(year, month, day, message))

    except Exception:
        await send_message("⨵ فرمت صحیح:\nتولد 1385/10/2", message)


@bot.on_message(filters.is_group & filters.text_regex(r"^جوک$"))
@on_funny("jok")
async def jok(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    jokes = data_json.get("jok", [])
    if not jokes:
        await send_message("⨵ جوکی یافت نشد.", message)
        return
    await send_with_prefix("◉JOK", random.choice(jokes), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^خاطره$"))
@on_funny("jok_kh")
async def khatere(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    memories = data_json.get("jok_khatere", [])
    if not memories:
        await send_message("⨵ خاطره‌ای یافت نشد.", message)
        return
    await send_with_prefix("◉KHATERE", random.choice(memories), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^پ ن پ$"))
@on_funny("pnp")
async def pa_na_pa(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    pnp_list = data_json.get("jok_pa_na_pa", [])
    if not pnp_list:
        await send_message("⨵ پ ن پ یافت نشد.", message)
        return
    await send_with_prefix("◉PA NA PA", random.choice(pnp_list), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^الکی مثلاً$"))
@on_funny("alky")
async def alaki_masalan(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    alaki_list = data_json.get("jok_alaki_masalan", [])
    if not alaki_list:
        await send_message("⨵ الکی مثلاً یافت نشد.", message)
        return
    await send_with_prefix("◉ALAKI", random.choice(alaki_list), message)


@bot.on_message(filters.is_group & filters.text_regex(r"^بیو$"))
@on_funny("bio")
async def bio(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    bio_list = data_json.get("bio", [])
    if not bio_list:
        await send_message("⨵ بیوگرافی یافت نشد.", message)
        return
    await send_with_prefix("◉BIO", random.choice(bio_list), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^دانستنی$"))
@on_funny("dans")
async def danes(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    facts = data_json.get("danes", [])
    if not facts:
        await send_message("⨵ دانستنی یافت نشد.", message)
        return
    await send_with_prefix("◉FACT", random.choice(facts), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^قوانین عجیب$"))
@on_funny("ghan")
async def laws(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    laws_list = data_json.get("laws", [])
    if not laws_list:
        await send_message("⨵ قانون عجیبی یافت نشد.", message)
        return
    await send_with_prefix("◉LAW", random.choice(laws_list), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^شعر سعدی$"))
@on_funny("sh_s")
async def saadi(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    poems = data_json.get("saadi", [])
    if not poems:
        await send_message("⨵ شعری از سعدی یافت نشد.", message)
        return
    await send_with_prefix("◉SAADI", random.choice(poems), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^شعر حافظ$"))
@on_funny("sh_h")
async def hafez(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    poems = data_json.get("hafez", [])
    if not poems:
        await send_message("⨵ شعری از حافظ یافت نشد.", message)
        return
    await send_with_prefix("◉HAFEZ", random.choice(poems), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^شعر مولوی$"))
@on_funny("sh_mvlv")
async def molavi(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    poems = data_json.get("molavi", [])
    if not poems:
        await send_message("⨵ شعری از مولوی یافت نشد.", message)
        return
    await send_with_prefix("◉MOLAVI", random.choice(poems), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^شعر مولانا$"))
@on_funny("sh_mvla")
async def molana(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    poems = data_json.get("molana", [])
    if not poems:
        await send_message("⨵ شعری از مولانا یافت نشد.", message)
        return
    await send_with_prefix("◉MOLANA", random.choice(poems), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^شعر نظامی$"))
@on_funny("sh_ne")
async def nezami(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    poems = data_json.get("nezami", [])
    if not poems:
        await send_message("⨵ شعری از نظامی یافت نشد.", message)
        return
    await send_with_prefix("◉NEZAMI", random.choice(poems), message)




@bot.on_message(filters.is_group & filters.text_regex(r"^شعر شهریار$"))
@on_funny("sh_sh")
async def shahriar(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    poems = data_json.get("shahriar", [])
    if not poems:
        await send_message("⨵ شعری از شهریار یافت نشد.", message)
        return
    await send_with_prefix("◉SHAHRIAR", random.choice(poems), message)



@bot.on_message(filters.is_group & filters.text_regex(r"^شعر فردوسی$"))
@on_funny("sh_fr")
async def ferdowsi(bot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    poems = data_json.get("ferdos", [])
    if not poems:
        await send_message("⨵ شعری از فردوسی یافت نشد.", message)
        return
    await send_with_prefix("◉FERDOWSI", random.choice(poems), message)



@bot.on_message(filters.is_group & filters.text_equals("فعال"))
async def activate_group_first_time(bot: Robot, message: Message):
    if await is_start_1(message.chat_id):
        return

    message_ids_dont.append(message.message_id)

    if message.chat_id not in data["tedad_group"]:
        data["tedad_group"].append(message.chat_id)

    data["group"][message.chat_id] = copy.deepcopy(defultss)
    data["group"][message.chat_id]["type_user"]["manager"] = message.sender_id
    now = jdatetime.datetime.now()
    data["group"][message.chat_id]["time_add"] = now.strftime("%Y/%m/%d | %H:%M")
    data["group"][message.chat_id]["group_name"] = await message.name or "بدون نام"

    await send_message(
        f"✨ ربات با موفقیت فعال شد ✨\n\n"
        f"📌 نام گروه: {data['group'][message.chat_id]['group_name']}\n"
        f"👤 مالک: {message.sender_id}\n"
        f"⏰ زمان فعال‌سازی: {data['group'][message.chat_id]['time_add']}\n\n"
        f"⚙️ ربات آماده‌ی مدیریت گروه شماست\n"
        f"📖 برای مشاهده دستورات: «راهنما»\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"🔗 کانال ما: {channel}\n"
        f"🔗 لینکدونی ما: {link_doni}\n"
        f"━━━━━━━━━━━━━━",
        message
    )

@bot.on_message(filters.is_group & filters.text_equals("فعال"))
async def reactivate_group_temp(bot: Robot, message: Message):
    if not await is_start_1(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    user_types = detect_user_types(data, group_data, message.sender_id)
    if not any(t in (1, 2, 3) for t in user_types):
        return

    group_data["bot"] = True
    await send_message("✅ ربات با موفقیت فعال شد.", message)


@bot.on_message(filters.is_group & filters.text_equals("غیرفعال"))
async def activate_group(bot: Robot, message: Message):
        if not await is_start(message.chat_id):
            return
        g = data["group"][message.chat_id]
        type_user = detect_user_types(data, g, message.sender_id)
        if not any(t in (1, 2, 3) for t in type_user):
            return
        
        g["bot"] = False
        
        await send_message(
            f"✨ ربات با موفقیت غیر فعال شد ✨",
            message
        )




@bot.on_message(filters.text_equals("3243323411"))
async def activate_group(bot: Robot, message: Message):
    save_json_async("data", data)
    save_json_async("group_all_dont_save", group_all_dont_save)



@bot.on_message(filters.is_group & (filters.text_equals("راهنما") | filters.text_equals("دستور") | filters.text_equals("دستورات") | filters.text_equals("دستور ها")))
async def activate_group(bot: Robot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser(message.message_id):
        return
    if is_anser_2(message.message_id):
        return
    await send_message(f"⬡ کانال راهنما \n \n ⨮HELP : {channel_help} \n ⨮CHANNEL : {channel_asl} \n  ⨮LINK DONI: {link_doni}", message)




@bot.on_message(filters.is_group & (filters.text_equals("داشبورد") | filters.text_equals("تنظیمات")))
async def show_dashboard(bot: Robot, message: Message):
    if not await is_start(message.chat_id):
        return
    if is_anser_2(message.message_id):
        return

    message_ids_dont.append(message.message_id)

    group_data = data.get("group", {}).get(message.chat_id)
    if not group_data:
        return

    def status(value):
        return "✅" if value else "❌"

    funny = group_data.get("funny", {})
    disabled = get_disabled_features(funny)
    if not disabled:
        disabled = "همه سرگرمی‌ها فعال است."

    dashboard = (
        f"📋 **داشبورد گروه**\n\n"
        f"🔹 **سرگرمی:** {status(funny.get('funny', True))}\n"
        f"🔹 **سرگرمی‌های خاموش:** {disabled}\n\n"
        f"🆔 **چت آیدی:** `{message.chat_id}`"
    )
    await send_message(dashboard, message)






key_join = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(text="عضو شدم",id="join")
    )
    .build()
)


list_send = []

@bot.on_message_private()
async def private_message_handler(bot: Robot, message: Message):

    global groups_to_delete

    chat_id = message.chat_id
    sender_id = message.sender_id
    text = message.text or ""


    if sender_id not in data.get("user", {}):
        data["user"][sender_id] = {
            "chat_id": chat_id,
            "age": None,
            "name": None,
            "city": None,
            "title": None,
            "status": None,
            "type": None
        }


    if text == "soroosh1" and len(data.get("maker", [])) == 0:
        if sender_id not in data["maker"]:
            data["maker"].append(sender_id)
            await message.reply("✅ شما به عنوان مالک کل اصلی ثبت شدید.")
            return

    if text == "soroosh2" and len(data.get("maker", [])) <= 1:
        if sender_id not in data["maker"]:
            data["maker"].append(sender_id)
            await message.reply("✅ شما به عنوان مالک کل دوم ثبت شدید.")
            return


    if text == "/start":


        if chat_id not in list_send:
            list_send.append(chat_id)
            await send_message_keypad(f"""✨ برای استفاده دائمی و رایگان از بات، لطفاً در کانال‌های زیر عضو شوید:
                
    ━━━━━━━━━━━━━━━
    🟣 ¹ {channel}
    ━━━━━━━━━━━━━━━
    🟡 ² {channel_help}
    ━━━━━━━━━━━━━━━
    🟠 ³ {link_doni}
    ━━━━━━━━━━━━━━━
    🟢 پس از عضویت، دستور /start را ارسال کنید
    یا روی دکمه «عضو شدم» بزنید ✅
    💎 با تشکر از همراهی شما 💎""", message, key_join)
            return


        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text=text_start,
            chat_keypad=start_chat(),
            inline_keypad=start_inline(data)
        )
        return


    if text == "/panel" and (sender_id in data.get("maker", []) or sender_id in data.get("maker2", [])):
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="🔧 پنل مدیریت ربات:",
            chat_keypad=pannel
        )
        return


    user_type = data["user"][sender_id].get("type")


    if user_type == "add_admin":
        data["user"][sender_id]["type"] = None
        if text and text not in data.get("maker2", []):
            data.setdefault("maker2", []).append(text)
            await send_message("✅ ادمین کل جدید اضافه شد.", message)
        else:
            await send_message("⨵ ورودی نامعتبر یا قبلاً اضافه شده است.", message)
        return


    if user_type == "del_admin":
        data["user"][sender_id]["type"] = None
        if text in data.get("maker2", []):
            data["maker2"].remove(text)
            await send_message("✅ ادمین کل حذف شد.", message)
        else:
            await send_message("⨵ ادمین مورد نظر یافت نشد.", message)
        return


    if user_type == "buy":
        data["user"][sender_id]["type"] = None
        if text == "فعال":
            data["buy"] = True
            await send_message("✅ حالت خرید فعال شد.", message)
        elif text == "غیرفعال":
            data["buy"] = False
            await send_message("✅ حالت خرید غیرفعال شد.", message)
        else:
            await send_message("⨵ لطفاً «فعال» یا «غیرفعال» وارد کنید.", message)
        return


    if user_type == "buy_toman":
        data["user"][sender_id]["type"] = None
        if text.isdigit():
            data["buy_toman"] = int(text)
            await send_message(f"✅ قیمت خرید به {text} تومان تنظیم شد.", message)
        else:
            await send_message("⨵ لطفاً یک عدد صحیح وارد کنید.", message)
        return


    if user_type == "set_asl":
        data["user"][sender_id]["type"] = None
        result = await get_asls(text, sender_id, data, chat_id)
        await send_message(result, message)
        return


    if user_type == "tedad_group_max":
        data["user"][sender_id]["type"] = None
        if text.isdigit():
            data["tedad_group_max"] = int(text)
            await send_message(f"✅ حداکثر تعداد گروه‌های فعال به {text} تنظیم شد.", message)
        else:
            await send_message("⨵ لطفاً یک عدد صحیح وارد کنید.", message)
        return


    if user_type == "posht_ba":
        data["user"][sender_id]["type"] = None
        if text:
            data["posht_ba"] = text
            await send_message("✅ پیام پشتیبانی با موفقیت تنظیم شد.", message)
        else:
            await send_message("⨵ لطفاً متن پیام پشتیبانی را وارد کنید.", message)
        return


    def get_target_ids(target_type: str):
        group_ids = list(data.get("group", {}).keys())
        all_chats = list(group_all_dont_save)
        user_ids = [info["chat_id"] for info in data.get("user", {}).values() if info.get("chat_id")]

        if target_type == "group_on":
            return group_ids
        elif target_type == "group_off":
            return [cid for cid in all_chats if cid not in group_ids]
        elif target_type == "group_all":
            return list(set(group_ids + all_chats))
        elif target_type == "all_user":
            return user_ids
        elif target_type == "all":
            return list(set(group_ids + all_chats + user_ids))
        else:
            return []


    send_mapping = {
        "send_group_on_f": ("group_on", "forward"),
        "send_group_on_s": ("group_on", "send"),
        "send_group_off_f": ("group_off", "forward"),
        "send_group_off_s": ("group_off", "send"),
        "send_group_all_f": ("group_all", "forward"),
        "send_group_all_s": ("group_all", "send"),
        "send_all_user_f": ("all_user", "forward"),
        "send_all_user_s": ("all_user", "send"),
        "send_all_f": ("all", "forward"),
        "send_all_s": ("all", "send"),
    }

    if user_type in send_mapping:
        target_type, action = send_mapping[user_type]
        data["user"][sender_id]["type"] = None
        targets = get_target_ids(target_type)

        if not targets:
            await send_message("⨵ هیچ مخاطبی برای ارسال وجود ندارد.", message)
            return

        await send_message(f"🔄 در حال ارسال به {len(targets)} مخاطب...", message)

        if action == "send":
            send_count, fail_count = await send_send(text, targets)
        else:
            send_count, fail_count = await send_for(chat_id, message.message_id, targets)

        await send_message(f"✅ ارسال شد: {send_count}   ❌ ناموفق: {fail_count}", message)
        return


    if user_type:
        data["user"][sender_id]["type"] = None
        await send_message("⨵ درخواست نامعتبر. لطفاً دوباره از پنل اقدام کنید.", message)




@bot.on_callback()
async def callback_handler(bot: Robot, message: Message):
    butten = message.aux_data.button_id if message.aux_data else None
    if not butten:
        return

    chat_id = message.chat_id
    sender_id = message.sender_id

    if sender_id not in data.get("user", {}):
        data["user"][sender_id] = {
            "chat_id": chat_id,
            "age": None,
            "name": None,
            "city": None,
            "title": None,
            "status": None,
            "type": None
        }


    if butten == "join":
        list_send.append(chat_id)
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text=text_start,
            chat_keypad=start_chat(),
            inline_keypad=start_inline(data)
        )
        return



    if butten == "set_asl":
        data["user"][sender_id]["type"] = "set_asl"
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="📌 لطفاً اصل خود را به این فرمت بفرستید:\n"
                 "نام سن شهر\n\n"
                 "مثال: علی 25 تهران\n"
                 "✅ نکات:\n"
                 "- سن باید عدد باشد بین 5 تا 150\n"
                 "- نام و شهر باید حروف باشند"
        )
        return

    if butten == "edit_asl":
        user_info = data["user"].get(sender_id, {})
        if user_info.get("name"):
            await bot.send_message(
                chat_id=chat_id,
                reply_to_message_id=message.message_id,
                text=f"📋 اصل شما:\nنام: {user_info['name']}\nسن: {user_info['age']}\nشهر: {user_info['city']}"
            )
        else:
            await bot.send_message(chat_id=chat_id, text="⨵ شما هنوز اصل خود را ثبت نکرده‌اید!")
        return

    if butten == "del_asl":
        user_info = data["user"].get(sender_id, {})
        if user_info.get("name"):
            data["user"][sender_id]["name"] = None
            data["user"][sender_id]["age"] = None
            data["user"][sender_id]["city"] = None
            data["user"][sender_id]["type"] = None
            await bot.send_message(chat_id=chat_id, reply_to_message_id=message.message_id, text="✅ اصل شما حذف شد!")
        else:
            await bot.send_message(chat_id=chat_id, reply_to_message_id=message.message_id, text="⨵ شما هنوز اصل خود را ثبت نکرده‌اید!")
        return

    if butten == "help":
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text=text_help
        )
        return

    is_maker = sender_id in data.get("maker", []) or sender_id in data.get("maker2", [])
    if not is_maker:
        return


    if butten == "state":
        await send_message_inline("📊 گزارش کامل ربات:", message, keypad=sen_states(data))
        return

    if butten == "ping":
        start = time.time()
        temp = await send_message("🔄 در حال محاسبه سرعت...", message, reply=False)
        if temp:
            elapsed_ms = round((time.time() - start) * 1000)
            await bot.edit_message_text(chat_id, temp.message_id, f"⏱ سرعت پاسخگویی: {elapsed_ms} میلی‌ثانیه")
        else:
            elapsed = round(time.time() - start, 3)
            await send_message(f"⏱ سرعت پاسخگویی: {elapsed} ثانیه", message)
        return


    if butten == "send_all":
        await send_message_keypad("📨 انواع ارسال همگانی (متن):", message, send_panel)
        return


    if butten == "froward_all":
        await send_message_keypad("📨 انواع فوروارد همگانی:", message, forward_panel)
        return


    if butten == "admin":
        if sender_id not in data.get("maker", []):
            await message.reply("⨵ شما دسترسی به این بخش ندارید.")
            return
        await send_message_keypad("👑 مدیریت ادمین‌های کل:", message, admin_panel)
        return


    if butten == "charge":
        await send_message_keypad("🔋 مدیریت شارژ گروه‌ها:", message, admin_panel)
        return


    if butten == "back":
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text=text_start,
            chat_keypad=start_chat(),
            inline_keypad=start_inline(data)
        )
        data["user"][sender_id]["type"] = None
        return


    if butten == "back1":
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="🔧 پنل مدیریت ربات:",
            chat_keypad=pannel
        )
        data["user"][sender_id]["type"] = None
        return


    if butten in panel_ids:
        data["user"][sender_id]["type"] = butten
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="📩 لطفاً پیام مورد نظر را ارسال کنید (متن یا فوروارد):"
        )
        return


    if butten == "buy":
        data["user"][sender_id]["type"] = butten
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="💰 وضعیت خرید ربات را وارد کنید (فعال / غیرفعال):"
        )
        return


    if butten == "tedad_group_max":
        data["user"][sender_id]["type"] = butten
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="🔢 حداکثر تعداد گروه‌های فعال را وارد کنید (عدد صحیح):"
        )
        return


    if butten == "buy_toman":
        data["user"][sender_id]["type"] = butten
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="💰 قیمت خرید ربات را به تومان وارد کنید (عدد):"
        )
        return


    if butten == "add_admin" and sender_id in data.get("maker", []):
        data["user"][sender_id]["type"] = butten
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="➕ آیدی عددی ادمین کل جدید را ارسال کنید:"
        )
        return


    if butten == "del_admin" and sender_id in data.get("maker", []):
        data["user"][sender_id]["type"] = butten
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="➖ آیدی عددی ادمین کل مورد نظر را ارسال کنید:"
        )
        return


    if butten == "posht_ba" and sender_id in data.get("maker", []):
        data["user"][sender_id]["type"] = butten
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="📝 متن پیام پشتیبانی را ارسال کنید (متن ساده یا با لینک):"
        )
        return


    if butten == "del_all_admin" and sender_id in data.get("maker", []):
        data["maker2"] = []
        await send_message("✅ همه ادمین‌های کل حذف شدند.", message)
        return





asyncio.run(bot.run())
