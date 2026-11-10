from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, web_scrape
import os
from dotenv import load_dotenv

load_dotenv()

def to_text(content) -> str:
    """Convert LLM content (str or list of blocks) into plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    return str(content)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.3,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)
#1st agent
def build_agent_searcher():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

#2nd agent
def build_agent_scraper():
    return create_agent(
        model=llm,
        tools=[web_scrape]
    )

#writer chain

writer_chain = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that writes content based on the provided information."),
    ("user","""Write a detailed article based on the following information.

    Topics: {topic}

    Research Gathered: {research}

    Structure the article with an introduction, main content,key Findings(min 3 well explained points),
    and conclusion.
    Ensure the content is informative, engaging,
     and well-organized. Use clear headings 
     and subheadings where appropriate. Avoid plagiarism 
     and ensure the content is original"""
     )
])

writer_chain = writer_chain | llm | StrOutputParser()

#critique chain

critique_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a strict and professional AI Response Evaluator.

        Your task is to critically evaluate an AI-generated response
        based on the user's query and available tool outputs.

        Evaluate the response on the following parameters:

        1. Accuracy: Is the information factually correct?
        2. Relevance: Does it directly answer the user's question?
        3. Completeness: Does it cover all important points?
        4. Clarity: Is the response clear, simple, and well-structured?
        5. Reliability: Are the claims supported by the provided tool outputs?

        Provide your evaluation in the following format:

        **1. Score:**
        Give an overall score out of 10.

        **2. Verdict:**
        Give a short overall judgment:
        - Excellent (9-10)
        - Good (7-8)
        - Average (5-6)
        - Poor (3-4)
        - Very Poor (0-2)

        **3. Areas of Improvement:**
        Identify specific weaknesses, errors, missing information,
        irrelevant content, or unsupported claims.

        **4. How to Improve:**
        Give practical and actionable suggestions to improve the response.

        **5. Final Assessment:**
        Briefly explain whether the response is acceptable or needs revision.

        Be honest, objective, and strict.
        Do not give high scores just to be encouraging.
        Do not invent facts or assume information that is not provided.
        If information is insufficient to verify a claim, mention that clearly.
        """
    ),
    (
        "human",
        """
        User Query:
        {user_query}

        Tool Output:
        {tool_output}

        AI Response:
        {ai_response}

        Evaluate the AI response using the required format.
        """
    )
])

critique_chain = critique_prompt | llm | StrOutputParser()
