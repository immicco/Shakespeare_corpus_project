from file_utils import file_utils.py
from text_utils import text_utils.py

def analyze_single_text(filepath, filename):
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
  results['avg_word_length'] = average_word_length(text)
  results['longest_word'] = find_longest_word(text)
  results["personas"] = find_pronouns(text)
  results['sensations'] = define_sensations(text)
  return results

def analyze_corpus(corpus_folder, statistics_filepath):
    files_list = get_files_in_folder(corpus_folder)
    analyses_list = []
    statistics = []
    headers = ["filename","number of words", "number of lines", "Type-Token Ratio", "lexical density"]
    for f in files_list:
        analysis = analyze_single_text(corpus_folder, f)
        analyses_list.append(analysis)
        statistics_line = [f, str(analysis.get("words_number", 0)), str(analysis.get("lines_number", 0)), str(analysis.get("ttr", 0)), str(analysis.get("lexical_density", 0))]
        statistics.append(statistics_line)
    write_csvfile(f"{statistics_filepath}/statistics.csv", statistics, headers)
    corpus_analysis = {
        "avg_ttr": 0,
        "avg_words_number": 0,
        "avg_lines": 0,
        "avg_lexical_density": 0
        }
    total_number = len(analyses_list)
    print(total_number)
    total_ttr = 0
    total_words = 0
    total_lines = 0
    total_lexical_density = 0
    for a in analyses_list:
        total_ttr += a.get("ttr")
        total_words += a.get("words_number")
        total_lines += a.get("lines_number")
        total_lexical_density += a.get("lexical_density")
    print(total_lines)
    corpus_analysis["avg_ttr"] = round(total_ttr/total_number, 2)
    corpus_analysis["avg_words_number"]= round(total_words/total_number, 2)
    corpus_analysis["avg_lines"]= round(total_lines/total_number, 2)
    corpus_analysis["avg_lexical_density"] = round(total_lexical_density/total_number, 2)
    return corpus_analysis

def analyze_cycle(corpus_folder, statistics_filepath, metadata_filepath, cycle):
    files_list = get_files_in_folder(corpus_folder)
    analyses_list = []
    statistics = []
    headers = ["filename","number of words", "number of lines", "Type-Token Ratio", "lexical density"]
    texts_to_analyze = {}
    metadata = read_csvfile(metadata_filepath):
    for line in metadata:
      filename = line.get("filename", "")
      if cycle == line.get("cycle", ""):
        texts_to_analyze[filename] = True
      else:
        texts_to_analyze[filename] = False    
    for f in files_list:
        if texts_to_analyze[f] == True:
          analysis = analyze_single_text(corpus_folder, f)
          analyses_list.append(analysis)
          statistics_line = [f, str(analysis.get("words_number", 0)), str(analysis.get("lines_number", 0)), str(analysis.get("ttr", 0)), str(analysis.get("lexical_density", 0))]
          statistics.append(statistics_line)
    write_csvfile(f"{statistics_filepath}/f"statistics_cycle_{cycle}.csv", statistics, headers)
    corpus_analysis = {
        "avg_ttr": 0,
        "avg_words_number": 0,
        "avg_lines": 0,
        "avg_lexical_density": 0
        }
    total_number = len(analyses_list)
    print(total_number)
    total_ttr = 0
    total_words = 0
    total_lines = 0
    total_lexical_density = 0
    for a in analyses_list:
        total_ttr += a.get("ttr")
        total_words += a.get("words_number")
        total_lines += a.get("lines_number")
        total_lexical_density += a.get("lexical_density")
    corpus_analysis["avg_ttr"] = round(total_ttr/total_number, 2)
    corpus_analysis["avg_words_number"]= round(total_words/total_number, 2)
    corpus_analysis["avg_lines"]= round(total_lines/total_number, 2)
    corpus_analysis["avg_lexical_density"] = round(total_lexical_density/total_number, 2)
    return corpus_analysis
    
  def analyze_group(corpus_folder, statistics_filepath, metadata_filepath, group):
    files_list = get_files_in_folder(corpus_folder)
    analyses_list = []
    statistics = []
    headers = ["filename","number of words", "number of lines", "Type-Token Ratio", "lexical density"]
    texts_to_analyze = {}
    metadata = read_csvfile(metadata_filepath):
    for line in metadata:
      filename = line.get("filename", "")
      if group == line.get("group", ""):
        texts_to_analyze[filename] = True
      else:
        texts_to_analyze[filename] = False
        
    for f in files_list:
        if texts_to_analyze[f] == True:
          analysis = analyze_single_text(corpus_folder, f)
          analyses_list.append(analysis)
          statistics_line = [f, str(analysis.get("words_number", 0)), str(analysis.get("lines_number", 0)), str(analysis.get("ttr", 0)), str(analysis.get("lexical_density", 0))]
          statistics.append(statistics_line)
    write_csvfile(f"{statistics_filepath}/f"statistics_group_{group}.csv", statistics, headers)
    corpus_analysis = {
        "avg_ttr": 0,
        "avg_words_number": 0,
        "avg_lines": 0,
        "avg_lexical_density": 0
        "sensations_percentage" =
              {
              "vision": 0,
              "audition": 0,
              "olfaction": 0,
              "tactition": 0,
              "gustation": 0,
              "interoception": 0
              }
        "personas_percentage" = 
              {
              "I": 0,
              "thou": 0,
              "you": 0,
              "we": 0
              }
        }
    total_number = len(analyses_list)
    print(total_number)
    total_ttr = 0
    total_words = 0
    total_lines = 0
    total_lexical_density = 0
    for a in analyses_list:
        total_ttr += a.get("ttr")
        total_words += a.get("words_number")
        total_lines += a.get("lines_number")
        total_lexical_density += a.get("lexical_density")
    corpus_analysis["avg_ttr"] = round(total_ttr/total_number, 2)
    corpus_analysis["avg_words_number"]= round(total_words/total_number, 2)
    corpus_analysis["avg_lines"]= round(total_lines/total_number, 2)
    corpus_analysis["avg_lexical_density"] = round(total_lexical_density/total_number, 2)

      
      
    
    return corpus_analysis

if __name__ == "__main__":
  sample_analysis = analyze_single_text("corpus", "126.txt")
  corpus_analysis = analyze_corpus("corpus", "results")
  fair_youth_analysis = analyze_corpus_cycle("corpus", "results", "data/metadata.csv", "Fair Youth")
  dark_lady_analysis = analyze_corpus_cycle("corpus", "results", "data/metadata.csv", "Dark Lady")
  procreation_analysis = analyze_corpus_group("corpus", "results", "data/metadata.csv", "Procreation")
  procreation_analysis = analyze_corpus_group("corpus", "results", "data/metadata.csv", "Rival Poet")


