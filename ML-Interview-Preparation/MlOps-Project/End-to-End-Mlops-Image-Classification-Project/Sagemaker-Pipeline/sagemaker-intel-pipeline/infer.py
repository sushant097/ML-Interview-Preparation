import io
import logging
import numpy as np
import torch
import torchvision
import torchvision.transforms as T
import torch.nn.functional as F

import json
import os
from alibi_detect.cd import MMDDriftOnline
from utils import extract_model, download_file_from_s3, extract_archive

device = "cuda" if torch.cuda.is_available() else "cpu"

transform = T.Compose([T.ToPILImage(),
                       T.Resize((224, 224)),
                       T.ToTensor(),
                       T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

idx_to_class = {
    0: 'buildings', 1: 'forest', 2: 'glacier', 3: 'mountain', 4: 'sea', 5: 'street'
}


def stream_intel(dataset_dir: str = None):
    transform = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

    train_dataset = torchvision.datasets.ImageFolder(root=dataset_dir, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=1)
    ds_iter = iter(train_loader)

    while True:
        try:
            img = next(ds_iter)[0][0]
        except Exception:
            ds_iter = iter(train_loader)
            img = next(ds_iter)[0][0]
        yield img.numpy()


bucket_name = 'sagemaker-us-east-1-input-data'
file_name = 'mini_dataset.zip'
dataset_dir = "mini_dataset"

file_dir = "/tmp"
# download and extract zip dataset
download_file_from_s3(bucket_name, file_name)
logging.info("::Files and Folders in current directory:: {}".format(os.listdir(f"{file_dir}/")))
# dataset is extracted in the path name "{model_dir}/mini_dataset"
# inside mini_dataset -> six folders of each class
extract_archive(
    from_path=f"{file_dir}/" + file_name,
    to_path=None  # extract on same folder where zip file downloaded
)

# print("::Files and Folders in current directory::")
logging.info("::Files and Folders in current directory:: {}".format(os.listdir(f"{file_dir}/")))
# print(os.listdir())
dataset_dir = f"{file_dir}/{dataset_dir}/"
logging.info(f"Initializing reference dataset:: {dataset_dir}")
N = 50  # size of reference set
stream_i = stream_intel(dataset_dir=dataset_dir)
x_ref = np.stack([next(stream_i) for _ in range(N)], axis=0)
ERT = 150  # expected run-time in absence of change
W = 2  # size of test window

# fit for drift detection for N samples
logging.info("::Fiting for drift detection on reference samples::")
dd = MMDDriftOnline(x_ref, ERT, W, backend='pytorch')


# load model
def model_fn(model_dir):
    model = torch.jit.load(f"{model_dir}/model.scripted.pt")

    model.to(device).eval()

    return model


# data preprocessing
def input_fn(request_body, request_content_type):
    assert request_content_type == "application/json"
    data = json.loads(request_body)["inputs"]
    data = transform(np.array(data).astype(np.uint8)).unsqueeze(0).to(device)
    return data


# inference
def predict_fn(input_object, model):
    with torch.no_grad():
        prediction = model(input_object)
        prediction = F.softmax(prediction, dim=1)

    confidences, cat_ids = torch.topk(prediction, 5)
    outputs = {
        idx_to_class[idx.item()]: c.item() for c, idx in zip(confidences[0], cat_ids[0])
    }
    logging.info("::Model Output:: {}".format(outputs))

    ######### DRIFT DETECTION #################
    # image with no batch dimension ; [1, C, H, W] => [C, H, W]
    input_object = input_object.squeeze(0)
    logging.info("Shape after squeeze: {}".format(input_object.shape))
    drift_preds = dd.predict(np.array(input_object), return_test_stat=True)
    print("####################################################################")
    logging.info("::Dift statistics:: {} ".format(drift_preds))
    print("::Dift statistics:: {} ".format(drift_preds))
    print("####################################################################")
    # return outputs
    return outputs


# postprocess
def output_fn(outputs, content_type):
    assert content_type == "application/json"
    # Print top categories per image
    return outputs
