import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import ffmpeg

# Function to find all video files in a directory and its subdirectories
def find_video_files(directory):
    video_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm')):
                video_files.append(os.path.join(root, file))
    return video_files

# Function to split audio from video and save as mp3
def split_audio(video_file):
    audio_output = video_file.replace(os.path.splitext(video_file)[1], '.mp3')
    ffmpeg_extract_audio(video_file, audio_output, codec="mp3")

# Main function
if __name__ == "__main__":
    folder_path = "your_folder_path_here"  # Replace with the path to your folder
    
    video_files = find_video_files(folder_path)
    
    if not video_files:
        print("No video files found.")
    else:
        # Save the list of video paths and names to a text file
        with open('listvideo.txt', 'w') as file:
            for video_file in video_files:
                file.write(video_file + '\n')
        
        # Split audio from each video and save as mp3
        for video_file in video_files:
            split_audio(video_file)
    
    print("Task completed.")
