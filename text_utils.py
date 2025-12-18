import nltk
import os
from nltk.corpus import stopwords
nltk.download('punkt')       
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet') 
nltk.download('stopwords') 
from nltk import pos_tag
from file_utils import read_txtfile
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from file_utils import get_files_in_folder
from collections import Counter

def count_lines (text):
    """
    Подсчитывает количество строк в тексте.

    Args:
        text (str): Текст для анализа

    Returns:
        int: Количество строк
    """
    lines = text.split("\n")
    lines = [line for line in lines if line.strip()]
    return len(lines)

def count_words(text):
    """
    Подсчитывает количество слов в тексте.

    Args:
        text (str): Текст для анализа

    Returns:
        int: Количество слов
    """
    symbols_to_remove = ".,-–?!;:"
    for symbol in symbols_to_remove:
        text = text.replace(symbol, "")
    words = text.split()
    return len(words)

def get_wordnet_pos(nltk_tag):
    """Конвертирует NLTK POS-тег в формат WordNet."""
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # По умолчанию — существительное

def lemmatize_english(text):
    """
    Лемматизация английского текста с учётом части речи.

    Args:
        text (str): Английский текст

    Returns:
        list: Список лемм
    """
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text.lower())
    tagged = pos_tag(words)

    lemmas = []
    for word, tag in tagged:
        if word.isalpha():  # Только слова (без пунктуации)
            wordnet_pos = get_wordnet_pos(tag)
            lemma = lemmatizer.lemmatize(word, pos=wordnet_pos)
            lemmas.append(lemma)
    return lemmas

def calculate_ttr(text):
    """
    Подсчитывает Type-Token Ratio для данного текста.

    Args:
        text (str): Текст для анализа

    Returns:
        float: Type-Token Ratio
    """
    lemmas = lemmatize_english(text)
    unique_words = len(set(lemmas))
    words = count_words(text)
    ttr = unique_words/words
    ttr = round(ttr, 2)
    return ttr

def calculate_lexical_density(text):
    """
    Подсчитывает лексическую плотность текста.

    Args:
        text (str): Текст для анализа

    Returns:
        float: Лексическая плотнсть
    """
    punctuation = ",.:;?!–—"
    for p in punctuation:
        text = text.replace(p, "")
    words = lemmatize_english(text)
    tagged = pos_tag(words)
    content_words_tags = [
    'CD',
    'DT', 
    'FW', 
    'JJ',
    'JJR',
    'JJS',
    'MD',
    'NN', 
    'NNP', 
    'NNPS', 
    'NNS', 
    'PDT', 
    'PRP', 
    'PRP$', 
    'RB', 
    'RBR', 
    'RBS', 
    'VB', 
    'VBD', 
    'VBG', 
    'VBN', 
    'VBP',
    'VBZ', 
    'WDT', 
    'WP', 
    'WP$', 
    'WRB'
    ]
    content_words = 0
    for word, tag in tagged:
        if tag in content_words_tags:
            content_words += 1
    lexical_density = content_words/len(words)
    lexical_density = round(lexical_density, 2)
    return lexical_density

def average_word_length(text):
    """
    Подсчитывает среднюю длину слов текста.

    Args:
        text (str): Текст для анализа

    Returns:
        float: Средняя длина слов
    """
    punctuation = ",.:;?!–—"
    for p in punctuation:
        text = text.replace(p, "")
    if not text or not text.strip():
        return 0.0
    words = text.split()
    if not words:
        return 0.0
    total_length = sum(len(word) for word in words)
    return total_length / len(words)

def find_longest_word(text):
    punctuation = ",.:;?!–—"
    for p in punctuation:
        text = text.replace(p, "")
    text = text.split()
    text_by_length = sorted(text, key=len, reverse=True)
    longest = []
    example = len(text_by_length[0])
    for w in text_by_length:
     if len(w) == example:
        longest.append(w.lower())
    longest = set(longest)
    longest = list(longest)
    return longest
    
def count_unique_words(text):
    """
    Подсчет количества уникальных слов в тексте (с лемматизацией с помощью инструментов nltk).
    
    Args:
        text (str): Исходный текст
    
    Returns:
        int: Количество уникальных слов
    """
    text = text.lower()
    punctuation = ",.:;?!–—"
    for p in punctuation:
        text = text.replace(p, "")
    words = lemmatize_english(text)
    unique_words = set(words)
    return len(unique_words)
    

