from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_APIVERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY")
)

chat_model_id = os.getenv("CHATGPT_MODEL")



def generate_post(product_name, product_type, organization_name, target_audience, product_features, social_platform):
    system_message = f"""
    You are a marketing writing assistant. Create a social media post for {social_platform} about the product "{product_name}" 
    (a {product_type}) by {organization_name}. The target audience is {target_audience}. 
    The key features of the product are: {product_features}. 
    Write in a friendly yet professional tone that best suits the specified audience and platform.
    """

    conversation_history = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": "Generate a social media post based on the provided information."}
    ]
    
    try:
        response = client.chat.completions.create(
            model=chat_model_id,
            messages=conversation_history,
            max_tokens=8000,
            temperature=0.4
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return str(e)