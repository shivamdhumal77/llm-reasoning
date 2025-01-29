from langchain.chat_models import ChatOpenAI

# Define Llama 3.2 Vision model
llm_vision = ChatOpenAI(
    api_key="ollama",  # Required, even if unused
    base_url="https://sunny-gerri-finsocialdigitalsystem-d9b385fa.koyeb.app/v1",
    model="llama3.2vision"  # Specify the vision model
)

def generate_response(prompt, image_path=None):
    """
    Generate a text response using the Llama 3.2 Vision model.

    Args:
    - prompt (str): The text prompt for the model.
    - image_path (str, optional): The path to the image file to include in the query.

    Returns:
    - str: The response text from the model.
    """
    try:
        # Include the image file if provided
        if image_path:
            with open(image_path, "rb") as img_file:
                response = llm_vision.predict(prompt=prompt, files={"image": img_file})
        else:
            response = llm_vision.predict(prompt=prompt)
        return response
    except Exception as e:
        return f"Error with Llama 3.2 Vision model: {e}"
