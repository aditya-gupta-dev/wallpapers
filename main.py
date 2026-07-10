import os 

folder = 'images'
files = os.listdir(folder)
readme_file_name = "README.md"
data = ''

for i, file in enumerate(files):
    path = f'{folder}/{file}'
    data += f'### {file} \n![wallpaper-{i}]({path})\n\n\n'

with open(readme_file_name, 'w') as f: 
    f.write(data)
