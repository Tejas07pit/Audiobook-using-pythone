import PyPDF2
import pyttsx3
from tkinter.filedialog import *

from pyttsx3 import engine

book = askopenfilename()  # ask PDF File Name
pdfReader = PyPDF2.PdfFileReader(book)
pages = pdfReader.numPages
print(pages)

for num in range(0, pages):  # Starting From Page Number 1 To Last Page
    page = pdfReader.getPage(num)  # integer (256) last page number of pdf
    text = page.extractText()
    player = pyttsx3.init()
    voices = player.getProperty('voices')
    print(voices)
    # changing index, changes voices, 0 for male
    # player.setProperty('voices', [0])
    # changing index, changes voices, 1 for female
    # player.setProperty('voices', [1])
    volume: object = engine.getProperty('10')
    print(volume)
    engine.setProperty('', 1.0)
    player.setProperty('rate', 150)
    player.say(text)
    player.runAndWait()

player.stop()


