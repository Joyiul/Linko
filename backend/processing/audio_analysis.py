def analyze_audio(transcript):
    # Placeholder logic
    if "sorry" in transcript.lower():
        return "Apologetic or Polite"
    elif "whatever" in transcript.lower():
        return "Dismissive or Irritated"
    return "Neutral"
