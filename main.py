from file_utils import read_txtfile
from text_utils import count_words
from text_utils import count_lines
from text_utils import calculate_ttr
from file_utils import rom_arab
from text_utils import calculate_lexical_density
from file_utils import get_files_in_folder
from file_utils import write_csvfile
from file_utils import read_csvfile
from collections import Counter
from text_utils import count_unique_words
from text_utils import average_word_length
from text_utils import find_longest_word
from text_utils import find_pronouns
from text_utils import identify_sensations
from text_utils import get_most_common_words
from text_utils import seek_love
from text_utils import translate_pos_tag
from text_utils import translate_sense
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')       
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet') 
nltk.download('stopwords') 
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk import word_tokenize
from file_utils import write_txtfile


def analyze_single_text(filepath, filename):
  """
  Анализирует содержание текстового файла.

  Args:
      filepath (str): Путь к файлу
      filename (str): Название файла

  Returns:
      dict: Словарь с результатами анализа
  """
  if not "txt" in filename:
    filename = filename + ".txt"
  try:
    text = read_txtfile(f"{filepath}/{filename}")
  except:
    return "Incorrect filename"
  results = {}
  results["words_number"] = count_words(text)
  results["unique_words_number"] = count_unique_words(text)
  results["lines_number"] = count_lines(text)
  results['ttr'] = calculate_ttr(text)
  results['lexical_density'] = calculate_lexical_density(text)
  results['avg_word_length'] = round(average_word_length(text), 2)
  results['longest_word'] = find_longest_word(text)
  results["personas"] = find_pronouns(text)
  results['sensations'] = identify_sensations(text)
  results['three_most_common_words'] = get_most_common_words(text, 3)
  results["love"] = seek_love(text)
  results["longest words"] = find_longest_word(text)
  return results

def analyze_corpus(corpus_folder, statistics_folder):
    """
    Анализирует корпус текстов. Записывает csv файл со статистикой по каждому тексту

    Args:
        corpus_folder (str): Папка со всеми текстами для анализа
        statistics_filepath (str): Папка, где должен располагаться csv файл со статистикой

    Returns:
        dict: Словарь с результатами анализа корпуса
    """
    files_list = get_files_in_folder(corpus_folder)
    analyses_list = []
    statistics = []
    headers = ["filename","number of words", "number of unique words", "number of lines", "Type-Token Ratio", "lexical density", "sensations", "personas", "love", "longest words"]
    for f in files_list:
        analysis = analyze_single_text(corpus_folder, f)
        analyses_list.append(analysis)
        statistics_line = [f, str(analysis.get("words_number", "0")), str(analysis.get("unique_words_number", "0")), str(analysis.get("lines_number", "0")), str(analysis.get("ttr", "0")), str(analysis.get("lexical_density", "0"))]
        sensations_to_add = analysis["sensations"]
        sensations_to_add = " ".join(sensations_to_add)
        statistics_line.append(sensations_to_add)
        personas_to_add = analysis["personas"]
        personas_to_add = " ".join(personas_to_add)
        statistics_line.append(personas_to_add)
        if analysis.get("love", False) == True:
           statistics_line.append("yes")
        else:
           statistics_line.append("no")
        lw = analysis["longest words"]
        lw = " ".join(lw)
        statistics_line.append(lw)
        statistics_line = ",".join(statistics_line)
        statistics.append(statistics_line)
    write_csvfile(f"{statistics_folder}/statistics.csv", statistics, headers)
    corpus_analysis = {
        "avg_ttr": 0,
        "avg_words_number": 0,
        "avg_unique_words_number": 0,
        "avg_lines": 0,
        "avg_lexical_density": 0, 
        "sensations_percentage": {
            "vision": 0,
            "audition": 0,
            "olfaction": 0,
            "tactition": 0,
            "gustation": 0,
            "interoception": 0
          
        },
        "personas_percentage": {
          "I": 0,
          "thou": 0,
          "you": 0, 
          "we": 0
        },
        "texts_with_love": 0,
        "love_percentage": 0

        }
    total_number = len(analyses_list)
    total_ttr = 0
    total_words = 0
    total_lines = 0
    total_lexical_density = 0
    total_unique_words = 0
    total_love = 0
    for a in analyses_list:
        total_ttr += a.get("ttr")
        total_words += a.get("words_number")
        total_lines += a.get("lines_number")
        total_lexical_density += a.get("lexical_density")
        total_unique_words += a.get("unique_words_number")
        if a.get("love") == True:
           total_love += 1
    corpus_analysis["avg_ttr"] = round(total_ttr/total_number, 2)
    corpus_analysis["avg_words_number"]= round(total_words/total_number, 2)
    corpus_analysis["avg_unique_words_number"] = round(total_unique_words/total_number, 2)
    corpus_analysis["avg_lines"]= round(total_lines/total_number, 2)
    corpus_analysis["avg_lexical_density"] = round(total_lexical_density/total_number, 2)
    all_personas = []
    all_sensations = []
    for a in analyses_list:
        personas = a.get("personas")
        all_personas.extend(personas)
        sensations = a.get("sensations")
        all_sensations.extend(sensations)
    personas_counted = Counter(all_personas)
    sensations_counted = Counter(all_sensations)
    for k, v in corpus_analysis["personas_percentage"].items():
        persona_number = personas_counted[k]
        percentage = round(persona_number/total_number*100, 2)
        corpus_analysis["personas_percentage"][k] = percentage
    for k, v in corpus_analysis["sensations_percentage"].items():
        sensation_number = sensations_counted[k]
        percentage = round(sensation_number/total_number*100, 2)
        corpus_analysis["sensations_percentage"][k] = percentage
    corpus_analysis["texts_with_love"] = total_love
    corpus_analysis["love_percentage"] = round(total_love/total_number*100, 2)
    big_headers = []
    big_line_of_data = []
    for k, v in corpus_analysis.items():
      if isinstance(v, int | float):
          big_headers.append(k)
          big_line_of_data.append(str(v))
      else:
         for c, w in corpus_analysis[k].items():
            big_headers.append(c)
            big_line_of_data.append(str(w))
    big_data = [",".join(big_line_of_data)]
    write_csvfile("Shakespeare_corpus_project/results/total_statistics.csv", big_data, big_headers)
    return corpus_analysis

