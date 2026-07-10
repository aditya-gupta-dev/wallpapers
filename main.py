import os 
import subprocess 
import concurrent

wallpaper_folder = 'images'
thumbnail_folder = 'thumbnails'
readme_file = 'README.md'
data = '# Wallpapers\n'
is_gen_thumbnail = True


if not os.path.exists(thumbnail_folder): 
    os.mkdir(thumbnail_folder)


def get_file_name(file: str) -> str: 
    return file.split('.')[0]


def generate_thumbnail(file: str): 
    file_name = get_file_name(file)

    command = [
        "ffmpeg",
        "-y", 
        "-i", f"{wallpaper_folder}/{file}",     
        "-vf", "scale=480:-1", 
        f"{thumbnail_folder}/thumbnail-{file_name}.jpg"        
    ]
    
    try: 
        subprocess.run(
            command,
            capture_output=True,
            check=True, 
            text=True
        )
    except subprocess.CalledProcessError as error: 
        print(f'failed to generate thumbnail: {file} {error}')
    finally: 
        print(f'completed image generation {file}')


files = os.listdir(wallpaper_folder)

if is_gen_thumbnail: 
    for file in files: 
        generate_thumbnail(file)

for i, file in enumerate(files): 
    file_name = get_file_name(file)
    thumbnail_path = f'{thumbnail_folder}/thumbnail-{file_name}.jpg'
    data += f'[{file_name}]({wallpaper_folder}/{file})\n\n![wallpaper-{i+1}]({thumbnail_path})\n\n\n'

with open(readme_file, 'w') as f: 
    f.write(data)


