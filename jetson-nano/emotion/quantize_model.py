import torch
model = torch.load('weights/yolo.pt')
print(model.__doc__)