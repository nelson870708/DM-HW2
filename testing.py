import os
import pickle

import pandas as pd
import torch
from PIL import Image
from torch import nn
from torchvision import models, transforms

n_classes = 6
input_size = 224
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = models.resnet18(pretrained=False)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, n_classes)
model.load_state_dict(torch.load('./model/ResNet18v4'))
model.to(device)
model.eval()

data_transforms = transforms.Compose([
  transforms.Resize(256),
  transforms.CenterCrop(224),
  transforms.ToTensor(),
  transforms.Normalize([0.5, 0.5, 0.5], [0.25, 0.25, 0.25]),
])

def load_obj(dic_name):
  with open(dic_name + '.pkl', 'rb') as f:
    return pickle.load(f)

class_dict = load_obj('dict_4')
inv_class_dict = {v: k for k, v in class_dict.items()}

pred_list = []
id_list = []
for root, dirs, files in os.walk("./test_input", topdown=True):
  for name in files:
    img = Image.open(os.path.join(root, name))
    img_rgb = img.convert('RGB')
    x_test = data_transforms(img_rgb).to(device)
    x_test.unsqueeze_(0)  # Add batch dimension
    output = model(x_test)
    pred = torch.argmax(output, 1)
    class_pred = inv_class_dict[pred.cpu().numpy()[0]]
    id_list.append(name)
    pred_list.append(class_pred)
id_list = [img_id.split('.')[0] for img_id in id_list]

dic = {
  'id': id_list,
  'label': pred_list
}
df = pd.DataFrame(dic)
df.to_excel('submission.xlsx', index=False, header=False)
