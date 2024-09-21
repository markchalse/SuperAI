


import random
import numpy as np















def random_num(num):

    random_list_1d = [random.randint(50, 100) for _ in range(num)]
    return random_list_1d


def comment(score):

    phrases_1 = ["知识点掌握的很牢", "对知识了解的很透彻", "知识掌握的很好"]
    phrases_2 = ["对知识点的理解尚可", "对知识的掌握上表现良好", "知识掌握的一般"]
    phrases_3 = ["对知识点的掌握不够扎实", "对知识的理解不到位", "知识掌握的较差"]

    if score>=8:
        return random.choice(phrases_1)
    elif 8>score>=6:
        return random.choice(phrases_2)
    return random.choice(phrases_3)


def jungement(num):

    jungement_dict = {
    }
    scores = random_num(num)
    jungement_dict["scores"] = scores
    commentword = []
    for i in range(len(scores)):
        word = comment(scores[i])
        commentword.append(word)
    jungement_dict["comment"] = commentword

    return jungement_dict