sensory_dictionary = {
    "vision": [
            "see", "look", "watch", "observe", "view", "gaze", "stare", "glance",
            "glimpse", "peer", "scan", "survey", "witness", "notice", "spot",
            "detect", "perceive", "inspect", "examine", "scrutinize", "behold",
            "admire", "ogle", "peek", "peep", "leer", "squint", "blink", "wink",
            "sight", "vision", "view", "look", "gaze", "glance", "glimpse",
            "scene", "picture", "image", "appearance", "aspect", "display",
            "spectacle", "show", "exhibition", "perspective", "vista", "panorama",
            "landscape", "seascape", "cityscape", "visibility", "lucidity",
            "clarity", "sharpness", "focus", "hue", "color", "colour", "tint", "shade",
            "brightness", "darkness", "light", "shadow", "glare", "glow", "eye", 
            "visible", "invisible", "clear", "blurry", "vivid", "dull", "bright",
            "dark", "colorful", "monochrome", "luminous", "radiant", "glowing",
            "shiny", "glossy", "matte", "transparent", "opaque", "translucent",
            "crystalline", "hazy", "foggy", "misty", "sparkling", "twinkling",
            "gleaming", "glistening", "dazzling", "blinding", "pale", "vibrant", 
            "red", "grey", "gray", "white", "black", "blue", "pink", "dun", "green"
        ],
    
    "audition": [
            "hear", "listen", "overhear", "eavesdrop", "audit", "detect",
            "perceive", "catch", "pick up", "attend", "heed", "tune in",
            "resonate", "echo", "reverberate", "vibrate", "ring", "chime",
            "clang", "clatter", "rattle", "hum", "buzz", "whisper", "murmur",
            "mutter", "shout", "yell", "scream", "screech", "roar", "howl",
            "sound", "noise", "voice", "tone", "pitch", "volume", "loudness",
            "quietness", "silence", "echo", "reverberation", "resonance",
            "vibration", "acoustics", "audio", "hearing", "listening",
            "audition", "earshot", "whisper", "murmur", "shout", "scream",
            "yell", "roar", "bang", "crash", "thud", "thump", "clap",
            "ring", "bell", "chime", "melody", "harmony", "rhythm", "beat", "music",
            "loud", "quiet", "silent", "noisy", "audible", "inaudible",
            "deafening", "thunderous", "piercing", "shrill", "muffled",
            "muted", "soft", "gentle", "melodious", "harmonious", "discordant",
            "cacophonous", "euphonious", "resonant", "echoing", "reverberant",
            "sonorous", "stentorian", "strident", "hoarse", "husky", "clear",
            "distinct", "faint", "fuzzy", "crisp", "sharp", "dull", "mellow"
        ],
    
    "olfaction": [
            "smell", "scent", "sniff", "inhale", "detect", "perceive",
            "whiff", "catch a whiff", "nose", "breathe in", "snuff",
            "get a whiff", "stench", "reek", "stink", "odorize", "perfume",
            "aromatize", "fragrance", "pong", "niff",
            "smell", "scent", "odor", "odour", "aroma", "fragrance", "perfume",
            "bouquet", "stench", "stink", "reek", "whiff", "nose",
            "olfaction", "nostril", "sniff", "incense",
            "redolence", "malodor", "foulness", "mustiness",
            "pungency", "acridity",
            "fragrant", "aromatic", "sweet-smelling", "perfumed",
            "scented", "odorous", "malodorous", "stinky", "reeking",
            "foul", "rancid", "putrid", "rotten", "musty", "moldy",
            "fresh", "clean", "pungent", "acrid", "sharp", "bitter",
            "floral", "spicy", "woody", "earthy", "musky",
            "fishy", "gamy", "medicinal", "chemical", "metallic"
        ],

    
    "tactition": [
            "touch", "feel", "sense", "handle", "finger", "stroke", "caress",
            "pat", "tap", "rub", "massage", "knead", "scratch", "itch",
            "tickle", "brush", "graze", "contact", "press", "squeeze",
            "pinch", "grasp", "hold", "clutch", "grip", "embrace", "hug",
            "cuddle", "nuzzle", "fondle", "palpate", "manipulate",
            "touch", "feel", "feeling", "sensation", "texture", "surface",
            "contact", "pressure", "temperature", "heat", "cold", "warmth",
            "chill", "pain", "itch", "tickle", "tingle", "vibration",
            "roughness", "smoothness", "softness", "hardness", "firmness",
            "tenderness", "tactility", "handling", "embrace", "hug",
            "caress", "stroke", "massage", "scratch", "abrasion", "friction",
            "soft", "hard", "rough", "smooth", "slick", "slippery", "sticky",
            "tacky", "wet", "dry", "moist", "damp", "humid", "arid",
            "hot", "cold", "warm", "cool", "chilly", "freezing", "burning",
            "painful", "painless", "tender", "sore", "itchy", "ticklish",
            "tingly", "numb", "sensitive", "insensitive", "fuzzy", "furry",
            "fluffy", "prickly", "spiky", "jagged", "sharp", "blunt",
            "flexible", "rigid", "elastic", "brittle", "malleable"
        ],

    
    "gustation": 
            ["taste", "savor", "sample", "try", "test", "detect", "perceive",
            "relish", "enjoy", "sip", "lick", "nibble", "bite", "chew",
            "swallow", "digest", "regurgitate", "spit", "devour", "consume",
            "ingest", "suckle", "sup", "gulp", "slurp", "munch", "crunch"
            "taste", "flavor", "savor", "palate", "tongue", "gustation",
            "aftertaste", "bitterness", "sweetness", "sourness", "saltiness",
            "umami", "spiciness", "piquancy", "zest", "tang", "relish",
            "savoriness", "deliciousness", "tastiness", "blandness",
            "insipidity", "appetite", "hunger", "thirst", "craving",
            "mouthfeel", "texture", "consistency", "aroma", "bouquet",
            "sweet", "sour", "bitter", "salty", "savory", "umami",
            "spicy", "hot", "mild", "bland", "tasteless", "flavorful",
            "delicious", "tasty", "scrumptious",
            "mouthwatering", "appetizing", "unappetizing", "disgusting",
            "revolting", "nauseating", "palatable", "unpalatable",
            "tangy", "zesty", "piquant", "peppery", "fiery",            
            "dry", "moist", "tender", "tough", "chewy", "crunchy",
            "crispy", "soft", "hard", "gritty", "smooth", "chalky"
        ],

    
   "interoception": [
            "feel", "sense", "experience", "perceive", "suffer", "enjoy",
            "endure", "bear", "tolerate", "ache", "hurt", "pain", "throb",
            "pulse", "beat", "flutter", "quiver", "shiver", "tremble",
            "shake", "quake", "vibrate", "tingle", "prickle", "sting",
            "burn", "freeze", "swell", "inflame", "nauseate", "sicken",
            "pain", "ache", "hurt", "suffering", "discomfort", "pleasure",
            "joy", "happiness", "sadness", "anger", "fear", "anxiety",
            "stress", "tension", "pressure", "relaxation", "comfort",
            "warmth", "cold", "heat", "chill", "fever", "nausea",
            "dizziness", "vertigo", "fatigue", "exhaustion", "energy",
            "vitality", "weakness", "strength", "hunger", "thirst",
            "fullness", "emptiness", "breath", "breathing", "heartbeat",
            "pulse", "blood", "sweat", "tears", "saliva",
            "painful", "painless", "aching", "sore", "tender", "sharp",
            "dull", "throbbing", "pulsating", "tingling", "prickling",
            "burning", "freezing", "chilly", "feverish", "nauseous",
            "dizzy", "vertiginous", "fatigued", "exhausted", "energetic",
            "vital", "weak", "strong", "hungry", "thirsty", "full",
            "empty", "breathless", "winded", "heartfelt", "emotional",
            "anxious", "stressed", "tense", "relaxed", "comfortable",
            "uncomfortable", "restless", "calm", "peaceful", "agitated"
        ]
}


