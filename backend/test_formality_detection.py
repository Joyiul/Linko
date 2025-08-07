#!/usr/bin/env python3
"""
Test script for formality detection system
Demonstrates different formality levels with explicit labeling
"""

from processing.formality_analysis import analyze_formality

def test_formality_detection():
    """Test formality detection with various text samples"""
    
    test_samples = [
        # Formal/Academic
        {
            "text": "I am writing to formally request your consideration regarding the aforementioned proposal. The comprehensive analysis demonstrates significant potential for implementation. I would be grateful for your feedback at your earliest convenience.",
            "expected": "formal"
        },
        
        # Professional/Business
        {
            "text": "Let's circle back on this initiative and drill down into the actionable items. We need to leverage our core competencies to optimize the deliverables and move the needle on our KPIs.",
            "expected": "professional"
        },
        
        # Informal/Conversational
        {
            "text": "Hey! How's it going? I was wondering if you could help me out with something. It's not a big deal, but I'd really appreciate it if you have time.",
            "expected": "informal"
        },
        
        # Casual/Slang
        {
            "text": "Yo bro, that party was absolutely lit! The vibes were immaculate and everyone was lowkey having the time of their lives. No cap, it was fire!",
            "expected": "casual"
        },
        
        # Neutral
        {
            "text": "The meeting is scheduled for 3 PM today. Please bring the required documents and arrive on time.",
            "expected": "neutral/formal"
        },
        
        # Mixed formality
        {
            "text": "I'm really excited about this opportunity! The research shows promising results, and I think we can totally make this work.",
            "expected": "mixed"
        }
    ]
    
    print("=== FORMALITY DETECTION TEST RESULTS ===\n")
    
    for i, sample in enumerate(test_samples, 1):
        print(f"TEST {i}: {sample['expected'].upper()} TEXT")
        print("-" * 50)
        print(f"Text: \"{sample['text']}\"\n")
        
        result = analyze_formality(sample['text'])
        
        print(f"🎯 DETECTED FORMALITY: {result['formality_level'].upper()}")
        print(f"📊 CONFIDENCE: {result['confidence']:.1%}")
        print(f"📝 SUMMARY: {result['summary']}\n")
        
        print("📋 DETAILED BREAKDOWN:")
        for category, percentage in result['details']['formality_distribution'].items():
            if percentage > 0:
                print(f"   • {category.title()}: {percentage}%")
        
        print("\n🔍 SPECIFIC INDICATORS FOUND:")
        for category, indicators in result['indicators'].items():
            if indicators:
                print(f"   {category.title()} ({len(indicators)}):")
                for indicator in indicators[:3]:  # Show first 3
                    print(f"     - {indicator}")
                if len(indicators) > 3:
                    print(f"     ... and {len(indicators) - 3} more")
        
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_formality_detection()
