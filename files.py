import os
import random
from PIL import Image


class UniqueImagePaths:
    def __init__(self):
        self.downloads_folder = os.path.join(os.curdir, "test")
        self.supported_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".tiff",
            ".webp",
        ]
        self.image_paths = self.get_valid_paths()
        self.used_paths = set()

    def get_valid_paths(self):
        image_paths = []

        for root, dirs, files in os.walk(self.downloads_folder):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.splitext(file_path)[1].lower() in self.supported_extensions:
                    try:
                        img = Image.open(file_path)
                        img.close()
                        image_paths.append(file_path)
                    except (IOError, OSError):
                        # PIL couldn't open the file, likely not a valid image
                        pass

        return image_paths

    def get_unique_path(self):
        remaining_paths = [
            path for path in self.image_paths if path not in self.used_paths
        ]

        if not remaining_paths:
            raise StopIteration("All image paths have been used")

        unique_path = random.choice(remaining_paths)
        self.used_paths.add(unique_path)

        return unique_path


if __name__ == "__main__":
    # Example usage:
    image_paths_generator = UniqueImagePaths(10, 10)

    try:
        for _ in range(700):  # Change the number to the desired number of unique paths
            image_path = image_paths_generator.get_unique_path()
            print(image_path)
    except StopIteration:
        print("All image paths have been used.")
