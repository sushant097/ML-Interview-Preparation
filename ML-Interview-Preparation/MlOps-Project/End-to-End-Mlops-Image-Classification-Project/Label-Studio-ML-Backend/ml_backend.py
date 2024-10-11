import io
import torch
import torchvision.transforms as T
import torch.nn.functional as F

from PIL import Image
import os
import boto3

import tarfile
from urllib.parse import urlparse

from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import get_single_tag_keys, get_choice, is_skipped

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


transform = T.Compose([T.Resize((224, 224)),
                       T.ToTensor(),
                       T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

idx_to_class = {
    0: 'buildings', 1: 'forest', 2: 'glacier', 3: 'mountain', 4: 'sea', 5: 'street'
}

# LOAD MODEL
model_dir = os.path.dirname(__file__)

image_cache_dir = os.path.join(model_dir, 'image-cache')
os.makedirs(image_cache_dir, exist_ok=True)


def get_model_bucket_key(s3_url):
    o = urlparse(s3_url)
    bucket = o.netloc
    key = o.path
    return bucket, key


def extract_model(model_s3_uri, extract_folder):
    s3 = boto3.client('s3')
    try:
        filename = model_dir + '/' + 'model.tar.gz'
        bucket, key = get_model_bucket_key(model_s3_uri)
        print("Bucket: {}, Key: {}".format(bucket, key))
        s3.download_file(bucket, key[1:], filename)

        tar = tarfile.open(filename)
        tar.extractall(extract_folder)
        print("All files in the directory after extracting:: {} ".format(os.listdir(extract_folder)))
        tar.close()
    except Exception as e:
        raise e


def get_image(image_s3_url):
    """
    Takes s3 url image and return PIL image
    Args:
        image_s3_url: s3 url of image [.jpg, .png]

    Returns: PIL format image
    """
    s3 = boto3.client('s3')
    try:
        bucket, key = get_model_bucket_key(image_s3_url)
        new_obj = s3.get_object(Bucket=bucket, Key=key)
        image_dl = new_obj['Body'].read()
        image = Image.open(io.BytesIO(image_dl)).convert("RGB")
        return image
    except Exception as e:
        raise e


def inference(model_input, model):
    """
    Internal inference methods
    :param model_input: transformed model input data
    :return: inference output label
    """
    with torch.no_grad():
        prediction = model(model_input)
        prediction = F.softmax(prediction, dim=1)

    # Get the top  confidence of prediction
    confidence, cat_id = torch.topk(prediction, 1)
    label = idx_to_class[cat_id[0].item()]
    score = confidence[0].item()
    return score, label


def get_transformed_image(url):
    image = get_image(url)

    return transform(image).unsqueeze(0).to(device)


def model_fn(device):
        model = torch.jit.load("model.scripted.pt")

        model.to(device).eval()

        return model


class ImageClassifierAPI(LabelStudioMLBase):
    def __init__(self, **kwargs):
        super(ImageClassifierAPI, self).__init__(**kwargs)
        self.from_name, self.to_name, self.value, self.classes = get_single_tag_keys(
            self.parsed_label_config, 'Choices', 'Image')
        # self.extract_model = False
        print("Model_dir : ", model_dir)
        # download model file from S3 into model_dir folder
        # if not self.extract_model:
        #     print(":: Model is not extracted!! ")
        #     print(":: Extracting model ...")
        #     extract_model(MODEL_S3_URI, model_dir)

        print(":: Loading model ...")
        self.model = model_fn(device)

    def predict(self, tasks, **kwargs):
        image_urls = [task['data'][self.value] for task in tasks]
        print("Number of tasks: ", len(image_urls))
        predictions = []
        for i, image_url in enumerate(image_urls):
            image = get_transformed_image(image_url)
            score, predicted_label = inference(image, self.model)
            print("Score: {} , prediction: {}".format(score, predicted_label))
            # prediction result for the single task
            result = [{
                'from_name': self.from_name,
                'to_name': self.to_name,
                'type': 'choices',
                'value': {'choices': [predicted_label]}
            }]

            # expand predictions with their scores for all tasks
            predictions.append({'result': result, 'score': float(score)})
            print("::Pred: {}: > {}".format(i, result))
        print("Predictions: {}".format(predictions))
        return predictions
