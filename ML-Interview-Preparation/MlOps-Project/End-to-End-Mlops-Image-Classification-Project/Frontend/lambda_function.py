import json
import os
import io
import boto3
import json
from PIL import Image
import base64
import numpy as np

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.Session().client(service_name="sagemaker-runtime", region_name='us-east-1')

response_headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
}


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def decode_base64_to_image(encoding: str):
    content = encoding.split(";")[1]
    image_encoded = content.split(",")[1]
    return Image.open(io.BytesIO(base64.b64decode(image_encoded)))


def lambda_handler(event, context):
    # TODO implement
    print("Received event: " + json.dumps(event, indent=2))

    # body = json.loads(json.dumps(event))
    payload = event['body']

    try:
        img_array = decode_base64_to_image(payload)
        np_image_array = np.asarray(img_array)
        print("Shape: ", np_image_array.shape)
        data = {"inputs": np_image_array.tolist()}  # same without convert into list

        response = None
        try:
            # sagemaker only accepts content type application/json
            response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                               ContentType='application/json',
                                               Body=json.dumps(data))

        except Exception as e:
            print(e)

            return {
                "statusCode": 500,
                "headers": response_headers,
                "body": json.dumps({"message": "Endpoint Response: Failed to process image: {}".format(e)}),
            }

        result = json.loads(response['Body'].read().decode())
        print("Result: \n", result)
        return result

    except Exception as e:
        print(e)

        return {
            "statusCode": 500,
            "headers": response_headers,
            "body": json.dumps({"message": "Failed to process image: {}".format(e)}),
        }

