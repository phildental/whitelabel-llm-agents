from langchain import OpenAI, ConversationChain
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the OPENAI_API_KEY
api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(temperature=0.5)
conversation = ConversationChain(llm=llm, verbose=True)

output = conversation.predict(input="Ask something about anything")
print(output)