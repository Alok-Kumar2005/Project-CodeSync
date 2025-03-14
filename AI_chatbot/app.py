import os
import re
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# LangChain imports
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

load_dotenv()

app = Flask(__name__)

# Conversation memory
# NOTE: We set `output_key="text"` so it matches the chain's default output.
memory = ConversationBufferMemory(
    memory_key="history",
    input_key="input",
    output_key="text"
)

# Prompt template referencing {history} and {input}
template = """
You are a code-only programming assistant. Follow these rules STRICTLY:
1. Respond ONLY to programming/code-related questions
2. Return PURE CODE without any explanations, comments, or markdown
3. Never use code blocks (```) or natural language
4. Format code with proper line breaks and indentation
5. If question is non-programming, respond "I specialize in programming queries only."

Conversation so far:
{history}

User query: {input}
"""

prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=template
)

# Initialize ChatGroq LLM
llm = ChatGroq(
    model="qwen-2.5-coder-32b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

# llm_chain = prompt | llm | memory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message', '')
    try:
        raw_output = llm_chain.run(user_message)

        cleaned = re.sub(r'```[a-z]*\n?', '', raw_output)
        cleaned = re.sub(r'\n\s*```', '', cleaned)
        cleaned = cleaned.strip()

        return jsonify({'status': 'success', 'message': cleaned})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
