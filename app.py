import streamlit as st
from PIL import Image
#from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from transformers import pipeline
import back_app as bk

toxicity_detector = pipeline("text-classification", model="unitary/toxic-bert")
#bias_detector = pipeline("text-classification", model="d4data/bias-detection-model")
st.set_page_config(page_title="Social Media Post Generator", page_icon="📱", layout="wide")

col1, col2 = st.columns([1, 4])

logo = Image.open("static/logo.png")
col1.image(logo, width=100)  # Adjust width as needed

col2.title("Social Media Post Generator")

with st.form("post_generator_form"):
    product_name = st.text_input("Product Name*")
    product_type = st.text_input("Type of Product*")
    organization_name = st.text_input("Organization's Name*")
    target_audience = st.text_input("Target Audience*")
    product_features = st.text_area("Features of the Product*")
    social_platform = st.selectbox("Social Media Platform*", ["X (Twitter)", "LinkedIn", "Instagram", "Facebook"])

    submitted = st.form_submit_button("Generate Post")

if submitted:
    if product_name and product_type and organization_name and target_audience and product_features and social_platform:
        with st.spinner("Generating post..."):
            generated_post = bk.generate_post(product_name, product_type, organization_name, target_audience, product_features, social_platform)
        toxicity_result = toxicity_detector(generated_post)
        toxicity_score = toxicity_result[0]['score']
        #bias_result = bias_detector(generated_post)
        #bias_score = bias_result[0]['score']
        st.subheader("Generated Post:")
        st.write(generated_post)
        st.subheader("Analysis Results:")
        st.write(f"Toxicity Score: {toxicity_score:.2f}")
        #st.write(f"Bias Score: {bias_score:.2f}")
        
        if toxicity_score > 0.5:
            st.warning("The generated post may contain toxic content. Please review.")
        
        #if bias_score > 0.5:
            #st.warning("The generated post may contain biased content. Please review.")
    else:
        st.error("Please fill in all fields before generating a post.")

st.sidebar.title("About")
st.sidebar.info("""This app generates social media posts using AI 📱.
                \nEnter your product details and get a customized post for your chosen platform.
                \nFields marked with * are mandatory to fill.""")

