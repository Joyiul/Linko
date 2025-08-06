import cv2
import numpy as np
from .facial_analysis import analyze_facial_features
import os
import tempfile

def extract_frames_from_video(video_path, max_frames=30, skip_frames=10):
    """Extract frames from video for analysis"""
    try:
        cap = cv2.VideoCapture(video_path)
        frames = []
        frame_count = 0
        extracted_count = 0
        
        while cap.read()[0] and extracted_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Skip frames to reduce processing
            if frame_count % skip_frames == 0:
                frames.append(frame)
                extracted_count += 1
            
            frame_count += 1
        
        cap.release()
        print(f"Extracted {len(frames)} frames from video")
        return frames
        
    except Exception as e:
        print(f"Error extracting frames: {e}")
        return []

def analyze_video_facial_features(video_path):
    """Analyze facial features in video frames"""
    try:
        # Extract frames
        frames = extract_frames_from_video(video_path)
        
        if not frames:
            return {"error": "No frames could be extracted from video"}
        
        # Analyze each frame
        frame_results = []
        for i, frame in enumerate(frames):
            result = analyze_facial_features(frame)
            
            if "error" not in result:
                frame_results.append({
                    "frame_number": i,
                    "predicted_class": result.get("predicted_class"),
                    "confidence": result.get("confidence"),
                    "timestamp": i * 10 / 30  # Approximate timestamp based on skip_frames
                })
        
        if not frame_results:
            return {"error": "No facial features detected in any frame"}
        
        # Aggregate results
        predictions = [r["predicted_class"] for r in frame_results if r["predicted_class"]]
        confidences = [r["confidence"] for r in frame_results if r["confidence"]]
        
        if predictions:
            # Most common prediction
            most_common = max(set(predictions), key=predictions.count)
            avg_confidence = sum(confidences) / len(confidences)
            
            return {
                "overall_prediction": most_common,
                "avg_confidence": avg_confidence,
                "frame_count": len(frame_results),
                "frame_results": frame_results
            }
        else:
            return {"error": "No valid predictions from video frames"}
            
    except Exception as e:
        print(f"Error analyzing video: {e}")
        return {"error": f"Video analysis failed: {str(e)}"}

def analyze_video_with_multimodal(video_path, audio_transcript=None, audio_tone=None):
    """Combine video facial analysis with audio analysis"""
    try:
        # Analyze video for facial features
        video_results = analyze_video_facial_features(video_path)
        
        # Combine with audio analysis if available
        combined_results = {
            "video_analysis": video_results,
            "audio_analysis": {
                "transcript": audio_transcript,
                "tone": audio_tone
            } if audio_transcript or audio_tone else None
        }
        
        # Create overall assessment
        if "error" not in video_results:
            overall_emotion = video_results.get("overall_prediction")
            video_confidence = video_results.get("avg_confidence", 0)
            
            # If we have audio tone, try to combine insights
            if audio_tone and overall_emotion:
                combined_results["multimodal_analysis"] = {
                    "visual_emotion": overall_emotion,
                    "audio_tone": audio_tone,
                    "visual_confidence": video_confidence,
                    "analysis": f"Visual analysis detected {overall_emotion} with {video_confidence:.2f} confidence, while audio shows {audio_tone} tone."
                }
        
        return combined_results
        
    except Exception as e:
        print(f"Error in multimodal analysis: {e}")
        return {"error": f"Multimodal analysis failed: {str(e)}"}