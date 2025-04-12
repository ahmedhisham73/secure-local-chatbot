from llama_cpp import Llama
import os
from loguru import logger

# Path to the model
MODEL_PATH = os.environ.get("MODEL_PATH", "models/TinyLLAMA/tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf")

# Load the model using llama.cpp
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=512,  # Context size
    n_threads=8,  # Number of threads (adjust this depending on the system)
    verbose=False  # Set to True if you need detailed logging
)

# Configure the logger to log responses
logger.add("app/log_service/responses_logs/chatbot_logs.log", rotation="1 MB", retention="7 days", compression="zip")

# Function to generate a response
def generate_response(prompt: str) -> str:
    # Strip unnecessary spaces from the prompt
    prompt = prompt.strip()
    
    # Log the received prompt
    logger.info(f"Received prompt: {prompt}")

    # Create a friendly assistant prompt to ensure the response is warm, helpful, and friendly
    friendly_prompt = f"""You are a friendly and engaging digital assistant. Always respond in a warm, 
empathetic, and conversational manner. Make sure your responses are natural, helpful, and always sound approachable. 
Answer the following question with emojis: {prompt}"""

    # Generate the response using the model with temperature for relevance
    response = llm(
        friendly_prompt, 
        max_tokens=300, 
        stop=["</s>"], 
        temperature=0.3  # Adjust the temperature for more relevant, yet creative answers
    )

    # Extract and log the generated response
    generated_text = response["choices"][0]["text"].strip()
    logger.info(f"Generated response: {generated_text}")

    return generated_text


