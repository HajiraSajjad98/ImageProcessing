import os
import cv2
import numpy as np
import random

# Class definition for Image Category
class ImageCategory:
    def __init__(self, category_name, image_paths):
        self.category_name = category_name
        self.image_paths = image_paths

    #  convert an image to grayscale
    def load_image(self, image_path):
        print(f"Loading image: {image_path}")  # Debugging
        if not os.path.isfile(image_path):
            print(f"Error: File  not exist {image_path}")
            return None, None
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to load image {image_path}")
            return None, None
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image, gray_image

    # calculate texture using Laplacian of Gaussian (LoG)
    def calculate_texture(self, image):
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        texture = np.var(laplacian)  # Calculate variance as a measure of texture
        return texture

    #  randomly select an image from the category
    def get_random_image(self):
        random_image_path = random.choice(self.image_paths)
        return random_image_path

    # compare two textures using absolute difference
    def compare_textures(self, texture1, texture2, threshold=0.1):
        distance = abs(texture1 - texture2)
        return distance < threshold, distance


# Defining absolute image paths for each category
base_path = "C:/Users/win 10/PycharmProjects/IP/"  # Base path for your images

# Combine images from all categories to one list
image_paths = []
image_paths.extend([os.path.join(base_path, f"cheeta{i}.jfif") for i in range(1, 6)])
image_paths.extend([os.path.join(base_path, f"tiger{i}.jfif") for i in range(1, 6)])
image_paths.extend([os.path.join(base_path, f"lion{i}.jfif") for i in range(1, 6)])

# Create a single instance of ImageCategory with all images
combined_category = ImageCategory("Combined", image_paths)

# Randomly select one image from the combined category
selected_image_path = combined_category.get_random_image()
selected_image, gray_selected_image = combined_category.load_image(selected_image_path)

# Check if the selected image was loaded properly
if selected_image is None:
    print("The selected image could not be loaded. Exiting...")
else:
    selected_texture = combined_category.calculate_texture(gray_selected_image)

    print(f"Texture of Selected Image: {selected_texture}")

    # Randomly select two more images from the combined category for comparison
    comparison_image1_path = combined_category.get_random_image()
    comparison_image2_path = combined_category.get_random_image()

    comparison_image1, gray_comparison_image1 = combined_category.load_image(comparison_image1_path)
    comparison_image2, gray_comparison_image2 = combined_category.load_image(comparison_image2_path)

    # Check if comparison images were loaded properly
    if comparison_image1 is None or comparison_image2 is None:
        print("One or both comparison images could not be loaded. Exiting...")
    else:
        texture_comparison1 = combined_category.calculate_texture(gray_comparison_image1)
        texture_comparison2 = combined_category.calculate_texture(gray_comparison_image2)

        print(f"Texture of Comparison Image 1: {texture_comparison1}")
        print(f"Texture of Comparison Image 2: {texture_comparison2}")

        # Compare textures with the selected image's texture
        match1, distance1 = combined_category.compare_textures(selected_texture, texture_comparison1)
        match2, distance2 = combined_category.compare_textures(selected_texture, texture_comparison2)

        # Output results for comparison with first image
        if match1:
            print("Texture match found with Comparison Image 1!")
            closest_match_info_1 = "Match found"
        else:
            print("Textures do not match with Comparison Image 1!")
            closest_match_info_1 = "No match"

        # Output results for comparison with second image
        if match2:
            print("Texture match found with Comparison Image 2!")
            closest_match_info_2 = "Match found"
        else:
            print("Textures do not match with Comparison Image 2!")
            closest_match_info_2 = "No match"

        # Display all three images regardless of matches
        cv2.imshow("Selected Image", selected_image)
        cv2.imshow("Comparison Image 1", comparison_image1)
        cv2.imshow("Comparison Image 2", comparison_image2)

        # Wait for a key press and close windows
        cv2.waitKey(0)
        cv2.destroyAllWindows()