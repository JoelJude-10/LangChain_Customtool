from langchain.memory.buffer_window import ConversationBufferWindowMemory
from langchain.agents import AgentExecutor
from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.agents import create_csv_agent
from langchain_groq import ChatGroq

from langchain_community.tools.tavily_search import TavilySearchResults

import os
os.environ['COHERE_API_KEY'] = "AQWILHeT6TLrmqR94NrY4xDqAZSwUp1MmjsSPqV8"

chat = ChatGroq(model="llama3-70b-8192",groq_api_key="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", temperature=0.3)
def processing_tool(user_input):
    def file_processor(input=""):
        chat = ChatGroq(model="llama3-70b-8192",groq_api_key="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",temperature=0.3)

        csv_file_path = 'healthcare_source 6.csv'

        agent=create_csv_agent(chat,csv_file_path,allow_dangerous_code=True)
        r=agent.run(input)
        return r
    tool1=Tool(
        name="process_tool",
        func=file_processor,
        description="think yourself as a data analyst. answer to the user request using LLM and create the csv file as per the user request"
    )

    def tavi(input=""):
        tav=TavilySearchResults(api_key="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")
        query=input
        response=tav.search(query)
        if response["results"][0]:
            result=response["results"][0]
            return (result.get("content"))
    sear_t=Tool(
        name="search_engine",
        func=tavi,
        description="you are search tool .you need to answer the user query"
    )

    tools=[tool1,sear_t]

    memory=ConversationBufferWindowMemory(memory_key='chat_history',k=3,return_message=True)

    agent1 = initialize_agent(
        agent="conversational-react-description",
        tools=tools,
        llm=chat,
        max_iterations=10000,
        verbose=True,
        early_stopping_method="generate",
        memory=memory,
        handle_parsing_errors=True
    )

    a=agent1(user_input)
    return a