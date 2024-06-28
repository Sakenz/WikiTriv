import wikipediaapi
def fetch_wikipedia_content(topic):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='MyBot/1.0')
    page = wiki_wiki.page(topic)

    if page.exists():
        return page.text
    else:
        return None

if __name__ == "__main__":
    topics = ["Football", "Anime", "Bollywood", "Hollywood", "F1", "Education", "Career"]
    topic = input("Choose a topic: " + ", ".join(topics) + ": ")
    
    if topic in topics:
        content = fetch_wikipedia_content(topic)
        if content:
            with open(f"./data/{topic}.txt", "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Content fetched and saved to {topic}.txt")
        else:
            print("Failed to retrieve content.")
    else:
        print("Invalid topic.")