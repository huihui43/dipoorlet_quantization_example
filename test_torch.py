# test accuracy for the fp32 model

import torch, torchvision
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torchvision.datasets as datasets
import torch.utils.data as data
import torchvision.transforms as transforms
from torch.autograd import Variable
import torchvision.models as models
import matplotlib.pyplot as plt
import time, os, copy, numpy as np
from dataset import get_dataset
from tqdm import tqdm


model = torch.load("models/mobilev2_model.pth")

if isinstance(model,torch.nn.DataParallel):
    model = model.module


_, val_dataset, _ = get_dataset()
dataloaders = torch.utils.data.DataLoader(
    val_dataset, batch_size=32, shuffle=True, num_workers=4
)
running_corrects = 0.0
total_time = 0.
for i, (inputs, labels) in enumerate(dataloaders):

    print("process batch {}".format(i))
    inputs = inputs.cuda()
    labels = labels.cuda()
    t1 = time.time()
    outputs = model(inputs)
    total_time += time.time() - t1
    _, preds = torch.max(outputs, 1)
    running_corrects += torch.sum(preds == labels.data)

print(f"Accuracy : {running_corrects / len(val_dataset) * 100}%")
print("using {} seconds for single inference".format(total_time/len(val_dataset)))


# Accuracy : 67.7699966430664%


'''
# convert to onnx
if isinstance(model, torch.nn.DataParallel):
    model = model.module
x = torch.randn(1, 3, 224, 224).cuda()
# torch.onnx.export(
#     model, x, "models/rs18_model.onnx", export_params=True, opset_version=13
# )

torch.onnx.export(
    model, x, "models/mobilev2_model.onnx", export_params=True, opset_version=13
)
'''