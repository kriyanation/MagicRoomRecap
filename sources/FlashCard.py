import os
import tkinter as tk
from tkinter import ttk
import threading,configparser
import data_capture_flashcard, FlashUtils, FlashLeaderBoard
from pathlib import Path
from PIL import ImageTk, Image





class MagicFlashApplication(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s = ttk.Style(self)
        s.theme_use('clam')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        s.configure('Red.TLabelframe', background='steelblue3',bordercolor="midnight blue")
        s.configure('Red.TLabelframe.Label', font=('helvetica', 15, 'bold'))
        s.configure('Red.TLabelframe.Label', foreground='white')
        s.configure('Red.TLabelframe.Label', background='steelblue3')
        s.configure('Blue.TButton', background='white', foreground='midnight blue',font=('helvetica', 12, 'bold'),bordercolor="midnight blue")
        s.map('Blue.TButton', background=[('active', '!disabled', 'cyan'), ('pressed', 'white')],
              foreground=[('pressed', 'midnight blue'), ('active', 'midnight blue')])
        s.configure('TScrollbar', background='midnight blue', foreground='steelblue3')
        s.map('TScrollbar', background=[('active', '!disabled', 'steelblue3'), ('pressed', 'snow')],
              foreground=[('pressed', 'midnight blue'), ('active', 'midnight blue')])

        self.title("Lesson Flashcards")
        self.configure(background='steelblue3')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.bind("<Configure>",self.resize_c)
        self.labelframeone = ttk.Labelframe(self,
                                            text="Choose Lessons", borderwidth=2,relief=tk.RIDGE,style="Red.TLabelframe")

        self.choice_label = ttk.Label(self.labelframeone, text="Select your lessons for the flash card game ",
                                      font=("helvetica",16,'bold'),background='steelblue3',foreground='white')
        self.scroll_frame = ttk.Frame(self.labelframeone)
        self.choice_list = tk.Listbox(self.scroll_frame,highlightbackground="midnight blue",selectmode=tk.MULTIPLE,background='white',selectbackground='midnight blue',selectforeground='white',foreground ="midnight blue",bd=2)
        self.lesson_button = ttk.Button(self.labelframeone,text="Select Lessons",command = self.start_flashcards,style='Blue.TButton')

        self.lesson_list = data_capture_flashcard.get_Lessons()
        for element in self.lesson_list:
            self.choice_list.insert(tk.END,str(element[0])+' : '+element[1])
        self.labelframeone.grid(row = 0,sticky=tk.EW)
        self.choice_label.grid(row=0,column=0)
        self.scroll_frame.grid(row=1,column=0)
        self.choice_list.grid(row=0,column=0,sticky=tk.NSEW)
        self.lesson_button.grid(row=2,column=0,pady=10)
        self.scrollbar = ttk.Scrollbar(self.scroll_frame,style='TScrollbar')
        self.choice_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.choice_list.yview)
        self.scrollbar.grid(row = 0,column=1,sticky=tk.NSEW)
        self.controlframe = tk.Frame(self,background='steelblue3')
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

        self.twocontrolframe = tk.Frame(self.labelframetwo, background="steelblue3")

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

        self.controlframe.grid(row=0,column=0,sticky=tk.W,pady=5)
        self.show_leaderboard.grid(row=0, column=0,padx=10)
        self.show_button.grid(row=0, column=1)

        lesson_list = []
        items = self.choice_list.curselection()
        for item in items:
            self.data = self.choice_list.get(item)
            index = self.data[0:self.data.index(':')-1]
            lesson_list.append(int(index.strip()))
        term_text_list = data_capture_flashcard.get_Fact_Terms(lesson_list)
        description_text_list = data_capture_flashcard.get_Fact_Descriptions(lesson_list)
        image_list = data_capture_flashcard.get_Images(lesson_list)

        self.all_terms = FlashUtils.expandList(term_text_list)
        self.all_descriptions = FlashUtils.expandList(description_text_list)
        self.all_images = FlashUtils.expandImageList(image_list)


        self.twocontrolframe.grid(row=0, column=0, sticky=tk.W,pady=5)
        self.next_button.grid(row=0,column=4, sticky=tk.W,padx=5)

        self.reveal_button.grid(row=0, column=2, sticky=tk.W,padx=5)
        self.image_button.grid(row=0, column=3, sticky=tk.W, padx=5)

        self.term_text = tk.Text(self.labelframetwo, borderwidth=2, highlightthickness=0, relief=tk.RAISED,highlightcolor="midnight blue",
                                 wrap=tk.WORD,width=int(self.winfo_width()/60), height=int(self.winfo_height()/70), font=("comic sans", 25), foreground="midnight blue", background='white',
                                )
        self.answer_text = tk.Text(self.labelframetwo, borderwidth=2, highlightthickness=0, relief=tk.RAISED,highlightcolor="midnight blue",
                                   wrap=tk.WORD,width=int(self.winfo_width()/60), height=int(self.winfo_height()/70), font=("comic sans", 25), foreground="midnight blue", background='white',
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
        if text.cget('background')=="white":
            text.configure(background="cyan")
        else:
            text.configure(background="white")
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
        sound_speak = threading.Thread(target=FlashUtils.playtextsound,
                                       args=(text, 'f'))
        sound_speak.start()


    def  image_flashcard(self):
            win = tk.Toplevel()
            win.wm_title("Image Clue")
            win.wm_geometry('360x400+500+300')
            win.configure(background='steelblue3')

            self.image_clue = ImageTk.PhotoImage(Image.open(data_capture_flashcard.file_root+os.path.sep+"Lessons"+
                                                            os.path.sep+"Lesson"+str(self.all_images[self.text_index-1][0])+os.path.sep+
                                                            "images"+os.path.sep+self.all_images[self.text_index-1][1]).resize((350,350)))
            self.image_label = ttk.Label(win,image=self.image_clue)
            self.image_label.grid(row=0, column=0)
            win.attributes("-topmost", True)
            b = ttk.Button(win, text="Close",style='Blue.TButton', command=win.destroy)
            b.grid(row=1, column=0,pady=5)

    def show_board(self):
        win = tk.Toplevel()
        win.wm_title("Leaderboard")
        win.wm_geometry('315x400+500+500')
        win.configure(background='steelblue3')
        win.attributes("-topmost",True)
        self.leaderboard = FlashLeaderBoard.MagicLeaderBoard(win)
        self.leaderboard.grid(row=0, column =0)

        b = ttk.Button(win, text="Close", style='Blue.TButton', command=win.destroy)
        b.grid(row=1, column=0,pady=5)




if __name__ == "__main__":
    app = MagicFlashApplication()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    app.geometry(str(screen_width)+'x'+str(screen_height)+'+5+5')
    a = threading.Thread(target=app.process_joystick,name="gamepad",daemon=True)
    print(a)
    a.start()
    app.mainloop()

