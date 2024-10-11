import io
import logging
import numpy as np
import torch
import torchvision
import torchvision.transforms as T
import torch.nn.functional as F

from PIL import Image
import base64
import json
import os
from alibi_detect.cd import MMDDriftOnline
from utils import extract_model, download_file_from_s3, extract_archive


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


# load model
def model_fn(model_dir, device):
    model = torch.jit.load(f"{model_dir}/model.scripted.pt")

    model.to(device).eval()

    return model


class ModelHandler(object):
    """
    A sample Model handler implementation.
    """

    def __init__(self):
        self.initialized = False
        self.dd = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.transform = T.Compose([T.Resize((224, 224)),
                                    T.ToTensor(),
                                    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        self.idx_to_class = {
            0: 'buildings', 1: 'forest', 2: 'glacier', 3: 'mountain', 4: 'sea', 5: 'street'
        }
        # for drift detection
        # download file
        # Set the bucket name and file name
        self.bucket_name = 'sagemaker-us-east-1-input-data'
        self.file_name = 'mini_dataset.zip'
        self.dataset_dir = "/tmp/mini_dataset"

    # stack samples of minidataset for drift detection
    def initialize(self, context):
        """
        Initialize model. This will be called during model loading time
        :param context: Initial context contains model server system properties.
        :return:
        """
        self.initialized = True
        # properties = context.system_properties
        # # Contains the url parameter passed to the load request
        # model_dir = properties.get("model_dir")

        # download model file from S3 into /tmp folder
        extract_model(os.environ['MODEL_S3_URI'], '/tmp')
        # LOAD MODEL
        model_dir = "/tmp/"
        self.model = model_fn(model_dir, self.device)
        # download and extract zip dataset
        download_file_from_s3(self.bucket_name, self.file_name)
        logging.info("::Files and Folders in current directory:: {}".format(os.listdir("/tmp/")))
        # dataset is extracted in the path name "/tmp/mini_dataset"
        # inside mini_dataset -> six folders of each class
        extract_archive(
            from_path="/tmp/" + self.file_name,
            to_path=None  # extract on same folder where zip file downloaded
        )

        # print("::Files and Folders in current directory::")
        logging.info("::Files and Folders in current directory:: {}".format(os.listdir("/tmp/")))
        # print(os.listdir())

        N = 50  # size of reference set
        stream_i = stream_intel(dataset_dir=self.dataset_dir)
        logging.info("Initializing reference dataset:: ")
        x_ref = np.stack([next(stream_i) for _ in range(N)], axis=0)
        ERT = 150  # expected run-time in absence of change
        W = 2  # size of test window
        B = 50_000  # number of simulations to configure threshold

        # fit for drift detection for N samples
        logging.info("::Fiting for drift detection on reference samples::")
        self.dd = MMDDriftOnline(x_ref, ERT, W, backend='pytorch')

    def preprocess(self, img_path):
        """
        Transform raw input into model input data.
        :param img_path: One image path
        :return: preprocessed model input data
        """
        # Take the input data and pre-process it make it inference ready
        # data preprocessing
        data = Image.open(img_path)
        data = data.convert('RGB')
        data = self.transform(data).unsqueeze(0).to(self.device)
        logging.info("::Preprocess data shape:: {}".format(data.shape))
        return data

    def inference(self, model_input):
        """
        Internal inference methods
        :param model_input: transformed model input data
        :return: inference output in json
        """
        with torch.no_grad():
            prediction = self.model(model_input)
            prediction = F.softmax(prediction, dim=1)

        # Get the top 5 confidence of prediction
        confidences, cat_ids = torch.topk(prediction, 5)
        outputs = {
            self.idx_to_class[idx.item()]: c.item() for c, idx in zip(confidences[0], cat_ids[0])
        }
        logging.info("::Model Output:: {}".format(outputs))

        ######### DRIFT DETECTION #################
        # image with no batch dimension ; [1, C, H, W] => [C, H, W]
        input_object = model_input.squeeze(0)
        logging.info("Shape after squeeze: {}".format(input_object.shape))
        drift_preds = self.dd.predict(np.array(input_object), return_test_stat=True)
        print("####################################################################")
        logging.info("::Dift statistics:: {} ".format(drift_preds))
        print("####################################################################")
        # return outputs
        return outputs

    def postprocess(self, inference_output):
        """
        Return predict result in as list.
        :param inference_output: inference output
        :return: Json of inference output
        """
        results = json.dumps(inference_output)
        logging.info("::Postprocess: {}".format(results))
        return results

    def handle(self, img_path, context):
        """
        Call preprocess, inference and post-process functions
        :param img_path: Path where image is saved
        :param context: mms context
        """
        print("Calling handle ...")
        model_input = self.preprocess(img_path)
        model_out = self.inference(model_input)
        return self.postprocess(model_out)


_service = ModelHandler()


def stringToImage(event):
    image_bytes = event['body'].encode('utf-8')
    base64_string = base64.b64decode(image_bytes)
    image = Image.open(io.BytesIO(base64_string))
    image.save(fp='/tmp/image.png')
    image_path = str('/tmp/image.png')
    print("img_path: ", image_path)
    return image_path


def handler(event, context):
    # body = json.loads(event['body'])
    # df = pd.DataFrame(body, index=[0])
    # data = xgboost.DMatrix(df.values)
    #
    # # PREDICT
    # prediction = model.predict(data)
    if not _service.initialized:
        logging.info("Initializing ...")
        _service.initialize(context)

    if event is None:
        return None

    print("event", event)
    img_path = stringToImage(event)
    print(img_path)

    return _service.handle(img_path, context)
