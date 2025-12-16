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
    corpus_analysis["avg_ttr"] = total_ttr/total_number
    corpus_analysis["avg_words_number"]= total_words/total_number
    corpus_analysis["avg_lines"]= total_lines/total_number
    corpus_analysis["avg_lexical_density"] = total_lexical_density/total_number
    return corpus_analysis
        
if __name__ == "__main__":
  sample_analysis = analyze_single_text("corpus", "126.txt")


