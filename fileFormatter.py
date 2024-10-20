import os, time
from datetime import datetime, timedelta
import imageio
from PIL import Image
import re

# Check TimeZone !! When Travle in Abroad
TIME_DIFFENCY=0

def get_taken_datetime(file_path):
    # Function to extract taken date and time from EXIF information
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data and 36867 in exif_data:  # 36867 corresponds to DateTimeOriginal
                taken_datetime = datetime.strptime(exif_data[36867], "%Y:%m:%d %H:%M:%S")
                return taken_datetime + timedelta(hours=TIME_DIFFENCY)
    except (OSError, Image.UnidentifiedImageError):
        pass

    # If EXIF information is not available, use file modification time
    return "00000000"# datetime.fromtimestamp(os.path.getmtime(file_path))

def get_date_encoded(file_path):
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data and 306 in exif_data:  # 306 corresponds to Date Time Digitized
                date_encoded = exif_data[306]
                return date_encoded + timedelta(hours=TIME_DIFFENCY)
    except (OSError, Image.UnidentifiedImageError):
        pass
    return datetime.fromtimestamp(os.path.getmtime(file_path)) + timedelta(hours=TIME_DIFFENCY)

def get_unique_file_path(destination_folder, new_file_name):
    # Function to get a unique file path by appending "-n" if the file name already exists
    base_name, extension = os.path.splitext(new_file_name)
    counter = 1

    while os.path.exists(os.path.join(destination_folder, new_file_name)):
        new_file_name = f"{base_name}-{counter}{extension}"
        counter += 1

    return os.path.join(destination_folder, new_file_name)

def rename_file(file_path, format_info):
    # Function to rename the file based on given format rules
    taken_datetime = get_taken_datetime(file_path)
    print("taken date time: ", taken_datetime)
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    file_extension = file_extension[1:].lower()  # Remove the dot and convert to lowercase
    destination_folder = os.path.dirname(file_path)

    image_formats = format_info["Image format list"]
    video_formats = format_info["Video format list"]

    if file_extension in image_formats:
        new_format = "jpg"
    elif file_extension in video_formats:
        new_format = "mp4"
    else:
        return  # Skip files with unsupported formats
    
    if taken_datetime != "00000000":
        taken_date = taken_datetime.strftime("%Y%m%d")
        taken_time = taken_datetime.strftime("%H%M%S")
        new_file_name = f"{taken_date}_{taken_time}.{new_format}"
        new_file_path = get_unique_file_path(destination_folder, new_file_name)
        os.rename(file_path, new_file_path)
    else:
        new_file_name = f"{file_name}.{new_format}"
        date_encoded = get_date_encoded(file_path)
        print("date_encoded: ", date_encoded)
        if date_encoded != "00000000":
            encoded_date = datetime.strftime(date_encoded, "%Y%m%d")
            encoded_time = datetime.strftime(date_encoded, "%H%M%S")
            new_file_name = f"{encoded_date}_{encoded_time}.{new_format}"
        os.rename(file_path, os.path.join(destination_folder, new_file_name))

    print(f"Renamed: {file_path} to {new_file_name}")

def rename_dji_file(file_path, format_info):
    # Extract date and time information using regular expression
    match = re.search(r'DJI_(\d{8})_(\d{6})', file_path)
    
    file_name, file_extension = os.path.splitext(file_path)
    file_extension = file_extension[1:].lower()  # Remove the dot and convert to lowercase

    image_formats = format_info["Image format list"]
    video_formats = format_info["Video format list"]

    if file_extension in image_formats:
        new_format = "jpg"
    elif file_extension in video_formats:
        new_format = "mp4"
    else:
        return  # Skip files with unsupported formats
    
    if match:
        date_part = match.group(1)
        time_part = match.group(2)
        
        # Create the new file name
        new_file_name = f"{date_part}_{time_part}.{new_format}"
        
        # Get the destination folder and create the new file path
        destination_folder = os.path.dirname(file_path)
        new_file_path = os.path.join(destination_folder, new_file_name)
        
        # Rename the file
        os.rename(file_path, new_file_path)
        print(f"Renamed: {file_path} to {new_file_name}")
    else:
        print(f"Invalid file name format: {file_path}")

def process_folder(folder_path, format_info):
    # Function to process all files in the given folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            trigger_text = ["IMG_", "IMG-", "MVI_", "VID_", "Screenshot_", "VideoCapture_", "MDG_"]
            
            if any(trigger in file for trigger in trigger_text):
                rename_file(file_path, format_info)
            elif "DJI_" in file:
                rename_dji_file(file_path, format_info)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    # directory given
    folder_path = sys.argv[1]
    # directory of the running script
    # folder_path = os.path.dirname(os.path.abspath(__file__))
    format_info = {
        "Image format list": ["jpg", "jpeg", "heic", "png"],
        "Video format list": ["avi", "mp4", "mov", "hevc"]
    }

    process_folder(folder_path, format_info)
