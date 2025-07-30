import dotenv
import os
import openai
import csv
import io
from typing import List

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_completion(prompt, model="gpt-4o-search-preview"):
    system_prompt = """
    You are a helpful assistant. You are given a leetcode problem and you need to generate a flashcard for it.
    
    The flashcard should have the following content:
    
    FRONT section should contain:
    - Problem title (leetcode number, title, difficulty)
    - Problem description
    - Sample test cases
    
    BACK section should contain:
    - Steps for brute force solution
    - Time complexity for brute force solution
    - Steps for optimized solution
    - Time complexity for optimized solution
    - Key points to remember for the optimized solution
    - Don't include code in the flashcard
    
    IMPORTANT: Return ONLY a single CSV row with exactly 2 columns (Front,Back). 
    Format: "front content","back content"
    
    Example format:
    "Two Sum (1, Easy): Find two numbers that add up to target. Input: [2,7,11,15], target=9. Output: [0,1]","Brute Force: Check all pairs O(n²). Optimized: Use hashmap to store complements O(n). Key: Store value->index mapping while iterating."
    
    Do NOT include CSV headers. Return only the data row.
    """
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

def process_questions_to_csv(questions: List[str], output_filename: str = "leetcode_flashcards.csv"):
    """
    Process a list of LeetCode questions and save them as flashcards in CSV format.
    
    Args:
        questions: List of question names/numbers to process
        output_filename: Name of the output CSV file
    """
    all_flashcards = []
    
    print(f"Processing {len(questions)} questions...")
    
    for i, question in enumerate(questions, 1):
        print(f"Processing question {i}/{len(questions)}: {question}")
        
        try:
            # Get the completion for this question
            completion = get_completion(question).strip()
            
            # Parse the CSV response - should be a single row
            csv_reader = csv.reader(io.StringIO(completion))
            rows = list(csv_reader)
            
            # Process the response
            if rows and len(rows) > 0:
                # Take the first valid row with 2 columns
                for row in rows:
                    if len(row) >= 2 and row[0].strip() and row[1].strip():
                        # Clean up the front and back content
                        front = row[0].strip().strip('"')
                        back = row[1].strip().strip('"')
                        all_flashcards.append([front, back])
                        break
                else:
                    # If no valid row found, create a fallback entry
                    all_flashcards.append([f"Question: {question}", f"Error: Could not parse response - {completion[:100]}..."])
            else:
                # Empty response
                all_flashcards.append([f"Question: {question}", "Error: Empty response from AI"])
            
        except Exception as e:
            print(f"Error processing question '{question}': {e}")
            # Add error entry to maintain record
            all_flashcards.append([f"Error: {question}", f"Failed to generate flashcard: {str(e)}"])
    
    # Write all flashcards to CSV file
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Front', 'Back'])
        
        # Write all flashcard data
        writer.writerows(all_flashcards)
    
    print(f"Successfully saved {len(all_flashcards)} flashcards to {output_filename}")
    return output_filename

def test_single_question(question: str):
    """
    Test function to see the output format for a single question.
    
    Args:
        question: A single LeetCode question to test
    """
    print(f"Testing question: {question}")
    print("=" * 50)
    
    try:
        completion = get_completion(question).strip()
        print("Raw AI Response:")
        print(completion)
        print("\n" + "=" * 50)
        
        # Parse the CSV
        csv_reader = csv.reader(io.StringIO(completion))
        rows = list(csv_reader)
        
        if rows and len(rows) > 0:
            for i, row in enumerate(rows):
                if len(row) >= 2 and row[0].strip() and row[1].strip():
                    front = row[0].strip().strip('"')
                    back = row[1].strip().strip('"')
                    print(f"Parsed CSV Row {i+1}:")
                    print(f"FRONT: {front}")
                    print(f"BACK: {back}")
                    break
        else:
            print("Could not parse CSV from response")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test with a single question first
    print("Testing single question format:")
    test_single_question('680. Valid Palindrome II')
    
    print("\n" + "="*70 + "\n")

    # parse the problem name in each line
    problems = []
    with open('leetcode_problems.txt', 'r') as file:
        for line in file:
            problems.append(line.strip())
    
    # # Example usage with multiple questions
    # questions = [
    #     '680. Valid Palindrome II',
    #     '1. Two Sum'
    # ]
    
    # Process questions and save to CSV
    output_file = process_questions_to_csv(problems, "leetcode_flashcards.csv")
    print(f"Flashcards saved to: {output_file}")