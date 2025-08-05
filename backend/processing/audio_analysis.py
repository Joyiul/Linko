import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load and prepare tone dataset
def load_tone_dataset():
    try:
        # Path to the tone dataset - using absolute path
        tone_file_path = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/tone_v1.txt'
        
        # Read the tone dataset
        tone_data = []
        with open(tone_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if ' || ' in line:
                    text, tone = line.split(' || ')
                    # Clean up the tone (remove trailing periods)
                    tone = tone.rstrip('.')
                    tone_data.append({'text': text.strip(), 'tone': tone.strip()})
        
        print(f"Loaded {len(tone_data)} tone examples from dataset")
        return pd.DataFrame(tone_data)
    except Exception as e:
        print(f"Error loading tone dataset: {e}")
        return None

# Global variables for the tone analysis model
TONE_DATA = load_tone_dataset()
VECTORIZER = None
TONE_VECTORS = None

def initialize_tone_model():
    """Initialize the TF-IDF vectorizer and compute tone vectors"""
    global VECTORIZER, TONE_VECTORS
    
    if TONE_DATA is None:
        return False
    
    # Create TF-IDF vectorizer
    VECTORIZER = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2),  # Include both unigrams and bigrams
        lowercase=True
    )
    
    # Fit the vectorizer on the tone dataset
    TONE_VECTORS = VECTORIZER.fit_transform(TONE_DATA['text'])
    
    return True

def map_to_main_categories(specific_tone):
    """Map specific tones to main categories"""
    tone_mapping = {
        # Appreciative category
        'Appreciative': 'Appreciative',
        'Admiring': 'Appreciative', 
        'Benevolent': 'Appreciative',
        'Altruistic': 'Appreciative',
        'Thoughtful': 'Appreciative',
        
        # Cautionary category
        'Cautionary': 'Cautionary',
        'Aggressive': 'Cautionary',
        'Belligerent': 'Cautionary',
        'Accusatory': 'Cautionary',
        
        # Diplomatic category
        'Diplomatic': 'Diplomatic',
        'Candid': 'Diplomatic',
        'Apologetic': 'Diplomatic',
        'Ambivalent': 'Diplomatic',
        
        # Direct category
        'Direct': 'Direct',
        'Assertive': 'Direct',
        'Ardent': 'Direct',
        'Animated': 'Direct',
        
        # Informative category
        'Informative': 'Informative',
        
        # Inspirational category
        'Inspirational': 'Inspirational',
        'Amused': 'Inspirational',
        'Witty': 'Inspirational',
        
        # Additional mappings for other tones
        'Angry': 'Direct',
        'Bitter': 'Cautionary',
        'Callous': 'Cautionary',
        'Caustic': 'Cautionary',
        'Arrogant': 'Direct',
        'Apathetic': 'Neutral',
        'Absurd': 'Neutral',
        'Acerbic': 'Cautionary',
        'Aggrieved': 'Diplomatic'
    }
    
    return tone_mapping.get(specific_tone, 'Neutral')

def predict_tone_advanced(transcript):
    """Use machine learning to predict tone based on similarity to training data"""
    global VECTORIZER, TONE_VECTORS
    
    if VECTORIZER is None or TONE_VECTORS is None:
        if not initialize_tone_model():
            return predict_tone_basic(transcript)  # Fallback to basic method
    
    try:
        # Transform the input transcript
        input_vector = VECTORIZER.transform([transcript])
        
        # Calculate cosine similarity with all tone examples
        similarities = cosine_similarity(input_vector, TONE_VECTORS).flatten()
        
        # Find the most similar example
        best_match_idx = np.argmax(similarities)
        confidence = similarities[best_match_idx]
        
        # If confidence is too low, fall back to keyword-based analysis
        if confidence < 0.1:
            return predict_tone_basic(transcript)
        
        specific_tone = TONE_DATA.iloc[best_match_idx]['tone']
        main_tone = map_to_main_categories(specific_tone)
        
        return main_tone
        
    except Exception as e:
        print(f"Error in advanced tone prediction: {e}")
        return predict_tone_basic(transcript)

def predict_tone_basic(transcript):
    """Basic keyword-based tone prediction as fallback"""
    transcript_lower = transcript.lower()
    
    # Appreciative keywords
    appreciative_words = ['thank', 'appreciate', 'grateful', 'amazing', 'wonderful', 'incredible', 'inspiring', 'brilliant', 'fantastic', 'excellent']
    
    # Cautionary keywords  
    cautionary_words = ['careful', 'watch out', 'don\'t', 'avoid', 'beware', 'warning', 'danger', 'risk', 'caution']
    
    # Direct keywords
    direct_words = ['need', 'must', 'should', 'please', 'now', 'immediately', 'urgent', 'required']
    
    # Diplomatic keywords
    diplomatic_words = ['perhaps', 'might', 'could', 'consider', 'suggest', 'understand', 'perspective', 'compromise']
    
    # Informative keywords
    informative_words = ['is', 'are', 'was', 'were', 'fact', 'data', 'information', 'according', 'research', 'study']
    
    # Inspirational keywords
    inspirational_words = ['believe', 'achieve', 'dream', 'possible', 'success', 'motivation', 'inspire', 'goal']
    
    # Count occurrences
    tone_scores = {
        'Appreciative': sum(1 for word in appreciative_words if word in transcript_lower),
        'Cautionary': sum(1 for word in cautionary_words if word in transcript_lower),
        'Direct': sum(1 for word in direct_words if word in transcript_lower),
        'Diplomatic': sum(1 for word in diplomatic_words if word in transcript_lower),
        'Informative': sum(1 for word in informative_words if word in transcript_lower),
        'Inspirational': sum(1 for word in inspirational_words if word in transcript_lower)
    }
    
    # Return the tone with the highest score, or Neutral if all scores are 0
    max_tone = max(tone_scores, key=tone_scores.get)
    if tone_scores[max_tone] > 0:
        return max_tone
    else:
        return "Neutral"

def analyze_audio(transcript):
    """Main function to analyze tone from transcript"""
    if not transcript or not transcript.strip():
        return "Neutral"
    
    # Try advanced analysis first, fall back to basic if needed
    return predict_tone_advanced(transcript)
