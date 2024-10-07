import os
import shutil
from datetime import datetime
from PIL import Image, ExifTags
import tqdm


# Constants
SOURCE_DIR = '100CANON'  # Replace this with the path to your folder
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.webp']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mts', '.m2ts', '.3gp', '.m4v', '.mpg', '.mpeg']

def parse_date_string(date_str):
    """Parse a date string with multiple possible formats."""
    formats = [
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y:%m:%d %H:%M:%S'
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def get_file_date(filepath, file_type):
    """Get the creation date of a file."""
    if file_type == 'image':
        try:
            image = Image.open(filepath)
            exif_data = image._getexif()
            if exif_data:
                exif = {ExifTags.TAGS.get(k): v for k, v in exif_data.items() if k in ExifTags.TAGS}
                if 'DateTimeOriginal' in exif:
                    date_str = exif['DateTimeOriginal']
                    return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        except Exception as e:
            print(f"Error processing {file_type} {filepath}: {e}")
    return datetime.fromtimestamp(os.path.getmtime(filepath))

def create_directory(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def move_file(src_path, dest_path):
    """Move a file from the source path to the destination path."""
    shutil.move(src_path, dest_path)

def process_files(source_dir):
    """Process files in the source directory."""
    moved_files = 0
    total_files = len(os.listdir(source_dir))
    
    for filename in tqdm.tqdm(os.listdir(source_dir)):
        filepath = os.path.join(source_dir, filename)
        if not os.path.isfile(filepath):
            continue  # Skip if not a file

        ext = os.path.splitext(filename)[1].lower()

        if ext in IMAGE_EXTENSIONS:
            file_type = 'Pictures'
            date_taken = get_file_date(filepath, 'image')
        elif ext in VIDEO_EXTENSIONS:
            file_type = 'Videos'
            date_taken = get_file_date(filepath, 'video')
        else:
            print(f"Unsupported file type: {ext}")
            continue  # Skip if not an image or video

        date_folder_name = date_taken.strftime('%Y-%m-%d')
        date_folder_path = os.path.join(source_dir, date_folder_name)
        create_directory(date_folder_path)

        type_folder_path = os.path.join(date_folder_path, file_type)
        create_directory(type_folder_path)

        dest_path = os.path.join(type_folder_path, filename)
        move_file(filepath, dest_path)
        moved_files += 1

    print(f"Moved {moved_files} of {total_files} files.")

# Main program
if __name__ == '__main__':
    process_files(SOURCE_DIR)
