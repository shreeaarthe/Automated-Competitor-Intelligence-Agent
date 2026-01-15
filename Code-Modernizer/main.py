import os
import sys
from dotenv import load_dotenv
from graph import create_graph

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not found in .env")
        return

    print("Code Modernizer: Legacy Code Migration Agent")
    print("--------------------------------------------")
    print("Enter your Java code snippet below (press Ctrl+Z then Enter to finish):")
    
    # Read multi-line input
    try:
        lines = []
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
        
    input_code = "\n".join(lines)
    
    if not input_code.strip():
        print("No code provided.")
        return

    # Initialize graph
    app = create_graph()

    # Initial state
    initial_state = {
        "input_code": input_code,
        "source_lang": "Java",
        "target_lang": "Python",
        "iterations": 0,
        "errors": []
    }

    print(f"\nStarting migration...\n")
    
    # Run graph
    try:
        final_state = app.invoke(initial_state)
        print("\n" + "="*50)
        print("FINAL PYTHON CODE")
        print("="*50 + "\n")
        print(final_state['generated_code'])
        
        if final_state.get('errors'):
             print("\nNote: Some errors could not be resolved after max retries.")
             print(final_state['errors'])
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
