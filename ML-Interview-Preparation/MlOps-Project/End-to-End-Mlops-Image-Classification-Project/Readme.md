# End-to-End MLOps Image Classification Project

## Table of Contents
1. [MLOps-Hyperparameter-Tuning](./Mlops-Hyperparameter-Tuning/)
2. [Model-Evaluation-And-Explanation](./Model-Evaluation-And-Experiment/)
3. [Sagemaker-Pipeline](./Sagemaker-Pipeline/)
4. [CI-CD-Pipeline](./CI-CD-Pipeline/)
5. [Label-Studio-Ml-Backend ](./Label-Studio-ML-Backend/)
6. [Project Frontend](./Frontend/)


**Complete end-to-end architecture:**
![](images/tsai_emlov2-project_file.drawio.png)


# MLOps Pipeline for Image Classification

This project implements a complete MLOps pipeline designed for an end-to-end image classification task. The primary goal is to streamline the process of annotating images, retraining models, and deploying models to production environments with minimal manual intervention. This project was developed as part of the Extensive Machine Learning Operations (EMLOv2) course by the School of AI.

---

### Overview

The pipeline leverages **AWS services** like **SageMaker**, **S3**, **EventBridge**, **CodeBuild**, **CloudFormation**, and **Lambda** to automate the image classification workflow. The project is integrated with **Label Studio** for semi-automated annotation, and the frontend for making predictions is built using a **Streamlit** app.

---

### Pipeline Components

1. **Data Ingestion and Annotation:**
   - **Label Studio**: Used as a semi-automated annotation tool. The initial model predictions aid in faster labeling of new images. This process speeds up annotation by predicting labels for images, and manual corrections can be made as needed.
   - **AWS S3**: Once the annotations are complete, the images and their labels are manually pushed to an **S3 bucket**, triggering the rest of the pipeline.

2. **Triggering the MLOps Pipeline:**
   - **AWS EventBridge**: Detects new events (new images and annotations uploaded to the S3 bucket) and triggers the SageMaker MLOps pipeline.

3. **Model Build and Deployment Pipeline:**
   - **SageMaker Pipeline**: Reads the newly uploaded images and annotations from the S3 bucket to retrain the model with updated data.
   - **AWS CodeBuild**: Compiles and tests the model code to ensure successful execution before deployment.
   - **AWS CodePipeline**: Manages the continuous integration and deployment (CI/CD) process for both the model and infrastructure updates.
   - **CloudFormation**: Handles the creation and update of stacks, ensuring that the staging and production environments are always up-to-date with the latest model versions.
   - **Manual Approval Stage**: There is a manual approval process before deploying the model to the production environment.
   - **AWS Lambda and API Gateway**: Used to interact with the deployed model endpoint for making real-time predictions.

4. **Model Registry and Artifacts:**
   - **Model Registry**: Maintains different versions of models, enabling easy tracking and rollback if needed.
   - **S3 Buckets**: Store the training artifacts, such as images and annotations, along with model artifacts for reproducibility.

5. **Frontend Prediction Application:**
   - **Streamlit App**: Provides a user-friendly interface for interacting with the model. Users can upload images through the app, and the app communicates with the SageMaker model endpoint to retrieve predictions.

---

### Workflow Overview

The high-level flow of the project is as follows:
1. Images are uploaded to **Label Studio** for annotation.
2. Once annotations are complete, they are pushed to the **S3 bucket**.
3. **EventBridge** triggers the **SageMaker MLOps pipeline**.
4. The pipeline retrieves new data from S3, retrains the model, and updates the model in the staging environment.
5. After manual approval, the model is deployed to production using **CloudFormation**.
6. A **Streamlit app** provides a frontend for end-users to upload images and receive predictions from the deployed model.

---

### AWS Services Used
- **Amazon S3**: For storing images, annotations, and model artifacts.
- **Amazon SageMaker**: For training, testing, and deploying machine learning models.
- **AWS EventBridge**: To trigger the pipeline when new data is available.
- **AWS CodePipeline**: To manage the end-to-end CI/CD process.
- **AWS CodeBuild**: To build and test the model artifacts.
- **AWS CloudFormation**: To manage the infrastructure as code, ensuring consistent environments.
- **AWS Lambda & API Gateway**: To create the endpoint that serves the model predictions to the frontend.

---

### Prerequisites

- **AWS Account**: You need an active AWS account to deploy this pipeline.
- **Label Studio**: Installed for semi-automated annotation.
- **Python**: The backend code for the pipeline uses Python, so ensure Python 3.x is installed.
- **Streamlit**: The frontend is built using Streamlit, so ensure you have this installed for testing locally.

---

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sushantproject/TSAI-EMLOv2-MainProjectRepo.git
   cd TSAI-EMLOv2-MainProjectRepo
   ```

2. **Setup AWS Environment**:
   - Ensure you have the AWS CLI configured with necessary permissions to access S3, SageMaker, EventBridge, and other AWS services.
   - Use the **CloudFormation** template provided in the repository to set up the required infrastructure.

3. **Run the Pipeline**:
   - Upload images to **Label Studio** and annotate them.
   - Push the annotated data to the configured **S3 bucket**.
   - The pipeline will automatically trigger once new data is detected.

4. **Access the Frontend**:
   - The **Streamlit app** is hosted separately but can be run locally for testing. Simply navigate to the `frontend` folder and start the Streamlit app:
     ```bash
     streamlit run app.py
     ```

---

### Folder Structure

```
.
├── src/                   # Source code for model training and deployment
├── pipeline/              # Pipeline configuration files
├── cloudformation/        # Infrastructure as code using CloudFormation templates
├── s3-buckets/            # Data storage and model artifacts
├── label-studio/          # Label studio configuration for image annotations
└── frontend/              # Streamlit frontend code for image prediction
```

---

### Future Enhancements

- Automating the process of pushing annotated images to S3 after Label Studio annotations.
- Implementing more sophisticated annotation feedback loops to improve the model's accuracy faster.
- Supporting different types of image classification tasks beyond the current scope.

---

### Contributing

I welcome contributions! Please feel free to submit pull requests or open issues on GitHub.

---

### License

This project is licensed under the MIT License. See the LICENSE file for more information.

---

### Acknowledgments

- **School of AI** for offering the EMLOv2 course and guiding the development of this pipeline.
- The **AWS** team for providing comprehensive services for end-to-end MLOps pipelines.
