from transformers import pipeline
import random
import re

# Pre-defined questions based on the topic
def generate_questions(topic):
    questions_dict = {
        "Football": [
            "What is football?",
            "Who are some famous football players?",
            "What are the rules of football?",
            "How is football played?",
            "What are some major football tournaments?"
        ],
        "Anime": [
            "What is anime?",
            "Who are some famous anime characters?",
            "What are some popular anime series?",
            "How is anime created?",
            "What is the history of anime?"
        ],
        "Bollywood": [
            "What is Bollywood?",
            "Who are some famous Bollywood actors?",
            "What are some popular Bollywood movies?",
            "How did Bollywood evolve?",
            "What are some major Bollywood awards?"
        ],
        "Hollywood": [
            "What is Hollywood?",
            "Who are some famous Hollywood actors?",
            "What are some popular Hollywood movies?",
            "How did Hollywood evolve?",
            "What are some major Hollywood awards?"
        ],
        "F1": [
            "What is F1?",
            "Who are some famous F1 drivers?",
            "What are the rules of F1?",
            "How is an F1 race conducted?",
            "What are some major F1 races?"
        ],
        "Education": [
            "What is education?",
            "What are some types of education?",
            "What is the importance of education?",
            "How has education evolved over time?",
            "What are some challenges in education?"
        ],
        "Career": [
            "What is a career?",
            "How can one choose a career?",
            "What are some popular career paths?",
            "What is career development?",
            "What are some challenges in career progression?"
        ]
    }
    return questions_dict.get(topic, ["What is this topic about?"])

def generate_answers(context, question):
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    answer = qa_pipeline(question=question, context=context)
    return answer['answer']

def generate_distractors(context, correct_answer):
    sentences = re.split(r'(?<=[.!?]) +', context)
    distractors = [sentence for sentence in sentences if correct_answer not in sentence]
    distractors = random.sample(distractors, min(3, len(distractors)))
    distractors.append(correct_answer)
    random.shuffle(distractors)
    return distractors

def ask_questions(questions, context):
    score = 0
    total_questions = len(questions)
    
    for question in questions:
        print("\nQuestion:", question)
        correct_answer = generate_answers(context, question)
        options = generate_distractors(context, correct_answer)

        for i, option in enumerate(options):
            print(f"{i+1}. {option}")

        user_answer = input("Choose the correct option (1/2/3/4): ")
        
        if options[int(user_answer)-1] == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer is: {correct_answer}")
    
    print(f"\nYour score: {score}/{total_questions}")

if __name__ == "__main__":
    topic = input("Enter the topic (e.g., Football): ").replace(".txt", "")
    
    try:
        with open(f"backend/data/{topic}.txt", "r", encoding="utf-8") as file:
            content = file.read()
        
        questions = generate_questions(topic)
        ask_questions(questions, content)
    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")