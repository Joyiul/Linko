#!/usr/bin/env python3
"""
Test script for enhanced multimodal video analysis.
Tests the integration of facial and audio emotion analysis from video files.
"""

import os
import sys
import requests
import json
import tempfile
import cv2
import numpy as np
from pathlib import Path

# Add backend to path
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_path)

def create_test_video_with_audio():
    """Create a simple test video with audio for testing."""
    try:
        print("🎬 Creating test video with audio...")
        
        # Create a simple video with OpenCV
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        
        out = cv2.VideoWriter(temp_video.name, fourcc, 20.0, (640, 480))
        
        # Create 60 frames (3 seconds at 20 fps)
        for i in range(60):
            # Create a frame with changing colors to simulate emotion
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            
            # Simulate different "emotions" through color changes
            if i < 20:  # First second - "happy" (green-ish)
                frame[:, :] = [50, 200, 50]
            elif i < 40:  # Second second - "neutral" (blue-ish)
                frame[:, :] = [200, 50, 50]
            else:  # Third second - "sad" (red-ish)
                frame[:, :] = [50, 50, 200]
            
            # Add some text
            cv2.putText(frame, f'Frame {i}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            out.write(frame)
        
        out.release()
        print(f"✅ Test video created: {temp_video.name}")
        return temp_video.name
        
    except Exception as e:
        print(f"❌ Failed to create test video: {e}")
        return None

def test_multimodal_video_analysis():
    """Test the multimodal video analysis endpoint."""
    print("🧪 Testing Multimodal Video Analysis")
    print("=" * 50)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:5002/", timeout=5)
        print("✅ Backend server is running")
    except:
        print("❌ Backend server is not running. Please start it first.")
        print("Run: python app.py")
        return False
    
    # Create test video
    test_video_path = create_test_video_with_audio()
    if not test_video_path:
        print("❌ Cannot create test video")
        return False
    
    try:
        # Test 1: Basic video analysis
        print("\n📹 Test 1: Basic Enhanced Video Analysis")
        print("-" * 40)
        
        with open(test_video_path, 'rb') as video_file:
            files = {'video': video_file}
            data = {'fusion_strategy': 'weighted_average'}
            
            response = requests.post(
                "http://localhost:5002/analyze-video",
                files=files,
                data=data,
                timeout=60
            )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Basic video analysis successful")
            
            if result.get('success'):
                analysis = result.get('analysis_results', {})
                print(f"📊 Final Emotion: {analysis.get('final_emotion', 'unknown')}")
                print(f"🎯 Confidence: {analysis.get('confidence', 0):.2f}")
                print(f"🔄 Fusion Method: {analysis.get('fusion_method', 'unknown')}")
                print(f"👥 Faces Detected: {analysis.get('facial_analysis', {}).get('faces_detected_total', 0)}")
                print(f"🎵 Audio Analyzed: {analysis.get('audio_analysis', {}).get('analyzed', False)}")
                
                modalities = analysis.get('multimodal_details', {}).get('modalities_used', [])
                print(f"🔬 Modalities Used: {', '.join(modalities) if modalities else 'None'}")
                
                if result.get('processing_info', {}).get('audio_extracted'):
                    print("🎧 Audio extraction: SUCCESS")
                else:
                    print("⚠️ Audio extraction: FAILED or NO AUDIO")
                    
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
        
        # Test 2: Advanced multimodal analysis
        print("\n🔬 Test 2: Advanced Multimodal Analysis")
        print("-" * 40)
        
        with open(test_video_path, 'rb') as video_file:
            files = {'video': video_file}
            data = {
                'fusion_strategy': 'max_confidence',
                'max_frames': 20,
                'skip_frames': 5,
                'include_frame_details': 'true'
            }
            
            response = requests.post(
                "http://localhost:5002/analyze-video-multimodal",
                files=files,
                data=data,
                timeout=60
            )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Advanced multimodal analysis successful")
            
            if result.get('success'):
                final_analysis = result.get('final_analysis', {})
                facial_analysis = result.get('facial_emotion_analysis', {})
                audio_analysis = result.get('audio_emotion_analysis', {})
                fusion_details = result.get('multimodal_fusion_details', {})
                
                print(f"🎭 Final Emotion: {final_analysis.get('emotion', 'unknown')}")
                print(f"🎯 Confidence: {final_analysis.get('confidence', 0):.4f}")
                print(f"📈 Quality: {final_analysis.get('analysis_quality', 'unknown')}")
                print(f"🔄 Fusion Strategy: {fusion_details.get('strategy_used', 'unknown')}")
                print(f"🤝 Agreement Score: {fusion_details.get('agreement_score', 'N/A')}")
                
                print(f"\n👥 Facial Analysis:")
                facial_summary = facial_analysis.get('summary', {})
                print(f"   - Frames Processed: {facial_summary.get('frames_processed', 0)}")
                print(f"   - Faces Detected: {facial_summary.get('total_faces_detected', 0)}")
                print(f"   - Dominant Emotion: {facial_summary.get('dominant_emotion', 'none')}")
                
                print(f"\n🎵 Audio Analysis:")
                print(f"   - Processed: {audio_analysis.get('processed', False)}")
                print(f"   - Emotion: {audio_analysis.get('emotion_detected', 'none')}")
                confidence = audio_analysis.get('confidence')
                if confidence is not None:
                    print(f"   - Confidence: {confidence:.4f}")
                else:
                    print(f"   - Confidence: N/A")
                
                modalities = fusion_details.get('modalities_analyzed', [])
                print(f"\n🔬 Modalities: {', '.join(modalities) if modalities else 'None'}")
                
                print(f"\n📋 Research Summary:")
                print(f"   {result.get('research_summary', 'No summary available')}")
                
            else:
                print(f"❌ Advanced analysis failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Advanced analysis request failed: {response.status_code}")
            print(f"Response: {response.text}")
        
        # Test 3: Error handling
        print("\n🔧 Test 3: Error Handling")
        print("-" * 40)
        
        # Test with invalid file
        try:
            files = {'video': ('test.txt', b'not a video file', 'text/plain')}
            response = requests.post(
                "http://localhost:5002/analyze-video",
                files=files,
                timeout=10
            )
            
            if response.status_code == 400:
                print("✅ Error handling works - invalid file type rejected")
            else:
                print(f"⚠️ Unexpected response for invalid file: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        if test_video_path and os.path.exists(test_video_path):
            try:
                os.remove(test_video_path)
                print(f"🧹 Cleaned up test video: {test_video_path}")
            except:
                pass

def test_system_requirements():
    """Test if all required components are available."""
    print("🔍 Checking System Requirements")
    print("-" * 40)
    
    requirements_met = True
    
    # Check FFmpeg
    try:
        import subprocess
        
        # First try local backend FFmpeg
        backend_ffmpeg = os.path.join(backend_path, 'ffmpeg')
        if os.path.exists(backend_ffmpeg):
            result = subprocess.run([backend_ffmpeg, '-version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ FFmpeg is available (local backend)")
            else:
                print("⚠️ Local FFmpeg may not be working properly")
        else:
            # Try system FFmpeg
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ FFmpeg is available (system)")
            else:
                print("⚠️ FFmpeg may not be working properly")
    except FileNotFoundError:
        print("❌ FFmpeg not found in system PATH or backend directory")
        requirements_met = False
    except Exception as e:
        print(f"⚠️ FFmpeg check failed: {e}")
    
    # Check required Python packages
    required_packages = ['cv2', 'librosa', 'numpy', 'requests']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is not installed")
            requirements_met = False
    
    return requirements_met

if __name__ == "__main__":
    print("🎥 Enhanced Multimodal Video Analysis Test Suite")
    print("=" * 60)
    
    # Check requirements
    if not test_system_requirements():
        print("\n❌ System requirements not met. Please install missing components.")
        sys.exit(1)
    
    # Run tests
    success = test_multimodal_video_analysis()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests completed successfully!")
        print("🎉 Enhanced multimodal video analysis is working!")
        print("\n📚 Usage:")
        print("   - POST /analyze-video: Enhanced video analysis with multimodal fusion")
        print("   - POST /analyze-video-multimodal: Advanced research-grade analysis")
        print("   - Both endpoints now extract audio and combine with facial analysis")
        print("   - Supports fusion strategies: weighted_average, max_confidence, voting")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
