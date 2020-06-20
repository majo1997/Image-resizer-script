import os
from pathlib import Path
from PIL import Image
import piexif

class Resizer:
	#init basic parameters
	def __init__(self, max_size_length, dir=None, filename_tag=None):
		self.max_size_length = max_size_length
		self.dir = dir
		self.filename_tag = filename_tag # suffix
			
	def resizeAll(self, path):
		for filename in os.listdir(path):
			file_path = os.path.join(path, filename)
	
			self.resize_image(file_path)
			
	def resize_image(self, file_path):
		try:
			image = Image.open(file_path)
			exif_dict = piexif.load(file_path)
			exif_bytes = piexif.dump(exif_dict)
			
			width, height = self.new_lengths(image)
			
			if self.dir and not self.dir_exist(file_path):
				self.create_directory(file_path)
			
			#print(exif_dict)
			#print(image.width)
			#print(image.height)
			#print(file_path)

			new_file_path = self.get_new_path(file_path)
			
			print('Resizing:', file_path, 'into', new_file_path)
			image = image.resize((width, height), Image.ANTIALIAS)
			image.save(new_file_path, exif=exif_bytes)
		
		except OSError: pass	# not an image
		
	def new_lengths(self, image):
		width = image.width
		height = image.height
		
		if width > height:
			new_width = self.max_size_length
			ratio = width / new_width
			new_height = int(height / ratio)
		else:
			new_height = self.max_size_length
			ratio = height / new_height
			new_width = int(width / ratio)
		
		return new_width, new_height
		
	def dir_exist(self, path):
		dir_path = os.path.split(path)[0]
		if self.dir:
			dir_path = os.path.join(dir_path, self.dir)
		return os.path.isdir(dir_path)
		
	def create_directory(self, path):
		path = os.path.split(path)[0]
		dir_path = os.path.join(path, self.dir)
		os.mkdir(dir_path)
		
	def get_new_path(self, path):
		path, filename = os.path.split(path)[0], os.path.split(path)[1]
		
		if self.filename_tag:
			filename_list = list(os.path.splitext(filename))
			filename_list.insert(1, self.filename_tag)
			filename = ''.join(filename_list)
		
		if self.dir:
			path = os.path.join(path, self.dir)
		
		new_path = os.path.join(path, filename)
		
		return new_path
	
if __name__ == '__main__':
	path = os.getcwd()
	resizer = Resizer(1920, filename_tag='ccc', dir='ccd') # use dash for better filename tag
	
	resizer.resizeAll(path)

