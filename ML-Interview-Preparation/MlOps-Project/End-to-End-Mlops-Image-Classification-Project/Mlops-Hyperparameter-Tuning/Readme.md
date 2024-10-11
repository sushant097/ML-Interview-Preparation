# Model Training Logging

## 1. Model Training & Logging

### 1.1 PyTorch lightning auto learning rate finder
* First `pl` learning rate finder is run to find the best learning rate of each models and optimzers.
* Second trained the model with new learning rate suggested by learning rate finder.

**Final learning rate dict:**
```python
{'regnetz_c16': {'ADAM': 0.0019054607179632484, 'SGD': 0.47863009232263803, 'RMS': 0.0005248074602497723}, 'resnet18': {'ADAM': 0.0003019951720402019, 'SGD': 0.030199517204020192, 'RMS': 0.0002089296130854041}, 'efficientnet_b0': {'ADAM': 0.0009120108393559097, 'SGD': 0.04365158322401657, 'RMS': 0.0005248074602497723}}
```

For figure and logs see this [notebook](notebook/1-optuna-hparam-tuning.ipynb)

**Tensorboard dev**
```
$ tensorboard dev upload --logdir lr_logs --name "Pytorch Lightning lr finder" --description "Trained model based on best lr suggest by lr_finder"
```
**Tensorboard Logs for pl learning rate finder: https://tensorboard.dev/experiment/T7FMeGy8S0asGVr9wzg3Lw/**

### 1.2 PyTorch lightning Training with best lr
* Trained with regnetz_c16 and logs it
* logs f1 score, precision, recall, confusion-matrix

**Tensorboard dev**
```
$ tensorboard dev upload --logdir logs \
    --name "My latest experiment - Model Training" \
    --description " Logging of different metrics, training on regnetz_c16"
```

**Tensorboard dev: https://tensorboard.dev/experiment/HMtbAgckTjmz1EWi3mJelQ/**

**Hyperparameters in `hparams.yaml`**
```
learning_rate: 1.2e-05
lr: 1.2e-05
model_name: regnetz_c16
num_classes: 6
optimizer_name: ADAM
```

For augmentation of Images I use random transformation like degree rotation, contrast increase and so on. It is detailed on following code:
```python
import torchvision.transforms as T

transforms1 = T.RandomApply(
            [
                T.RandomRotation(degrees=(0, 70)),
                T.RandomHorizontalFlip(p=0.5),
                T.ColorJitter(brightness=(0.1, 0.6), contrast=1, saturation=0, hue=0.3),
                T.GaussianBlur(kernel_size=(5, 9), sigma=(0.1, 5)),
                T.RandomHorizontalFlip(p=0.3),
            ], 
            p=0.3
        )
transforms = T.Compose([
                transforms1,
                T.Resize((224, 224)),
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
```

For confusion matrix in tensorboard logs [**Image not uploaded to tensorboard dev experiment**]:
![](files/confusion_matrix_1.gif)

### 2 - Optuna Hparam Search
**Tensorboard dev:   https://tensorboard.dev/experiment/74spvuyAQpCZnb3nK4MyJQ**

```python
Trail with : 

lr_rate:0.00011006008295331135 model name: resnet18 optimizer name: RMS
=========================================
Trail with : 

lr_rate:0.0003880858334105841 model name: resnet18 optimizer name: ADAM
=========================================
Study statistics: 
  Number of finished trials:  2
  Number of pruned trials:  0
  Number of complete trials:  2
Number of finished trials: 2
Best trial:
  Value: 0.921875
Trail with : 
  Params: 
    lr: 0.0003880858334105841
    model_name: resnet18
    optimizer: ADAM


Trail with : 

lr_rate:1.547691630918372e-05 model name: efficientnet_b0 optimizer name: SGD
=========================================
Trail with : 

lr_rate:0.00027665284312550367 model name: efficientnet_b0 optimizer name: RMS
=========================================

Study statistics: 
  Number of finished trials:  2
  Number of pruned trials:  0
  Number of complete trials:  2
Number of finished trials: 2
Best trial:
  Value: 0.734375
Trail with : 
  Params: 
    lr: 0.00027665284312550367
    model_name: efficientnet_b0
    optimizer: RMS
    
    
Trail with : 

lr_rate:2.1172144867677624e-05 model name: regnetz_c16 optimizer name: SGD
=========================================
Trail with : 

lr_rate:0.00012310173574776534 model name: regnetz_c16 optimizer name: ADAM
=========================================
# for more logs see notebook
Study statistics: 
  Number of finished trials:  2
  Number of pruned trials:  0
  Number of complete trials:  2
Number of finished trials: 2
Best trial:
  Value: 0.83203125
  
Params: 
    lr: 0.00012310173574776534
    model_name: regnetz_c16
    optimizer: ADAM
```

**For more do visit [notebook](notebook/1-optuna-hparam-tuning.ipynb)**