def get_sense_by_word(word):
    """
    Определяет принадлежность слова к одной из шести категорий чувственного восприятия по заранее заданному словарю(с лемматизацией с помощью инструментов nltk).
    
    Args:
        word (str): Слово
    
    Returns:
        str: Категория
    """
    word_lower = word.lower()
    for k, v in sensory_dictionary.items():
        if word_lower in v:
            return k
    return ""
    

def identify_sensations(text):
    """
    Определяет принадлежность слов текста к одной из шести категорий чувственного восприятия по заранее заданному словарю(с лемматизацией с помощью инструментов nltk).
    
    Args:
        text (str): Текст
    
    Returns:
        list: Список категорий
    """
    symbols_to_remove = ".,-–?!;:'"
    for symbol in symbols_to_remove:
        text = text.replace(symbol, " ")
    text = text.lower()
    text = lemmatize_english(text)
    sensations_list = []
    for lemma in text:
        new_sense = get_sense_by_word(lemma)
        if new_sense not in sensations_list:
            sensations_list.append(new_sense)
    for c in sensations_list:
        if c == '':
            sensations_list.remove(c)
    return sensations_list

def find_pronouns(text):
    """
    Проверяет наличие в тексте местоимений I, you thou, we, их падежных, притяжательных и возвратных форм (с лемматизацией с помощью инструментов nltk).
    
    Args:
        text (str): Текст
    
    Returns:
        list: список упомянутых местоимений (в форме личного местоимения именительного падежа, без учёта количества упоминаний)
    """
    symbols_to_remove = ".,-–?!;:"
    for symbol in symbols_to_remove:
        text = text.replace(symbol, "")
    text = lemmatize_english(text)
    pronouns = {
        "I": ["I", "me", "mine", "my", "myself"],
        "thou": ["thou", "thee", "thy", "thine", "thyself"],
        "you": ["you", "your", "yours", "yourself"],
        "we": ["we", "our", "ours", "ourselves"] }
    personas = []
    for lemma in text:
        for k, v in pronouns.items():
            if lemma in v:
                 pronoun_forms = pronouns.get(k, "")
                 personas.append(pronoun_forms[0])
    personas = set(personas)
    return personas

