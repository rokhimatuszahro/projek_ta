import re
import string
import nltk
import pandas as pd
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from django.contrib.staticfiles.storage import staticfiles_storage

class Preprocessing:
    # default constructor 
    def __init__(self):
        # Membaca data normalisasi yang berupa file .xlsx menggunakan modul pandas
        self.file_normalisasi = staticfiles_storage.path('normalisasi.xlsx')
        self.normalizad_word = pd.read_excel(self.file_normalisasi)
        self.normalizad_word_dict = {}
        for index, row in self.normalizad_word.iterrows():
            if row[0] not in self.normalizad_word_dict:
                self.normalizad_word_dict[row[0]] = row[1]
        
        self.file_stop = staticfiles_storage.path('stopwords.txt')
        self.stop_more = [line.strip() for line in open(self.file_stop)]

    #---------------------------------------- Cleaning Data ----------------------------------------#
    # Cleaning data yaitu proses dimana menghilangkan noise pada data agar tidak mengganggu pada saat pemrosesan data.
    def __cleaning_text(self, documents):
        # Menghapus tanda baca, mengubah huruf kapital menjadi huruf kecil semua, menghapus whitespace (karakter kosong)
        documents = documents.translate(str.maketrans('', '', string.punctuation)).lower().strip()
        # Menghapus Mention
        documents = re.sub(r'@[A-Za-z0-9]', '', documents)
        # Menghapus link
        documents = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)(?:(?:\/[^\s/]))*', '', documents)
        # Menghapus hashtag
        documents = re.sub(r'#', '', documents)
        # Menghapus url
        documents = re.sub(r'https\S+', '', documents)
        documents = re.sub(r'http\S+', '', documents)
        # Menghilangkan beberapa spasi menjadi satu spasi (multiple whitespace into single whitespace)
        documents = re.sub('\s+', ' ', documents)
        # Menghapus karakter tunggal (single char)
        documents = re.sub(r'\b[a-zA-Z]\b', '', documents)
        # Menghapus angka
        documents = re.sub(r'\d+', '', documents)
        # Menghapus emoticon
        regrex_pattern = re.compile(pattern='['
                                            u'\U0001F600-\U0001F64F'
                                            u'\U0001F300-\U0001F5FF'
                                            u'\U0001F680-\U0001F6FF'
                                            u'\U0001F1E0-\U0001F1FF'
                                            ']+', flags=re.UNICODE)
        documents = regrex_pattern.sub(r'', documents)
        # Menghilangkan tab, baris baru, dan back slice
        documents = documents.replace('\\t', ' ').replace('\\n', ' ').replace('\\u', ' ').replace('\\', '')
        # Menghilangkan non ASCII (emoticon, chinese word, .etc)
        documents = documents.encode('ascii', 'replace').decode('ascii')
        return documents

    #---------------------------------------- Normalisasi ----------------------------------------#
    def __normlized_text(self, documents):
        term_token = nltk.tokenize.word_tokenize(documents)
        norm = [self.normalizad_word_dict[term] if term in self.normalizad_word_dict else term for term in term_token]
        return ' '.join([text for text in norm])

    #---------------------------------------- Filtering / Stopword ----------------------------------------#
    # Filtering menggunakan sastrawi (custom)
    def __filtering_sastrawi(self, documents):
        stop_factory = StopWordRemoverFactory().get_stop_words()
        list_stop = stop_factory + self.stop_more
        dictionary = ArrayDictionary(list_stop)
        stopwords = StopWordRemover(dictionary)
        stop = stopwords.remove(documents)
        return stop

    #---------------------------------------- Steaming ----------------------------------------#
    # Steaming menggunakan sastrawi
    def __steaming_sastrawi(self, documents):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        documents = stemmer.stem(documents)
        return documents

    #---------------------------------------- Tokenizing ----------------------------------------#
    # Tokenizing proses pemisahan teks menjadi potongan-potongan kata yang disebut token untuk kemudian dianalisa.
    def __tokenizing_text(self, documents):
        documents = nltk.tokenize.word_tokenize(documents)
        return documents

    #---------------------------------------- Filtering (Stopword Removel) ----------------------------------------#
    # Filtering menggunakan nltk
    def __filtering_nltk(self, documents):
        # Mendapatkan stopwords indonesia
        liststopwords = set(stopwords.words('indonesian'))
        documents = [word for word in documents if not word in liststopwords]
        # return removed
        return documents

    # Conver to list
    def __convert_text_list(self, documents):
        return ' '.join([text for text in documents])

    def process(self, datasets):
        df = pd.DataFrame(data=datasets, columns=['nama', 'username','tanggal', 'tweet'])
        df['cleaning'] = df.tweet.apply(self.__cleaning_text)
        df['normalisasi'] = df.cleaning.apply(self.__normlized_text)
        df['filtering_sastrawi'] = df.normalisasi.apply(self.__filtering_sastrawi)
        df['steaming_sastrawi'] = df.filtering_sastrawi.apply(self.__steaming_sastrawi)
        df['tokenizing'] = df.steaming_sastrawi.apply(self.__tokenizing_text)
        df['stopword_nltk'] = df.tokenizing.apply(self.__filtering_nltk)
        df['list_tweet'] = df.stopword_nltk.apply(self.__convert_text_list)
        return df