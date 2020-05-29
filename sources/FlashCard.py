import os
import tkinter as tk
from tkinter import ttk
import threading,configparser

import LessonListFlash
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
        s.configure('Red.TLabelframe', background='deepskyblue4',bordercolor="royalblue4")
        s.configure('Red.TLabelframe.Label', font=('helvetica', 15, 'bold'))
        s.configure('Red.TLabelframe.Label', foreground='white')
        s.configure('Red.TLabelframe.Label', background='deepskyblue4')
        s.configure('Blue.TButton', background='cyan', foreground='royalblue4',font=('helvetica', 12, 'bold'),bordercolor="royalblue4")
        s.map('Blue.TButton', background=[('active', '!disabled', 'cyan'), ('pressed', 'white')],
                   foreground=[('pressed', 'royalblue4'), ('active', 'royalblue4')])
        s.configure('TScrollbar', background='royalblue4', foreground='deepskyblue4')
        s.map('TScrollbar', background=[('active', '!disabled', 'deepskyblue4'), ('pressed', 'white')],
              foreground=[('pressed', 'royalblue4'), ('active', 'royalblue4')])

        self.title("Lesson Flashcards")
        self.configure(background='deepskyblue4')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.bind("<Configure>",self.resize_c)




        self.lesson_list = []
        app = LessonListFlash.MagicLessonList(parent=self)
        app.geometry("350x600+50+50")
        self.wait_window(app)
        self.start_flashcards()


    def resize_c(self,event):
        if hasattr(self,"term_text"):
            self.term_text.configure( width=int(self.winfo_width()/60), height=int(self.winfo_height()/70))
        if hasattr(self, "answer_text"):
            self.answer_text.configure(width=int(self.winfo_width() / 60), height=int(self.winfo_height() / 70))




    def start_flashcards(self):
        self.text_index = 0
        self.reveal_index = 0
        self.text_fact_index = 0
        self.labelframetwo = ttk.Labelframe(self,
                                            text="Flash Cards", borderwidth=2,relief=tk.RIDGE,style="Red.TLabelframe")

        self.twocontrolframe = tk.Frame(self.labelframetwo, background="deepskyblue4")

        self.next_button = ttk.Button(self.twocontrolframe, text="Next Card",
                                      command=lambda: self.next_flashcard(self.text_index),
                                      style='Blue.TButton')
        self.reveal_button = ttk.Button(self.twocontrolframe, text="Reveal Card", command=self.answer_flashcard,
                                          style='Blue.TButton')
        self.reveal_button.configure(state="disabled")
        self.image_button = ttk.Button(self.twocontrolframe, text="Image Clue", command=self.image_flashcard,
                                        style='Blue.TButton')
        self.show_leaderboard = ttk.Button(self.twocontrolframe, text="Show Leaderboard", command=self.show_board,
                                           style='Blue.TButton')
        self.buttonimage = tk.PhotoImage(file="../images/speaker.png")











        term_text_list = data_capture_flashcard.get_Fact_Terms(self.lesson_list)
        description_text_list = data_capture_flashcard.get_Fact_Descriptions(self.lesson_list)
        image_list = data_capture_flashcard.get_Images(self.lesson_list)

        self.all_terms = FlashUtils.expandList(term_text_list)
        self.all_descriptions = FlashUtils.expandList(description_text_list)
        self.all_images = FlashUtils.expandImageList(image_list)


        self.twocontrolframe.grid(row=0, column=0, sticky=tk.W,pady=5)
        self.next_button.grid(row=0,column=4, sticky=tk.W,padx=5)

        self.reveal_button.grid(row=0, column=2, sticky=tk.W,padx=5)
        self.image_button.grid(row=0, column=3, sticky=tk.W, padx=5)
        self.show_leaderboard.grid(row=0, column=1, padx=10)

        self.term_text = tk.Text(self.labelframetwo, borderwidth=2, highlightthickness=0, relief=tk.RAISED,highlightcolor="royalblue4",
                                 wrap=tk.WORD,width=int(self.winfo_width()/60), height=int(self.winfo_height()/70), font=("comic sans", 25), foreground="royalblue4", background='white',
                                )
        self.answer_text = tk.Text(self.labelframetwo, borderwidth=2, highlightthickness=0, relief=tk.RAISED,highlightcolor="royalblue4",
                                   wrap=tk.WORD,width=int(self.winfo_width()/60), height=int(self.winfo_height()/70), font=("comic sans", 25), foreground="royalblue4", background='white',
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
            win.configure(background='deepskyblue4')

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
        win.wm_geometry('315x600+100+100')
        win.configure(background='deepskyblue4')
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

