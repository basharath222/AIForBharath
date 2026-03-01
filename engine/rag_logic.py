from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import boto3
import json
from .prompts import get_system_prompt, format_rag_prompt

def process_document(file_path):
    """
    Loads a PDF, splits it into chunks, and prepares it for the AI.
    """
    # 1. Load the PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 2. Split into small chunks so the AI can find specific info
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    
    return chunks

import os
import boto3
import json
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

def get_bedrock_response(prompt):
    # Now the function reads keys directly from the environment
    client = boto3.client(
        service_name='bedrock-runtime',
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    })

    try:
        response = client.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
            body=body
        )
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text']
    except Exception as e:
        return f"❌ Error: {str(e)}"



def call_bedrock(query, context, mode_student, aws_access_key=None):
    """
    Connects to Amazon Bedrock (Claude 3) using Boto3.
    """
    if not aws_access_key:
        return "⚠️ Please enter your AWS Access Key in the sidebar to activate the AI."

    # Initialize the Bedrock client
    client = boto3.client(
        service_name='bedrock-runtime', 
        region_name='us-east-1', # Or your specific AWS region
        aws_access_key_id=aws_access_key
    )
    
    system_msg = get_system_prompt(mode_student)
    user_msg = format_rag_prompt(query, context)

    # Example payload for Claude 3
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": user_msg}
        ],
        "system": system_msg
    }

    try:
        response = client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0', 
            body=json.dumps(payload)
        )
        result = json.loads(response.get('body').read())
        return result['content'][0]['text']
    except Exception as e:
        return f"❌ Error connecting to Bedrock: {str(e)}"

def mock_bedrock_response(query, context, mode_student):
    """
    Simulates the AI response to verify UI flow.
    """
    if mode_student:
        return (
            "🎓 **Student Mode Active:** I've analyzed your document. "
            "Think of this logic like a post office: your data is the 'letter', "
            "and this function is the 'sorting machine' that decides where it goes."
        )
    return "Architecture Analysis: Input data mapped to processing node 1.0."