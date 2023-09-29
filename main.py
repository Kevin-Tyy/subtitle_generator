import os
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr


def combine_video_audio(video_path, audio_path, output_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        print(f"Video and audio combined and saved as {output_path}")
    except Exception as e:
        print(f"Error combining video and audio: {str(e)}")


def transcribe_audio(audio_path):
    try:
        recognizer = sr.Recognizer()
        audio = sr.AudioFile(audio_path)
        with audio as source:
            audio_data = recognizer.record(source)
        transcript = recognizer.recognize_google(audio_data)
        return transcript
    except FileNotFoundError:
        print(f"Error: File not found - {audio_path}")
    except sr.UnknownValueError:
        print("Error: Unable to transcribe audio - UnknownValueError")
    except sr.RequestError as e:
        print(f"Error: Unable to transcribe audio - RequestError: {str(e)}")
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")


def create_subtitle_srt(transcript, srt_file_path):
    try:
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
        print(f"SRT subtitle file saved as {srt_file_path}")
    except Exception as e:
        print(f"Error creating SRT subtitle: {str(e)}")


def main():
    try:
        video_path = input("Enter the path to the video file: ")
        audio_path = input("Enter the path to the audio file: ")
        output_folder = input("Enter the path to the folder where the output file will be placed: ")
        srt_file = input("Enter the path for the output SRT subtitle file: ")

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        output_file_path = os.path.join(output_folder, "combined_video.mp4")
        combine_video_audio(video_path, audio_path, output_file_path)

        # Transcribe the audio
        transcript = transcribe_audio(audio_path)
        print("Transcription:")
        print(transcript)

        # Create SRT subtitle file
        create_subtitle_srt(transcript, srt_file)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
