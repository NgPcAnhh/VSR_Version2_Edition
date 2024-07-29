import random
import re

# Global list to store selected elements
kq = []


# Function to choose a random topic from provided file paths
def choose_random_topic(file_paths):
    chosen_file = random.choice(file_paths)
    with open(chosen_file, 'r', encoding='utf-8') as file:
        topics = file.read().split('topic_')

    chosen_topic = random.choice(topics).strip()
    matches = re.findall(r'\[([^]]+)\]', chosen_topic)

    if matches:
        elements = [element.strip() for element in matches[0].split(',')]
        kq.append(elements[0])
        kq.extend(elements[1:] if len(elements[1:]) <= 3 else random.sample(elements[1:], 4))


# Function to select random questions from a given list
def select_questions_from_list(question_list, num_questions=2):
    return random.sample(question_list, num_questions)


# Function to read topics from a file and return the 'topics' variable if it exists
def read_topics_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    topics = {}
    exec(content, globals(), topics)
    return topics.get('topics', {})


def main():
    output = []

    # Question frames and subframes
    frame1 = [
        "Which town or city do you live in now?",
        "Are there any things you don’t like about your area? (What are they?)",
        "Do you think you will continue to live there for a long time? (Why? Why not?)",
        "What are some changes in the area recently?",
        "Do you live in a house or an apartment?", "What is your favourite room in your home? (Why?)",
        "What things make your home pleasant to live in? (Why?)",
        "Are the people in your neighbourhood nice and friendly?",
        "Do you know any of your neighbours?", "Is the place where you live quiet or noisy?"
    ]

    frame2 = {
        "work": [
            "What kind of work do you do?", "What do you find most interesting about your work? (Why?)",
            "Which is more important to you – the people you work with or the work you do? (Why?)",
            "Do you work best in the morning or the afternoon? (Why?)",
            "Would you like to change the place you work? (Why?)"
        ],
        "study": [
            "What do you study?", "What do you find most interesting about your studies? (Why?)",
            "Which is more important to you—the teachers or the other students on your course? (Why?)",
            "How much time do you spend studying every week?", "How do you usually travel to the city where you study?",
            "Do you study best in the morning or the afternoon? (Why?)",
            "Have you always wanted to study this subject/ these subjects (Why/ Why not?)"
        ],
    }

    # Randomly select from frame or subframe
    if random.randint(1, 2) == 1:
        output.extend(select_questions_from_list(frame1))
    else:
        output.extend(select_questions_from_list(random.choice(list(frame2.values()))))

    # Read topics from file and randomly select questions from topics
    file_path = 'done/part1.py'
    topics = read_topics_from_file(file_path)

    if topics:
        selected_topics = random.sample(list(topics.keys()), 4)
        for topic in selected_topics:
            if isinstance(topics[topic], list):
                output.extend(select_questions_from_list(topics[topic]))

    # Choose random topic and add to output
    choose_random_topic(['done/part2.txt'])
    output.extend(kq)

    return output


if __name__ == "__main__":
    output = main()

    # Additional code to extract elements from the 'output' list
    for question in output:
        print(question)
