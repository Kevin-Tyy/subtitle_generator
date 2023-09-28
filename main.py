import os
import openai
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr

# Constants
API_KEY = "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"

def get_user_input():
    video_path = input("Enter the path to the video file: ")
    audio_path = input("Enter the path to the audio file: ")
    output_folder = input("Enter the path to the folder where the output file will be placed: ")
    srt_file = input("Enter the path for the output SRT subtitle file: ")

    return video_path, audio_path, output_folder, srt_file

def combine_video_audio(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_path)
    with audio as source:
        audio_data = recognizer.record(source)
    transcript = recognizer.recognize_google(audio_data)  # You can choose a different recognizer, e.g., recognize_bing

    return transcript

def create_subtitle_srt(transcript, srt_file_path):
    subtitles = []
    lines = transcript.split('\n')
    current_time = 0
    subtitle_counter = 1

    with open(srt_file_path, 'w') as srt_file:
        for line in lines:
            srt_file.write(str(subtitle_counter) + '\n')
            srt_file.write("{:02d}:{:02d}:{:02d},000 --> {:02d}:{:02d}:{:02d},000\n".format(
                current_time // 3600, (current_time // 60) % 60, current_time % 60,
                (current_time + 5) // 3600, ((current_time + 5) // 60) % 60, (current_time + 5) % 60
            ))
            srt_file.write(line + '\n\n')
            current_time += 5
            subtitle_counter += 1

def main():
    video_path, audio_path, output_folder, srt_file = get_user_input()

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    output_file_path = os.path.join(output_folder, "combined_video.mp4")
    combine_video_audio(video_path, audio_path, output_file_path)
    print(f"Combined video saved as {output_file_path}")

    # Transcribe the audio
    transcript = transcribe_audio(audio_path)
    print("Transcription:")
    print(transcript)

    # Create SRT subtitle file
    create_subtitle_srt(transcript, srt_file)
    print(f"SRT subtitle file saved as {srt_file}")

if __name__ == "__main__":
    main()
