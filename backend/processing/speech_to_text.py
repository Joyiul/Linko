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
    """Convert audio file to WAV format if needed - handles ANY audio format"""
    # Get file extension
    file_ext = os.path.splitext(audio_path)[1].lower()
    
    # Check if already WAV
    if file_ext == '.wav':
        # Still validate it's a proper WAV file
        try:
            import wave
            with wave.open(audio_path, 'rb') as wav_file:
                # If we can open it as WAV, it's good
                return audio_path
        except:
            # File has .wav extension but isn't proper WAV, convert it
            pass
    
    # Convert to WAV using multiple methods for maximum compatibility
    try:
        base_name = os.path.splitext(audio_path)[0]
        wav_path = base_name + '_converted.wav'
        
        # Method 1: Try pydub with local ffmpeg (most reliable)
        try:
            # Load audio with pydub (handles many formats including WebM)
            audio = AudioSegment.from_file(audio_path)
            
            print(f"Original audio: {len(audio)/1000:.1f} seconds, {audio.frame_rate}Hz, {audio.channels} channels")
            
            # Convert to the format speech_recognition expects:
            # - 16-bit PCM
            # - Mono channel  
            # - 16kHz sample rate (good for speech recognition)
            # - Make sure we don't lose any audio content
            audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
            
            # Normalize audio volume to ensure it's audible
            # Increase volume if too quiet (but don't clip)
            if audio.max_dBFS < -20:  # If audio is very quiet
                audio = audio + (min(10, abs(audio.max_dBFS + 20)))  # Boost volume safely
                print(f"Boosted quiet audio by {min(10, abs(audio.max_dBFS + 20))}dB")
            
            # Export as WAV - ensure we capture the full duration
            audio.export(wav_path, format="wav")
            
            print(f"Successfully converted {audio_path} to {wav_path} using pydub")
            print(f"Converted audio: {len(audio)/1000:.1f} seconds")
            return wav_path
            
        except Exception as pydub_error:
            print(f"Pydub conversion failed: {pydub_error}")
            
            # Method 2: Direct ffmpeg subprocess (fallback)
            import subprocess
            
            ffmpeg_cmd = [
                FFMPEG_PATH,
                '-i', audio_path,           # input file
                '-acodec', 'pcm_s16le',     # 16-bit PCM
                '-ar', '16000',             # 16kHz sample rate
                '-ac', '1',                 # mono
                '-f', 'wav',                # WAV format
                '-y',                       # overwrite
                wav_path
            ]
            
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Successfully converted {audio_path} to {wav_path} using direct ffmpeg")
                return wav_path
            else:
                print(f"FFmpeg direct conversion failed: {result.stderr}")
                
                # Method 3: Try without local ffmpeg (use system)
                try:
                    # Reset pydub to use system ffmpeg
                    AudioSegment.converter = "ffmpeg"
                    AudioSegment.ffmpeg = "ffmpeg"
                    AudioSegment.ffprobe = "ffprobe"
                    
                    audio = AudioSegment.from_file(audio_path)
                    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
                    audio.export(wav_path, format="wav")
                    
                    print(f"Successfully converted {audio_path} to {wav_path} using system ffmpeg")
                    return wav_path
                    
                except Exception as system_error:
                    print(f"System ffmpeg conversion failed: {system_error}")
                    
                    # Method 4: Install ffmpeg-python as last resort
                    try:
                        import ffmpeg
                        
                        (
                            ffmpeg
                            .input(audio_path)
                            .output(wav_path, acodec='pcm_s16le', ar=16000, ac=1)
                            .overwrite_output()
                            .run(quiet=True)
                        )
                        
                        print(f"Successfully converted {audio_path} to {wav_path} using ffmpeg-python")
                        return wav_path
                        
                    except ImportError:
                        print("ffmpeg-python not available. Install with: pip install ffmpeg-python")
                    except Exception as ffmpeg_python_error:
                        print(f"ffmpeg-python conversion failed: {ffmpeg_python_error}")
        
        # If all methods fail, return None
        print(f"All conversion methods failed for {audio_path}")
        return None
            
    except Exception as e:
        print(f"Error in audio conversion: {e}")
        return None

