import subprocess
import whisper
import io

def extract_audio_and_transcribe(mkv_file, audio_track=0):
    """
    Extracts a specific audio track from an MKV file and transcribes it using Whisper.
    
    Args:
    - mkv_file (str): Path to the MKV file.
    - audio_track (int): Index of the audio track to extract (default is 0).

    Returns:
    - str: Transcribed text.
    """
    try:
        # Step 1: Extract audio using FFmpeg (in-memory stream)
        audio_data = subprocess.run(
            f'ffmpeg -i "{mkv_file}" -map 0:a:{audio_track} -ac 1 -ar 16000 -vn -f wav pipe:1',
            shell=True,
            check=True,
            stdout=subprocess.PIPE
        ).stdout

        # Step 2: Load Whisper model and transcribe audio
        model = whisper.load_model("base")  # Choose 'tiny', 'base', 'small', etc.
        
        # Whisper can take in bytes-like object (audio data)
        result = model.transcribe(io.BytesIO(audio_data))
        
        return result["text"]

    except Exception as e:
        return f"An error occurred: {e}"