def get_most_common_words(text, number):    
    """
    Сортирует слова по частотности употребленияб отбирает необходимое количество (с лемматизацией и исключением стоп-слов при помощи инструментов nltk).
    
    Args:
        text (str): Текст
        number (int): Количество искомых слов
    
    Returns:
        list: Список самых частотных слов
    """
    symbols_to_remove = ".,-–?!;:"
    for symbol in symbols_to_remove:
        text = text.replace(symbol, "")
    stop_words = set(stopwords.words("english"))
    text = lemmatize_english(text) 
    for lemma in text:
        if lemma in stop_words:
            text.remove(lemma)
    lemmas_counted = Counter(text)
    lemmas_sorted = sorted(lemmas_counted.items(), key=lambda x: x[1], reverse=True)
    required = lemmas_sorted[:number]
    return required

def seek_love(text):
    """
    Проверяет наличие в тексте слов: "love" и всех его форм, "beloved" ("belov'd") (с лемматизацией при помощи инструментов nltk).
    
    Args:
        text (str): Текст
    
    Returns:
        bool 
    """
    symbols_to_remove = ".,-–?!;:"
    for symbol in symbols_to_remove:
        text = text.replace(symbol, "")
    text = lemmatize_english(text)
    loveforms = ["love", "loving", "loved", "beloved", "lov'd", " belov'd"]
    for lemma in text:
        if lemma in loveforms:
            return True
    return False

def translate_pos_tag(pos_tag):
    """
    Преобразует pos_tag в название части речи (более широкую категорию)
    
    Args:
        text (str): Тэг
    
    Returns:
        text (str): Часть речи 
    """
    part_of_speech = {'CC': "functor", 
    'CD': "numeral", 
    'DT': "determinative", 
    'EX': "functor",
    'FW': "non english word", 
    'IN': "funtor",
    'JJ': "adjective or ordinal numeral",
    'JJR': "adjective or ordinal numeral",
    'JJS': "adjective or ordinal numeral",
    'MD': "modal verb",
    'NN': "noun", 
    'NNP': "noun", 
    'NNPS': "noun", 
    'NNS': "noun", 
    'PDT': "determinative", 
    'PRP': "pronoun", 
    'PRP$': "pronoun", 
    'RB': "adverb", 
    'RBR': "adverb", 
    'RBS': "adverb", 
    'RP': "functor", 
    'TO':"functor", 
    'UH': "interjection", 
    'VB': "verb", 
    'VBD':"verb", 
    'VBG': "verb", 
    'VBN': "verb", 
    'VBP': "verb",
    'VBZ': "verb", 
    'WDT': "pronoun", 
    'WP': "pronoun", 
    'WP$': "pronoun", 
    'WRB': "pronoun"}
    name_found = False
    for tag, name in part_of_speech.items():
        if pos_tag == tag:
            name_found == True
            return name
    if name_found == False:
        return "?"
    
def translate_sense(word):
    """
    Переводит на русский названия категорий чувственного восприятия
    
    Args:
        text (str): Название категории на английском
    
    Returns:
        text (str): Название категории на русском
    """
    senses = {"vision": "зрение",
             "olfaction": "обоняние",
             "tactition": "прикосновение",
             "gustation": "вкус",
             "audition": "слух",
             "interoception": "внутренние ощущения"}
    for k, v in senses.items():
      if word.strip() == k:
         return v