import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which

def convert_audio_to_wav(audio_path):
    """Convert audio file to WAV format if needed"""
    # Get file extension
    file_ext = os.path.splitext(audio_path)[1].lower()
    
    if file_ext == '.wav':
        return audio_path
    
    # Convert to WAV using pydub
    try:
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.replace(file_ext, '.wav')
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        print(f"Error converting audio: {e}")
        return None

def transcribe_audio(audio_path):
    """Convert audio file to text using speech recognition"""
    recognizer = sr.Recognizer()
    
    try:
        # Convert to WAV if needed
        wav_path = convert_audio_to_wav(audio_path)
        if not wav_path:
            return {"error": "Could not convert audio file"}
        
        # Load audio file
        with sr.AudioFile(wav_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            # Listen for the data (load audio to memory)
            audio_data = recognizer.listen(source)
        
        # Try to recognize speech using Google's free API
        try:
            transcript = recognizer.recognize_google(audio_data)
            return {
                "transcript": transcript,
                "success": True
            }
        except sr.UnknownValueError:
            return {"error": "Could not understand audio"}
        except sr.RequestError as e:
            return {"error": f"Could not request results; {e}"}
            
    except Exception as e:
        return {"error": f"Error processing audio: {str(e)}"}

def transcribe_with_whisper(audio_path):
    """Alternative: Use OpenAI Whisper for better accuracy (requires openai-whisper)"""
    try:
        import whisper
        model = whisper.load_model("base")  # You can use "tiny", "base", "small", "medium", "large"
        result = model.transcribe(audio_path)
        return {
            "transcript": result["text"],
            "success": True
        }
    except ImportError:
        return {"error": "Whisper not installed. Use: pip install openai-whisper"}
    except Exception as e:
        return {"error": f"Whisper error: {str(e)}"}
