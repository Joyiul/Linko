import pandas as pd
import os
import re
import json

class EnhancedSlangDetector:
    def __init__(self):
        self.slang_map = {}
        self.genz_words = {}
        self.genz_slang = {}
        self.emoji_meanings = {}
        self.load_all_datasets()
    
    def load_all_datasets(self):
        """Load all slang and emoji datasets"""
        try:
            # Get absolute paths
            current_dir = os.path.dirname(os.path.abspath(__file__))
            datasets_dir = os.path.join(current_dir, '..', 'Datasets')
            
            # Load original slang dataset (acronyms/expansions)
            self.slang_map = self.load_original_slang(datasets_dir)
            print(f"Loaded {len(self.slang_map)} original slang terms")
            
            # Load Gen Z words dataset
            self.genz_words = self.load_genz_words(datasets_dir)
            print(f"Loaded {len(self.genz_words)} Gen Z words")
            
            # Load Gen Z slang dataset
            self.genz_slang = self.load_genz_slang(datasets_dir)
            print(f"Loaded {len(self.genz_slang)} Gen Z slang terms")
            
            # Load emoji meanings
            self.emoji_meanings = self.load_emoji_meanings(datasets_dir)
            print(f"Loaded {len(self.emoji_meanings)} emoji meanings")
            
            print(f"Total slang/emoji database: {len(self.slang_map) + len(self.genz_words) + len(self.genz_slang) + len(self.emoji_meanings)} entries")
            
        except Exception as e:
            print(f"Error loading slang datasets: {e}")
            self.fallback_slang_map()

    def load_original_slang(self, datasets_dir):
        """Load original slang.csv file"""
        try:
            csv_path = os.path.join(datasets_dir, 'slang.csv')
            df = pd.read_csv(csv_path)
            
            slang_map = {}
            for _, row in df.iterrows():
                acronym = str(row['acronym']).lower().strip()
                expansion = str(row['expansion']).strip()
                if acronym and expansion and acronym != 'nan':
                    slang_map[acronym] = {
                        'meaning': expansion,
                        'type': 'acronym',
                        'popularity': 'medium'
                    }
            return slang_map
        except Exception as e:
            print(f"Error loading original slang: {e}")
            return {}

    def load_genz_words(self, datasets_dir):
        """Load gen_zz_words.csv file"""
        try:
            csv_path = os.path.join(datasets_dir, 'gen_zz_words.csv')
            df = pd.read_csv(csv_path)
            
            genz_map = {}
            for _, row in df.iterrows():
                word = str(row['Word/Phrase']).lower().strip()
                definition = str(row['Definition']).strip()
                example = str(row['Example Sentence']).strip()
                popularity = str(row['Popularity/Trend Level']).lower().strip()
                
                if word and definition and word != 'nan':
                    genz_map[word] = {
                        'meaning': definition,
                        'example': example,
                        'popularity': popularity,
                        'type': 'genz_word'
                    }
            return genz_map
        except Exception as e:
            print(f"Error loading Gen Z words: {e}")
            return {}

    def load_genz_slang(self, datasets_dir):
        """Load genz_slang.csv file"""
        try:
            csv_path = os.path.join(datasets_dir, 'genz_slang.csv')
            df = pd.read_csv(csv_path)
            
            slang_map = {}
            for _, row in df.iterrows():
                keyword = str(row['keyword']).lower().strip()
                description = str(row['description']).strip()
                
                if keyword and description and keyword != 'nan':
                    slang_map[keyword] = {
                        'meaning': description,
                        'type': 'genz_slang',
                        'popularity': 'high'  # Gen Z slang is generally current/popular
                    }
            return slang_map
        except Exception as e:
            print(f"Error loading Gen Z slang: {e}")
            return {}

    def load_emoji_meanings(self, datasets_dir):
        """Load genz_emojis.csv file"""
        try:
            csv_path = os.path.join(datasets_dir, 'genz_emojis.csv')
            df = pd.read_csv(csv_path)
            
            emoji_map = {}
            for _, row in df.iterrows():
                emoji = str(row['emoji']).strip()
                name = str(row['Name']).strip()
                description = str(row['Description']).strip()
                
                if emoji and description and emoji != 'nan':
                    emoji_map[emoji] = {
                        'name': name,
                        'meaning': description,
                        'type': 'emoji',
                        'popularity': 'high'
                    }
            return emoji_map
        except Exception as e:
            print(f"Error loading emoji meanings: {e}")
            return {}

    def fallback_slang_map(self):
        """Fallback slang map if files can't be loaded"""
        self.slang_map = {
            "cap": {"meaning": "lie or not true", "type": "acronym", "popularity": "high"},
            "deadass": {"meaning": "seriously", "type": "acronym", "popularity": "high"}, 
            "fr": {"meaning": "for real", "type": "acronym", "popularity": "high"},
            "bussin": {"meaning": "really good", "type": "acronym", "popularity": "high"},
            "sus": {"meaning": "suspicious", "type": "acronym", "popularity": "high"},
            "bet": {"meaning": "yes or okay", "type": "acronym", "popularity": "high"},
            "no cap": {"meaning": "no lie", "type": "acronym", "popularity": "high"},
            "salty": {"meaning": "upset or bitter", "type": "acronym", "popularity": "medium"},
            "flex": {"meaning": "show off", "type": "acronym", "popularity": "high"},
            "lowkey": {"meaning": "kind of or secretly", "type": "acronym", "popularity": "high"},
            "periodt": {"meaning": "period, end of discussion", "type": "acronym", "popularity": "high"},
            "slaps": {"meaning": "is really good", "type": "acronym", "popularity": "high"},
            "hits different": {"meaning": "is exceptionally good", "type": "acronym", "popularity": "high"},
            "mid": {"meaning": "mediocre or average", "type": "acronym", "popularity": "medium"},
            "based": {"meaning": "being yourself authentically", "type": "acronym", "popularity": "medium"},
            "cringe": {"meaning": "embarrassing or awkward", "type": "acronym", "popularity": "high"}
        }

    def clean_text_for_matching(self, text):
        """Clean text for better slang matching"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        # Keep emojis, letters, numbers, and basic punctuation
        text = re.sub(r'[^\w\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000027BF\U0001F900-\U0001F9FF.,!?\'"()-]', '', text)
        return text

    def detect_emojis(self, text):
        """Detect and explain emojis in text"""
        found_emojis = {}
        
        # Check for emoji combinations first (like 👁️👄👁️)
        for emoji_combo, info in self.emoji_meanings.items():
            if emoji_combo in text and len(emoji_combo) > 1:
                found_emojis[emoji_combo] = info
        
        # Check for individual emojis
        for emoji, info in self.emoji_meanings.items():
            if len(emoji) == 1 and emoji in text and emoji not in found_emojis:
                found_emojis[emoji] = info
        
        return found_emojis

    def detect_slang_terms(self, text):
        """Detect slang terms from all datasets"""
        found_slang = {}
        clean_text = self.clean_text_for_matching(text)
        
        # Combine all slang dictionaries
        all_slang = {**self.slang_map, **self.genz_words, **self.genz_slang}
        
        # Check for multi-word slang first (like "no cap", "hits different")
        for term, info in all_slang.items():
            if ' ' in term and term in clean_text:
                found_slang[term] = info
        
        # Check for single word slang
        words = clean_text.split()
        for word in words:
            # Remove punctuation for matching
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in all_slang and clean_word not in found_slang:
                found_slang[clean_word] = all_slang[clean_word]
        
        return found_slang

    def get_popularity_score(self, item_info):
        """Get numeric popularity score for sorting"""
        popularity = item_info.get('popularity', 'medium').lower()
        scores = {'high': 3, 'medium': 2, 'low': 1}
        return scores.get(popularity, 2)

    def detect_slang(self, text):
        """Main function to detect all slang and emojis with enhanced information"""
        if not text or not text.strip():
            return {}
        
        # Detect slang terms
        found_slang = self.detect_slang_terms(text)
        
        # Detect emojis
        found_emojis = self.detect_emojis(text)
        
        # Combine results
        all_found = {**found_slang, **found_emojis}
        
        # Sort by popularity (high to low)
        sorted_items = dict(sorted(all_found.items(), 
                                 key=lambda x: self.get_popularity_score(x[1]), 
                                 reverse=True))
        
        return sorted_items

    def get_slang_statistics(self):
        """Get statistics about the loaded slang database"""
        total_original = len(self.slang_map)
        total_genz_words = len(self.genz_words)
        total_genz_slang = len(self.genz_slang)
        total_emojis = len(self.emoji_meanings)
        
        return {
            'original_slang': total_original,
            'genz_words': total_genz_words,
            'genz_slang': total_genz_slang,
            'emojis': total_emojis,
            'total': total_original + total_genz_words + total_genz_slang + total_emojis
        }

# Create global instance
enhanced_detector = EnhancedSlangDetector()

# Maintain backward compatibility with existing code
def load_slang_data():
    """Legacy function for backward compatibility"""
    return enhanced_detector.slang_map

def detect_slang(text):
    """Enhanced slang detection with all datasets"""
    return enhanced_detector.detect_slang(text)

# Export the enhanced detector for direct use
SLANG_MAP = enhanced_detector.slang_map
