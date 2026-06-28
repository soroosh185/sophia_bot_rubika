import random
import re

ZALGO_MARKS = [
    "̇", "ّ", "َ", "ِ", "ُ", "̃", "̸", "̷", "⃝", "ۛ", "ۗ", "ۖ", "ۘ"
]

FARSI_STYLES: dict[int, callable] = {
    1: lambda t: "ـ" + "ـ".join(t),
    2: lambda t: "".join(f"{c}ّ" for c in t),
    3: lambda t: "".join(f"{c}̸" for c in t),
    4: lambda t: "".join(c + random.choice(ZALGO_MARKS) for c in t),
    5: lambda t: f"¸„.-•~¹°\"ˆ˜¨  {t}  ¨˜ˆ\"°¹~•-.„¸",
    6: lambda t: t + " ◡̈⃝ ",
    7: lambda t: "".join(f"{c}ـ" for c in t),
    8: lambda t: "ـّ" + "ّـّ".join(t) + "ّـ",
    9: lambda t: "  ".join(t),
   10: lambda t: "".join(f"{c}ۛ" for c in t),
}

FARSI_STYLE_NAMES = {
    1: "کشیده",
    2: "تشدیدی",
    3: "خط‌دار",
    4: "زالگو",
    5: "قاب کلاسیک",
    6: "ایموجی‌دار",
    7: "موجی",
    8: "تزئینی سنگین",
    9: "هوایی",
   10: "ستاره‌دار",
}

_ALPHA = "abcdefghijklmnopqrstuvwxyz"

ENGLISH_FONTS: dict[int, dict] = {
    1: dict(zip(_ALPHA, "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇")),
    2: dict(zip(_ALPHA, "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻")),
    3: dict(zip(_ALPHA, "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏")),
    4: dict(zip(_ALPHA, "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷")),
    5: dict(zip(_ALPHA, "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ")),
    6: dict(zip(_ALPHA, "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉")),
    7: dict(zip(_ALPHA, "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳")),
    8: dict(zip(_ALPHA, "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫")),
}

ENGLISH_STYLE_NAMES = {
    1: "Bold",
    2: "Italic",
    3: "Script",
    4: "Fraktur",
    5: "Bubble",
    6: "Square",
    7: "Bold Serif",
    8: "Double Struck",
}


def font_farsi(text: str, style: int = 1) -> str:
    transform = FARSI_STYLES.get(style)
    if not transform:
        return text
    return transform(text)


def font_english(text: str, style: int = 1) -> str:
    font_map = ENGLISH_FONTS.get(style, {})
    return "".join(font_map.get(ch.lower(), ch) for ch in text)




def font_auto(text: str, style: int = 1):
    parts = re.findall(r'[\u0600-\u06FF\s]+|[a-zA-Z]+|.', text)

    result = []

    for part in parts:
        if re.search(r'[\u0600-\u06FF]', part):
            result.append(font_farsi(part, style))
        elif re.search(r'[a-zA-Z]', part):
            result.append(font_english(part, style))
        else:
            result.append(part)

    return "".join(result)

def list_styles(lang: str = "fa") -> str:
    styles = FARSI_STYLE_NAMES if lang == "fa" else ENGLISH_STYLE_NAMES
    lines  = [f"  {i}.  {name}" for i, name in styles.items()]
    header = "🎨 استایل‌های فارسی" if lang == "fa" else "🎨 English Styles"
    return f"{header}\n" + "┄" * 20 + "\n" + "\n".join(lines)