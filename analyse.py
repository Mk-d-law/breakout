import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def process_scraped_data(scraped_data, prompt, previous_info=None, search_history=None):
    """Processes scraped data using Groq AI to answer the user's prompt, with awareness of past searches."""
    client = Groq(api_key=os.getenv("GROQAI_KEY"))
    context = "\n".join([f"- {item['title']}: {item['link']}" for item in scraped_data])

    # Add awareness of previous info and search history
    additional_context = ""
    if previous_info:
        additional_context += f"\n\nPreviously found partial info:\n{previous_info}"
    if search_history:
        additional_context += f"\n\nPrevious search queries attempted:\n" + "\n".join(search_history)

    query_prompt = f"Using this data:\n{context}{additional_context}\n{prompt}"

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query_prompt}
        ],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content.strip()

