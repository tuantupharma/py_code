import cv2
import os

def create_video(input_folder, image_pattern, fps):
    # Set the output video file path
    output_file = os.path.join(input_folder, "video.mp4")

    # Get the list of image files in the input folder
    image_files = sorted([f for f in os.listdir(input_folder) if f.startswith(image_pattern.split("#")[0])])

    # Read the first image to get its dimensions
    first_image_path = os.path.join(input_folder, image_files[0])
    first_image = cv2.imread(first_image_path)
    height, width, channels = first_image.shape

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Specify the video codec
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Iterate through the image files and write them to the video
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)
        video_writer.write(image)

    # Release the VideoWriter
    video_writer.release()

    print("Video creation completed!")
