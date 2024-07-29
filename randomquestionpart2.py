import random
import re
kq = []

def choose_random_topic(file_paths):
    # Choose a random file from the provided file paths
    chosen_file = random.choice(file_paths)

    with open(chosen_file, 'r', encoding='utf-8') as file:
        topics = file.read().split('topic_')

    chosen_topic = random.choice(topics).strip()
    matches = re.findall(r'\[([^]]+)\]', chosen_topic)

    if matches:
        elements = matches[0].split(',')
        elements = [element.strip() for element in elements]

    s = elements[1:]
    kq.append(elements[0])
    if len(s) <= 3:
        for i in s:
            kq.append(i)
    else:
        selected_elements = random.sample(s, 4)
        for i in selected_elements:
            kq.append(i)
    for i in kq:
        print(i)


def main():
    # Example usage
    file_paths = ['script/part2.txt']
    choose_random_topic(file_paths)

if __name__ == "__main__":
    main()
