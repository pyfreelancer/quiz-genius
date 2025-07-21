# utils/ai_generator.py
import os
import json
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st # For st.error and st.warning

# Load the Gemini key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", # Using gemini-1.5-flash for efficiency
    google_api_key=GEMINI_API_KEY,
    temperature=0.2 # Slightly increased temperature for more varied questions
)

# Prompt template for MCQ generation
template = """
You are a professional teacher. Generate {num_questions} Multiple Choice Questions (MCQs) based on the following text.
Each question should have:
- A clear question text.
- Exactly 4 options (A, B, C, D) provided as a list of strings.
- The correct answer as a string, which must be one of the provided options.
- A category for the question.
- A difficulty level (Easy, Medium, or Hard).

Ensure the output is a JSON array of objects, strictly adhering to the following schema.
Do NOT include any additional text or markdown outside the JSON array.

JSON Schema:
[
  {{
    "question": "string",
    "options": ["string", "string", "string", "string"],
    "correct_answer": "string",
    "category": "string",
    "difficulty": "string"
  }},
  // ... more question objects
]

Text to generate questions from:
{text}

Number of questions to generate: {num_questions}
Desired Difficulty: {difficulty}
Desired Category: {category} (If 'None' or empty, infer a relevant category from the text.)
"""

prompt = PromptTemplate(
    input_variables=["text", "num_questions", "difficulty", "category"],
    template=template
)

# LLM Chain
chain = LLMChain(llm=llm, prompt=prompt)

# Function to call Gemini and get MCQs - RENAMED TO generate_mcqs
def generate_mcqs(text: str, num_questions: int, difficulty: str, category: str) -> list:
    """
    Generates MCQs from a given text using the AI model.

    Args:
        text (str): The input text to generate questions from.
        num_questions (int): The number of questions to generate.
        difficulty (str): The desired difficulty level (Easy, Medium, Hard).
        category (str): The desired category.

    Returns:
        list: A list of dictionaries, each representing an MCQ.
    """
    if not GEMINI_API_KEY:
        st.error("Gemini API Key not found. Please set it in your .env file.")
        return []

    try:
        # Ensure category is not None, convert to empty string if so for prompt
        category_for_prompt = category if category else "General" # Default to "General" if empty

        output = chain.run(
            text=text,
            num_questions=num_questions,
            difficulty=difficulty,
            category=category_for_prompt
        )
        
        # --- FIX: Remove Markdown code block fences ---
        if output.strip().startswith("```json") and output.strip().endswith("```"):
            output = output.strip()[len("```json"):].strip()[:-len("```")].strip()
        # --- END FIX ---

        # Attempt to parse the JSON output
        mcqs = json.loads(output)
        
        # Basic validation of the generated MCQs
        validated_mcqs = []
        for mcq in mcqs:
            # Check for required keys and correct types
            if all(k in mcq and isinstance(mcq[k], str) for k in ["question", "correct_answer", "category", "difficulty"]) \
               and "options" in mcq and isinstance(mcq["options"], list) and len(mcq["options"]) == 4:
                
                if mcq["correct_answer"] in mcq["options"]:
                    validated_mcqs.append(mcq)
                else:
                    st.warning(f"AI generated an MCQ with correct answer not in options. Skipping: {mcq.get('question', 'N/A')}")
            else:
                st.warning(f"AI generated an invalid MCQ format. Skipping: {mcq}")
        
        return validated_mcqs
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON from AI response. This might be due to an invalid API key or a malformed response from the model. Details: {e}. Raw AI Output: '{output}'") # Added raw output print
        print(f"AI Output (problematic): {output}") # For developer debugging
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred during MCQ generation: {e}. Please check your API key and try again.")
        print(f"An unexpected error occurred during MCQ generation: {e}") # For developer debugging
        return []
