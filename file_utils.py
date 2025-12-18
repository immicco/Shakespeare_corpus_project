import os
#from Roman to Arabic
def rom_arab(p):
	z=0
	try:
		p=str(p)
		for i in range(0, len(p)):
			if p[i]=='I' or p[i]=='i':
				try:
					if p[i+1]=='V' or p[i+1]=='X' or p[i+1]=='v' or p[i+1]=='x': 
						z-=1
					else:
						z+=1
				except:
					z+=1
			elif p[i]=='V' or p[i]=='v':
				z+=5
			elif p[i]=='X' or p[i]=='x':
				try:
					if p[i+1]=='C' or p[i+1]=='L' or p[i+1]=='c' or p[i+1]=='l': 
						z-=10
					else:
						z+=10
				except:
					z+=10
			elif p[i]=='L' or p[i]=='l':
				z+=50
			elif p[i]=='C' or p[i]=='c':
				try:
					if p[i+1]=='M' or p[i+1]=='D' or p[i+1]=='m' or p[i+1]=='d': 
						z-=100
					else:
						z+=100
				except:
					z+=100
			elif p[i]=='D' or p[i]=='d':
				z+=500
			elif p[i]=='M' or p[i]=='m':
				z+=1000
			else:
				print("Invalid number")
	except:
		print("Invalid number")
	return z


#from Arabic to Roman
def arab_rom(s):
	v=""
	try:
		s=int(s)
		while s>0:
			if s>=1000:
				s-=1000
				v+="M"
			elif s>=900:
				s-=900
				v+="CM"
			elif s>=500:
				s-=500
				v+="D"
			elif s>=400:
				s-=400
				v+="CD"
			elif s>=100:
				s-=100
				v+="C"
			elif s>=90:
				s-=90
				v+="XC"
			elif s>=50:
				s-=50
				v+="L"
			elif s>=40:
				s-=40
				v+="XL"
			elif s>=10:
				s-=10
				v+="X"
			elif s>=9:
				s-=9
				v+="IX"
			elif s>=5:
				s-=5
				v+="V"
			elif s>=4:
				s-=4
				v+="IV"
			elif s>=1:
				s-=1
				v+="I"
	except:
		print("Invalid number")
	return v

def get_files_in_folder(folder_path, extension='.txt'):
    """
    Получает список файлов в указанной папке с заданным расширением.

    Args:
        folder_path (str): Путь к папке
        extension (str): Расширение файлов (по умолчанию '.txt')

    Returns:
        list: Список имен файлов с указанным расширением
    """
    files = os.listdir(folder_path)
    required_files = [file for file in files if file.endswith(extension)]
    return required_files

def read_txtfile(filepath):
    """
    Читает содержимое текстового файла.

    Args:
        filepath (str): Путь к файлу

    Returns:
        str: Содержимое файла или сообщение об ошибке
    """
    try:
        with open (filepath, "r", encoding = "utf-8") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "Ошибка: Файл не найден"
    except UnicodeDecodeError:
        return "Ошибка: Неверная кодировка файла"

def read_csvfile(filepath):
	"""
    Читает содержимое csv файла.

    Args:
        filepath (str): Путь к файлу

    Returns:
        list: Список словарей
    """
	texts_data = []
	try:
		with open (filepath, "r", encoding = "utf-8") as file:
			content = file.read()
	except FileNotFoundError:
		return "Ошибка: Файл не найден"
	except UnicodeDecodeError:
		return "Ошибка: Неверная кодировка файла"
	content = content.split("\n")
	titles = content[0].split(",")
	clean_content = content[1:]
	for line in clean_content:
		one_text_data = {}
		line = line.split(",")
		for i in range(len(titles)):
			one_text_data[titles[i]] = one_text_data.get(titles[i], line[i])
		texts_data.append(one_text_data)
	return texts_data

def write_csvfile(filepath, data, headers):
    """
    Записывает данные в CSV файл.

    Args:
        filepath (str): Полный путь к файлу, включая папку и название файла
                       Например: 'results/statistics.csv'
        data (list): Список списков [[val1, val2], [val1, val2], ...]
        headers (list): Список заголовков ['col1', 'col2']

    Returns:
        bool: True если успешно
    """
    titles = ",".join(headers)
    text = "\n".join(data)
    text = titles + "\n" + text
    try:
        with open(filepath, "w", encoding = "utf-8") as file:
            file.write(text)
            return True
    except:
        return False


def write_txtfile(filepath, text):
    """
    Записывает данные в текстовый файл.

    Args:
        filepath (str): Полный путь к файлу, включая папку и название файла
                       Например: 'results/001.txt'
        text (str): Текст

    Returns:
        bool: True если успешно
    """
    try:
        with open(filepath, "w", encoding = "utf-8") as file:
            file.write(text)
            return True
    except:
        return False