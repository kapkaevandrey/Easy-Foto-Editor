import os

from PIL import Image, ImageFilter
from PIL.ImageQt import ImageQt


class ImageProcessor:
    def __init__(self):
        self.base_dir = None
        self.filename = None
        self.image = None
        self.images = []
        self.changed_dir = 'modified'
        self.size = 0
        self.head = 0

    def get_front(self, qt=True):
        if self.size == 0 or self.head == self.size - 1:
            return
        self.head += 1
        if qt:
            return ImageQt(self.images[self.head])
        return self.images[self.head]

    def get_back(self, qt=True):
        if self.size == 0 or self.head == 0:
            return
        self.head -= 1
        if qt:
            return ImageQt(self.images[self.head])
        return self.images[self.head]

    def get_image(self, qt=True):
        if self.size == 0:
            raise IndexError(f"{__name__} is empty.")
        if qt:
            return ImageQt(self.images[self.head])
        return self.images[self.head]

    def load_image(self, base_dir, filename):
        path_image = os.path.join(base_dir, filename)
        try:
            self.image = Image.open(path_image)
            self.image = self.image.convert("RGB")
        except:
            raise ValueError(f"Can't open image for path {self.image}")
        self.base_dir = base_dir
        self.filename = filename
        self.images.append(self.image)
        self.size += 1

    def save_image(self, path):
        self.images[self.head].save(f"{path}.png")

    def do_bw(self):
        current_image = self.images[self.head]
        self.images.append(current_image.convert('L'))
        self.head = self.size
        self.size += 1

    def rotate_mirror(self):
        current_image = self.images[self.head]
        self.images.append(current_image.transpose(Image.FLIP_LEFT_RIGHT))
        self.head = self.size
        self.size += 1

    def rotate_right(self):
        current_image = self.images[self.head]
        self.images.append(current_image.transpose(Image.ROTATE_90))
        self.head = self.size
        self.size += 1

    def rotate_left(self):
        current_image = self.images[self.head]
        self.images.append(current_image.transpose(Image.ROTATE_270))
        self.head = self.size
        self.size += 1

    def make_sharpness(self):
        current_image = self.images[self.head]
        self.images.append(current_image.filter(ImageFilter.SHARPEN))
        self.head = self.size
        self.size += 1

    def __str__(self):
        return f"Image {self.filename}"


class ImageManager:
    def __init__(self):
        self.image_processors = {}
        self.current_processor = None

    def get_or_create(self, base_dir, filename):
        image_path = os.path.join(base_dir, filename)
        if not os.path.isfile(image_path):
            raise ValueError(f"Wrong path {image_path}")
        file = open(image_path, "rb")
        image_processor = hash(file.read())
        if image_processor not in self.image_processors:
            proc = ImageProcessor()
            proc.load_image(base_dir, filename)
            self.image_processors[image_processor] = proc
        self.current_processor = self.image_processors[image_processor]
        return self.image_processors[image_processor]

