import os 
import math 
import subprocess 
import concurrent.futures

wallpaper_folder = 'images'
thumbnail_folder = 'thumbnails'
readme_file = 'README.md'
data = '# Wallpapers\n'
is_gen_thumbnail = True 


if not os.path.exists(thumbnail_folder): 
    os.mkdir(thumbnail_folder)


def get_file_name(file: str) -> str: 
    return file.split('.')[0]


def chunk_generate_thumbnail(thread_id: int, files_chunk: list[str]) -> list[str]: 
    results = []

    for file in files_chunk:
        results.append(generate_thumbnail(thread_id, file))

    return results


def generate_thumbnail(thread_id:int, file: str) -> str: 
    tag = f'[image-gen-thread-{thread_id}]'
    file_name = get_file_name(file)
    output_file = f'{thumbnail_folder}/thumbnail-{file_name}.jpg'

    if os.path.exists(output_file): 
        return f'{tag} image already exists, skipping.[{file}] -> [{output_file}]'
        

    command = [
        "ffmpeg",
        "-y", 
        "-i", f"{wallpaper_folder}/{file}",     
        "-vf", "scale=480:-1", 
        f"{output_file}"        
    ]
    
    try: 
        subprocess.run(
            command,
            capture_output=True,
            check=True, 
            text=True
        )
    except subprocess.CalledProcessError as error: 
        return f'{tag}: [{file}] [{error}]'
     
    return f'{tag}: [{file}] -> [{output_file}]'


files = os.listdir(wallpaper_folder)

if is_gen_thumbnail: 
    
    futures = []
    workers_count = int((os.cpu_count() or 4) / 2) 
    chunk_size = math.ceil(len(files) / workers_count)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers_count) as thread_pool: 
    
        for i in range(workers_count):
            start = i * chunk_size
            stop = start + chunk_size
        
            chunk = files[start:stop]
    
            if not chunk:
                continue
            
            futures.append(thread_pool.submit(chunk_generate_thumbnail, i, chunk))
        
        for future in concurrent.futures.as_completed(futures): 
            for result in future.result(): 
                print(result)

for i, file in enumerate(files): 
    file_name = get_file_name(file)
    thumbnail_path = f'{thumbnail_folder}/thumbnail-{file_name}.jpg'
    data += f'[{file_name}]({wallpaper_folder}/{file})\n\n![wallpaper-{i+1}]({thumbnail_path})\n\n\n'

with open(readme_file, 'w') as f: 
    f.write(data)


