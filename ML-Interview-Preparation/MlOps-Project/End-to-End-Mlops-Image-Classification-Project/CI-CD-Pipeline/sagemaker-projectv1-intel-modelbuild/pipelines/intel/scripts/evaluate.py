from typing import Any, Dict, Optional, Tuple

import os
import subprocess
import torch
import timm
import json
import tarfile

import pytorch_lightning as pl
import torchvision.transforms as T
import torch.nn.functional as F

from pathlib import Path


from model import LitResnet
from dataset import IntelClassificationDataModule

ml_root = Path("/opt/ml")

model_artifacts = ml_root / "processing" / "model"
dataset_dir = ml_root / "processing" / "test"


def eval_model(trainer, model, datamodule):
    test_res = trainer.test(model, datamodule)[0]
    
    idx_to_class = {k: v for v,k in datamodule.data_train.class_to_idx.items()}
    model.idx_to_class = idx_to_class

    # calculating per class accuracy
    nb_classes = datamodule.num_classes

    confusion_matrix = torch.zeros(nb_classes, nb_classes)
    # acc_all = 0
    with torch.no_grad():
        for i, (images, targets) in enumerate(datamodule.test_dataloader()):
            # images = images.to(device)
            # targets = targets.to(device)
            outputs = model(images)
            # acc_all += (outputs == targets).sum()
            _, preds = torch.max(outputs, 1)
            for t, p in zip(targets.view(-1), preds.view(-1)):
                confusion_matrix[t.long(), p.long()] += 1
    """
    Simple Logic may be useful:
    acc = [0 for c in list_of_classes]
    for c in list_of_classes:
        acc[c] = ((preds == labels) * (labels == c)).float() / (max(labels == c).sum(), 1))
    """
    
    # acc_all = acc_all / len(datamodule.test_dataloader())

    accuracy_per_class = {
        idx_to_class[idx]: val.item() * 100 for idx, val in enumerate(confusion_matrix.diag() / confusion_matrix.sum(1))
    }
    print(accuracy_per_class)
    
    report_dict = {
        "multiclass_classification_metrics": {
            "accuracy": {
                "value": test_res["test/acc"],
                "standard_deviation": "0",
            },
            "confusion_matrix" : accuracy_per_class,
        },
    }

    eval_folder = ml_root / "processing" / "evaluation"
    eval_folder.mkdir(parents=True, exist_ok=True)
    
    out_path = eval_folder / "evaluation.json"
    
    print(f":: Writing to {out_path.absolute()}")
    
    with out_path.open("w") as f:
        f.write(json.dumps(report_dict))

        
if __name__ == '__main__':
    
    model_path = "/opt/ml/processing/model/model.tar.gz"
    with tarfile.open(model_path) as tar:
        tar.extractall(path=".")
    
    datamodule = IntelClassificationDataModule(
        train_data_dir=dataset_dir.absolute(),
        test_data_dir=dataset_dir.absolute(),
        num_workers=os.cpu_count()
        )
    datamodule.setup()

    model = LitResnet.load_from_checkpoint(checkpoint_path="last.ckpt")
    
    trainer = pl.Trainer(
        accelerator="auto",
    )
    
    print(":: Evaluating Model")
    eval_model(trainer, model, datamodule)