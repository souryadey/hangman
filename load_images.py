import os


image_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
image_files = [f for f in os.listdir(image_directory) if f.startswith('h') and f.endswith('.png')]
image_files.sort(key = lambda f: int(os.path.splitext(f)[0][1:]))
image_files = [os.path.join(image_directory,f) for f in image_files]

IMAGE_FILES = image_files[:]