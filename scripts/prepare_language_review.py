import pandas as pd
import re
from pathlib import Path

INPUT = Path("data/raw/youtube_comments.csv")
OUTPUT = Path("data/processed/language_review.csv")

df = pd.read_csv(INPUT)

HINDI_WORDS = {
    "hai", "hain", "he", "tha", "thi", "the", "nahi", "nahin",
    "kya", "kyu", "kyun", "kaise", "ka", "ki", "ke", "ko",
    "se", "mein", "me", "par", "aur", "ye", "yeh", "woh",
    "vo", "is", "iska", "iski", "iske", "us", "mujhe",
    "hume", "hum", "aap", "apne", "mera", "meri", "mere",
    "bahut", "bohot", "accha", "achha", "acha", "bura",
    "duniya", "pani", "paani", "desh", "log", "insaan",
    "kyunki", "lekin", "agar", "toh", "to", "bhi", "hi",
    "kar", "karo", "kare", "raha", "rahi", "rahe",
    "hoga", "hogi", "honge", "hona", "chahiye",
    "parivartan", "jalvayu", "prithvi", "dharti",
    "garam", "garmi", "mausam", "badal", "badlav"
}

BENGALI_WORDS = {
    "ami", "amar", "amra", "tumi", "tomar", "apni",
    "amader", "bhalo", "valo", "kharap", "kintu",
    "karon", "ebong", "onek", "khub", "manush",
    "prithibi", "poriborton", "jalbayu", "ushnota",
    "hobe", "hoy", "kore", "kora", "keno", "ki",
    "na", "theke", "jodi", "tahole", "sob", "shob",
    "pokhe", "bipokho", "kicu", "kichu", "korar",
    "nai", "manuser", "manusher", "jonno", "hoche",
    "hocche", "prithvir", "fus", "jungle", "agun",
    "amadarka", "sundor", "postar", "shakhanor",
    "dhonnobad", "onek", "onk", "informative",
    "chilo", "bujhechi", "bhujechi", "bhalo",
    "valo", "sir", "baiya", "samne", "dekteci"
}

def classify_comment(text):
    if pd.isna(text) or not str(text).strip():
        return "uncertain", "empty comment"

    text = str(text).strip()

    has_devanagari = bool(re.search(r"[\u0900-\u097F]", text))
    has_bengali = bool(re.search(r"[\u0980-\u09FF]", text))
    has_latin = bool(re.search(r"[A-Za-z]", text))

    if has_devanagari and has_bengali:
        return "mixed_hi_bn_review", "both Indic scripts"

    if has_devanagari:
        if has_latin:
            return "hi_mixed", "Devanagari and Latin"
        return "hi", "Devanagari script"

    if has_bengali:
        if has_latin:
            return "bn_mixed", "Bengali and Latin"
        return "bn", "Bengali script"

    if not has_latin:
        return "uncertain", "no recognizable language script"

    words = set(re.findall(r"[a-z]+", text.lower()))

    hi_matches = words & HINDI_WORDS
    bn_matches = words & BENGALI_WORDS

    if len(hi_matches) >= 2 and len(bn_matches) >= 2:
        return "romanized_hi_bn_review", "Hindi and Bengali vocabulary"

    if len(hi_matches) >= 2:
        return "hi_Latn_candidate", "Hindi vocabulary: " + ", ".join(sorted(hi_matches))

    if len(bn_matches) >= 2:
        return "bn_Latn_candidate", "Bengali vocabulary: " + ", ".join(sorted(bn_matches))

    return "Latin_review", "English or uncertain Roman-script text"

results = df["comment_text"].apply(classify_comment)

df["script_language_candidate"] = results.apply(lambda x: x[0])
df["language_reason"] = results.apply(lambda x: x[1])

df["confirmed_language"] = ""
df["language_review_status"] = "Pending"

df["stance"] = ""
df["stance_review_status"] = "Pending"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)

print("\n===== LANGUAGE CANDIDATE DISTRIBUTION =====")
print(df["script_language_candidate"].value_counts().to_string())

print("\n===== REVIEW FILE =====")
print(OUTPUT)
print("Total comments:", len(df))

print("\n===== ROMANIZED HINDI EXAMPLES =====")
for text in df.loc[
    df["script_language_candidate"] == "hi_Latn_candidate",
    "comment_text"
].head(15):
    print("-", text)
