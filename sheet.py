import os
import sys
import argparse
from PIL import Image

def create_image_atlas(input_dir, output_dir, grid_size, atlas_size):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Calculate the size of each image in the grid
    image_size = atlas_size // grid_size

    # Create a new blank atlas image
    atlas = Image.new('RGBA', (atlas_size, atlas_size))

    # Get a list of images in the input directory
    images = [os.path.join(input_dir, img) for img in os.listdir(input_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Ensure we have enough images to fill the grid
    if len(images) < grid_size * grid_size:
        print(f"Warning: Not enough images to fill the {grid_size}x{grid_size} grid.")
    
    # Process the images and place them in the grid
    for index, image_path in enumerate(images[:grid_size * grid_size]):
        # Open and resize the image
        with Image.open(image_path) as img:
            img = img.resize((image_size, image_size))

            # Calculate the position to paste this image in the atlas
            row = index // grid_size
            col = index % grid_size
            x = col * image_size
            y = row * image_size

            # Paste the image into the atlas
            atlas.paste(img, (x, y))
    
    # Save the atlas image
    output_path = os.path.join(output_dir, 'atlas.png')
    atlas.save(output_path)
    print(f"Atlas saved to {output_path}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Generate a squared atlas from images in a grid.")
    parser.add_argument("grid_size", type=int, help="The number of rows and columns in the grid (e.g., 3 for 3x3).")
    parser.add_argument("atlas_size", type=int, help="The size of the final atlas image (e.g., 4096 for a 4096x4096 atlas).")

    # Parse arguments
    args = parser.parse_args()
    grid_size = args.grid_size
    atlas_size = args.atlas_size

    # Directories
    current_directory = os.path.dirname(__file__)  # Get the current directory where the script is located
    input_directory = os.path.join(current_directory, "input")
    output_directory = os.path.join(current_directory, "output")

    # Generate the atlas
    create_image_atlas(input_directory, output_directory, grid_size, atlas_size)
