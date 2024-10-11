import streamlit as st
from PIL import Image
import requests
import base64
from io import BytesIO

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """


# @st.cache
def predict(encoded_string):
    url = 'https://fb5md1fca4.execute-api.us-east-1.amazonaws.com/test/intel-predictor'
    data = {'body': encoded_string}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers).json()
    # print(response)
    # print(type(response))
    # print(response.keys())
    # print(response.values())
    try:

        confidences = {}
        confidences['Labels'] = list(response.keys())
        confidences['Confidence (%)'] = list(response.values())
        confidences['Confidence (%)'] = [i * 100 for i in confidences['Confidence (%)']]
        return confidences
    except Exception as e:
        return response


def main():
    st.set_page_config(
        page_title="EMLOv2 - Project",
        layout="centered",
        page_icon="✔️",
        initial_sidebar_state="expanded",
    )

    st.title("Intel Classifier using Lambda")
    st.subheader("Upload an image to classify it")

    uploaded_file = st.file_uploader(
        "Choose an image...", type=["jpg", "png", "jpeg"]
    )

    if st.button("Predict"):
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            image = image.resize((300, 300)) # resize so that large files can easily pass to endpoint
            io_buffer = BytesIO()
            image.save(io_buffer, format="JPEG")
            encoded_string = base64.b64encode(io_buffer.getvalue()).decode("utf-8")
            encoded_string = "data:image/jpeg;base64," + encoded_string
            # encoded_string = "inputs:" + encoded_string

            st.image(image, caption="Uploaded Image", use_column_width=False)
            st.write("")
            predictions = None
            try:
                with st.spinner("Predicting..."):
                    predictions = predict(encoded_string)
                    # print(predictions)
                    # get key with highest value
                    st.success(f"Predictions are...")
                    st.markdown(hide_table_row_index, unsafe_allow_html=True)
                    st.table(predictions)
            except:
                st.error("Something went wrong. Please try again.")
                st.error(f"Error: {predictions}")
                st.error("Error can be due to: \n 1. Large file size [endpoint is small instance, sorry for now]"
                         "\n 2. Maybe corrupted image. \n 3. Try again. Best of luck!")
        else:
            st.warning("Please upload an image.")


if __name__ == "__main__":
    main()