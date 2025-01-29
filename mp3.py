import whisper

# Function to extract text from an MP3 file using Whisper
def extract_text_from_mp3(mp3_file_path):
    # Load the Whisper model (you can choose 'base', 'small', 'medium', 'large' models)
    model = whisper.load_model("base")  # Use the "base" model for faster performance (or "large" for higher accuracy)
    
    # Transcribe the MP3 file
    result = model.transcribe(mp3_file_path)
    
    # Return the transcribed text directly
    return result['text']
