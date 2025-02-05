from dotenv import load_dotenv
# from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from third_parties.linkdin import scrape_linkdin_profile
from agents.linkdin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break_with(name: str) -> str:

    linkedin_username = linkedin_lookup_agent(name=name)
    linkdin_data = scrape_linkdin_profile(linkdin_profile_url=linkedin_username)

    summary_template = """
            given the Linkdin information {information} about a person from I want you to create:
            1. a short summary
            2. two interesting facts about them
        """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    # llm = ChatOllama(model="llama3")
    # llm = ChatOllama(model="mistral")

    chain = summary_prompt_template | llm #| StrOutputParser()

    res = chain.invoke(input={"information": linkdin_data})

    print(res)


if __name__ == "__main__":
    load_dotenv()

    print("Ice Break Enter")
    ice_break_with(name="Santosh Patil")

    # linkdin_data = scrape_linkdin_profile(
    #     linkdin_profile_url="https://www.linkedin.com/in/santosh-patil-6b30326",
    #     mock=True,
    # )

