from google.colab import drive
drive.mount('/content/drive')

#To remove duplicate and corrupt images

import os
import hashlib
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Define dataset path
dataset_path = "/content/drive/MyDrive/Dataset/Maize"  # Change to your dataset location

# Verify dataset structure
print("Classes found:", os.listdir(dataset_path))

# Initialize variables
corrupt_images = []
image_hashes = {}
duplicates = []
image_size = (224, 224)  # Resize all images to this size

# Process each class folder
for class_folder in os.listdir(dataset_path):
    class_path = os.path.join(dataset_path, class_folder)

    if os.path.isdir(class_path):  # Ensure it's a directory
        print(f"Processing class: {class_folder}...")

        for img_file in os.listdir(class_path):
            img_path = os.path.join(class_path, img_file)

            # Check if the file still exists before processing
            if not os.path.exists(img_path):
                continue  # Skip missing files

            try:
                # Open image
                with Image.open(img_path) as img:
                    img.verify()  # Check if it's corrupt

                # Check for duplicate images using hashing
                with open(img_path, 'rb') as f:
                    img_hash = hashlib.md5(f.read()).hexdigest()

                if img_hash in image_hashes:
                    duplicates.append(img_path)
                    os.remove(img_path)  # Delete duplicate
                else:
                    image_hashes[img_hash] = img_path

                # Resize image to standard size (only if it still exists)
                if os.path.exists(img_path):
                    img = Image.open(img_path).resize(image_size)
                    img.save(img_path)  # Overwrite with resized image

            except Exception as e:
                corrupt_images.append(img_path)
                if os.path.exists(img_path):  # Only delete if the file still exists
                    os.remove(img_path)

# Summary of cleaning
print(f"Removed {len(corrupt_images)} corrupt images.")
print(f"Removed {len(duplicates)} duplicate images.")

# Class distribution check
class_counts = {class_folder: len(os.listdir(os.path.join(dataset_path, class_folder)))
                for class_folder in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, class_folder))}

# Plot distribution
plt.figure(figsize=(10, 5))
plt.bar(class_counts.keys(), class_counts.values(), color='blue')
plt.xticks(rotation=45)
plt.xlabel("Classes")
plt.ylabel("Number of Images")
plt.title("Class Distribution")
plt.show()

print("✅ Data cleaning complete!")


#To remove blurry images

import os
import cv2
import numpy as np
from PIL import Image
from google.colab import drive



# Define dataset path
dataset_path = "/content/drive/MyDrive/Dataset/Maize"  # Change to your dataset path

# Set blur detection threshold
blur_threshold = 100.0  # Adjust if needed
blurry_images = []

# Process each class folder
for class_folder in os.listdir(dataset_path):
    class_path = os.path.join(dataset_path, class_folder)

    if os.path.isdir(class_path):  # Ensure it's a directory
        print(f"Processing class: {class_folder}...")

        for img_file in os.listdir(class_path):
            img_path = os.path.join(class_path, img_file)

            # Skip if file is missing
            if not os.path.exists(img_path):
                continue

            try:
                # Convert image to grayscale
                image_cv = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if image_cv is not None:
                    # Compute Laplacian variance (sharpness measure)
                    laplacian_var = cv2.Laplacian(image_cv, cv2.CV_64F).var()

                    # If variance is below threshold, delete the image
                    if laplacian_var < blur_threshold:
                        blurry_images.append(img_path)
                        os.remove(img_path)  # Delete blurry image

            except Exception as e:
                print(f"Error processing {img_path}: {e}")

# Summary
print(f"Removed {len(blurry_images)} blurry images.")
print("✅ Blurry image removal complete!")


#To check the classes and data in it after data cleaning

import os
import matplotlib.pyplot as plt
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Define dataset path
dataset_path = "/content/drive/MyDrive/Dataset/Maize"  # Change to your dataset path

# Dictionary to store class counts
class_counts = {}

# Loop through class folders
for class_folder in os.listdir(dataset_path):
    class_path = os.path.join(dataset_path, class_folder)

    if os.path.isdir(class_path):  # Ensure it's a directory
        num_images = len([f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))])
        class_counts[class_folder] = num_images

# Print class-wise image count
print("📊 Number of images per class:")
for class_name, count in class_counts.items():
    print(f"{class_name}: {count} images")

# Plot distribution
plt.figure(figsize=(10, 5))
plt.bar(class_counts.keys(), class_counts.values(), color='blue')
plt.xticks(rotation=45)
plt.xlabel("Classes")
plt.ylabel("Number of Images")
plt.title("Class Distribution")
plt.show()
