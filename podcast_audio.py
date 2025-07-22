import edge_tts
import asyncio
from pydub import AudioSegment
import uuid
import os

SPEAKER_VOICE = {
    "sky": "en-IN-NeerjaNeural",
    "expert": "en-IN-PrabhatNeural"
}

async def generate_audio(script_path = "script.txt",output_path="audio.mp3"):
    print("Generating audio...")

    with open(script_path, "r" , encoding = "utf-8") as f:
        lines = f.readlines()

    temp_files = []

    # choosing voice
    for line in lines:
        print(f"\nRaw line: {repr(line)}")
        line = line.replace("\u200b", "").replace("\u00a0", "").strip() #removed unwanted and hidden characters

        if not line or ":" not in line: #not a dialogue
            print(f"Skipped: Not a dialogue → {line}") 
            continue

        speaker, text = line.split(":", 1) #splitting speaker and text
        speaker = speaker.strip().lower()
        text = text.strip()

        #print(f"Detected → Speaker: '{speaker}' | Text: '{text}'")

        if speaker not in SPEAKER_VOICE:
            print(f"Skipped: Unknown speaker → {speaker}")
            continue

        voice = SPEAKER_VOICE[speaker]
        print(f"{speaker.capitalize()} speaking: {text}")

        if text:
            print(f"{voice} speaking: {text}")
            audio_file = f"temp_{uuid.uuid4().hex}.mp3"  #unique temp file for each segment
            tts = edge_tts.Communicate(text=text, voice=voice)
            await tts.save(audio_file)
            temp_files.append(audio_file)

            # Add pause
            pause_file = f"pause_{uuid.uuid4().hex}.mp3"
            AudioSegment.silent(duration=1000).export(pause_file, format="mp3")
            temp_files.append(pause_file)

    if not temp_files:
        print("no voice files generated")
        return           
    
    print("Merging audio segments...")
    final = AudioSegment.empty()
    for file in temp_files:
        final += AudioSegment.from_mp3(file) #merging

    final.export(output_path, format="mp3")
    print(f"Podcast audio saved as {output_path}")

    # Clean up temp files
    for file in temp_files:
        os.remove(file)
        
"""if __name__ == "__main__":

    asyncio.run(generate_audio("podcast_script.txt"))      """