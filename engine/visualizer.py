import base64

def generate_mermaid_chart(code_summary):
    """
    Converts a logic summary into a Mermaid.js flowchart string.
    """
    # This is a template. Later, Bedrock will fill 'nodes' and 'edges'.
    mermaid_code = f"""
    graph TD
        A[User Request] --> B[Processing Logic]
        B --> C{{Decision Point}}
        C -->|Success| D[Final Output]
        C -->|Failure| E[Error Handling]
    """
    return mermaid_code

def render_mermaid(code):
    """
    Encodes the mermaid code into a URL format that Streamlit can display as an image.
    """
    graphbytes = code.encode("ascii")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    return "https://mermaid.ink/img/" + base64_string