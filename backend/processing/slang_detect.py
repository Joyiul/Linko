import pandas as pd
import os

# Load the complete slang dataset
def load_slang_data():
    try:
        # Path to the slang CSV file
        csv_path = os.path.join('backend', 'Datasets', 'slang.csv')
        df = pd.read_csv(csv_path)
        
        # Create a dictionary mapping acronyms to expansions
        slang_map = {}
        for _, row in df.iterrows():
            acronym = str(row['acronym']).lower().strip()
            expansion = str(row['expansion']).strip()
            if acronym and expansion and acronym != 'nan':
                slang_map[acronym] = expansion
        
        return slang_map
    except Exception as e:
        print(f"Error loading slang data: {e}")
        # Fallback to basic slang map
        return {
            "cap": "lie or not true",
            "deadass": "seriously", 
            "fr": "for real",
            "bussin": "really good",
            "sus": "suspicious",
            "bet": "yes or okay",
            "no cap": "no lie",
            "salty": "upset or bitter",
            "flex": "show off",
            "lowkey": "kind of or secretly"
        }

# Load the slang data once when module is imported
SLANG_MAP = load_slang_data()

def detect_slang(text):
    """Detect slang terms in text and return their meanings"""
    found = {}
    words = text.lower().split()
    
    # Check for single word slang
    for word in words:
        # Remove punctuation
        clean_word = word.strip('.,!?";:()[]{}')
        if clean_word in SLANG_MAP:
            found[clean_word] = SLANG_MAP[clean_word]
    
    # Check for multi-word slang (like "no cap")
    text_lower = text.lower()
    for slang_term in SLANG_MAP:
        if ' ' in slang_term and slang_term in text_lower:
            found[slang_term] = SLANG_MAP[slang_term]
    
    return found
