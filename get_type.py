import time
import re
from typing import List, Dict, Any



def is_hang_code(text: str) -> bool:
    if "." not in text:
        return False
    parts = [p for p in text.split(".") if p]
    if len(parts) < 5:
        return False
    if not all(p.isdigit() for p in parts):
        return False
    if len(set(parts)) == 1:
        return True
    n = len(parts)
    for period in range(1, n // 2 + 1):
        if n % period != 0:
            continue
        pattern = parts[:period]
        if pattern * (n // period) == parts:
            return True
    return False


def safe_inc(d: dict, key: str, amount: int = 1):
    d[key] = d.get(key, 0) + amount



def detect_message_types(message, group_data: Dict[str, Any]) -> List[str]:

    types = []
    user_id = str(message.sender_id)
    now = time.time()

    group_data.setdefault("users", {})
    group_data.setdefault("num_message", {})

    users = group_data["users"]
    if user_id not in users:
        users[user_id] = {
            "all_message": 0,
            "num_spam": 0, "num_text": 0, "num_photo": 0, "num_video": 0,
            "num_audio": 0, "num_music": 0, "num_voice": 0, "num_document": 0,
            "num_archive": 0, "num_executable": 0, "num_font": 0, "num_gif": 0,
            "num_sticker": 0, "num_poll": 0, "num_contact": 0, "num_location": 0,
            "num_live_location": 0, "num_link": 0, "num_id": 0, "num_forwarded": 0,
            "num_hashtag": 0, "num_number": 0, "num_english": 0, "num_filters": 0,
            "num_reply": 0, "num_buttons": 0, "num_metadata": 0,
            "num_suspicious_file": 0, "num_hang_code": 0,
            "last_messages_time": []
        }

    user_data = users[user_id]
    user_data["all_message"] += 1
    safe_inc(group_data["num_message"], "total_messages", 1)

    user_data["last_messages_time"].append(now)
    user_data["last_messages_time"] = [
        t for t in user_data["last_messages_time"] if now - t <= 4
    ]
    if len(user_data["last_messages_time"]) > 4:
        types.append("spam")
        user_data["num_spam"] += 1
        safe_inc(group_data["num_message"], "num_spam", 1)


    if getattr(message, "is_text", False):
        text = getattr(message, "text", "") or ""
        types.append("text")
        user_data["num_text"] += 1
        safe_inc(group_data["num_message"], "num_text", 1)

        if "#" in text:
            types.append("hash")
            user_data["num_hashtag"] += 1
            safe_inc(group_data["num_message"], "num_hashtag", 1)

        if getattr(message, "has_link", False):
            types.append("link")
            user_data["num_link"] += 1
            safe_inc(group_data["num_message"], "num_link", 1)

        if re.search(r'@\w+', text):
            types.append("id")
            user_data["num_id"] += 1
            safe_inc(group_data["num_message"], "num_id", 1)


        for word in group_data.get("list_filters", []):
            if word and word in text:
                types.append("filters")
                user_data["num_filters"] += 1
                safe_inc(group_data["num_message"], "num_filters", 1)
                break


        if text.count(".") >= 10:
            types.append("hang_code")
            user_data["num_hang_code"] += 1
            safe_inc(group_data["num_message"], "num_hang_code", 1)


    if getattr(message, "is_media", False):
        if getattr(message, "is_photo", False):
            types.append("photo")
            user_data["num_photo"] += 1
            safe_inc(group_data["num_message"], "num_photo", 1)
        if getattr(message, "is_video", False):
            types.append("video")
            user_data["num_video"] += 1
            safe_inc(group_data["num_message"], "num_video", 1)
        if getattr(message, "is_gif", False):
            types.append("gif")
            user_data["num_gif"] += 1
            safe_inc(group_data["num_message"], "num_gif", 1)
        if getattr(message, "is_music", False):
            types.append("music")
            user_data["num_music"] += 1
            safe_inc(group_data["num_message"], "num_music", 1)
        if getattr(message, "is_audio", False):
            types.append("audio")
            user_data["num_audio"] += 1
            safe_inc(group_data["num_message"], "num_audio", 1)
        if getattr(message, "is_voice", False):
            types.append("voice")
            user_data["num_voice"] += 1
            safe_inc(group_data["num_message"], "num_voice", 1)
        if getattr(message, "is_document", False):
            types.append("document")
            user_data["num_document"] += 1
            safe_inc(group_data["num_message"], "num_document", 1)
        if getattr(message, "is_archive", False):
            types.append("archive")
            user_data["num_archive"] += 1
            safe_inc(group_data["num_message"], "num_archive", 1)
        if getattr(message, "is_executable", False):
            types.append("executable")
            user_data["num_executable"] += 1
            safe_inc(group_data["num_message"], "num_executable", 1)
        if getattr(message, "is_font", False):
            types.append("font")
            user_data["num_font"] += 1
            safe_inc(group_data["num_message"], "num_font", 1)


        file_obj = getattr(message, "file", None)
        if file_obj and getattr(file_obj, "size", 0) < 500:
            types.append("suspicious_file")
            user_data["num_suspicious_file"] += 1
            safe_inc(group_data["num_message"], "num_suspicious_file", 1)

    if getattr(message, "sticker", False):
        types.append("sticker")
        user_data["num_sticker"] += 1
        safe_inc(group_data["num_message"], "num_sticker", 1)
    if getattr(message, "is_poll", False):
        types.append("poll")
        user_data["num_poll"] += 1
        safe_inc(group_data["num_message"], "num_poll", 1)
    if getattr(message, "is_contact", False):
        types.append("contact")
        user_data["num_contact"] += 1
        safe_inc(group_data["num_message"], "num_contact", 1)
    if getattr(message, "is_location", False):
        types.append("location")
        user_data["num_location"] += 1
        safe_inc(group_data["num_message"], "num_location", 1)
    if getattr(message, "is_live_location", False):
        types.append("live_location")
        user_data["num_live_location"] += 1
        safe_inc(group_data["num_message"], "num_live_location", 1)
    if getattr(message, "is_forwarded", False):
        types.append("forwarded")
        user_data["num_forwarded"] += 1
        safe_inc(group_data["num_message"], "num_forwarded", 1)
    if getattr(message, "is_reply", False):
        types.append("reply")
        user_data["num_reply"] += 1
        safe_inc(group_data["num_message"], "num_reply", 1)
    if getattr(message, "has_buttons", False):
        types.append("buttons")
        user_data["num_buttons"] += 1
        safe_inc(group_data["num_message"], "num_buttons", 1)
    if getattr(message, "is_metadata", None):
        types.append("metadata")
        user_data["num_metadata"] += 1
        safe_inc(group_data["num_message"], "num_metadata", 1)

    return types



def detect_user_types(all_data: Dict[str, Any], group_data: Dict[str, Any], sender_id: str) -> List[int]:
    types = []
    type_user = group_data.get("type_user")
    if not isinstance(type_user, dict):
        return types

    now = int(time.time())


    if sender_id == all_data.get("bot"):
        return [0]
    if sender_id in all_data.get("maker", []):
        return [1]
    if sender_id in all_data.get("maker2", []):
        return [2]
    if sender_id == type_user.get("manager"):
        return [3]


    admin_dict = type_user.get("admin", {})
    if sender_id in admin_dict:
        info = admin_dict[sender_id]
        end_time = info.get("end_time")
        if end_time is None or end_time > now:
            return [4]
        else:
            del admin_dict[sender_id]


    silent_dict = type_user.get("silent", {})
    if sender_id in silent_dict:
        info = silent_dict[sender_id]
        end_time = info.get("end_time")
        if end_time is None or end_time > now:
            types.append(5)
        else:
            del silent_dict[sender_id]


    no_ansewr_dict = type_user.get("no_ansewr", {})
    if sender_id in no_ansewr_dict:
        info = no_ansewr_dict[sender_id]
        end_time = info.get("end_time")
        if end_time is None or end_time > now:
            types.append(6)
        else:
            del no_ansewr_dict[sender_id]


    mauf_dict = type_user.get("mauf", {})
    if sender_id in mauf_dict:
        info = mauf_dict[sender_id]
        end_time = info.get("end_time")
        if end_time is None or end_time > now:
            types.append(7)
        else:
            del mauf_dict[sender_id]


    kill_dict = type_user.get("kill", {})
    if sender_id in kill_dict:
        info = kill_dict[sender_id]
        end_time = info.get("end_time")
        if end_time is None or end_time > now:
            types.append(8)
        else:
            del kill_dict[sender_id]

    return types