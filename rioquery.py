import os
import re
import sys
import uuid
from triz_config import TrizConfig as CONFIG
from langdetect import detect
import chromadb
from openai import OpenAI, OpenAIError


class DocUpload:
    pass


class DocumentData:

    def __init__(self) -> None:
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path="vectordb")
        self.collection_name = "triz"

        # Read the document contents
        with open(os.path.join(CONFIG.DOC_FOLDER, CONFIG.DEFAULT_FILENAME), 'r') as file:
            self.contents = file.read()

        # Split the document into text blocks based on the occurrences of [[ and ]]
        self.text_blocks = re.findall(r'\[\[(.*?)\]\]', self.contents, re.DOTALL)

        # Print the extracted text blocks
        for idx, block in enumerate(self.text_blocks, 1):
            print(f"Text block {idx}:")
            print(block)
            print("--------------------")


        # store segments in ChromaDB collection
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception as e:
            print(e)

        self.collection = self.client.create_collection(name=self.collection_name)

        # Add segments to collection with unique IDs
        # collection.add(documents=text_blocks, ids=[f"block_{i}" for i in range(len(text_blocks))])
        ids = []
        for i in range(len(self.text_blocks)):
            ids.append(f"block_{i}")

        for counter, block in enumerate(self.text_blocks):
            self.collection.add(documents=block, ids=ids[counter-1])

        print(f"TEXT_BLOCKS:\n", self.text_blocks)



class TrizDoc():

    def __init__(self, retrieval_document) -> None:

        self.openai = OpenAI(api_key=CONFIG.OAI_APIKEY)
        self.collection = retrieval_document
        self.summary = ""
        self.history = []



    def detect_language(self, text):
        try:
            language = detect(text)
            return language
        except:
            return 'en'


    def append_to_history(self, role, message):
        self.history.append([role, message])


    def get_history(self) -> str:
        max_depth = len(self.history)
        if max_depth < CONFIG.HISTORY_DEPTH * 2:
            target_depth = max_depth
        else:
            target_depth = CONFIG.HISTORY_DEPTH * 2 # times 2 because question and answer is considered as 1
        
        hist = ""
        for i in range(target_depth):
            hist += self.history[i][0].upper() + ": " + self.history[i][1] + "\n"

        # print("\n\n\nHISTORY:", hist, "\n______________________\n\n\n")
        return hist

    def request_ai(self, model :str, prompt : str, max_tokens : str, temperature : str) -> str:
        
        response = self.openai.completions.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        clean_response = response.choices[0].text.strip()
        return clean_response


    def get_summary(self) -> str:
        hist_len = len(self.history)
        target_len = CONFIG.HISTORY_DEPTH * 2

        if len(self.history) <= target_len:
            return ""
        summary_end = hist_len - target_len 
        
        raw_summary = " ".join([" ".join(inner_list) for inner_list in self.history[:summary_end]])
        summary = self.request_ai(
            model=CONFIG.OAI_HELPER_MODEL,
            prompt="Summarize the following text: " + raw_summary,
            max_tokens=400,
            temperature=0.2
            )
        # print("\n\n\n\nSUMMARY ####################: \n", summary, "\n\n\n")
        return summary + "\n"
        

        


    def query(self, prompt :str, session_id : str) -> str:
        query = prompt
        print("\n\n\nSESSION_ID:", session_id)

        language = self.detect_language(query)
        print("\n\nidentified language: ", language, "\n\n")

        response = self.openai.completions.create(
            model=CONFIG.OAI_HELPER_MODEL,
            prompt=CONFIG.TRANSLATE_PROMPT.format(query),
            max_tokens=50,
            temperature=0.1,
        )
        brasilian_query = response.choices[0].text.strip()
        # print(f"BRASILIAN-QUERY:", brasilian_query)

        result = self.collection.query(
            query_texts=[brasilian_query],
            n_results=16
        )

        # print(result, "\n\n")

        searchdoc = "\n\n".join(element for block in result['documents'] for element in block)
        # print("\n\nTEXT RETRIEVED:\n\n", searchdoc)

        system_prompt = CONFIG.SYSTEM_PROMPT + "\n\n" + "Summary before chat history:\n" + self.get_summary() + "\nChat history:\n" + self.get_history() + "\nEnd of chat history.\n\n"
        user_prompt = CONFIG.USER_PROMPT.format(language, query)
        assistant_prompt = CONFIG.ASSISTANT_PROMPT.format(searchdoc)

        print("\n\n\nSYSTEM PROMPT ###########:\n", system_prompt, "\n\nUSER_PROMPT ###########:\n", user_prompt, "\n\n")

        # print(f"System Prompt: \n{system_prompt}")


        # non-chat model
        # response = self.openai.completions.create(
        #     model=CONFIG.OAI_MODEL,
        #     prompt= system_prompt + "\n" + assistant_prompt + "\n" + user_prompt,
        #     max_tokens=CONFIG.OAI_MAX_TOKENS,
        #     temperature=CONFIG.OAI_TEMPERATURE,
        # )

        # chat model
        response = self.openai.chat.completions.create(
            model=CONFIG.OAI_MODEL,
            messages=[
                {
                    "role": "system", "content": system_prompt
                },
                {
                    "role": "assistant", "content": assistant_prompt, 
                },
                {
                    "role": "user", "content": user_prompt,
                }
            ],
            stream=False,
            max_tokens=CONFIG.OAI_MAX_TOKENS,
            temperature=CONFIG.OAI_TEMPERATURE,
        )


        # for completion response only
        # clean_response = response.choices[0].text.strip()

        # for chat response only:
        clean_response = response.choices[0].message.content
        self.append_to_history("user", query)
        self.append_to_history("system", clean_response)
        # print ("\n\n", clean_response)
        self.get_history()
        if CONFIG.HISTORY_SUMMARY:
            self.get_summary()

        return clean_response, session_id
