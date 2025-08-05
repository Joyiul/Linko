import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which

# Set path to local ffmpeg binary using absolute paths
BACKEND_DIR = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend'
FFMPEG_PATH = os.path.join(BACKEND_DIR, 'ffmpeg')
FFPROBE_PATH = os.path.join(BACKEND_DIR, 'ffprobe')
AudioSegment.converter = FFMPEG_PATH
AudioSegment.ffmpeg = FFMPEG_PATH
AudioSegment.ffprobe = FFPROBE_PATH

def convert_audio_to_wav(audio_path):
    """Convert audio file to WAV format if needed"""
    # Get file extension
    file_ext = os.path.splitext(audio_path)[1].lower()
    
    if file_ext == '.wav':
        return audio_path
    
    # Convert to WAV using pydub with local ffmpeg
    try:
        # Make sure ffmpeg binaries are executable
        import subprocess
        
        # Use direct subprocess call to ffmpeg for better control
        base_name = os.path.splitext(audio_path)[0]  # Remove extension
        wav_path = base_name + '.wav'
        
        # Direct ffmpeg command
        ffmpeg_cmd = [
            FFMPEG_PATH,
            '-i', audio_path,      # input file
            '-acodec', 'pcm_s16le', # audio codec
            '-ar', '16000',         # sample rate
            '-ac', '1',             # mono channel
            '-y',                   # overwrite output
            wav_path
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return wav_path
        else:
            print(f"FFmpeg error: {result.stderr}")
            return None
            
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
            return {"error": "Currently only WAV audio files are supported. Please convert your file to WAV format first."}
        
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
            return {"error": "Could not understand audio - please ensure the audio is clear and contains speech"}
        except sr.RequestError as e:
            return {"error": f"Could not request results from speech recognition service; {e}"}
            
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
