#!/usr/bin/env python3
"""
Simple test to check video analysis endpoint
"""

import requests
import tempfile
import cv2
import numpy as np

def create_simple_test_video():
    """Create a very simple test video"""
    temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    temp_file.close()
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_file.name, fourcc, 10.0, (320, 240))
    
    # Create 30 simple frames
    for i in range(30):
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        frame[:, :] = [100, 100, 100]  # Gray frame
        cv2.putText(frame, f'Frame {i}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        out.write(frame)
    
    out.release()
    return temp_file.name

def test_video_endpoint():
    """Test the video analysis endpoint"""
    print("🧪 Testing video analysis endpoint...")
    
    # Create test video
    video_path = create_simple_test_video()
    print(f"Created test video: {video_path}")
    
    try:
        # Test the endpoint
        with open(video_path, 'rb') as video_file:
            files = {'video': video_file}
            response = requests.post(
                "http://localhost:5002/analyze-video",
                files=files,
                timeout=30
            )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Video analysis endpoint working!")
            else:
                print(f"❌ Analysis failed: {data.get('error')}")
        else:
            print(f"❌ HTTP Error {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    finally:
        # Cleanup
        import os
        try:
            os.remove(video_path)
        except:
            pass

if __name__ == "__main__":
    test_video_endpoint()
