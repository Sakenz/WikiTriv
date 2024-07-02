import wikipediaapi
from transformers import pipeline

def scrape_wikipedia(topic):
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(topic)
    return page.text

def generate_qa_pairs(content):
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    sentences = content.split('. ')
    qa_pairs = []
    for sentence in sentences:
        if len(sentence) < 30:
            continue
        qa = qa_pipeline(question="What is this sentence about?", context=sentence)
        if qa['score'] > 0.7:
            qa_pairs.append({
                'question_text': qa['question'],
                'correct_answer': qa['answer'],
                'option_1': 'Option 1',
                'option_2': 'Option 2',
                'option_3': 'Option 3',
                'option_4': qa['answer']
            })
    return qa_pairs
