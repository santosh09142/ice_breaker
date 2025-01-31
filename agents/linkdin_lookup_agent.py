import os
from dotenv import load_dotenv
from langchain.chains.summarize.refine_prompts import prompt_template
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import  hub

from tools.tools import get_profile_url_tavily

load_dotenv()

def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        # model_name='gpt-4o-mini',
        model_name='llama3'
    )
    template = """ given the full name {name_of_person} I want you to get it me a link to their Linkdin profile page
                    Your answer should contain only a URL"""

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
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=true)

    result = agent_executor.invoke(
        input={ "input": prompt_template.format_prompt(name_of_persom=name)}
    )
    print("Entering new AgentExecutor Chain...")
    linkdin_profile_url = result["output"]
    return linkdin_profile_url

if __name__ == "__main__":
    #linkdin_url = lookup(name= "Santosh Patil")
    print(linkdin_url)