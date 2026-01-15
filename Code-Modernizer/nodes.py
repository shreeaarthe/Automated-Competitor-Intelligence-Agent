import os
import sys
import tempfile
import subprocess
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# --- LLM Setup ---
llm = ChatGroq(model="llama-3.3-70b-versatile") # Using capable model

# --- Node 1: Translator ---
def translator(state):
    input_code = state['input_code']
    source_lang = state.get('source_lang', 'Java')
    target_lang = state.get('target_lang', 'Python')
    iterations = state.get('iterations', 0)
    errors = state.get('errors', [])
    
    print(f"--- Translator Node (Iteration {iterations}) ---")
    
    if errors:
        print(f"Fixing errors: {errors}")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert code migrator and fixer. You previously converted code, but it had errors. Fix the code based on the error message. Output ONLY the fixed Python code, no markdown, no explanations."),
            ("human", "Original Code:\n{input_code}\n\nPrevious Generated Code:\n{generated_code}\n\nErrors:\n{errors}")
        ])
        chain = prompt | llm | StrOutputParser()
        # We need the previous generated code from state if we are fixing
        previous_code = state.get('generated_code', '')
        generated_code = chain.invoke({
            "input_code": input_code, 
            "generated_code": previous_code, 
            "errors": "\n".join(errors)
        })
    else:
        print(f"Translating {source_lang} to {target_lang}...")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert code migrator. Convert the following {source_lang} code to idiomatic {target_lang}. Output ONLY the {target_lang} code, no markdown, no explanations."),
            ("human", "{input_code}")
        ])
        chain = prompt | llm | StrOutputParser()
        generated_code = chain.invoke({"source_lang": source_lang, "target_lang": target_lang, "input_code": input_code})
    
    # Strip markdown code blocks if present
    generated_code = generated_code.replace("```python", "").replace("```", "").strip()
    
    return {"generated_code": generated_code, "iterations": iterations + 1}

# --- Node 2: Reviewer (Pylint/Syntax Check) ---
def reviewer(state):
    generated_code = state['generated_code']
    print(f"--- Reviewer Node ---")
    
    errors = []
    
    # Create a temporary file to run pylint/syntax check
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
        tmp.write(generated_code)
        tmp_path = tmp.name
        
    try:
        # 1. Syntax Check (Fastest)
        subprocess.check_call([sys.executable, "-m", "py_compile", tmp_path], stderr=subprocess.STDOUT)
        
        # 2. Pylint (Deeper check) - Optional, can be strict. 
        # For this demo, let's stick to syntax error + critical pylint errors if we want, 
        # but let's just do syntax first to ensure it runs.
        # If we want to capture pylint output:
        # result = subprocess.run(["pylint", "-E", tmp_path], capture_output=True, text=True) # -E for errors only
        # if result.returncode != 0:
        #    errors.append(result.stdout)
        
        print("Code is valid.")
        
    except subprocess.CalledProcessError as e:
        # Syntax error caught
        print("Syntax Error found!")
        # To get the actual error message, we might need to run it safely
        try:
             subprocess.check_output([sys.executable, "-m", "py_compile", tmp_path], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as sub_e:
             errors.append(sub_e.output.decode() if sub_e.output else "Unknown syntax error")
    finally:
        os.remove(tmp_path)
        
    return {"errors": errors}
