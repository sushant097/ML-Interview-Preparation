
# Predicting Customer Satisfaction Before the Order

[![Python Version](https://img.shields.io/pypi/pyversions/zenml)](https://pypi.org/project/zenml/)

## Introduction

Have you ever wondered how businesses could predict how customers will feel about a product *before* they've even ordered it? In this project, we explore exactly that—predicting customer satisfaction based on their past interactions with the marketplace. 

This is no longer a far-fetched idea but a reality, thanks to the power of machine learning and automation. By analyzing a customer's purchase history and various order features, we can predict their satisfaction score for their next purchase.

The dataset we are using is the **[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**, which provides rich insights from over 100,000 orders between 2016 and 2018. Our goal? To predict the customer satisfaction score based on features like order status, price, payment method, product characteristics, and more.

### ZenML to the Rescue

To tackle this problem in a real-world setting, we aren't just building a model we're creating a robust pipeline using **[ZenML](https://zenml.io/)**. This pipeline is designed to automate model training, deployment, and inference. Whether it's tracking our model’s performance using **MLflow** or showcasing results with **Streamlit**, we're creating an end-to-end solution for customer satisfaction prediction.

---

## :snake: Python Environment Setup

First things first, let’s set up the environment. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/zenml-io/zenml-projects.git
cd zenml-projects/customer-satisfaction
pip install -r requirements.txt
```

### Required Tools
- **ZenML**
- **MLflow**
- **Scikit-learn**
- **Streamlit**
- **Pandas** (and more)

---

## Project Features

This project is more than just a simple prediction model: it's a complete machine learning lifecycle management system with some cool features:

- **Pipeline Management:** ZenML allows us to manage and track all the steps from data ingestion to deployment.
- **Continuous Deployment:** Automatically redeploy models based on predefined accuracy thresholds.
- **MLflow Integration:** Track model metrics, hyperparameters, and results using MLflow’s seamless integration.
- **Streamlit App:** A user-friendly interface that allows anyone to make predictions using the latest deployed model.

### :rocket: Real-World Solution

The solution we’re building is designed to handle continuous data flow. Every new order updates the pipeline, retrains the model if necessary, and triggers a redeployment if the updated model meets our accuracy standards. The pipeline keeps everything organized and runs smoothly in a production-like environment.

---

## Pipelines

### Training Pipeline

Our training pipeline automates several key steps to ensure seamless model training and evaluation:

1. **Data Ingestion:** Gathers data from various sources and converts it into a DataFrame.
2. **Data Cleaning:** Cleans and preprocesses the data to remove unnecessary columns and outliers.
3. **Model Training:** Trains the model and logs all relevant data into MLflow using its autologging features.
4. **Evaluation:** Evaluates model performance and stores metrics (like MSE) for future comparison.

### Continuous Deployment Pipeline

This extended pipeline ensures that every time the model is retrained, it checks for performance against a configurable threshold. If the model passes, it is redeployed.

Additional steps in this pipeline include:
- **Deployment Trigger:** Evaluates whether the newly trained model should be deployed.
- **Model Deployer:** Deploys the model using MLflow’s deployment capabilities if the criteria are met.

---

## :computer: Running the Project

To get the pipelines up and running, follow these steps:

### 1. Training the Model:
```bash
python run_pipeline.py
```

### 2. Running the Continuous Deployment Pipeline:
```bash
python run_deployment.py
```

---

## 🕹️ Streamlit App

We've also developed a **Streamlit** app to visualize and interact with our prediction models. This app takes input features (such as product and order details) and returns a predicted customer satisfaction score. To run it locally:

```bash
streamlit run streamlit_app.py
```

**Demo Video:**:
<video src='https://github.com/user-attachments/assets/fc533976-3986-48fb-ba25-8df34a7e5de5' ></video>
---

## :bar_chart: ZenML Dashboard

ZenML comes with a built-in dashboard where you can view your pipelines and components. You can launch it with:

```bash
pip install zenml[server]
zenml up
```

From here, we can track your training pipelines, deployment status, and more in an intuitive interface.

---

## :sparkles: What’s Next?

This project has the potential to be scaled even further by integrating advanced deployment strategies (e.g., `Kubernetes`) or fine-tuning the model further with more robust feature engineering and hyperparameter tuning.

Feel free to clone the repo, experiment with different models, and even extend the pipeline for additional use cases. This is just the beginning, imagine what we could build with ZenML!
