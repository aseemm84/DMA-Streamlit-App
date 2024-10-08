# from openai import AzureOpenAI
# from dotenv import load_dotenv
# import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import re

# load_dotenv()

# client = AzureOpenAI(
#     api_version=os.getenv("AZURE_OPENAI_APIVERSION"),
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     api_key=os.getenv("AZURE_OPENAI_KEY")
# )

# chat_model_id = os.getenv("CHATGPT_MODEL")
groq = st.secrets["Groq_API_Key"]

def get_llm(temperature): 
    """
    Returns an instance of the ChatGroq LLM with the specified temperature.
    """
    return ChatGroq(
        model="llama-3.1-70b-versatile",
        groq_api_key=groq,
        temperature=0,
        max_tokens = 1000
        # other params...
    )

def check_for_rate_limit_error(response_content):
    """Checks if the response content contains a Groq rate limit error."""
    error_pattern = r"Rate limit reached.*in (\d+m\d+\.\d+s)"
    match = re.search(error_pattern, response_content)
    if match:
        wait_time = match.group(1)
        # Return an error message string instead of using st.error
        return f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}."
    return False

def generate_post(product_name, product_type, organization_name, target_audience, product_features, social_platform):
    
    template = """
    You are a marketing writing assistant for creating social media marketing posts.
    Create a social media post for {social_platform} about the product "{product_name}" (a {product_type}) by {organization_name}. 
    The target audience is {target_audience}.
    The key features of the product are: {product_features}.
    Use emojis, keep it concise, and use a conversational style as if you were talking to a friend.
    The post should include 3-5 relevant hashtags.
    Include a call to action encouraging users to "Learn more" by clicking the link in the bio.
    Write in a friendly and enthusiastic yet professional tone that best suits the specified audience and platform.
    The length of the post should suit the specified platform.
    """
    llm = get_llm(temperature)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    # conversation = [
    #     {"role": "system", "content": system_message},
    #     {"role": "user", "content": "Generate a social media post based on the provided information."}
    # ]

    try:
        response = chain.invoke({
            "product_name": product_name,
            "product_type": product_type,
            "target_audience": target_audience,
            "product_features": product_features,
            "social_platform": social_platform
        })
        # Check for rate limit error in the response content
        error_message = check_for_rate_limit_error(response.content) 
        if error_message:
            return error_message # Return the error string
        else: 
            return response.content
    except Exception as e:
        error_message = check_for_rate_limit_error(str(e))
        if error_message:
            return error_message # Return the error string
        else: 
            return f"An error occurred: {e}"
    
    # try:
    #     response = client.chat.completions.create(
    #         model=chat_model_id,
    #         messages=conversation,
    #         max_tokens=8000,
    #         temperature=0.4
    #     )
        
    #     return response.choices[0].message.content
    # except Exception as e:
    #     return str(e)
    
