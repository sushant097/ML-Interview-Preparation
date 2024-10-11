## Overview 
This is the Label Studio ML Backend for Image classification with the possibility of transfer learning. 




## How to initialize ml backend

At first start the label studio docker as:
`docker run -it -p 8080:8080 -v $(pwd)/mydata:/label-studio/data heartexlabs/label-studio:latest`
Then follow steps as:

1. Override predict method of `LabelStudioMLBase` class.
Here is code script of my case:
```python
from label_studio_ml.model import LabelStudioMLBase
class ImageClassifierAPI(LabelStudioMLBase):

    def __init__(self, **kwargs):
        super(ImageClassifierAPI, self).__init__(**kwargs)
        self.from_name, self.to_name, self.value, self.classes = get_single_tag_keys(
            self.parsed_label_config, 'Choices', 'Image')
        self.model = model_fn(model_dir, device)

    def predict(self, tasks, **kwargs):
        image_urls = [task['data'][self.value] for task in tasks]
        predictions = []
        for image_url in image_urls:
            image = get_transformed_image(image_url)
            score, predicted_label = inference(image, self.model)
            # prediction result for the single task
            result = [{
                'from_name': self.from_name,
                'to_name': self.to_name,
                'type': 'choices',
                'value': {'choices': [predicted_label]}
            }]

            # expand predictions with their scores for all tasks
            predictions.append({'result': result, 'score': float(score)})

        return predictions

```

2. Initialize backend by: `label-studio-ml init my-ml-backend --script Label-Studio-Ml-Backend/ml_backend.py --force`
3. Start ml backend by:: `label-studio-ml start my-ml-backend/`

**Refernce: https://www.youtube.com/watch?v=43Ph805ukEc&t=991s**

## Quickstart

Build and start Machine Learning backend on `http://localhost:9090`

```bash
docker-compose up

Check if it works:

```bash
$ curl http://localhost:9090/health
{"status":"UP"}
```

Then connect running backend to Label Studio:

```bash
label-studio start --init new_project --ml-backends http://localhost:9090 --template image_classification
```


## Writing your own model
1. Place your scripts for model training & inference inside root directory. Follow the [API guidelines](#api-guidelines) described bellow. You can put everything in a single file, or create 2 separate one say `my_training_module.py` and `my_inference_module.py`

2. Write down your python dependencies in `requirements.txt`

3. Create ML backend with your model
```bash
label-studio-ml init my-ml-backend --script pytorch_transfer_learning/pytorch_transfer_learning.py
```

4. Start ML backend at http://localhost:9090
```bash
label-studio-ml start my-ml-backend
```

5. Start Label Studio with ML backend connection
```bash
label-studio start my-annotation-project --init --ml-backend http://localhost:9090
```
   
## API guidelines

Check out https://github.com/heartexlabs/label-studio-ml-backend/tree/master#Create_your_own_ML_backend

## License

This software is licensed under the [Apache 2.0 LICENSE](/LICENSE) © [Heartex](https://www.heartex.com/). 2022

<img src="https://github.com/heartexlabs/label-studio/blob/master/images/opossum_looking.png?raw=true" title="Hey everyone!" height="140" width="140" />