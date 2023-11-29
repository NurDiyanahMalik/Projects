import json
from difflib import get_close_matches

def load_knowledge(file_path:str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge(file_path:str,data:dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def best_match_found(user_question:str,questions:list[str]) -> str | None:
    matches: list = get_close_matches(user_question,questions,n=1,cutoff=0.5)
    return matches[0] if matches else None

def get_answer(question:str,knowledge_base:dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot():
    knowledge_base: dict = load_knowledge('knowledge.json')

    while(True):
        user_input: str = input('Enter Question: ')

        if user_input.lower() == 'quit':
            break
          
        best_match: str | None = best_match_found(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer(best_match,knowledge_base)
            print(f'Chatbot: {answer}')

        else:
            print('Bot: Sorry, I do not understand your question.')
            new_answer: str = input('Type the answer')

            knowledge_base["questions"].append({"question":user_input,"answer":new_answer})
            save_knowledge('knowledge.json', knowledge_base)
            print(f'Chatbot: New response recorded')

if __name__ == '__main__':
    chat_bot()
