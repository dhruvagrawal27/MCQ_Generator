import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

from langchain_nvidia_ai_endpoints import ChatNVIDIA
#imporing necessary packages packages from langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
key=os.getenv("NVIDIA_LLAMA2_KEY")


llm = ChatNVIDIA(
  model="meta/llama2-70b",
  api_key=key, 
  temperature=0.45
)

template="""
You are an accomplished educational assessment designer specializing in creating engaging multiple-choice questions (MCQs). 

INPUT TEXT:
{text}

TASK:
Create {number} thought-provoking MCQs based on the provided text, tailored for a {tone} difficulty level.

REQUIREMENTS:
1. Subject Analysis:
   - Identify the primary subject area and specific topics covered
   - Consider the learning objectives evident in the text
   - Align questions with educational standards when applicable

2. Question Design:
   - Create questions that test different cognitive levels (recall, understanding, application, analysis)
   - Include a mix of:
     * Direct concept questions
     * Scenario-based questions
     * Application-oriented questions
     * Critical thinking questions
   - Ensure questions progress from simpler to more complex concepts
   - Avoid repetitive content or question patterns

3. Answer Options:
   - Provide 4 options per question
   - Include one clearly correct answer
   - Create plausible distractors that:
     * Reflect common misconceptions
     * Are grammatically consistent
     * Are similar in length
     * Follow logical ordering (numerical/alphabetical when applicable)

4. Quality Control:
   - Verify all questions are answerable from the provided text
   - Ensure language clarity and accessibility
   - Double-check factual accuracy
   - Avoid cultural or regional bias
   - Include explanations for correct answers
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "tone", "response_json"],
    template=template)


quiz_chain=LLMChain(llm=llm,prompt=quiz_generation_prompt,output_key="quiz",verbose=True)


template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["quiz"], template=template2)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)


# This is an Overall Chain where we run the two chains in Sequence
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)