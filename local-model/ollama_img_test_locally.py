from PIL import Image
from io import BytesIO
import base64
from langchain_core.messages import HumanMessage
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="deepseek-r1")

img = Image.open("dog.jpg")
buffer = BytesIO()
img.save(buffer, format="JPEG")
img_bytes = buffer.getvalue()
img_b64 = base64.b64encode(img_bytes).decode('utf-8')

message = HumanMessage(
    content=[
        {"type": "text",
         "text": "What do you see in this image? Can you describe it?"},
        {
            "type": "image",
            "source_type": "base64",
            "mime_type": "image/jpeg",
            "data": img_b64
        },
    ]
)

response = llm.invoke([message])
print(response)
