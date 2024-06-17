import json
import os
from shapely.geometry import Polygon
from shapely.ops import unary_union

# Function to calculate the overlap area between two bounding boxes
def calculate_overlap_area(poly1, poly2):
    intersection = poly1.intersection(poly2)
    return intersection.area

# Function to merge overlapping bounding boxes
def merge_bounding_boxes(bounding_boxes, threshold=0.2):
    polygons = []
    for box in bounding_boxes:
        points = box["points"]
        if len(points) >= 4:  # Ensure there are at least 4 values to form a polygon
            # Assuming points contain (x1, y1, x2, y2, ...), we create a simple bounding box
            x1, y1, x2, y2 = points[:4]
            poly = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
            polygons.append({"class_id": box["class_id"], "polygon": poly})
        else:
            print(f"Skipping invalid bounding box with points: {points}")

    merged_polygons = []
    while polygons:
        base_poly = polygons.pop(0)
        merged = False
        for i, target_poly in enumerate(polygons):
            overlap_area = calculate_overlap_area(base_poly["polygon"], target_poly["polygon"])
            base_area = base_poly["polygon"].area
            if overlap_area / base_area >= threshold:
                merged_poly = unary_union([base_poly["polygon"], target_poly["polygon"]])
                polygons.pop(i)  # Remove the merged polygon
                polygons.append({"class_id": base_poly["class_id"], "polygon": merged_poly})
                merged = True
                break
        if not merged:
            merged_polygons.append(base_poly)

    # Append any remaining polygons that were not merged
    merged_polygons.extend(polygons)

    return merged_polygons

# Load bounding box data from JSON file
bounding_boxes_file = os.path.join("4pred", "bounding_boxes.json")
with open(bounding_boxes_file, "r") as f:
    bounding_boxes = json.load(f)

# Merge bounding boxes
merged_bounding_boxes = merge_bounding_boxes(bounding_boxes, threshold=0.2)

# Save merged bounding boxes to a new JSON file
output_file = os.path.join("4pred", "merged_bounding_boxes.json")
merged_data = []
for box in merged_bounding_boxes:
    merged_data.append({
        "class_id": box["class_id"],
        "points": list(box["polygon"].exterior.coords)
    })

with open(output_file, "w") as f:
    json.dump(merged_data, f, indent=4)

print("Merged bounding box data saved to:", output_file)
