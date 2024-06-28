from transformers import pipeline

def generate_qa_pairs(text):
    qa_pipeline = pipeline("question-generation")
    return qa_pipeline(text)

def ask_questions(qa_pairs):
    score = 0
    total_questions = len(qa_pairs)
    
    for qa_pair in qa_pairs:
        print("\nQuestion:", qa_pair['question'])
        user_answer = input("Your answer: ")
        
        if user_answer.lower() == qa_pair['answer'].lower():
            print("Correct!")
            score += 1
        else:
            print("Incorrect. The correct answer is:", qa_pair['answer'])
    
    print(f"\nYour score: {score}/{total_questions}")

if __name__ == "__main__":
    topic = input("Enter the topic file (e.g., Football.txt): ")
    
    try:
        with open(topic, "r", encoding="utf-8") as file:
            content = file.read()
        
        qa_pairs = generate_qa_pairs(content)
        ask_questions(qa_pairs)
    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
