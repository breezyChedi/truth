from PIL import Image, ImageDraw
import numpy as np
import json
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

def average_color(image, polygon):
    np_image = np.array(image)
    mask = Image.new('L', (image.width, image.height), 0)
    ImageDraw.Draw(mask).polygon(polygon, outline=1, fill=1)
    np_mask = np.array(mask)

    pixels = np_image[np_mask == 1]
    if len(pixels) == 0:
        return (0, 0, 0)  # Avoid division by zero if no pixels are within the polygon

    return tuple(np.mean(pixels, axis=0).astype(int))

def create_sub_image(image, polygon, avg_color):
    min_x, min_y, max_x, max_y = polygon.bounds
    original_sub_image = image.crop((int(min_x), int(min_y), int(max_x), int(max_y)))

    mask_width = int(max_x - min_x)
    mask_height = int(max_y - min_y)
    mask = Image.new('L', (mask_width, mask_height), 0)
    polygon_shifted = [(x - min_x, y - min_y) for x, y in polygon.exterior.coords]
    ImageDraw.Draw(mask).polygon(polygon_shifted, outline=1, fill=255)

    np_original_sub_image = np.array(original_sub_image)
    np_mask = np.array(mask)

    # Ensure dimensions match for padding
    pad_y = max(0, np_mask.shape[0] - np_original_sub_image.shape[0])
    pad_x = max(0, np_mask.shape[1] - np_original_sub_image.shape[1])
    np_original_sub_image = np.pad(np_original_sub_image, ((0, pad_y), (0, pad_x), (0, 0)), mode='constant', constant_values=0)

    pad_y = max(0, np_original_sub_image.shape[0] - np_mask.shape[0])
    pad_x = max(0, np_original_sub_image.shape[1] - np_mask.shape[1])
    np_mask = np.pad(np_mask, ((0, pad_y), (0, pad_x)), mode='constant', constant_values=0)


    for i in range(3):
        np_original_sub_image[..., i] = np.where(np_mask == 255, np_original_sub_image[..., i], avg_color[i])

    sub_image = Image.fromarray(np_original_sub_image)
    return sub_image

def create_sub_images(image_path, merged_boxes_path, output_dir):
    # Load merged bounding boxes from JSON
    with open(merged_boxes_path) as f:
        merged_boxes_data = json.load(f)

    image = Image.open(image_path)

    for box_data in merged_boxes_data:
        class_id = box_data["class_id"]
        points = box_data["points"]
        points_flat = [coord for sublist in points for coord in sublist]

        if len(points_flat) % 2 != 0:
            print("Error: Points list does not contain pairs of coordinates\n",points,"\n\n")
            continue  # Skip this bounding box data and move to the next one
        

        

# Create a Polygon using the flattened list of coordinates
        polygon = Polygon([(points_flat[i], points_flat[i + 1]) for i in range(0, len(points_flat), 2)])
        # Convert points to polygon
        #polygon = Polygon([(points[i], points[i+1]) for i in range(0, len(points), 2)])
        
        # Get bounding box coordinates
        min_x, min_y, max_x, max_y = polygon.bounds
        bounding_box = (int(min_x), int(min_y), int(max_x), int(max_y))
        
        # Crop sub-image using bounding box
        sub_image = image.crop(bounding_box)
        
        # Save sub-image
        sub_image.save(f"{output_dir}/sub_image_{class_id}.png")

# Load merged bounding boxes from JSON
with open('4pred/merged_bounding_boxes.json') as f:
    merged_bounding_boxes = json.load(f)

image_path = '4pred/chem.png'
image = Image.open(image_path)

# Convert merged bounding boxes to shapely Polygons
merged_polygons = [{"class_id": box["class_id"], "polygon": Polygon(box["points"])} for box in merged_bounding_boxes]

# Process each merged bounding box and create sub-images
for poly in merged_polygons:
    avg_color = average_color(image, poly["polygon"].exterior.coords)
    sub_image = create_sub_images(image_path, '4pred/merged_bounding_boxes.json','4pred/subimgs')
  #  sub_image.save(f'4pred/sub_image_{poly["class_id"]}.png')
