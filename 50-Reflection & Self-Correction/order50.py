from google import genai
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("api key not found")


original_question = input("What is your question: ")

state = {}

state["original_question"]=original_question

client = genai.Client(api_key=API_KEY)

plan_prompt = f"""
    Below is the user's question, its a decision making question:

    <user's question>
        {original_question}
    </user's question>

    To answer this question, we need to create a plan, the plan includes all the requirements to thoroughly answer this question.
    The plan should be in a json format exactly like this:

    {{
        "plan":[requirement1, requirement2, requiremesnt3....]
    }}

    replace requirement1, requirement2, requirement3... with your actual requirements needed to answer this question.
    You need 5 requiements (max and min)

    DO NOT INCLUDE QUOTES AT THE TOP AND BOTTOM OF YOUR RESPONSE

"""

class Plan(BaseModel):
    plan:list[str]

try:
    interaction1_plan = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=plan_prompt
    )
except Exception as e:
    print(str(e))


plan = Plan.model_validate_json(interaction1_plan.output_text)

state["plan"] = plan.plan




#-----api call 2-------



req_question = f"""
    Provide your question and within your question provide as much information about these are possible
    Answer as many of these are you can:
    requirement 1: {state['plan'][0]}\n
    requirement 2: {state['plan'][1]}\n
    requirement 3: {state['plan'][2]}\n
    requirement 4: {state['plan'][3]}\n
    requirement 5: {state['plan'][4]}\n

    Provide your question and answers in one line


"""

question = input(req_question)

requirements_prompt = f"""
    Below is the user's question:

    <user's question>
        {question}
    </user's question>


    The user has provided a question and as much background information as possible below is all the information required to answer the user's question,
    you can ONLY answer the user's question if all this information is met

    <requirements>
        {state['plan']}
    </requirements?



    For some of these requirements you would need the user's input and for others you can use external information to find out the answer.

    Examples:
        1. requirement = Need to know background of the user, does he or she have experience with Computer Science? 
        **We need user's input for this question, we cannot find the information about user's background from external sources

        2. requirement - Assess the current job market in AI
        **We dont need the user's input, we can look at external sources/ statistics to find out how the job market is performing

    You need to return a json exactly like this:

    {{
        "hit_all_requirements":True/False (either True or False)
        "information":["**replace this with information that satisfies requirement1**", "**replace this with information that satisfies requirement2**",... ]

                    
    }}

    If the requirement cannot be hit either with user's input or external information -  "hit_all_requirements" is False
    and in for "information":[**replace this with information that satisfies requirement1**, **replace this with information that satisfies requirement2**, null, **replace this with information that satisfies requirement4**, ....]


    DO NOT INCLUDE QUOTES AT THE TOP AND BOTTOM OF YOUR RESPONSE


"""

class Requirements(BaseModel):
    hit_all_requirements:bool
    information:list[str|None]

try:
    interaction2_requirements = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=requirements_prompt
    )
except Exception as e:
    print(str(e))


requirements = Requirements.model_validate_json(interaction2_requirements.output_text)

state["requirements"] = {"hit_all_requirements":requirements.hit_all_requirements, "information":requirements.information}


#---api_call #3----
class Final(BaseModel):
    verdict:str


final_prompt = f"""
    Here is the user's question:

    <user's question>
        {state['original_question']}
    </user's question>


    Below are all the requirements and the information for each requiment to answer the question:

    <requirements>
        {state['plan']}
    </requirements>


    <information>
        {state['requirements']}
    </information>

    Using all of this information, you need to return a json with your decision of explicitly answering the user's question and your explanation
    Follow this json format exactly:

    {{
        "verdict":"**Replace this with your explanation**"
    }}

    DO NOT INCLUDE QUOTES AT THE TOP AND BOTTOM OF YOUR RESPONSE

"""

final_interaction = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input=final_prompt
)



final_verdict = Final.model_validate_json(final_interaction.output_text)

state["final_verdict"] = final_verdict.verdict


print(f"\n\nGEMINI FINAL VERDICT: {state["final_verdict"]}")