def transcribe_long_audio_chunked(wav_path, recognizer):
    """Transcribe long audio by breaking it into chunks"""
    try:
        from pydub import AudioSegment
        
        # Load the audio file
        audio = AudioSegment.from_wav(wav_path)
        
        # If audio is shorter than 30 seconds, don't chunk
        if len(audio) < 30000:  # 30 seconds in milliseconds
            return None
            
        print(f"Audio is {len(audio)/1000:.1f} seconds long, using chunked transcription...")
        
        # Split into 30-second chunks with 2-second overlap
        chunk_length_ms = 30000  # 30 seconds
        overlap_ms = 2000        # 2 seconds overlap
        chunks = []
        transcripts = []
        
        for i in range(0, len(audio), chunk_length_ms - overlap_ms):
            chunk = audio[i:i + chunk_length_ms]
            if len(chunk) < 1000:  # Skip chunks shorter than 1 second
                continue
                
            # Save chunk as temporary WAV
            chunk_path = wav_path.replace('.wav', f'_chunk_{len(chunks)}.wav')
            chunk.export(chunk_path, format="wav")
            chunks.append(chunk_path)
            
            # Transcribe this chunk
            try:
                with sr.AudioFile(chunk_path) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
                    
                # Try Google recognition on chunk
                try:
                    chunk_transcript = recognizer.recognize_google(audio_data, language="en-US")
                    transcripts.append(chunk_transcript)
                    print(f"Chunk {len(chunks)} transcribed: {chunk_transcript[:50]}...")
                except:
                    print(f"Chunk {len(chunks)} failed transcription")
                    
            except Exception as chunk_error:
                print(f"Error processing chunk {len(chunks)}: {chunk_error}")
            
            # Clean up chunk file
            try:
                os.remove(chunk_path)
            except:
                pass
        
        # Combine all transcripts
        if transcripts:
            full_transcript = ' '.join(transcripts)
            # Clean up duplicate words at chunk boundaries
            words = full_transcript.split()
            cleaned_words = []
            
            for i, word in enumerate(words):
                # Skip if this word is the same as the previous word (likely overlap)
                if i == 0 or word.lower() != words[i-1].lower():
                    cleaned_words.append(word)
            
            return ' '.join(cleaned_words)
        
        return None
        
    except Exception as e:
        print(f"Chunked transcription error: {e}")
        return None

