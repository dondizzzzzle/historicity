"""
Dion Cenalia

HIST 486N : Digital History

Professor Bradley Skopyk

Hopefully to be handed in alongside standard fare assignments

This is an open source module designed to perform the following tasks:
    - scour your current working directory for appropriate file formats:
        - plaintext
        - PDFs
    - analyse the above file formats in various ways
    - plot or export your analysis in various formats
    
Attributes:
    `default`: Yields the user's default working directory.
    
    `english`: A list containing nearly every word in the English language.
    `stops`: A list containing every stopword / function word in the English language.
    `punctuation`: A string containing all ASCII punctuation characters.
    
    `scifi_list`: A list containing science fiction indexing terms. Good to use as a default.
    
Classes:
    `Extract`: extracts information from the specified directory
    `Analyze`: plots or exports analysis of the user's choice (not finished)
"""

## all necessary imports below
import os
import nltk
import csv

from pypdf import PdfReader
from datetime import datetime as dt

from nltk.corpus import words
from nltk.corpus import stopwords
from string import punctuation

english = words.words()
stops = stopwords.words("english")
punctuation = list(punctuation)+["’",'”','“'] # remove all punctuation which could interfere with word counts

default = str(os.getcwd())

scifi_list = [
    "alien","aliens","mars","quantum","radiation","venus","civilization","laser","lazer","light","horror","terror","space","war","conquest","colonize","invasion","body","snatcher","hidden","hiding","among","planet","extraterrestrial","terrestrial","plasma","cosmos","speed","universe","multiverse","hole","antimatter","anti","matter","orbit","orbital","blackhole","wormhole","hologram","holograph","holographic","computer","robot","nanotechnology","nanotech","nanoparticles","nanobots","nano","bots","droids","droid","android","androids","singularity","robots","event","horizon","black","spaghettification","raygun","gun","ray","rays","guns","spaceship","spaceships","galactic","ship","ships","empire","empires","quazar","quazars","beam","beams","warp","warps","drive","drives","teleport","teleportation","teleporter","teleporters","hyperdrive","tractor","interplanetary","planets","void","abyss","abyssal","neutron","neutrons","neuron","neurons","pizza","electron","electrons","proton","protons","star","stars","nuclear","atom","atoms","atomic","bomb","bombs","cryogenic","cryogenics"
]

###################################################################
###################################################################

class Extract:
    """
    Args:
        `path` (String, optional): Filepath to desired directory. Defaults to current working directory.
    
    Methods:
        `read_directory`: Returns the elements and filepath of current working directory. Perhaps optional.
        `pdf_to_text`: Creates a folder containing extracted text from PDF files within specified directory. If none specified, then the default directory will be chosen.
        
    """
    def __init__(self, path=default):
        self.path = path
    
    def read_directory(self):
        """
        Reads the file names in the given directory.

        Returns:
            `dir_list` (List): the files contained inside the given directory
            `path` (String): the given directory. Defaults to current working directory.
            
        Raises:
            FileNotFoundError:: only when directory cannot be found
        """
        dir_list = list(os.listdir(str(self.path)))
        return dir_list, self.path

    
    def pdf_to_text(self, folder_name="PDF Extractions"):
        """
        Attempts to convert all PDF files within the given or default directory to text files, which are then stored in a new folder within said directory.
        
        This process is not guaranteed to produce usable data, and may yield either empty text files or garbage data; this outcome is dependent on the quality of the PDFs used.
        
        Args:
            `folder_name` (String): desired name for the new folder. Defaults to "PDF Extractions."
            
        Returns:
            `f"{self.path}/{folder_name}"` (String): can be passed into class that takes the "path" argument.
        """
        p = 0
        
        if self.path == default:
            print(f"Current Working Directory: {self.path}\n")
        else:
            print(f"Given Working Directory: {self.path}\n")
                    
        dir_list = os.listdir(self.path)
        pdf_files = [i for i in dir_list if i.endswith(".pdf")]
        
        print(f"Found {len(pdf_files)} files in directory.\n")
        
        os.chdir(self.path)
        os.mkdir(str(folder_name))
        
        while pdf_files: # True only when 'pdf_files' is not empty
            for file in pdf_files:
                x = 0
                text = ""
                reader = PdfReader(str(file))
                while True:
                    try:
                        page = reader.pages[x]
                        x += 1
                        text = text + page.extract_text() # 'page.extract_text()' yields a string
                    except:
                        print(f"{x} pages extracted from '{file}'")
                        
                        file = str(file)[:file.index('.')]
                        name = f"{file}_extracted.txt"
                        
                        with open(name, "w") as f:
                            f.write(text)
                        os.rename(f"{self.path}/{name}", f"{self.path}/{folder_name}/{name}")
                        
                        size = os.path.getsize(f"{self.path}/{folder_name}/{name}")
                        print(f"'{name}' has a file size of {size} bytes.\n")
                        break
                p += 1
            break
        
        os.chdir(default)
        
        print(f"{p} new text file(s) created at: {self.path}/{folder_name}\n")
        return f"{self.path}/{folder_name}"

