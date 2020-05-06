import os
import tkinter as tk
from tkinter import ttk
import threading,configparser
import DataCapture, FlashUtils, FlashLeaderBoard
from pathlib import Path
from PIL import ImageTk, Image



config = configparser.RawConfigParser()
two_up = Path(__file__).absolute().parents[2]
print(str(two_up)+'/magic.cfg')
config.read(str(two_up)+'/magic.cfg')

db = config.get("section1",'dataroot')
imageroot = config.get("section1",'image_root')
videoroot = config.get("section1",'video_root')

class MagicFlashApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s = ttk.Style(self)
        s.theme_use('clam')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        s.configure('Red.TLabelframe', background='beige')
        s.configure('Red.TLabelframe.Label', font=('courier', 14, 'bold', 'italic'))
        s.configure('Red.TLabelframe.Label', foreground='brown')
        s.configure('Red.TLabelframe.Label', background='beige')
        s.configure('Blue.TButton', background='firebrick', foreground='snow')
        s.map('Blue.TButton', background=[('active', '!disabled', 'peru'), ('pressed', 'firebrick')],
              foreground=[('pressed', 'snow'), ('active', 'snow')])
        s.configure('TScrollbar', background='firebrick', foreground='beige')

        self.title("Lesson Flashcards")
        self.configure(background='beige')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.bind("<Configure>",self.resize_c)
        self.labelframeone = ttk.Labelframe(self,
                                            text="Choose Lessons", borderwidth=2,relief=tk.RIDGE,style="Red.TLabelframe")

        self.choice_label = ttk.Label(self.labelframeone, text="Select your lessons for the flash card game ",
                                      font=("Comic Sans",14,'bold'),background='beige',foreground='brown')
        self.scroll_frame = ttk.Frame(self.labelframeone)
        self.choice_list = tk.Listbox(self.scroll_frame,selectmode=tk.MULTIPLE,background='beige',selectbackground='sienna',selectforeground='white',bd=0)
        self.lesson_button = ttk.Button(self.labelframeone,text="Select Lessons",command = self.start_flashcards,style='Blue.TButton')

        self.lesson_list = DataCapture.get_Lessons()
        for element in self.lesson_list:
            self.choice_list.insert(tk.END,str(element[0])+' : '+element[1])
        self.labelframeone.grid(row = 0,sticky=tk.EW)
        self.choice_label.grid(row=0,column=0)
        self.scroll_frame.grid(row=1,column=0)
        self.choice_list.grid(row=0,column=0,sticky=tk.NSEW)
        self.lesson_button.grid(row=2,column=0)
        self.scrollbar = ttk.Scrollbar(self.scroll_frame,style='TScrollbar')
        self.choice_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.choice_list.yview)
        self.scrollbar.grid(row = 0,column=1,sticky=tk.NSEW)
        self.controlframe = tk.Frame(self,background='beige')
        self.show_leaderboard = ttk.Button(self.controlframe, text="Show Leaderboard", command=self.show_board,
                                        style='Blue.TButton')
        self.show_button = ttk.Button(self.controlframe, text="Show Lessons", command=self.show_lessons,
                                      style='Blue.TButton')

    # self.show_leaderboard.grid(row = 0, column=0,sticky=tk.W)

    def resize_c(self,event):
        if hasattr(self,"term_text"):
            self.term_text.configure( width=int(self.winfo_width()/60), height=int(self.winfo_height()/70))
        if hasattr(self, "answer_text"):
            self.answer_text.configure(width=int(self.winfo_width() / 60), height=int(self.winfo_height() / 70))

    def show_lessons(self):
        self.labelframetwo.grid_remove()
        self.labelframeone.grid(row=0,column=0,sticky=tk.EW)
        self.show_button.grid_remove()
        self.show_leaderboard.grid_remove()
        self.controlframe.grid_remove()

    def process_joystick(self):
       pass


    def start_flashcards(self):
        self.text_index = 0
        self.reveal_index = 0
        self.text_fact_index = 0
        self.labelframetwo = ttk.Labelframe(self,
                                            text="Flash Cards", borderwidth=2,relief=tk.RIDGE,style="Red.TLabelframe")

        self.twocontrolframe = tk.Frame(self.labelframetwo, background="beige")

        self.next_button = ttk.Button(self.twocontrolframe, text="Next Card",
                                      command=lambda: self.next_flashcard(self.text_index),
                                      style='Blue.TButton')
        self.reveal_button = ttk.Button(self.twocontrolframe, text="Reveal Card", command=self.answer_flashcard,
                                          style='Blue.TButton')
        self.reveal_button.configure(state="disabled")
        self.image_button = ttk.Button(self.twocontrolframe, text="Image Clue", command=self.image_flashcard,
                                        style='Blue.TButton')
        self.buttonimage = tk.PhotoImage(file="../images/speaker.png")


        self.flash_audio_button_description = ttk.Button(self.labelframetwo, text="hello", image=self.buttonimage,
                                                  command=lambda: self.play_quote_audio(self.quote_text),
                                                style='Green.TButton')
        self.labelframeone.grid_remove()

        self.controlframe.grid(row=0,column=0,sticky=tk.W)
        self.show_leaderboard.grid(row=0, column=0,padx=10)
        self.show_button.grid(row=0, column=1)

        lesson_list = []
        items = self.choice_list.curselection()
        for item in items:
            self.data = self.choice_list.get(item)
            index = self.data[0:self.data.index(':')-1]
            lesson_list.append(int(index.strip()))
        term_text_list = DataCapture.get_Fact_Terms(lesson_list)
        description_text_list = DataCapture.get_Fact_Descriptions(lesson_list)
        image_list = DataCapture.get_Images(lesson_list)

        self.all_terms = FlashUtils.expandList(term_text_list)
        self.all_descriptions = FlashUtils.expandList(description_text_list)
        self.all_images = FlashUtils.expandImageList(image_list)


        self.twocontrolframe.grid(row=0, column=0, sticky=tk.W)
        self.next_button.grid(row=0,column=4, sticky=tk.W,padx=5)

        self.reveal_button.grid(row=0, column=2, sticky=tk.W,padx=5)
        self.image_button.grid(row=0, column=3, sticky=tk.W, padx=5)

        self.term_text = tk.Text(self.labelframetwo, borderwidth=2, highlightthickness=0, relief=tk.RAISED,
                                 wrap=tk.WORD,width=int(self.winfo_width()/60), height=int(self.winfo_height()/70), font=("comic sans", 25), foreground="firebrick", background='beige',
                                )
        self.answer_text = tk.Text(self.labelframetwo, borderwidth=2, highlightthickness=0, relief=tk.RAISED,
                                   wrap=tk.WORD,width=int(self.winfo_width()/60), height=int(self.winfo_height()/70), font=("comic sans", 25), foreground="firebrick", background='beige',
                                  )
        self.labelframetwo.grid(row=1, column=0, padx=200,pady=100,sticky=tk.NSEW)
        self.next_flashcard(self.text_index)
        #self.leaderboard.grid(row=1, column=1)

    def next_flashcard(self,indexa):

        self.reveal_button.configure(state="enabled")
        self.term_text.delete(1.0, tk.END)
        self.answer_text.delete(1.0, tk.END)
        print("next"+str(indexa))
        self.term_text.insert(1.0, self.all_terms[indexa])
        self.term_text.grid(row=1,column=0,padx=25,pady=10)
        self.text_index += 1
        if self.text_index == len(self.all_terms) :
            self.text_index = 0
        self.flash_audio_button_term = ttk.Button(self.labelframetwo, text="hello", image=self.buttonimage,
                                                  command=lambda: self.play_term_audio( self.all_terms[indexa]),
                                                  style='Blue.TButton')
        self.flash_audio_button_term.grid(row=1,column=1,padx=15)
        self.animate_flashcard(self.term_text,0)

    def animate_flashcard(self,text,index):
        if text.cget('background')=="bisque2":
            text.configure(background="beige")
        else:
            text.configure(background="bisque2")
        if(index == 5):
            return
        index += 1
        self.after(1000,self.animate_flashcard,text,index)

    def answer_flashcard(self):
        self.answer_text.delete(1.0, tk.END)
        self.reveal_index = self.text_index - 1

        self.answer_text.insert(1.0, self.all_descriptions[self.reveal_index])
        self.flash_audio_button_description = ttk.Button(self.labelframetwo, text="hello", image=self.buttonimage,
                                                  command=lambda: self.play_term_audio(self.all_descriptions[self.reveal_index]),
                                                  style='Blue.TButton')

        self.answer_text.grid(row=1,column=3,padx=15)
        self.flash_audio_button_description.grid(row=1, column=4)




    def play_term_audio(self,text):
        FlashUtils.playtextsound(text)

    def  image_flashcard(self):
            win = tk.Toplevel()
            win.wm_title("Image Clue")
            win.wm_geometry('400x400+500+300')
            win.configure(background='beige')

            self.image_clue = ImageTk.PhotoImage(Image.open(DataCapture.file_root+os.path.sep+"Lessons"+
                                                            os.path.sep+"Lesson"+str(self.all_images[self.text_index-1][0])+os.path.sep+
                                                            "images"+os.path.sep+self.all_images[self.text_index-1][1]).resize((400,400)))
            self.image_label = ttk.Label(win,image=self.image_clue)
            self.image_label.grid(row=0, column=0)

            b = ttk.Button(win, text="Close",style='Blue.TButton', command=win.destroy)
            b.grid(row=1, column=0)

    def show_board(self):
        win = tk.Toplevel()
        win.wm_title("Leaderboard")
        win.wm_geometry('300x400+500+500')
        win.configure(background='beige')
        self.leaderboard = FlashLeaderBoard.MagicLeaderBoard(win)
        self.leaderboard.grid(row=0, column =0)

        b = ttk.Button(win, text="Close", style='Blue.TButton', command=win.destroy)
        b.grid(row=1, column=0)




if __name__ == "__main__":
    app = MagicFlashApplication()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    app.geometry(str(screen_width)+'x'+str(screen_height)+'+5+5')
    a = threading.Thread(target=app.process_joystick,name="gamepad",daemon=True)
    print(a)
    a.start()
    app.mainloop()

