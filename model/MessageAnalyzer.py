from typing import List

from nltk import word_tokenize, sent_tokenize
import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from Config import KEYWORDS, EXCLUDED_PHRASES, EXCLUDED_KEYWORDS, PHRASES


class MessageAnalyzer:
    def __init__(self):
        nltk.download('stopwords')

    def lemmatize(self, message: str) -> List[List[str]]:
        morph = MorphAnalyzer()
        tokenized_sentences = [word_tokenize(sent) for sent in sent_tokenize(message)]
        lemmatized_sentences = []
        for sent in tokenized_sentences:
            words = [morph.normal_forms(word.strip())[0] for word in sent]
            words = list(filter(lambda w: len(w) > 1 and w not in stopwords.words('russian'), words))
            lemmatized_sentences.append(words)
        return lemmatized_sentences

    def generatePhrases(self, sentences: List[List[str]]) -> List[List[str]]:
        phrases = []
        for sentence in sentences:
            phrases_from_sentence = []
            for i in range(len(sentence) - 1):
                phrases_from_sentence.append(sentence[i] + " " + sentence[i + 1])
            phrases.append(phrases_from_sentence)
        return phrases

    def searchAccident(self, message: str) -> bool:
        match_count = 0
        lemmatized_sentences = self.lemmatize(message=message)
        # create phrases for each sentence of message
        lemmatized_sentence_phrases = self.generatePhrases(lemmatized_sentences)
        lemmatized_sentences_but_set = [set(sentence) for sentence in lemmatized_sentences]
        morph = MorphAnalyzer()

        keyword_lemmatized_set = set([morph.normal_forms(word.strip())[0] for word in KEYWORDS.split(',')])
        excluded_keyword_lemmatized_set = set(
            [morph.normal_forms(word.strip())[0] for word in EXCLUDED_KEYWORDS.split(',')])
        phrase_lemmatized_set = set([morph.normal_forms(phrase)[0] for phrase in PHRASES.split(',')])
        excluded_phrase_lemmatized_set = set([morph.normal_forms(phrase)[0] for phrase in EXCLUDED_PHRASES.split(',')])

        # search excluded keywords
        for excluded_keyword in excluded_keyword_lemmatized_set:
            for sentence in lemmatized_sentences_but_set:
                if excluded_keyword in sentence:
                    return False

        # search for excluded phrases
        for excluded_phrase in excluded_phrase_lemmatized_set:
            for lemmatized_phrases_of_sentence in lemmatized_sentence_phrases:
                if excluded_phrase in lemmatized_phrases_of_sentence:
                    return False

        # check keywords
        for keyword in keyword_lemmatized_set:
            for sentence in lemmatized_sentences_but_set:
                if keyword in sentence:
                    match_count += 1

        # check phrases
        for phrase in phrase_lemmatized_set:
            for sentence_phrases in lemmatized_sentence_phrases:
                if phrase in sentence_phrases:
                    match_count += 1

        return match_count >= 2


mes = """
В Кабардино-Балкарии спасатели МЧС России эвакуировали туриста из Екатеринбурга

В верховьях ущелья Безенги на высоте 3700 метров турист при камнепаде получил траву ноги. Мужчина проходил по маршруту 2-Б категории сложности в составе зарегистрированной группы из 11 человек.

Участники группы спустили пострадавшего на высоту 3200 метров.

В 15:30 на вертолете Ми-8 МЧС России на место выдвинулись спасатели.

В 17:00 работы завершены. Мужчину эвакуировали с ущелья в Нальчик, где его передали медикам. Его жизни ничего не угрожает.

На место привлекались 3 спасателя Эльбрусского высокогорного и вертолет Ми-8 МЧС России.
"""
message_analyzer = MessageAnalyzer()
message_analyzer.searchAccident(mes)
