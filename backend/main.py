import subprocess

def main():
    topics = ["Football", "Anime", "Bollywood", "Hollywood", "F1", "Education", "Career"]
    topic = input("Choose a topic: " + ", ".join(topics) + ": ")
    
    if topic not in topics:
        print("Invalid topic.")
        return
    
    # Scrape Wikipedia
    subprocess.run(["python", "scraper.py"], input=topic.encode(), check=True)
    
    # Generate and ask questions
    subprocess.run(["python", "qa_model.py"], input=(topic + ".txt").encode(), check=True)

if __name__ == "__main__":
    main()