def analyze_corpus_part(corpus_folder, statistics_folderpath, metadata_filepath, cycle=None, group=None):
    """
    Анализирует часть корпуса текстов. Записывает csv файл со статистикой по части корпуса

    Args:
        corpus_folder (str): Папка со всеми текстами для анализа
        statistics_folderpath (str): Папка, где должен располагаться csv файл со статистикой
        metadata_filepath (str): Папка с метаданными о всех текстах корпуса
        cycle (str): Искомое знание в колонке cycle в метаданных
        group (str): Искомое знание в колонке group в метаданных

    Аргументы cycle и group не могут быть заданы одновременно.

    Returns:
        dict: Словарь с результатами анализа корпуса
    """
    analyses_list = []
    if cycle and group:
      print("You may choose either a group or a cycle, not both")
    if cycle and not group:
       part = cycle
       metadata = read_csvfile(metadata_filepath)
       for line in metadata:
          if line.get("cycle", "") == cycle:
             f = line.get("filename", '')
             new_sonnet = read_txtfile(f"{corpus_folder}/{f}")
             a = analyze_single_text(corpus_folder, f)
             analyses_list.append(a)   
    if group and not cycle:
       part = group
       metadata = read_csvfile(metadata_filepath)
       for line in metadata:
          if line.get("group", "") == group:
             f = line.get("filename", '')
             new_sonnet = read_txtfile(f"{corpus_folder}/{f}")
             a = analyze_single_text(corpus_folder, f)
             analyses_list.append(a)
    corpus_analysis = {
        "avg_ttr": 0,
        "avg_words_number": 0,
        "avg_unique_words_number": 0,
        "avg_lines": 0,
        "avg_lexical_density": 0, 
        "sensations_percentage": {
            "vision": 0,
            "audition": 0,
            "olfaction": 0,
            "tactition": 0,
            "gustation": 0,
            "interoception": 0
          
        },
        "personas_percentage": {
          "I": 0,
          "thou": 0,
          "you": 0, 
          "we": 0
        },
        "texts_with_love": 0,
        "love_percentage": 0

        }
    total_number = len(analyses_list)
    total_ttr = 0
    total_words = 0
    total_lines = 0
    total_lexical_density = 0
    total_unique_words = 0
    total_love = 0
    for a in analyses_list:
        total_ttr += a.get("ttr")
        total_words += a.get("words_number")
        total_lines += a.get("lines_number")
        total_lexical_density += a.get("lexical_density")
        total_unique_words += a.get("unique_words_number")
        if a.get("love") == True:
           total_love += 1
    corpus_analysis["avg_ttr"] = round(total_ttr/total_number, 2)
    corpus_analysis["avg_words_number"]= round(total_words/total_number, 2)
    corpus_analysis["avg_unique_words_number"] = round(total_unique_words/total_number, 2)
    corpus_analysis["avg_lines"]= round(total_lines/total_number, 2)
    corpus_analysis["avg_lexical_density"] = round(total_lexical_density/total_number, 2)
    all_personas = []
    all_sensations = []
    for a in analyses_list:
        personas = a.get("personas")
        all_personas.extend(personas)
        sensations = a.get("sensations")
        all_sensations.extend(sensations)
    personas_counted = Counter(all_personas)
    sensations_counted = Counter(all_sensations)
    for k, v in corpus_analysis["personas_percentage"].items():
        persona_number = personas_counted[k]
        percentage = round(persona_number/total_number*100, 2)
        corpus_analysis["personas_percentage"][k] = percentage
    for k, v in corpus_analysis["sensations_percentage"].items():
        sensation_number = sensations_counted[k]
        percentage = round(sensation_number/total_number*100, 2)
        corpus_analysis["sensations_percentage"][k] = percentage
    corpus_analysis["texts_with_love"] = total_love
    corpus_analysis["love_percentage"] = round(total_love/total_number*100, 2)
    big_headers = []
    big_line_of_data = []
    for k, v in corpus_analysis.items():
      if isinstance(v, int | float):
          big_headers.append(k)
          big_line_of_data.append(str(v))
      else:
         for c, w in corpus_analysis[k].items():
            big_headers.append(c)
            big_line_of_data.append(str(w))
    big_data = [",".join(big_line_of_data)]
    part = part.lower()
    part = part.split(" ")
    part = "_".join(part)
    write_csvfile(f"{statistics_folderpath}/{part}_statistics.csv", big_data, big_headers)
    return corpus_analysis
            

   
