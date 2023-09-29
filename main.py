import os
import whisper
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
from pydub import AudioSegment


def get_user_input():
    try:
        video_path = input("Enter the path to the video file: ")
        audio_path = input("Enter the path to the audio file: ")
        output_folder = input("Enter the path to the folder where the output file will be placed: ")
        srt_file = input("Enter the path for the output SRT subtitle file: ")

        return video_path, audio_path, output_folder, srt_file
    except KeyboardInterrupt:
        print("\nUser interrupted the input. Exiting.")
        exit(1)


def combine_video_audio(video_path, audio_path, output_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    except Exception as e:
        print(f"Error combining video and audio: {str(e)}")
        exit(1)


import os
import speech_recognition as sr
from pydub import AudioSegment


def convert_audio_to_wav(input_audio_path, output_wav_path):
    print(input_audio_path)
    try:
        if input_audio_path.lower().endswith((".mp3", ".ogg")):
            audio = AudioSegment.from_file(input_audio_path)
            audio.export(output_wav_path, format="wav")
            return output_wav_path
        elif input_audio_path.lower().endswith(".wav"):
            # If the input audio is already in WAV format, no conversion is needed.
            return input_audio_path
        else:
            raise ValueError("Unsupported audio format. Please provide an mp3, ogg, or wav file.")

    except Exception as e:
        print(f"Error in audio conversion: {str(e)}")
        exit(1)


def create_subtitle_srt(audio_path, srt_file_path):
    try:
        # Initialize the recognizer
        recognizer = sr.Recognizer()
        combined_srt_file_path = os.path.join(srt_file_path, 'subtitles.srt')

        # Convert the audio to WAV if needed
        audio_path = convert_audio_to_wav(audio_path, os.path.join(srt_file_path, 'converted_audio.wav'))

        # Load the audio file
        audio_file = sr.AudioFile(audio_path)

        # Transcribe audio using Google Web Speech API
        with audio_file as source:
            audio_data = recognizer.record(source)

        # Perform speech recognition
        transcript = recognizer.recognize_google(audio_data)

        # Create SRT subtitle file with accurate timing
        with open(combined_srt_file_path, 'w') as srt_file:
            # Split the transcript into lines of 30 characters (adjust as needed)
            lines = [transcript[i:i + 30] for i in range(0, len(transcript), 30)]

            # Write subtitles with incremental timestamps
            for i, line in enumerate(lines):
                start_time = i * 5  # Adjust the timing as needed (5 seconds per subtitle)
                end_time = (i + 1) * 5  # Adjust the timing as needed (5 seconds per subtitle)

                srt_file.write(f"{i + 1}\n")
                srt_file.write(
                    f"{start_time:02d}:{start_time % 60:02d},000 --> {end_time:02d}:{end_time % 60:02d},000\n")
                srt_file.write(f"{line}\n\n")

        print(f"SRT subtitle file saved as {combined_srt_file_path}")

    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error in audio transcription or subtitle creation: {str(e)}")
        exit(1)


# Example usage:
# audio_path = "your_audio_file.mp3"
# srt_file_path = "output_directory"
# create_subtitle_srt(audio_path, srt_file_path


def main():
    try:
        video_path, audio_path, output_folder, srt_file = get_user_input()

        # Ensure the output folder exists
        # os.makedirs(output_folder, exist_ok=True)

        # output_file_path = os.path.join(output_folder, "combined_video.mp4")
        # combine_video_audio(video_path, audio_path, output_file_path)
        # print(f"Combined video saved as {output_file_path}")

        # Transcribe the audio using AssemblyAI

        # Create SRT subtitle file with accurate timing
        create_subtitle_srt(audio_path, srt_file)
        print(f"SRT subtitle file saved as {srt_file}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