def transcribe_audio(audio_path):
    """Convert audio file to text using speech recognition - handles ANY audio format"""
    recognizer = sr.Recognizer()
    
    # Configure recognizer for better phrase capture
    recognizer.energy_threshold = 200  # Lower threshold to catch quieter speech
    recognizer.dynamic_energy_threshold = True  # Adapt to audio conditions
    recognizer.pause_threshold = 1.2  # Allow longer pauses between words (default is 0.8)
    recognizer.phrase_threshold = 0.3  # Minimum length of phrase before processing
    recognizer.non_speaking_duration = 0.8  # How long to wait for silence before ending
    
    try:
        print(f"Starting transcription for: {audio_path}")
        
        # Convert to WAV if needed
        wav_path = convert_audio_to_wav(audio_path)
        if not wav_path:
            return {
                "error": "Could not convert audio file to WAV format. The file may be corrupted or in an unsupported format.",
                "suggestion": "Try recording again or using a different audio format."
            }
        
        print(f"Using WAV file: {wav_path}")
        
        # Verify the WAV file exists and is readable
        if not os.path.exists(wav_path):
            return {
                "error": "Converted audio file not found.",
                "suggestion": "Please try recording again."
            }
        
        # Load audio file with better error handling
        try:
            with sr.AudioFile(wav_path) as source:
                print("Loading audio file...")
                # Get audio file info
                audio_info = source.DURATION if hasattr(source, 'DURATION') else "unknown"
                print(f"Audio file duration: {audio_info} seconds")
                
                # Adjust for ambient noise (but with timeout)
                recognizer.adjust_for_ambient_noise(source, duration=min(1.0, audio_info if isinstance(audio_info, (int, float)) else 1.0))
                
                # Listen for ALL the data (not just part of it)
                # The key fix: Use record() instead of listen() to capture entire audio
                audio_data = recognizer.record(source)
                print(f"Audio loaded successfully. Full audio captured: {len(audio_data.frame_data)} bytes")
                
        except Exception as load_error:
            print(f"Error loading audio file: {load_error}")
            return {
                "error": f"Could not load audio file: {str(load_error)}",
                "suggestion": "The audio file may be corrupted. Try recording again."
            }
        
        # Try multiple speech recognition methods for better success rate
        transcript = None
        recognition_method = None
        
        # Method 1: Google Speech Recognition (free, good quality)
        try:
            print("Trying Google Speech Recognition...")
            # Use show_all=True to get more complete results and specify language
            transcript = recognizer.recognize_google(
                audio_data, 
                language="en-US",  # Specify language for better accuracy
                show_all=False     # Set to True to get confidence scores and alternatives
            )
            recognition_method = "Google Speech Recognition"
            print(f"Google recognition successful: {transcript}")
            
        except sr.UnknownValueError:
            print("Google could not understand audio")
        except sr.RequestError as e:
            print(f"Google Speech Recognition error: {e}")
        except Exception as e:
            print(f"Unexpected Google recognition error: {e}")
        
        # Method 2: Try with different audio settings if Google failed
        if not transcript:
            try:
                print("Trying Google recognition with show_all for better results...")
                # Try with show_all to get more complete transcription
                result = recognizer.recognize_google(
                    audio_data, 
                    language="en-US",
                    show_all=True
                )
                
                if result and 'alternative' in result and len(result['alternative']) > 0:
                    # Get the best alternative
                    transcript = result['alternative'][0]['transcript']
                    confidence = result['alternative'][0].get('confidence', 0.0)
                    recognition_method = f"Google Speech Recognition (detailed, confidence: {confidence:.2f})"
                    print(f"Google detailed recognition successful: {transcript}")
                
            except Exception as detailed_error:
                print(f"Google detailed recognition failed: {detailed_error}")
                
                # Method 2b: Try with adjusted energy settings
                try:
                    print("Trying Google recognition with adjusted energy threshold...")
                    recognizer.energy_threshold = 100  # Even lower threshold
                    recognizer.dynamic_energy_threshold = True
                    transcript = recognizer.recognize_google(audio_data, language="en-US")
                    recognition_method = "Google Speech Recognition (low threshold)"
                    print(f"Google low threshold recognition successful: {transcript}")
                    
                except:
                    print("Google recognition with adjustments failed")
        
        # Method 3: Sphinx (offline, lower quality but always available)
        if not transcript:
            try:
                print("Trying Sphinx (offline) recognition...")
                transcript = recognizer.recognize_sphinx(audio_data)
                recognition_method = "Sphinx (offline)"
                print(f"Sphinx recognition successful: {transcript}")
                
            except sr.UnknownValueError:
                print("Sphinx could not understand audio")
            except sr.RequestError as e:
                print(f"Sphinx recognition error: {e}")
            except Exception as e:
                print(f"Sphinx recognition failed: {e}")
        
        # Method 4: Try chunking for very long audio (if still no transcript)
        if not transcript:
            try:
                print("Trying chunked transcription for long audio...")
                transcript = transcribe_long_audio_chunked(wav_path, recognizer)
                if transcript:
                    recognition_method = "Google Speech Recognition (chunked)"
                    print(f"Chunked recognition successful: {transcript}")
                    
            except Exception as chunk_error:
                print(f"Chunked transcription failed: {chunk_error}")
        
        # If we got a transcript, return it
        if transcript and transcript.strip():
            return {
                "transcript": transcript.strip(),
                "success": True,
                "method": recognition_method,
                "audio_file": wav_path
            }
        else:
            return {
                "error": "Could not understand audio - no speech was detected or the audio quality was too low",
                "suggestion": "Try speaking more clearly, closer to the microphone, or in a quieter environment",
                "attempted_methods": ["Google Speech Recognition", "Sphinx offline recognition"]
            }
            
    except Exception as e:
        print(f"Unexpected error in transcribe_audio: {e}")
        import traceback
        traceback.print_exc()
        return {
            "error": f"Unexpected error during transcription: {str(e)}",
            "suggestion": "Please try again or contact support if the problem persists"
        }

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
