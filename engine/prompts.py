def get_system_prompt(mode_student):
    """
    Defines the AI's core behavior based on the selected mode.
    """
    if mode_student:
        return (
            "You are a supportive and expert Technical Tutor. "
            "Explain complex concepts using simple analogies. "
            "Avoid overly dense jargon and focus on the 'why' behind the technology."
        )
    else:
        return (
            "You are a Senior Software Architect. "
            "Provide concise, high-level technical breakdowns. "
            "Focus on efficiency, scalability, and structural integrity."
        )

def format_rag_prompt(query, context):
    """
    Combines user query with retrieved document context.
    """
    return f"""
    Context from uploaded documents:
    {context}
    
    User Question: {query}
    
    Instructions: Use the provided context to answer the question accurately. 
    If the answer isn't in the context, state that you don't know rather than hallucinating.
    """