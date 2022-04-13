import PyPDF2                                   # For PDF Reader
import pyttsx3                                  # For Speaking
import pickle
from tkinter.filedialog import *
from tkinter import PhotoImage
from pygame import mixer

book = askopenfilename()                  # ask PDF File Name
pdfReader = PyPDF2.PdfFileReader(book)
pages = pdfReader.numPages
print(pages)
class Player(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.songlist = None
        self.v = None
        self.volume = None
        self.slider = None
        self.list = None
        self.scrollbar = None
        self.next = None
        self.pause = None
        self.prev = None
        self.loadSongs = None
        self.songtrack = None
        self.canvas = None
        self.controls = None
        self.tracklist = None
        self.track = None
        self.master = master
        self.pack()
        mixer.init()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist=[]

        self.current = 0
        self.paused = True
        self.played = False

        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()

    def create_frames(self):
        self.track = tk.LabelFrame(self, text='Tracks',
                    font=("times new roman",20,"bold"),
                    bg="blue",fg="white",bd=5,relief=tk.GROOVE)
        self.track.config(width=450,height=400)
        self.track.grid(row=0, column=0, padx=5)

        self.tracklist = tk.LabelFrame(self, text=f'TrackList - {str(len(self.playlist))}',
                            font=("times new roman",20,"bold"),
                            bg="blue",fg="white",bd=5,relief=tk.GROOVE)
        self.tracklist.config(width=10,height=50)
        self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)

        self.controls = tk.LabelFrame(self,
                            font=("times new roman",20,"bold"),
                            bg="pink",fg="white",bd=5,relief=tk.GROOVE)
        self.controls.config(width=500,height=50)
        self.controls.grid(row=2, column=0, pady=2, padx=5)

    def track_widgets(self):
        self.canvas = tk.Label(self.track, image=img)
        self.canvas.configure(width=480, height=300)
        self.canvas.grid(row=0,column=0)

        self.songtrack = tk.Label(self.track, font=("times new roman",16,"bold"),
                        bg="white",fg="orange")
        self.songtrack['text'] = ''
        self.songtrack.config(width=30, height=1)
        self.songtrack.grid(row=1,column=0,padx=10)

    def control_widgets(self):
        self.loadSongs = tk.Button(self.controls, bg='green', fg='white', font=50)
        self.loadSongs['text'] = 'Songs'
        self.loadSongs['command'] = self.retrieve_songs
        self.loadSongs.grid(row=0, column=0, padx=5)

        self.prev = tk.Button(self.controls, image=prev)
        self.prev['command'] = self.prev_song
        self.prev.grid(row=0, column=1)

        self.pause = tk.Button(self.controls, image=pause)
        self.pause['command'] = self.pause_song
        self.pause.grid(row=0, column=2)

        self.next = tk.Button(self.controls, image=next_)
        self.next['command'] = self.next_song
        self.next.grid(row=0, column=3)

        self.volume = tk.DoubleVar(self)
        self.slider = tk.Scale(self.controls, from_ = 0, to = 10, orient = tk.HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider.set(5)
        mixer.music.set_volume(0.8)
        self.slider['command'] = self.change_volume
        self.slider.grid(row=0, column=4, padx=5)


    def tracklist_widgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')

        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,
                     yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
        self.enumerate_songs()
        self.list.config(height=22)
        self.list.bind('<Double-1>', self.play_song)

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    def retrieve_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
                for file in files:
                    if os.path.splitext(file)[1] == '.mp3':
                        path = (root_ + '/' + file).replace('\\','/')
                        self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)
        self.playlist = self.songlist
        self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
        self.list.delete(0, tk.END)
        self.enumerate_songs()

    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))


    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="white")

        print(self.playlist[self.current])
        mixer.music.load(self.playlist[self.current])
        self.songtrack['anchor'] = 'w'
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])

        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg='sky blue')

        mixer.music.play()

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause
        else:
            if not self.played:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play

    def prev_song(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='white')
        self.play_song()

    def next_song(self):
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current - 1, bg='white')
        self.play_song()

    def change_volume(self):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)

for num in range(0, pages):                    # Starting From Page Number 1 To Last Page
    page = pdfReader.getPage(num)                  # integer (256) last page number of pdf
    text = page.extractText()
    player = pyttsx3.init()
    player.setProperty('rate', 150)
    player.say(text)
    player.runAndWait()

    # ----------------------------- Main -------------------------------------------

    root = tk.Tk()
    root.geometry('650x430')
    root.wm_title('')

    img = PhotoImage(file='F:\Project 1.0\Music project\Music photo 3.gif')
    next_ = PhotoImage(file='F:\Project 1.0\Music project/next.gif')
    prev = PhotoImage(file='F:\Project 1.0\Music project/previous.gif')
    play = PhotoImage(file='F:\Project 1.0\Music project/play.gif')
    pause = PhotoImage(file='F:\Project 1.0\Music project/pause.gif')
    app = Player(master=root)
    app.mainloop()