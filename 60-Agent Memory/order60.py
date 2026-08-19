from google import genai
from dotenv import load_dotenv
import os
import chromadb
load_dotenv()
from pydantic import BaseModel
import uuid

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("Api Key not found")



chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
        name="collection_name",
        configuration={"hnsw": {"space": "cosine"}}

    )
client = genai.Client(api_key=API_KEY)

class Call1(BaseModel):
    found_mem:bool
    answer:str

class Call2(BaseModel):
    memory:list[str]

state = {
        "question":None,
        "context":[],
        "conversation_history":[],
        "found_mem":None,
        "answer":None
    }

while True:

    user_question = input("What is your question: ")

    print("\n=========================================\n")
    print(f"User's question: {user_question}")
    print("\n=========================================\n")

    state["question"] = user_question

    retrieved_context = collection.query(
        query_texts=user_question,
    )

    state["context"] = retrieved_context["documents"]

    print("\n=========================================\n")
    print(f"Retrived context from vector db: {retrieved_context}")
    print("\n=========================================\n")


    print("\n=========================================\n")
    print(f"Conversation History: {state['conversation_history']}")
    print("\n=========================================\n")
    

    
    prompt1 = f"""
    Answer the user's question using the context.

    <user's question>
        {state['question']}
    </user's question>

    Below is the context and conversation history. There are 3 scenarios for the context:
    scenario 1: The context and conversation history may contain useful info that could proteintially give your more context and help you answer the question better.
    scenario 2: The context and conversation history can contain information but it wont be useful (it will either stray from the scope or have nothing to do with the question)
    scenario 3: The context and conversation history is/are empty

    So you would need to make the judgement or whether or not to use the context and conversation history (if provided), the context and conversation history should only be taken into consideration if it helps answer the question.

    <context>
        {state['context']}
    </context>

    Below is the previous conversation history:

    <conversation history>
        {state['conversation_history']}
    </conversation history>


    You would need to return a json exactly in this format:
    {{
        "found_mem":"**Fill this in with True or False, True if you believe there memory worth keeping, the memory has to be based on the current interaction, not the previous interactions, the previous interactions can ofc provide support for long term memory, BUT the long term memory HAS to be found in the current user's message/question, it has to be a long-term worth keeping that can be used for future conversations. Examples of long term memory: User's favorite language, User's occupation, User preferences, User goals, Recurring interests, etc. Fill in with False if you believe nothing is worth remember/storing for future conversations**",
        "answer":"**Fill this in with the answer to the user's question**"
    }}

    **DO NOT INCLUDE ANY QUOTES THE BEGINNING OR THE END OF YOUR RESPONSE**
    """

    
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt1
    )

    call1 = Call1.model_validate_json(interaction.output_text)

    print("\n=========================================\n")
    print(f"Call1 found memory?: {call1.found_mem}")
    print("\n=========================================\n")

    print("\n=========================================\n")
    print(f"LLM Answer: {call1.answer}")
    print("\n=========================================\n")

    state["found_mem"] = call1.found_mem
    state["answer"] = call1.answer
    state["conversation_history"].append(
        {
            "user_message":user_question,
            "LLM_response":call1.answer

        }
    )


    print("\n=========================================\n")
    print(f"Conversation history updated: {state["conversation_history"]}")
    print("\n=========================================\n")



    if state["found_mem"] == True:
        prompt2 = f"""
        Below you will find the user's question and the answer to the user's question.
        Your primarily goal is to seek out if any memories are worth keeping for furture conversation with the user.
        **You would need at minimum atleast 1 memory.**
        These are long-term memories (memories that are unlikely to change soon)
        ex. User's favorite language

        ex. User's occupation

        ex. User preferences

        ex. User goals

        ex. Recurring interests

        The memory has to be based on the current interaction, not the previous interactions, the previous interactions can ofc provide support for long term memory, BUT the long term memory HAS to be found in the current user's message/question



        Below is the previous conversation history:

            <conversation history>
                {state['conversation_history']}
            </conversation history>

            
         <user's question>
            {state['question']}
        </user's question>



        You would need to return json exactly like this:

        {{
            "memory":["*Replace this with the long term memory*", "*Replace this with the long term memory*", "*Replace this with the long term memory*", etc...]
        }}

        **DO NOT INCLUDE ANY QUOTES THE BEGINNING OR THE END OF YOUR RESPONSE**
        
        """

        memory_find = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt2
        )

        call2 = Call2.model_validate_json(memory_find.output_text)

        print("\n=========================================\n")
        print(f"LLM Answer #2: {call2.memory}")
        print("\n=========================================\n")
        

        for item in call2.memory:
            id = uuid.uuid4()
            collection.add(
                ids=[str(id)],
                documents=[item],
            )

        







    