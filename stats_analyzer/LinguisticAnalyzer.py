import json
from collections import Counter

from nltk import ngrams

from texts.MessageTokenizer import get_normalized_words

# Укажите путь к вашему JSON-файлу
file_path = 'messages.json'
EXCLUDED_HASHTAGS = '#cтатья'

def get_hashtags_of_message(message: str):
    hashtags = []
    for word in message.split():
        if word.startswith('#'):
            hashtags.append(word.lower())
    return hashtags

def count_words_in_message(message: str):
    return Counter(get_normalized_words(message))

def count_n_grams(message: str, n: int = 2):
    message = get_normalized_words(message)
    n_grams = ngrams(message, n)
    return Counter(n_grams)

def print_counter_beautiful(counter: Counter, per_string: int, lines: int = 20):
    # Преобразуем Counter в список кортежей (слово, количество)
    items = sorted(list(counter.items()), key=lambda x: x[1], reverse=True)[:lines * per_string]

    # Выводим по per_string записей в строке
    for i in range(0, len(items), per_string):
        # Форматируем записи для вывода
        line = ", ".join(f"{word}: {count}" for word, count in items[i:i + per_string])
        print(line)


# Открываем файл и считываем данные
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Создаем словарь для хранения частоты использования слов
word_counts = Counter()
for message_entry in data:
    text = message_entry['text']
    word_counts.update(count_words_in_message(text))

print("===== words ==== ")
#print_counter_beautiful(word_counts, 5)

bi_word_counts = Counter()
for message_entry in data:
    text = message_entry['text']
    bi_word_counts.update(count_n_grams(text, 2))
print("===== bi-words ==== ")
#print_counter_beautiful(bi_word_counts, 5)

tri_word_counts = Counter()
for message_entry in data:
    text = message_entry['text']
    tri_word_counts.update(count_n_grams(text, 3))
print("===== tri-words ==== ")
print_counter_beautiful(tri_word_counts, 5)