def pos_statistics(corpus_folderpath, statistics_folderpath, metadata_filepath):
  """
  Собирает статистику по распределению слов по частям речи в корпусе, для каждого файла в отдельности, для циклов сонетов Fair Youth, Dark Lady, для групп сонетов Procreation, Rival Poet (c pos-tagging'ом и лемматизацией при помощи инструментов nltk)

  Args:
      corpus_folderpath (str): Папка со всеми текстами для анализа
      statistics_filepath (str): Папка, где должен располагаться csv файл со статистикой
      metadata_filepath (str): Папка с метаданными о всех текстах корпуса
  

  Returns:
      bool = True
  """
  all_lines = []
  files_list = get_files_in_folder(corpus_folderpath)
  all_sonnets = []
  for f in files_list:
    new_sonnet = read_txtfile(f"{corpus_folderpath}/{f}")
    all_sonnets.append(new_sonnet)
  all_sonnets = "\n".join(all_sonnets)
  symbols_to_remove = ".,-–?!;:"
  for symbol in symbols_to_remove:
    all_sonnets = all_sonnets.replace(symbol, "")
  all_sonnets = word_tokenize(all_sonnets)
  tags = pos_tag(all_sonnets)
  tags_translated = []
  for w, t in tags:
     tt = translate_pos_tag(t)
     tags_translated.append(tt)
  tags_number = len(tags)
  tags_counted = Counter(tags_translated)
  headers = ["noun","pronoun","modal verb","verb",
             "adjective or ordinal numeral","adverb","determinative","interjection","numeral",
             "non english word", "functor", "?"]
  corpus_line = ["corpus"]
  for t in headers:
        k_found = False
        for  k, v in tags_counted.items():
           if k == t:
              k_found = True
              corpus_line.append(str(round(v/tags_number*100, 2)))
        if k_found == False:
           corpus_line.append("0")
  corpus_line = ",".join(corpus_line)
  all_lines.append(corpus_line)
  metadata = read_csvfile(metadata_filepath)
  #COUNTING FAIR YOUTH SONNETS
  line_to_add = ["Fair Youth"]
  sonnets = []
  for line in metadata:
    if line.get("cycle", "") == "Fair Youth":
      filename = line.get("filename", "")
      sonnet = read_txtfile(f"{corpus_folderpath}/{filename}")
      symbols_to_remove = ".,-–?!;:"
      for symbol in symbols_to_remove:
        sonnet = sonnet.replace(symbol, "")
      sonnets.append(sonnet)
  sonnets = "\n".join(sonnets)
  sonnets = word_tokenize(sonnets)
  tags = pos_tag(sonnets)
  tags_translated = []
  for w, t in tags:
    tt = translate_pos_tag(t)
    tags_translated.append(tt)
  tags_number = len(tags)
  tags_counted = Counter(tags_translated)
  for t in headers:
        k_found = False
        for  k, v in tags_counted.items():
           if k == t:
              k_found = True
              line_to_add.append(str(round(v/tags_number*100, 2)))
        if k_found == False:
           line_to_add.append("0")
  line_to_add = ",".join(line_to_add)
  all_lines.append(line_to_add)
  #COUNTING DARK LADY SONNETS
  line_to_add = ["Dark Lady"]
  sonnets = []
  for line in metadata:
    if line.get("cycle", "") == "Dark Lady":
      filename = line.get("filename", "")
      sonnet = read_txtfile(f"{corpus_folderpath}/{filename}")
      symbols_to_remove = ".,-–?!;:"
      for symbol in symbols_to_remove:
        sonnet = sonnet.replace(symbol, "")
      sonnets.append(sonnet)
  sonnets = "\n".join(sonnets)
  sonnets = word_tokenize(sonnets)
  tags = pos_tag(sonnets)
  tags_translated = []
  for w, t in tags:
    tt = translate_pos_tag(t)
    tags_translated.append(tt)
  tags_number = len(tags)
  tags_counted = Counter(tags_translated)
  for t in headers:
        k_found = False
        for  k, v in tags_counted.items():
          if k == t:
            k_found = True
            line_to_add.append(str(round(v/tags_number*100, 2)))
        if k_found == False:
             line_to_add.append("0")
  line_to_add = ",".join(line_to_add)
  all_lines.append(line_to_add)
  #COUNTING PROCREATION SONNETS
  line_to_add = ["Procreation"]
  sonnets = []
  for line in metadata:
    if line.get("group", "") == "Procreation":
      filename = line.get("filename", "")
      sonnet = read_txtfile(f"{corpus_folderpath}/{filename}")
      symbols_to_remove = ".,-–?!;:"
      for symbol in symbols_to_remove:
        sonnet = sonnet.replace(symbol, "")
      sonnets.append(sonnet)
  sonnets = "\n".join(sonnets)
  sonnets = word_tokenize(sonnets)
  tags = pos_tag(sonnets)
  tags_translated = []
  for w, t in tags:
    tt = translate_pos_tag(t)
    tags_translated.append(tt)
  tags_number = len(tags)
  tags_counted = Counter(tags_translated)

  for t in headers:
        k_found = False
        for  k, v in tags_counted.items():
           if k == t:
              k_found = True
              line_to_add.append(str(round(v/tags_number*100, 2)))
        if k_found == False:
           line_to_add.append("0")
  line_to_add = ",".join(line_to_add)
  all_lines.append(line_to_add)
  #COUNTING RIVAL POET SONNETS SONNETS
  line_to_add = ["Rival Poet"]
  sonnets = []
  for line in metadata:
    if line.get("group", "") == "Rival Poet":
      filename = line.get("filename", "")
      sonnet = read_txtfile(f"{corpus_folderpath}/{filename}")
      symbols_to_remove = ".,-–?!;:"
      for symbol in symbols_to_remove:
        sonnet = sonnet.replace(symbol, "")
      sonnets.append(sonnet)
  sonnets = "\n".join(sonnets)
  sonnets = word_tokenize(sonnets)
  tags = pos_tag(sonnets)
  tags_translated = []
  for w, t in tags:
    tt = translate_pos_tag(t)
    tags_translated.append(tt)
  tags_number = len(tags)
  tags_counted = Counter(tags_translated)
  for t in headers:
        k_found = False
        for  k, v in tags_counted.items():
           if k == t:
              k_found = True
              line_to_add.append(str(round(v/tags_number*100, 2)))
        if k_found == False:
           line_to_add.append("0")
  line_to_add = ",".join(line_to_add)
  all_lines.append(line_to_add)
  
  #counting sonnet_by_sonnet
  for filename in files_list:
    line_to_add = [filename]
    sonnet = read_txtfile(f"{corpus_folderpath}/{filename}")
    symbols_to_remove = ".,-–?!;:"
    for symbol in symbols_to_remove:
      sonnet = sonnet.replace(symbol, "")
    sonnet = word_tokenize(sonnet)
    tags = pos_tag(sonnet)
    tags_translated = []
    for w, t in tags:
      tt = translate_pos_tag(t)
      tags_translated.append(tt)
    tags_number = len(tags)
    tags_counted = Counter(tags_translated)
    for t in headers:
          k_found = False
          for  k, v in tags_counted.items():
           if k == t:
              k_found = True
              line_to_add.append(str(round(v/tags_number*100, 2)))
          if k_found == False:
            line_to_add.append("0")
    line_to_add = ",".join(line_to_add)
    all_lines.append(line_to_add) 
    new_headers = ["object"]
    new_headers.extend(headers)
  write_csvfile(f"{statistics_folderpath}/pos_statistics.csv", all_lines, new_headers)
  return True


      
