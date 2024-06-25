from core.qa import get_qa

qa = get_qa()

def oneturn_chat(chat_history: list, question: str):
    return qa.oneturn_chat(question, chat_history)


if __name__ == "__main__":
    pass
