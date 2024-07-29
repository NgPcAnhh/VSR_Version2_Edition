import random

# Hàm chọn ngẫu nhiên câu hỏi từ một list cho trước
def select_questions_from_list(question_list, num_questions=2):
    return random.sample(question_list, num_questions)

# Hàm đọc nội dung từ file và trả về biến topics (nếu có)
def read_topics_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    topics = {}
    exec(content, globals(), topics)
    return topics.get('topics', {})

def main():
    # Các frame câu hỏi và subframe
    frame1 = [
        "Which town or city do you live in now?","Are there any things you don’t like about your area? (What are they?)","Do you think you will continue to live there for a long time? (Why? Why not?)","What are some changes in the area recently?","Do you live in a house or an apartment?","What is your favourite room in your home? (Why?)","What things make your home pleasant to live in? (Why?)","Are the people in your neighbourhood nice and friendly?","Do you know any of your neighbours?","Is the place where you live quiet or noisy?",
    ]

    frame2 = {
        "work": [
            "What kind of work do you do?","What do you find most interesting about your work? (Why?)","Which is more important to you – the people you work with or the work you do? (Why?)","Do you work best in the morning or the afternoon? (Why?)","Would you like to change the place you work? (Why?)",
        ],
        "study": [
            "What do you study?","What do you find most interesting about your studies? (Why?)","Which is more important to you—the teachers or the other students on your course? (Why?)","How much time do you spend studying every week?","How do you usually travel to the city where you study?","Do you study best in the morning or the afternoon? (Why?)","Have you always wanted to study this subject/ these subjects (Why/ Why not?)",
        ],
    }

    # Chọn ngẫu nhiên từ frame hoặc subframe
    n = random.randint(1, 2)
    if n == 1:
        selected_questions = select_questions_from_list(frame1)
    else:
        selected_subframe = random.choice(list(frame2.values()))
        selected_questions = select_questions_from_list(selected_subframe)

    # In ra các câu hỏi đã chọn
    for i, question in enumerate(selected_questions, 1):
        print(f"{question}")

    # Đọc topics từ file và chọn ngẫu nhiên câu hỏi từ các topic
    file_path = 'script/part1.py'
    topics = read_topics_from_file(file_path)

    if isinstance(topics, dict) and topics:
        selected_topics = random.sample(list(topics.keys()), 4)
        questions = []

        for topic in selected_topics:
            if isinstance(topics[topic], list):
                selected_questions = select_questions_from_list(topics[topic], 2)
                questions.extend(selected_questions)

        # In ra các câu hỏi đã chọn từ topics
        for i, question in enumerate(questions, 1):
            print(f"{question}")

if __name__ == "__main__":
    main()
