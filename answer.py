import json
import pymorphy2
from fuzzywuzzy import fuzz


def get_questions():
    with open('qanda.json') as file:
        qanda = json.load(file)
    questions_who = list(qanda.keys())
    return questions_who


def get_qanda():
    with open('qanda.json') as file:
        qanda = json.load(file)
    qanda = list(qanda.items())
    return qanda


def lemmatize(text):
    morph = pymorphy2.MorphAnalyzer()
    normal_text = ' '.join(morph.parse(
        word)[0].normal_form for word in text.split())
    return normal_text


def question_analyse(text):
    normal_user_question = lemmatize(text)

    questions_who = get_questions()
    normal_questions_who = []
    for question in questions_who:
        normal_questions_who.append(lemmatize(question))

    return normal_user_question, normal_questions_who


def search_similar_question(question_user):
    normal_question_user, normal_questions_who = question_analyse(question_user)
    scores = []
    for normal_question_who in normal_questions_who:
        scores.append(fuzz.token_sort_ratio(
            normal_question_who.lower(), normal_question_user.lower()))
        answer_number = scores.index(max(scores))
    questions = get_qanda()
    searched_question = questions[answer_number][0]
    searched_answer = questions[answer_number][1]
    return f'{searched_question}\n {searched_answer}'


answer = search_similar_question('что такое covid-19')
print(answer)

