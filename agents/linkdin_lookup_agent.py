import os
from dotenv import load_dotenv
# from langchain.chains.summarize.refine_prompts import prompt_template
from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import  hub
from tools.tools import get_profile_url_tavily

load_dotenv()

def lookup(name: str) -> str:

    llm = ChatOpenAI(
        temperature=0,
        model_name='gpt-4o-mini'
    )
    # llm = ChatOllama(
    #     temperature=1,
    #     model='llama3'
    # )
    print("testing")
    template = """ given the full name {name_of_person} I want you to get it me a link to their Linkdin profile page
                    Your answer should contain only a URL"""

    print("Before name of a person")

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Linkdin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkdin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={ "input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkdin_profile_url = result["output"]
    return linkdin_profile_url

if __name__ == "__main__":
   print(lookup(name="Santosh Patil"))
