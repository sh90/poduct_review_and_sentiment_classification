import tempfile
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import os
from agent import extract_code_from_answer

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_unit_tests(code_snippet, model="gpt-4o-mini"):
    prompt = (
        "Write comprehensive Python unittest test cases for the following code. "
        "Return only the test code, all the necessary imports and function for which the test cases are generated, wrapped in a single code block.\n\n"
        f"{code_snippet}"
    )

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(model=model,
                                              messages=[{"role": "system", "content": ""},{"role": "user", "content": prompt}],
                                              temperature=0)

    answer = response.choices[0].message.content
    code, _ = extract_code_from_answer(answer)
    return code or answer

def run_unit_tests(test_code):
    with tempfile.NamedTemporaryFile(suffix="_test.py", delete=False, mode='w',  encoding='utf-8') as tf:
        tf.write(test_code)
        test_path = tf.name
    try:
        result = subprocess.run(
            ["python", test_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        return result.stdout + result.stderr
    except Exception as e:
        return f"Error running tests: {e}"

def suggest_missing_test_cases(code_snippet, test_code, model="gpt-4o-mini"):
    prompt = (
        "Given the following function/class and its unit tests, list any missing important test scenarios or edge cases. "
        "Be specific and return as bullet points.\n\n"
        f"Function/class:\n{code_snippet}\n\nUnit tests:\n{test_code}"
    )
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(model=model,
                                              messages=[{"role": "system", "content": ""},{"role": "user", "content": prompt}],
                                              temperature=0)

    return response.choices[0].message.content

def refine_code_with_test_failures(code_snippet, test_code, test_results, model="gpt-4o"):
    prompt = (
        "You are a coding assistant. Here is a function and its test suite. "
        "Some tests are failing, as shown in the output below. "
        "Please modify the function so that all tests pass. "
        "Return only the corrected function code in a single code block.\n\n"
        "Function code:\n"
        f"{code_snippet}\n\n"
        "Test code:\n"
        f"{test_code}\n\n"
        "Test output:\n"
        f"{test_results}\n"
    )
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    code, _ = extract_code_from_answer(response.choices[0].message.content)
    return code or response.choices[0].message.content

def regenerate_tests_with_feedback(code_snippet, old_tests, feedback, model="gpt-4o"):
                prompt = (
                    "Given this function:\n"
                    f"{code_snippet}\n\n"
                    "And these existing unit tests:\n"
                    f"{old_tests}\n\n"
                    "And these suggestions for improvement:\n"
                    f"{feedback}\n\n"
                    "Please update or regenerate the test suite to cover all feedback and missing cases. "
                    "Return only the complete, improved test code in a single code block."
                )
                client = OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                )
                code, _ = extract_code_from_answer(response.choices[0].message.content)
                return code or response.choices[0].message.content
