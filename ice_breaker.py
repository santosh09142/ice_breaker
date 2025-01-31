from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from third_parties.linkdin import scrape_linkdin_profile



#information = """
#        Elon Reeve Musk (/ˈiːlɒn/; EE-lon; born June 28, 1971) is a businessman and investor. He is the founder, chairman, CEO, and CTO of SpaceX; angel investor, CEO, product architect and former chairman of Tesla, Inc.; owner, chairman and CTO of X Corp.; founder of the Boring Company and xAI; co-founder of Neuralink and OpenAI; and president of the Musk Foundation. He is the wealthiest person in the world, with an estimated net worth of US$232 billion as of December 2023, according to the Bloomberg Billionaires Index, and $254 billion according to Forbes, primarily from his ownership stakes in Tesla and SpaceX.[5][6]

#    """

if __name__ == "__main__":
    load_dotenv()

    print("Hello langchain")

    summary_template = """
        given the Linkdin information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    #llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    llm = ChatOllama(model="llama3")
    #llm = ChatOllama(model="mistral")


    chain = summary_prompt_template | llm | StrOutputParser()
    linkdin_data = scrape_linkdin_profile(
        linkdin_profile_url="https://www.linkedin.com/in/santosh-patil-6b30326",
        mock=True,
    )
    res = chain.invoke(input={"information": linkdin_data})

    print(res)