def generate_report():
  """
  Собирает текстовый отчёт. Записывает его в виде текстовго файла report.txt в папку results
  """
  metadata = read_csvfile("Shakespeare_corpus_project/data/metadata.csv")
  stats = read_csvfile("Shakespeare_corpus_project/results/statistics.csv")
  corpus_statisitcs = read_csvfile("Shakespeare_corpus_project/results/total_statistics.csv")
  corpus_statisitcs = corpus_statisitcs[0]
  pos_data = read_csvfile("Shakespeare_corpus_project/results/pos_statistics.csv")
  corpus_pos_data = pos_data[0]
  total_words = 0
  total_unique_words = 0
  total_lines = 0
  files_list = get_files_in_folder("Shakespeare_corpus_project/corpus")
  all_sonnets = []
  for f in files_list:
     newsonnet = read_txtfile(f"Shakespeare_corpus_project/corpus/{f}")
     all_sonnets.append(newsonnet)
  all_sonnets = "\n".join(all_sonnets)
  unique_sonnets_words = count_unique_words(all_sonnets)
  longest_words = find_longest_word(all_sonnets)
  common_words = get_most_common_words(all_sonnets, 10)
  ultimate_common_words = []
  for w, n in common_words:
     ultimate_common_words.append(w)
  for line in stats:
    total_words += int(line.get("number of words", 0))
    total_unique_words += int(line.get("number of unique words", 0))
    total_lines += int(line.get("number of lines", 0))
  large_separator = "="*30
  a = "Отчёт по анализу корпуса сонетов У. Шекспира"
  b = f"""Общая статистика:
  ___
  Всего текстов: {len(get_files_in_folder("Shakespeare_corpus_project/corpus"))}
  Всего слов: {total_words}
  Всего уникальных слов: {unique_sonnets_words}
  Всего строк: {total_lines}
  Среднее количество слов в тексте: {round(total_words/154, 2)}
  Среднее количество уникальных слов в тексте: {round(total_unique_words/154, 2)}
  Самые частые слова (исключены слова из списка stopwords от nltk): {", ".join(ultimate_common_words)}
  Самые длинные слова во всём корпусе: {" ,".join(longest_words)}
  Среднее количество строк: {corpus_statisitcs.get("avg_lines", 0)}
  Средний ttr: {corpus_statisitcs.get("avg_ttr", 0)}
  Средняя лексическая плотность: {corpus_statisitcs.get("avg_lexical_density", 0)}
  В каком количестве текстов есть "любовь" ("love" и его формы, "beloved"):  {corpus_statisitcs.get("texts_with_love", 0)}
  Процент текстов, содержащих "любовь": {corpus_statisitcs.get("love_percentage", 0)}"""
 
  file_to_write = large_separator + "\n" + a + "\n" + large_separator + "\n"*2 + b + "\n" + large_separator + "\n"*2
  c = f"""Обращение к чувственному опыту:
  ___
  Сколько текстов обращается к зрению? {corpus_statisitcs.get("vision", 0)}%
  Сколько текстов обращается к слуху? {corpus_statisitcs.get("audition", 0)}%
  Сколько текстов обращается к обнянию? {corpus_statisitcs.get("olfaction", 0)}%
  Сколько текстов обращается к тактильным ощущениям? {corpus_statisitcs.get("tactition", 0)}%
  Сколько текстов обращается к вкусовым ощущениям? {corpus_statisitcs.get("gustation", 0)}%
  Сколько текстов обращается к внутренним ощущениям? {corpus_statisitcs.get("interoception", 0)}%
  """

  d = f"""Я–ты–мы 
  ___
  В скольких текстах встречается местоимение "I"? {corpus_statisitcs.get("I", 0)}%
  В скольких текстах встречается thou? {corpus_statisitcs.get("thou", 0)}%
  В скольких текстах встречается you? {corpus_statisitcs.get("you", 0)}%
  В скольких текстах встречается we? {corpus_statisitcs.get("I", 0)}%
  """
  e = f"""Распределение слов по частям речи (в процентах):

  Существительные:  {corpus_pos_data.get("noun", 0)} %
  Глаголы: {round(float(corpus_pos_data.get("verb", 0))+float(corpus_pos_data.get("modal verb", 0)))} %
  Прилагательные и порядковые числительные: {corpus_pos_data.get("adjective or ordinal numeral", 0)} %
  Наречия: {corpus_pos_data.get("adverb", 0)} %
  Местоимения всех видов: {corpus_pos_data.get("pronoun", 0)} %
  Количественные числительные: {corpus_pos_data.get("numeral", 0)} %
  Междометия: {corpus_pos_data.get("interjection", 0)} %
  Другое: {round(float(corpus_pos_data.get("interjection", 0)) + float(corpus_pos_data.get("non english words", 0)) + float(corpus_pos_data.get("?", 0)) +
            float(corpus_pos_data.get("determinative", 0)) + float(corpus_pos_data.get("functor", 0)), 2)} %"""

  sensations = ["vision", "audition", "olfaction", "tactition", "gustation", "interoception"]
  personas = ["I", "thou", "you", "we"]
  dl_data = read_csvfile("Shakespeare_corpus_project/results/dark_lady_statistics.csv")
  fy_data = read_csvfile("Shakespeare_corpus_project/results/fair_youth_statistics.csv")
  dl_data = dl_data[0]
  fy_data = fy_data[0]
  lines_of_comparison = []
  lines_of_comparison2 = []
  for s in sensations:
      if float(fy_data.get(s, 0)) > float(dl_data.get(s, 0)):
        lines_of_comparison.append(f"Fair Youth {fy_data.get(s, 0)} <<<| Dark Lady {dl_data.get(s, 0)} ")
      elif float(fy_data.get(s, 0)) == float(dl_data.get(s, 0)):
        lines_of_comparison.append(f"Fair Youth {fy_data.get(s, 0)} ||| Dark Lady {dl_data.get(s, 0)} ")
      elif float(fy_data.get(s, 0)) < float(dl_data.get(s, 0)):
        lines_of_comparison.append(f"Fair Youth {fy_data.get(s, 0)} |>>> Dark Lady {dl_data.get(s, 0)} ")
  for p in personas:
      if float(fy_data.get(s, 0)) > float(dl_data.get(s, 0)):
        lines_of_comparison2.append(f"Fair Youth {fy_data.get(s, 0)} <<<| Dark Lady {dl_data.get(s, 0)} ")
      elif float(fy_data.get(s, 0)) == float(dl_data.get(s, 0)):
        lines_of_comparison2.append(f"Fair Youth {fy_data.get(s, 0)} ||| Dark Lady {dl_data.get(s, 0)} ")
      elif float(fy_data.get(s, 0)) < float(dl_data.get(s, 0)):
        lines_of_comparison2.append(f"Fair Youth {fy_data.get(s, 0)} |>>> Dark Lady {dl_data.get(s, 0)} ")
  lines_of_comparison3 = []
  if float(fy_data.get("avg_ttr", 0)) > float(dl_data.get("avg_ttr", 0)):
        lines_of_comparison3.append(f"Fair Youth {fy_data.get("avg_ttr", 0)} <<<| Dark Lady {dl_data.get("avg_ttr", 0)} ")
  elif float(fy_data.get("avg_ttr", 0)) == float(dl_data.get("avg_ttr", 0)):
        lines_of_comparison3.append(f"Fair Youth {fy_data.get(s, 0)} ||| Dark Lady {dl_data.get("avg_ttr", 0)} ")
  elif float(fy_data.get("avg_ttr", 0)) < float(dl_data.get("avg_ttr", 0)):
        lines_of_comparison3.append(f"Fair Youth {fy_data.get("avg_ttr", 0)} |>>> Dark Lady {dl_data.get("avg_ttr", 0)} ")

  if float(fy_data.get("avg_lexical_density", 0)) - float(dl_data.get("avg_lexical_density", 0)):
        lines_of_comparison3.append(f"Fair Youth {fy_data.get("avg_lexical_density", 0)} <<<| Dark Lady {dl_data.get("avg_lexical_density", 0)} ")
  elif float(fy_data.get("avg_lexical_density", 0)) == float(dl_data.get("avg_lexical_density", 0)):
        lines_of_comparison3.append(f"Fair Youth {fy_data.get("avg_lexical_density", 0)} ||| Dark Lady {dl_data.get("avg_lexical_density", 0)} ")
  elif float(fy_data.get("avg_lexical_density", 0)) < float(dl_data.get("avg_lexical_density", 0)):
        lines_of_comparison3.append(f"Fair Youth {fy_data.get("avg_lexical_density", 0)} |>>> Dark Lady {dl_data.get("avg_lexical_density", 0)} ")
     

  f = f"""Сравнение циклов Fair Youth и Dark Lady
  ___
  Чувственность (процент текстов, обращающихся к тому или иному ощущению)
  ...
  Зрение
  {lines_of_comparison[0]}

  Слух
  {lines_of_comparison[1]}

  Обоняние
  {lines_of_comparison[2]}

  Тактильные ощущения
  {lines_of_comparison[3]}

  Вкус
  {lines_of_comparison[4]}

  Внутренние ощущения
  {lines_of_comparison[5]}
  ___

  О ком речь?
  ...
  I
  {lines_of_comparison2[0]}
  
  THOU
  {lines_of_comparison2[0]}

  
  YOU
  {lines_of_comparison2[0]}
  
  WE
  {lines_of_comparison2[0]}

  ___

  Лексическое богатство
  Type-Token Ratio (Соотношение уникальных слов и слов в целом)
  {lines_of_comparison3[0]}

  Лексическая плотность (Соотношение слов, относящихся к самостоятельным частям речи, и слов в целом)
  {lines_of_comparison3[1]}
  """

  prc_data = read_csvfile("Shakespeare_corpus_project/results/procreation_statistics.csv")
  rp_data = read_csvfile("Shakespeare_corpus_project/results/rival_poet_statistics.csv")
  prc_data = prc_data[0]
  rp_data = rp_data[0]
  lines_of_comparison = []
  lines_of_comparison2 = []
  for s in sensations:
      if float(prc_data.get(s, 0)) > float(rp_data.get(s, 0)):
        lines_of_comparison.append(f"Procreation {prc_data.get(s, 0)} <<<| Rival Poet {rp_data.get(s, 0)} ")
      elif float(prc_data.get(s, 0)) == float(rp_data.get(s, 0)):
        lines_of_comparison.append(f"Procreation {prc_data.get(s, 0)} ||| Rival Poet {rp_data.get(s, 0)} ")
      elif float(prc_data.get(s, 0)) < float(rp_data.get(s, 0)):
        lines_of_comparison.append(f"Procreation {prc_data.get(s, 0)} |>>> Rival Poet {rp_data.get(s, 0)} ")
  for p in personas:
      if float(prc_data.get(s, 0)) > float(rp_data.get(s, 0)):
        lines_of_comparison2.append(f"Procreation {prc_data.get(s, 0)} <<<| Rival Poet {rp_data.get(s, 0)} ")
      elif float(prc_data.get(s, 0)) == float(rp_data.get(s, 0)):
        lines_of_comparison2.append(f"Procreation {prc_data.get(s, 0)} ||| Rival Poet {rp_data.get(s, 0)} ")
      elif float(prc_data.get(s, 0)) < float(rp_data.get(s, 0)):
        lines_of_comparison2.append(f"Procreation {prc_data.get(s, 0)} |>>> Rival Poet {rp_data.get(s, 0)} ")
  lines_of_comparison3 = []
  if float(prc_data.get("avg_ttr", 0)) > float(rp_data.get("avg_ttr", 0)):
        lines_of_comparison3.append(f"Procreation {prc_data.get("avg_ttr", 0)} <<<| Rival Poet {rp_data.get("avg_ttr", 0)} ")
  elif float(prc_data.get("avg_ttr", 0)) == float(rp_data.get("avg_ttr", 0)):
        lines_of_comparison3.append(f"Procreation {prc_data.get(s, 0)} ||| Rival Poet {rp_data.get("avg_ttr", 0)} ")
  elif float(prc_data.get("avg_ttr", 0)) < float(rp_data.get("avg_ttr", 0)):
        lines_of_comparison3.append(f"Procreation {prc_data.get("avg_ttr", 0)} |>>> Rival Poet {rp_data.get("avg_ttr", 0)}")

  if float(prc_data.get("avg_lexical_density", 0)) - float(rp_data.get("avg_lexical_density", 0)):
        lines_of_comparison3.append(f"Procreation {prc_data.get("avg_lexical_density", 0)} <<<| Dark Lady {rp_data.get("avg_lexical_density", 0)}")
  elif float(prc_data.get("avg_lexical_density", 0)) == float(rp_data.get("avg_lexical_density", 0)):
        lines_of_comparison3.append(f"Procreation {prc_data.get("avg_lexical_density", 0)} ||| Dark Lady {rp_data.get("avg_lexical_density", 0)}")
  elif float(prc_data.get("avg_lexical_density", 0)) < float(rp_data.get("avg_lexical_density", 0)):
        lines_of_comparison3.append(f"Procreation {prc_data.get("avg_lexical_density", 0)} |>>> Dark Lady {rp_data.get("avg_lexical_density", 0)}")
  g = f"""Сравнение групп сонетов Procreation и Rival Poet (из цикла Fair Youth)
  ___
  Чувственность
  ...
  Зрение
  {lines_of_comparison[0]}

  Слух
  {lines_of_comparison[1]}

  Обоняние
  {lines_of_comparison[2]}

  Тактильные ощущения
  {lines_of_comparison[3]}

  Вкус
  {lines_of_comparison[4]}

  Внутренние ощущения
  {lines_of_comparison[5]}
  ___

  О ком речь?
  ...
  I
  {lines_of_comparison2[0]}
  
  THOU
  {lines_of_comparison2[0]}

  
  YOU
  {lines_of_comparison2[0]}
  
  WE
  {lines_of_comparison2[0]}

  ___

  Лексическое богатство
  Type-Token Ratio (Соотношение уникальных слов и слов в целом)
  {lines_of_comparison3[0]}

  Лексическая плотность (Соотношение слов, относящихся к самостоятельным частям речи, и слов в целом)
  {lines_of_comparison3[1]}
  """
  file_to_write += c + "\n" + large_separator + "\n"*2 + d + "\n" + large_separator + "\n"*2 + e + "\n" + large_separator + "\n"*2 + f 
  file_to_write = file_to_write + "\n" + large_separator + "\n"*2 + g + "\n" + large_separator

  files_list = get_files_in_folder("Shakespeare_corpus_project/corpus")
  pos_per_sonnet = pos_data[5:]

  by_ld = sorted(stats, key=lambda s: s["lexical density"], reverse=True)
  highest_ld = []
  highest_ld_titles = []
  example = by_ld[0]["lexical density"]
  for t in by_ld:
     if t["lexical density"] == example:
        highest_ld.append(t["filename"])
  for line in metadata:
     for fn in highest_ld:
        if line.get("filename") == fn:
           highest_ld_titles.append(line.get("title", ""))


  by_ttr = sorted(stats, key=lambda x: x["Type-Token Ratio"], reverse=True)
  highest_ttr = []
  highest_ttr_titles = []
  example = by_ttr[0]["Type-Token Ratio"]
  for t in by_ttr:
     if t["Type-Token Ratio"] == example:
        highest_ttr.append(t["filename"])
  for line in metadata:
     for fn in highest_ttr:
        if line.get("filename") == fn:
           highest_ttr_titles.append(line.get("title", ""))

  by_w = sorted(stats, key=lambda x: x["number of words"], reverse=True)
  highest_w = []
  highest_w_titles = []
  example = by_w[0]["number of words"]
  for t in by_w:
     if t["number of words"] == example:
        highest_w.append(t["filename"])
  for line in metadata:
     for fn in highest_w:
        if line.get("filename") == fn:
           highest_w_titles.append(line.get("title", ""))

  by_uw = sorted(stats, key=lambda x: x["number of unique words"], reverse=True)
  highest_uw = []
  highest_uw_titles = []
  example = by_uw[0]["number of unique words"]
  for t in by_uw:
     if t["number of unique words"] == example:
        highest_uw.append(t["filename"])
  for line in metadata:
     for fn in highest_uw:
        if line.get("filename") == fn:
           highest_uw_titles.append(line.get("title", ""))
  six_senses = []
  six_senses_titles = []
  for t in stats:
     fn = t.get("filename", "")
     ss = t.get("sensations", "")
     ss = ss.split(" ")
     if len(ss) == 6:
        six_senses.append(fn)
  for line in metadata:
     for fn in six_senses:
        if line.get("filename") == fn:
           six_senses_titles.append(line.get("title", ""))
  records = f"""Рекорды:
  Тексты с наибольшим количеством слов: {", ".join(highest_w_titles)}

  Тексты с наибольшим количеством слов: {", ".join(highest_uw_titles)}

  Тексты с самым высоким: {", ".join(highest_ttr_titles)}

  Тексты с самой высокой лексической плотностью: {", ".join(highest_ld_titles)}

  Тексты, обращающиеся ко всем шести чувствам: {", ".join(six_senses_titles)}
  """
  file_to_write += "\n"*2 + records + "\n"*2
  for line in metadata:
    text = read_txtfile(f"Shakespeare_corpus_project/corpus/{line.get("filename", "")}")
    longest = find_longest_word(text)
    for pos_stat in pos_per_sonnet:
       if line.get("filename", "") == pos_stat.get("object", ""):
          this_pos_line = pos_stat
          break
    for s in stats:
       if line.get("filename", "") == s.get("filename", ""):
          this_stat_line = s
          break
    name_to_add = f"""Сонет {line.get("title", "")}
    Название файла: {line.get("filename", "")}"""
    if line.get("cycle", "") != "0":
      name_to_add += "\n" + f"Цикл: {line.get("cycle", 0)}"
    if line.get("group", "") != "0":
      name_to_add += "\n" + f"Группа: {line.get("group", 0)}"
    sensations = this_stat_line.get("sensations", '')
    sensations = sensations.replace("'", "")
    ru_s_line = []
    if sensations == "" or sensations.strip() == "":
       ru_s_line = "———"
    else:
       sensations = sensations.split(" ")
       for sen in sensations:
          ru_s = translate_sense(sen)
          ru_s_line.append(ru_s)
    ru_s_line = ", ".join(ru_s_line)

    personas = this_stat_line.get("personas", '')
    if personas == "":
       p_line = "———"
    else:
       p_line = personas.replace("'", "")
       p_line = p_line.split(" ")
       p_line = ", ".join(p_line)
    verbs = round(float(this_pos_line.get("verb", 0)) + float(this_pos_line.get("modal verb", 0)), 2)
    #determinative,interjection,numeral,non english word,functor,?
    other =  round(float(this_pos_line.get("determinative", 0)) + float(this_pos_line.get("interjection", 0)) + float(this_pos_line.get("numeral", 0)) + float(this_pos_line.get("non english word", 0)) + float(this_pos_line.get("functor", 0)) + float(this_pos_line.get("?", 0)), 2)
    love_to_find = "да" if this_stat_line.get("love", "no") == "yes" else "нет"
    text_to_add = f"""Год первой публикации: {line.get("first publication year", 0)}
    Количество строк: {this_stat_line.get("number of lines", 0)}
    Количество слов: {this_stat_line.get("number of words", 0)}
    Количество уникальных слов: {this_stat_line.get("number of unique words", 0)}
    Лексическая плотность: {this_stat_line.get("lexical density", 0)}
    Самые длинные слова в тексте: {", ".join(longest)}
    Чувства: {ru_s_line}
    Местоимения: {p_line}

    Распределение слов по частям речи:
      существительные: {this_pos_line.get("noun")}%
      глаголы: {verbs}%
      прилагательные: {this_pos_line.get("adjective or ordinal numeral")}%
      местоимения: {this_pos_line.get("pronoun")}%
      наречия: {this_pos_line.get("adverb")}%
      другие: {other}%

    Упоминается ли в тексте любвь: {love_to_find}"""
    text_note = name_to_add + "\n" + text_to_add
    file_to_write += "\n"*2 + large_separator + "\n"*2 + text_note
  write_txtfile("Shakespeare_corpus_project/results/report.txt", file_to_write)








  

