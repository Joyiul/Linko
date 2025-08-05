SLANG_MAP = {
    "cap": "lie or not true",
    "deadass": "seriously",
    "fr": "for real",
    "bussin": "really good",
    "sus": "suspicious"
}

def detect_slang(text):
    found = {}
    for word in text.lower().split():
        if word in SLANG_MAP:
            found[word] = SLANG_MAP[word]
    return found
