import nltk
import pymorphy2
from nltk.corpus import stopwords
import re

# Инициализация анализатора
morph = pymorphy2.MorphAnalyzer()

# Загрузка стоп-слов для русского языка
nltk.download('stopwords')  # Скачиваем стоп-слова, если они еще не загружены
stop_words = set(stopwords.words('russian'))

# Функция для очистки текста от пунктуации и приведения к нижнему регистру
def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.replace('\n', '').lower().strip())  # Удаляем пунктуацию и переносы строк


# Функция для нормализации слов (приведение к начальной форме)
def normalize_word(word):
    parsed_word = morph.parse(word)[0]  # Берем первый вариант разбора
    return parsed_word.normal_form

def get_normalized_words(message):
    # Очистка текста от пунктуации
    cleaned_text = clean_text(message)

    # Разделяем текст на слова
    words = cleaned_text.split()

    # Фильтрация стоп-слов и нормализация слов
    return [normalize_word(word) for word in words if word not in stop_words]