import os
from PIL import Image, ImageSequence
import cv2

def convert_webp_to_mp4(webp_file, output_file, fps=30):
    img = Image.open(webp_file)
    frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
    if not frames:
        raise ValueError(f"Could not load frames from {webp_file}")
    
    frame = frames[0]
    frame = frame.convert('RGB')
    frame.save('temp.png')
    img = cv2.imread('temp.png')
    height, width, layers = img.shape
    size = (width, height)
    
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    
    for frame in frames:
        frame = frame.convert('RGB')
        frame.save('temp.png')
        img = cv2.imread('temp.png')
        img = cv2.resize(img, size)
        out.write(img)
    
    out.release()
    os.remove('temp.png')

# Path to the directory containing .webp files
input_dir = 'filtered_data'
output_dir = 'filtered_data_2'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith('.webp'):
        webp_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + '.mp4')
        convert_webp_to_mp4(webp_file, output_file)
        print(f"Converted {filename} to {os.path.splitext(filename)[0]}.mp4")

print("Conversion complete.")