if __name__ == "__main__":
  sample_analysis = analyze_single_text("Shakespeare_corpus_project/corpus", "126.txt")
  corpus_analysis = analyze_corpus("Shakespeare_corpus_project/corpus", "Shakespeare_corpus_project/results")
  pos_statistics("Shakespeare_corpus_project/corpus", "Shakespeare_corpus_project/results", "Shakespeare_corpus_project/data/metadata.csv")
  fy_analysis = analyze_corpus_part("Shakespeare_corpus_project/corpus", "Shakespeare_corpus_project/results", 
                                    "Shakespeare_corpus_project/data/metadata.csv", cycle="Fair Youth")
  dl_analysis = analyze_corpus_part("Shakespeare_corpus_project/corpus", "Shakespeare_corpus_project/results", 
                                    "Shakespeare_corpus_project/data/metadata.csv", cycle="Dark Lady")
  prc_analysis = analyze_corpus_part("Shakespeare_corpus_project/corpus", "Shakespeare_corpus_project/results", 
                                    "Shakespeare_corpus_project/data/metadata.csv", group="Procreation")
  rp_analysis = analyze_corpus_part("Shakespeare_corpus_project/corpus", "Shakespeare_corpus_project/results", 
                                    "Shakespeare_corpus_project/data/metadata.csv", group="Rival Poet")
  generate_report()

