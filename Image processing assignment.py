import os
import cv2
import numpy as np
import random

# Class definition for Image Category
class ImageCategory:
    def __init__(self, category_name, image_paths):
        self.category_name = category_name
        self.image_paths = image_paths

    # Function to load and convert an image to grayscale
    def load_image(self, image_path):
        print(f"Loading image: {image_path}")  # Debugging
        if not os.path.isfile(image_path):
            print(f"Error: File does not exist {image_path}")
            return None, None
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to load image {image_path}")
            return None, None
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image, gray_image

    # Function to calculate texture using Laplacian of Gaussian (LoG)
    def calculate_texture(self, image):
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        texture = np.var(laplacian)  # Calculate variance as a measure of texture
        return texture

    # Function to randomly select an image from the category
    def get_random_image(self):
        random_image_path = random.choice(self.image_paths)
        return random_image_path

    # Function to compare two textures
    def compare_textures(self, texture1, texture2, threshold=0.1):
        return abs(texture1 - texture2) < threshold


# Defining absolute image paths for each category
base_path = "C:/Users/win 10/PycharmProjects/IP/"  # Base path for your images
cheetah_images = [os.path.join(base_path, f"cheeta{i}.jfif") for i in range(1, 6)]
tiger_images = [os.path.join(base_path, f"tiger{i}.jfif") for i in range(1, 6)]
lion_images = [os.path.join(base_path, f"lion{i}.jfif") for i in range(1, 6)]

# Create instances of ImageCategory class for each category
cheetah_category = ImageCategory("Cheetah", cheetah_images)
tiger_category = ImageCategory("Tiger", tiger_images)
lion_category = ImageCategory("Lion", lion_images)

# Randomly select images from two categories (Cheetah and Tiger in this case)
image1_path = cheetah_category.get_random_image()
image2_path = tiger_category.get_random_image()

# Load the images and calculate their textures
image1, gray_image1 = cheetah_category.load_image(image1_path)
image2, gray_image2 = tiger_category.load_image(image2_path)

# Check if images were loaded properly
if image1 is None or image2 is None:
    print("One or both images could not be loaded. Exiting...")
else:
    texture1 = cheetah_category.calculate_texture(gray_image1)
    texture2 = tiger_category.calculate_texture(gray_image2)

    print(f"Texture of Image 1 (Cheetah): {texture1}")
    print(f"Texture of Image 2 (Tiger): {texture2}")

    # Compare textures
    if cheetah_category.compare_textures(texture1, texture2):
        print("Texture match found!")
    else:
        print("Textures do not match!")

    # Display both images regardless of match
    cv2.imshow("Image 1 (Cheetah)", image1)
    cv2.imshow("Image 2 (Tiger)", image2)

    # Wait for a key press and close windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()