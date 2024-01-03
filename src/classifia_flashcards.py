import os
import sys

from huggingface_hub import hf_hub_download
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
## TEST LIB
from langchain.output_parsers import CommaSeparatedListOutputParser

from flashcard_repository import FlashCardRepository

MODEL = "models/models--TheBloke--Mistral-7B-Instruct-v0.1-GGUF/snapshots/731a9fc8f06f5f5e2db8a0cf9d256197eb6e05d1/"
MODEL_ID = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
MODEL_FILE = "mistral-7b-instruct-v0.1.Q4_K_S.gguf"


def get_llm():
    model_path = os.path.join(os.path.dirname(os.getcwd()), MODEL, MODEL_FILE)
    
    if not os.path.isfile(model_path):
        print("NO HAY MODELO")
        model_path = hf_hub_download(
            repo_id=MODEL_ID,
            filename=MODEL_FILE,
            resume_download=True,
            cache_dir=os.path.join(os.path.dirname(os.getcwd()), "models"),
        )

    model = LlamaCpp(
        model_path=model_path,
        n_gpu_layers=1,
        n_batch=512,
        f16_kv=True,
        max_tokens=2048,
        n_ctx=2048,
        top_p=1,
        #callback_manager=callback_manager,
        #verbose=True,
    )
    return model


def get_prompt():
    context = """
    [CONTEXT]
    A chat between a user looking to categorize a given medical text in the format of Q/A and an artificial intelligence assistant specialized in classifying content.
    This assistant responds with a list of five medical categories each time. Here are the requirements for response:
    1. Response must not contain extra information, explanations, url or empty strings.
    2. Each category must be a title-cased string.
    3. Special characters are not allowed.
    4. Tags must be all lowercase.
    5. Parse the output list like "item1,item2,item3,item4,item5" replade word item with classifcation tag.
    6. Do not use bullets
    [/CONTEXT]
    [INST]Assign up to five medical categories to the following Q/A text, categories must use as few words as possible and being close to the text context.
    Question: {question}
    Answer: {answer}
    [/INST]
    """
    prompt = PromptTemplate.from_template(context)
    return prompt



def main(args):
    print ("MAIN")

    llm = get_llm()

    prompt = get_prompt()
    
    flashcards: FlashCardRepository = FlashCardRepository().get_flashcards_dataframe()
    for flashcard in flashcards:
        for item, row in flashcard.iterrows():
            chain = prompt | llm | CommaSeparatedListOutputParser()
            response = chain.invoke({"question": item[1], "answer": item[2]})
            print(response)


if __name__ == '__main__':
    main(sys.argv[1:])

