import cohere
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))
#print(co)


def get_text_output(input):

    output = co.chat(
        model = "command-r-plus",
        message = input
    )

    return output.text
