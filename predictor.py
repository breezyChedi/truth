from ultralytics import YOLO
import os
import json

# Load a pretrained YOLOv8n-cls Classify model
model = YOLO("runs/detect/train31/weights/best.pt")
cd = os.getcwd()

# Correct the path to the image
image_path = os.path.join(cd, "4pred", "chem.png")

# Verify the 4pred directory contents
pred_dir = os.path.join(cd, "4pred")
if not os.path.exists(pred_dir):
    raise FileNotFoundError(f"{pred_dir} directory does not exist")

# Check if the file exists
if not os.path.exists(image_path):
    raise FileNotFoundError(f"{image_path} does not exist")

# Run inference on the image
results = model.predict(image_path, save=True, imgsz=2560)  # results list

# Process results and save bounding box data
bounding_boxes = []
for r in results:
    if r.boxes is not None:
        for box in r.boxes:
            box_data = box.data[0].tolist()  # Convert tensor to list
            class_id = box_data[0]
            points = box_data[1:9]  # Extract the points
            bounding_boxes.append({
                "class_id": class_id,
                "points": points
            })

# Save bounding box data to a JSON file
output_file = os.path.join(pred_dir, "bounding_boxes.json")
with open(output_file, "w") as f:
    json.dump(bounding_boxes, f, indent=4)

print("Bounding box data saved to:", output_file)
