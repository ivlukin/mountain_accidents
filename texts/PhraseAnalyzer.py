from nltk import ngrams

from Config.Config import EXCLUDED_PHRASES
from texts.MessageTokenizer import normalize_word

# Функция для поиска входных словосочетаний в тексте
def find_input_phrases(filtered_words, input_phrases):
    # Нормализация входных словосочетаний
    normalized_input_phrases = []
    for phrase in input_phrases:
        # Разделяем словосочетание на слова и нормализуем каждое слово
        normalized_phrase = [normalize_word(word) for word in phrase.split()]
        normalized_input_phrases.append(" ".join(normalized_phrase))

    normalized_excluded_phrases = []
    for phrase in EXCLUDED_PHRASES:
        normalized_phrase = [normalize_word(word) for word in phrase.split()]
        normalized_excluded_phrases.append(" ".join(normalized_phrase))

    # Генерация n-грамм (биграмм, триграмм и т.д.) из текста
    found_phrases = []
    for n in range(2, 4):  # Ищем биграммы и триграммы
        n_grams = ngrams(filtered_words, n)
        for gram in n_grams:
            # Преобразуем n-грамму в строку
            gram_str = " ".join(gram)
            # Проверяем есть ли эта n-грамма в списке исключаемых словосочетаний
            if gram_str in normalized_excluded_phrases:
                return None
            # Проверяем, есть ли эта n-грамма в списке входных словосочетаний
            if gram_str in normalized_input_phrases:
                found_phrases.append(gram_str)

    # Возвращаем список найденных словосочетаний
    return len(found_phrases)

# Пример текста для обработки
message = """☎️Вчера в 18:55 поступило сообщение о том, что на горе Аю-Даг две женщины и несовершеннолетний сбились с тропы. В связи с наступлением темного времени суток самостоятельно спуститься не могут. 

🚨Для оказания помощи выезжали сотрудники Алуштинского аварийно-спасательного отряда в составе 4-х человек.

⭕Спасатели прибыли к началу тропы и в пешем порядке приступили к поиску людей. Спустя 40 минут пострадавшие были обнаружены, в медицинской помощи они не нуждались. Сотрудники ГКУ РК "КРЫМ-СПАС" доставили туристов к остановке общественного транспорта.
"""

find_input_phrases(message, ["кот сидеть", "кормить молоко", "быть вкусный"])