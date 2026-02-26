"""scale_images.py

Scales images in a directory to a target width (default 680px), keeping
aspect ratio, and saves them with suffix "_scaled".

Usage: python scale_images.py [--dir DIR] [--width WIDTH] [--suffix SUFFIX] [--recursive]
"""

import os
import argparse
from PIL import Image, ImageOps


class ImageScaler:
	SUPPORTED_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

	def __init__(self, target_width=680, suffix='_scaled', recursive=False):
		self.target_width = int(target_width)
		self.suffix = suffix
		self.recursive = bool(recursive)

	@staticmethod
	def is_image_file(filename: str) -> bool:
		name = filename.lower()
		return any(name.endswith(ext) for ext in ImageScaler.SUPPORTED_EXT)

	def _scaled_path(self, src_path: str) -> str:
		dirpath, fname = os.path.split(src_path)
		name, ext = os.path.splitext(fname)
		return os.path.join(dirpath, f"{name}{self.suffix}{ext}")

	def scale_image(self, src_path: str, overwrite=False) -> str:
		if not self.is_image_file(src_path):
			raise ValueError(f"Unsupported image format: {src_path}")

		dst_path = self._scaled_path(src_path)
		if os.path.exists(dst_path) and not overwrite:
			return dst_path

		with Image.open(src_path) as im:
			im = ImageOps.exif_transpose(im)
			orig_w, orig_h = im.size
			if orig_w == 0:
				raise ValueError(f"Image has zero width: {src_path}")

			if orig_w == self.target_width:
				im_resized = im.copy()
			else:
				new_h = round((self.target_width * orig_h) / orig_w)
				im_resized = im.resize((self.target_width, new_h), Image.LANCZOS)

			save_kwargs = {}
			ext = os.path.splitext(dst_path)[1].lower()
			if ext in ('.jpg', '.jpeg'):
				save_kwargs['quality'] = 95
				if im_resized.mode in ('RGBA', 'LA'):
					background = Image.new('RGB', im_resized.size, (255, 255, 255))
					background.paste(im_resized, mask=im_resized.split()[-1])
					im_resized = background
				else:
					im_resized = im_resized.convert('RGB')

			im_resized.save(dst_path, **save_kwargs)
		return dst_path

	def process_directory(self, directory='.') -> list:
		directory = os.path.abspath(directory)
		processed = []

		if self.recursive:
			for root, _, files in os.walk(directory):
				for f in files:
					if self.suffix in f:
						continue
					if self.is_image_file(f):
						src = os.path.join(root, f)
						try:
							dst = self.scale_image(src)
							processed.append(dst)
						except Exception:
							continue
		else:
			for f in os.listdir(directory):
				if self.suffix in f:
					continue
				if self.is_image_file(f):
					src = os.path.join(directory, f)
					try:
						dst = self.scale_image(src)
						processed.append(dst)
					except Exception:
						continue

		return processed


def _build_parser():
	p = argparse.ArgumentParser(description='Scale images to a target width')
	p.add_argument('--dir', '-d', default='.', help='Directory to process')
	p.add_argument('--width', '-w', type=int, default=680, help='Target width in pixels')
	p.add_argument('--suffix', '-s', default='_scaled', help='Suffix for scaled files')
	p.add_argument('--recursive', '-r', action='store_true', help='Process directories recursively')
	return p


def main(argv=None):
	parser = _build_parser()
	args = parser.parse_args(argv)

	scaler = ImageScaler(target_width=args.width, suffix=args.suffix, recursive=args.recursive)
	processed = scaler.process_directory(args.dir)
	print(f"Processed {len(processed)} images")


if __name__ == '__main__':
	main()