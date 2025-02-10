# Функция для получения всех словоформ ключевого слова
from Config.Config import EXCLUDED_KEYWORDS
from texts.MessageTokenizer import morph


def get_word_forms(keyword):
    parsed_word = morph.parse(keyword)[0]  # Анализируем ключевое слово
    lexeme = parsed_word.lexeme  # Получаем все словоформы
    return {word.word for word in lexeme}  # Возвращаем множество словоформ


# Функция для проверки ключевых слов
def check_keywords(filtered_words, keywords):

    # Создаем множество всех словоформ для каждого ключевого слова
    keyword_forms = set()
    for keyword in keywords:
        keyword_forms.update(get_word_forms(keyword))

    excluded_keyword_forms = set()
    for keyword in EXCLUDED_KEYWORDS:
        excluded_keyword_forms.update(get_word_forms(keyword))

    # проверяем слова исключения
    for word in filtered_words:
        if word in excluded_keyword_forms:
            return None

    # Список для хранения найденных ключевых слов
    found_keywords = []
    # Перебираем каждое слово в тексте
    for word in filtered_words:
        # Если слово совпадает с одной из словоформ ключевых слов
        if word in keyword_forms:
            found_keywords.append(word)

    # Возвращаем список найденных ключевых слов
    return len(found_keywords)