###################################################################
###################################################################
   
class Analyze:
    """
    Args:
        `path` (String, optional): Filepath to desired directory. Defaults to current working directory.
    
    Methods:
        `clean_txt`: Tokenizes and cleans all text files within specified directory. If none specified, the default directory will be chosen. 
        `track_keywords`: Analyzes all text files within specified directory. If none speciied, the default directory will be chosen.
    """
    def __init__(self, path=default):
        self.path = path
        
    def clean_txt(self):
        """
        Tokenizes and cleans all text files within specified directory. If none specified, the default directory will be chosen. This may be declared as a variable and passed into other methods.
        
        This method is useful for analyzing the total frequency of words across a corpus of text.
        
        If you would like to analyze only one text file, please isolate it within its own directory and run the method as normal.

        Returns:
            `book_list` (list[str]): iterable element containing all words across all cleaned tokenizations
        """
        p = 0
        
        if self.path == default:
            print(f"Current Working Directory: {self.path}\n")
        else:
            print(f"Given Working Directory: {self.path}\n")
            
        dir_list = os.listdir(self.path)
        txt_files = [i for i in dir_list if i.endswith(".txt")]
        
        print(f"Found {len(txt_files)} files in directory.")
        
        os.chdir(self.path)
        
        book_list = []
        while txt_files:
            for file in txt_files:
                book = open(file, "r")
                book = book.read() # string
                book = book.lower()

                token_book = nltk.word_tokenize(book) # list
                clean_book = [i for i in token_book if i not in stops+punctuation] # cleaner list
                
                book_list = book_list + clean_book # total list
                p += 1
            break
        
        os.chdir(default)
        
        x = len(book_list)
        
        print(f"{p} text file(s) cleaned.\n")
        print(f"{x} total words.")
        return book_list
    
    def track_keywords(self, keywords:list[str], rowname="placeholder", csv_name="text_analysis.csv"):
        """
        Ennumerates instances of desirable indexing terms within all text files in specified directory and appends the collected data into a new CSV. If none specified, the default directory will be chosen.
        
        Reports the time to analyze each text file.

        Args:
            `keywords` (list[str]): list of desired indexing terms, each stored as strings.
            `csv_name` (str, optional): desired filename for the new csv. Defaults to "text_analysis.csv".
        """
        if type(keywords) != list[str]:
            raise TypeError("method only accepts list input.")
        
        p = 0
        
        if self.path == default:
            print(f"Current Working Directory: {self.path}\n")
        else:
            print(f"Given Working Directory: {self.path}\n")
        
        dir_list = os.listdir(self.path)
        txt_files = [i for i in dir_list if i.endswith(".txt")]
        
        print(f"\nFound {len(txt_files)} text files in directory.\n")
        
        os.chdir(self.path)
        
        csv_file = open(csv_name, "w", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        
        ## dict comprehension
        statistics = {k:v for (k,v) in zip(keywords,[0 for i in range(len(keywords))])}
        
        for file in txt_files:
            now = dt.now()
            
            book = open(file, "r")
            book = book.read() # returns a string
            book = book.lower()
            
            token_book = nltk.word_tokenize(book) # returns a list of strings
            rep_book = [i for i in token_book if i in keywords] # returns a much shorter list containing only the words I wish to track

            for i in rep_book:
                statistics[i] += 1
            
            later = dt.now()
            time = later - now
            
            print(f"Analyzed '{file}' in {time} seconds.\n")
            
            p += 1

        csv_writer.writerow([rowname]+list(statistics.values()))
        
        print(f"{p} text file(s) analyzed.")
        print(f"'{csv_name}' created in {self.path}.")
        
        os.chdir(default)
        return