from ultralytics import YOLO
# Load a model
import os
import torch

if __name__ == '__main__':    
    torch.cuda.empty_cache()
    print(torch.cuda.is_available())
    os.environ["CUDA_LAUNCH_BLOCKING"]="1"
    os.environ["CUDA_VISIBLE_DEVICES"]="0"
    model = YOLO("yolov8n.yaml")  
    model.to("cuda")
    #model_output = model(**encoded_input.to("cuda"))
    # build a new model from scratch
    #model = YOLO("best_8.pt")  # load a pretrained model (recommended for training)
    #model.to('cuda')
    # Use the model
    torch.cuda.memory_summary(device=None, abbreviated=False)
    results = model.train(data="data_config.yaml", epochs=15, imgsz=1280,verbose=True, batch=12)  # train the 
    torch.cuda.memory_summary(device=None, abbreviated=False)
    metrics = model.val()  # evaluate model performance on the validation set
    path = model.export(format='saved_model') 
    print(path)
    path = model.export(format="onnx") 
    print("\n",path)
#model.export(format="saved_model", opset=13, nms=True)
