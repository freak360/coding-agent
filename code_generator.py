# code_generator.py
from openai import OpenAI
import os
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# # OpenAI API setup
# api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key='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')

def generate_code(prompt):
    """
    Generates code using OpenAI GPT-4 model based on a prompt.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.6,
            messages=[
                {"role": "system", "content": "You are an expert in programming who knows all the computer languages."},
                {"role": "user", "content": prompt},
            ]
        )
        generated_code = completion.choices[0].message.content
        return generated_code.strip()
    except Exception as e:
        print(f"Error while generating code: {str(e)}")
        return e

def save_code_to_file(code, filename='generated_code.py'):
    with open(filename, 'w') as f:
        f.write(code)
    print(f"Code saved to {filename}")

if __name__ == "__main__":
    # Example prompt
    prompt = "Write a Python function that calculates the sum of two numbers."
    code = generate_code(prompt)
    save_code_to_file(code)
