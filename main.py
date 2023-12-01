
#Пока с костылями
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

root = Tk()
root.title("Question generator")
root.geometry("1300x500")

root.grid_rowconfigure(index=0, weight=1)
root.grid_columnconfigure(index=0, weight=1)
root.grid_columnconfigure(index=1, weight=1)
root.grid_columnconfigure(index=2, weight=1)
root.grid_columnconfigure(index=3, weight=1)

text_editor = Text()
text_editor.grid(column=0, columnspan=2, row=0)

questions_text_editor = Text()
questions_text_editor.grid(column=2, columnspan=2, row=0)


# ????????? ???? ? ????????? ????
def open_file():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        with open(filepath, "r", encoding = "utf-8") as file:
            text = file.read()
            text_editor.delete("1.0", END)
            text_editor.insert("1.0", text)
            print("Проверка1")
            return text


def chat_questions(user_input, chat):
    messages = [SystemMessage(
        content='Ты преподаватель, твоя цель сгенерировать 5 - 6 вопросов по тексту, который ведёт пользователь, так чтобы проверить его знания по этому тексту, например: текст:{Меня зовут Алёна , мне 32 года}, твой вопрос:{Как тебя зовут?}')
        , HumanMessage(content=user_input)]
    res = chat(messages)
    messages.append(res)
    print("Проверка2")

    return res.content


def chat_answer(questions, chat):
    messages = [SystemMessage(
        content='Тебе надо сгенерировать ответы на вопросы по тексту, который тебе пришлёт пользователь'),
        HumanMessage(content=questions)]
    res = chat(messages)
    messages.append(res)
    return res.content



def chat_bot():
    chat = GigaChat(
        credentials="MDQ0MzhkMTYtZTQ0NS00M2M0LWI5OGItNmRmZDdkYTNkZmFmOjA0MDliNzIzLTU0YjYtNDY3OC1iMjVjLTY4MjczYjExOWU3Yg==",
        verify_ssl_certs=False)

    def generate_questions():
        user_input = open_file()
        questions = chat_questions(user_input, chat=chat)
        #questions = start_place(user_input, chat_questions)
        questions_text_editor.delete("1.0", END)
        questions_text_editor.insert("1.0", questions)
        questions_text_editor.delete("10.0", END)
        questions_text_editor.insert("10.0", "\n \n")
        return [questions, user_input]

    def generate_answer(text):
        questions = chat_answer(text, chat=chat)
        questions_text_editor.delete("10.0", END)
        questions_text_editor.insert("10.0", questions)
        return questions

    questions = generate_questions()
    questions1 = questions[1] + questions[0]
    answer = generate_answer(questions1)
    print(answer)







'''open_button = ttk.Button(text="Открыть файл", command=open_file)
open_button.grid(column=0, row=1, sticky=NSEW, padx=10)'''

save_button = ttk.Button(text="Сгенерировать вопросы", command=chat_bot)
save_button.grid(column=2, row=1, sticky=NSEW, padx=10)

answer_button = ttk.Button(text="Ответить на вопросы", command=chat_bot)
answer_button.grid(column=0, row=1, sticky=NSEW, padx=10)

root.mainloop()