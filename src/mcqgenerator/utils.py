import os
import PyPDF2
import json
import traceback
import re

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )

def get_table_data(quiz_str):
    try:
        def parse_quiz_to_json(quiz_text):
            # Initialize the result dictionary
            result = {}

            # Split the text into individual questions
            questions = quiz_text.split("\n\n")

            current_question = None

            for question in questions:
                if not question.strip():
                    continue

                # Check if this line starts with a number followed by a period
                match = re.match(r'(\d+)\.\s+(.*)', question)
                if match:
                    question_num = match.group(1)
                    question_text = match.group(2)

                    # Initialize the question dictionary
                    current_question = {
                        "mcq": question_text,
                        "options": {},
                        "correct": ""
                    }

                    # Add the question to the result
                    result[question_num] = current_question

                # Parse options
                option_matches = re.finditer(r'([a-d])\)\s+(.*?)(?=\n[a-d]\)|$|\nCorrect answer)', question, re.DOTALL)
                for option_match in option_matches:
                    option_letter = option_match.group(1)
                    option_text = option_match.group(2).strip()
                    if current_question:
                        current_question["options"][option_letter] = option_text

                # Parse correct answer
                correct_match = re.search(r'Correct answer:\s+([a-d])\)\s+(.*?)$', question, re.MULTILINE)
                if correct_match and current_question:
                    current_question["correct"] = correct_match.group(1)

            return result

        # Parse the quiz text to JSON
        result_json = parse_quiz_to_json(quiz_str)

        # Convert to formatted JSON string
        formatted_json = json.dumps(result_json, indent=4)
        # convert the quiz from a str to dict
        quiz_dict = json.loads(formatted_json)
        quiz_table_data = []

        # iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join([
                f"{option}-> {option_value}" 
                for option, option_value in value["options"].items()
            ])

            correct = value["correct"]
            quiz_table_data.append({
                "MCQ": mcq,
                "Choices": options,
                "Correct": correct
            })

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False