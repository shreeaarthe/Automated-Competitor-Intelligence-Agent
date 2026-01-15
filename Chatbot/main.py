import os
import sys
from dotenv import load_dotenv
from graph import create_graph

# Add the current directory to path just in case
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not found in .env")
        return
    if not os.getenv("TAVILY_API_KEY"):
        print("Error: TAVILY_API_KEY not found in .env")
        return

    print("MarketPulse: Automated Competitor Intelligence Agent")
    print("----------------------------------------------------")
    
    company = input("Enter company name to research: ").strip()
    if not company:
        print("Please enter a valid company name.")
        return

    # Initialize graph
    app = create_graph()

    # Initial state
    initial_state = {"company": company}

    print(f"\nStarting research on {company}...\n")
    
    # Run graph
    try:
        final_state = app.invoke(initial_state)
        print("\n" + "="*50)
        print("FINAL REPORT")
        print("="*50 + "\n")
        print(final_state['report'])
        
        # Optionally save to file
        filename = f"{company.replace(' ', '_')}_report.md"
        with open(filename, "w", encoding='utf-8') as f:
            f.write(final_state['report'])
        print(f"\nReport saved to {filename}")
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
