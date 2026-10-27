from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq( model="openai/gpt-oss-120b", temperature=0, api_key=os.getenv("GROQ_API_KEY") )


def expand_query(query: str) -> str:
    """
    Expand the user's query with related search terms.
    Returns a single expanded query string.
    """

    prompt = f"""
    You are a Query Expansion Assistant for a Retrieval-Augmented Generation (RAG) system.

    Your job is to improve search retrieval.

    Rules:
    - Keep the original query.
    - Add only closely related search phrases and synonyms.
    - Do NOT answer the question.
    - Do NOT explain anything.
    - Do NOT use bullet points or numbering.
    - Return plain text only.

    User Query:
    {query}
    """

    response = llm.invoke(prompt)

    return response.content.strip()