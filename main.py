from file_utils import file_utils.py
from text_utils import text_utils.py

def analyze_single_text(filename):
  text = read_txtfile(f"corpus/{filename}")
  words_number = count_words(text)
  unique_words_number = count_unique_words(text)
  lines_number = count_lines(text)
  ttr = calculate_ttr(text)
  lexical_density = calculate_lexical_density(text)
  avg_word_length = average_word_length(text)
  longest_word = find_longest_word(text)

