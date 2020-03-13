import tkinter as tk
from tkinter import ttk
import DataCapture, FlashUtils,FlashLeaderBoard, threading
from PIL import ImageTk, Image

from evdev import InputDevice, categorize, ecodes


class MagicFlashApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s = ttk.Style(self)
        s.configure('Red.TLabelframe', background='beige')
        s.configure('Red.TLabelframe.Label', font=('courier', 14, 'bold', 'italic'))
        s.configure('Red.TLabelframe.Label', foreground='brown')
        s.configure('Red.TLabelframe.Label', background='beige')
        s.configure('Blue.TButton', background='firebrick', foreground='snow')
        s.map('Blue.TButton', background=[('active', '!disabled', 'peru'), ('pressed', 'firebrick')],
              foreground=[('pressed', 'snow'), ('active', 'snow')])
        s.configure('TScrollbar', background='firebrick', foreground='beige')

        self.title("FlashClues Recap")
        self.configure(background='beige')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.labelframeone = ttk.Labelframe(self, width=self.screen_width / 2.0, height=self.screen_height / 2.2,
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

    def show_lessons(self):
        self.labelframetwo.grid_remove()
        self.labelframeone.grid(row=0,column=0,sticky=tk.EW)
        self.show_button.grid_remove()
        self.show_leaderboard.grid_remove()
        self.controlframe.grid_remove()

    def process_joystick(self):
        self.gamepad = InputDevice("/dev/input/event16")
        print(self.gamepad)
        for event in self.gamepad.read_loop():
            print(categorize(event))
            if event.type == ecodes.EV_KEY:
                if (event.code==115 and event.value==0):
                    self.next_flashcard(self.text_index)
                if (event.code==114 and event.value==0):
                    self.next_flashcard(self.text_index)
                if (event.code==212 and event.value==0):
                    self.answer_flashcard()


    def start_flashcards(self):
        self.text_index = 0
        self.reveal_index = 0
        self.text_fact_index = 0
        self.labelframetwo = ttk.Labelframe(self, width=self.screen_width/1.5, height=self.screen_height /1.2,
                                            text="Flash Cards", borderwidth=2,relief=tk.RIDGE,style="Red.TLabelframe")

        self.twocontrolframe = tk.Frame(self.labelframetwo, background="beige")

        self.next_button = ttk.Button(self.twocontrolframe, text="Next Card",
                                      command=lambda: self.next_flashcard(self.text_index),
                                      style='Blue.TButton')
        self.reveal_button = ttk.Button(self.twocontrolframe, text="Reveal Card", command=self.answer_flashcard,
                                          style='Blue.TButton')
        self.image_button = ttk.Button(self.twocontrolframe, text="Image Clue", command=self.image_flashcard,
                                        style='Blue.TButton')
        self.buttonimage = tk.PhotoImage(file="./images/speaker.png")


        self.flash_audio_button_description = ttk.Button(self.labelframetwo, text="hello", image=self.buttonimage,
                                                  command=lambda: self.play_quote_audio(self.quote_text),
                                                  style='Green.TButton')
        self.labelframeone.grid_remove()
        self.show_leaderboard.grid_forget()
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
        self.all_images = FlashUtils.expandList(image_list)

        self.labelframetwo.grid(row=1,column=0,padx = 200,sticky=tk.EW)
        self.labelframetwo.grid_propagate(False)
        self.twocontrolframe.grid(row=0, column=0, sticky=tk.W)
        self.next_button.grid(row=0,column=4, sticky=tk.W,padx=5)

        self.reveal_button.grid(row=0, column=2, sticky=tk.W,padx=5)
        self.image_button.grid(row=0, column=3, sticky=tk.W, padx=5)
        self.term_text = tk.Text(self.labelframetwo, borderwidth=2, highlightthickness=0, relief=tk.RAISED,
                                 wrap=tk.WORD, font=("comic sans", 25), foreground="firebrick", background='beige',
                                 width=50, height=5)
        self.answer_text = tk.Text(self.labelframetwo, borderwidth=2, highlightthickness=0, relief=tk.RAISED,
                                   wrap=tk.WORD, font=("comic sans", 25), foreground="firebrick", background='beige',
                                   width=50, height=15)


        #self.leaderboard.grid(row=1, column=1)

    def next_flashcard(self,indexa):

        self.term_text.delete(1.0, tk.END)
        self.answer_text.delete(1.0, tk.END)
        print("next"+str(indexa))
        self.term_text.insert(1.0, self.all_terms[indexa])
        self.term_text.grid(row=1,column=0,columnspan=4,padx=25,pady=10)
        self.text_index += 1
        if self.text_index == len(self.all_terms) :
            self.text_index = 0
        self.flash_audio_button_term = ttk.Button(self.labelframetwo, text="hello", image=self.buttonimage,
                                                  command=lambda: self.play_term_audio( self.all_terms[indexa]),
                                                  style='Blue.TButton')
        self.flash_audio_button_term.grid(row=1,column=5)

    def answer_flashcard(self):
        self.answer_text.delete(1.0, tk.END)
        self.reveal_index = self.text_index - 1

        self.answer_text.insert(1.0, self.all_descriptions[self.reveal_index])
        self.flash_audio_button_description = ttk.Button(self.labelframetwo, text="hello", image=self.buttonimage,
                                                  command=lambda: self.play_term_audio(self.all_descriptions[self.reveal_index]),
                                                  style='Blue.TButton')

        self.answer_text.grid(row=2,column=0,padx=15,columnspan=4)
        self.flash_audio_button_description.grid(row=2, column=5)




    def play_term_audio(self,text):
        FlashUtils.playtextsound(text)

    def  image_flashcard(self):
            win = tk.Toplevel()
            win.wm_title("Image Clue")
            win.wm_geometry('300x300+500+500')
            win.configure(background='beige')

            self.image_clue = ImageTk.PhotoImage(Image.open('../MagicRoomPlayer/images/'+self.all_images[self.text_index-1]))
            self.image_label = ttk.Label(win,image=self.image_clue)
            self.image_label.grid(row=0, column=0)

            b = ttk.Button(win, text="Close",style='Blue.TButton', command=win.destroy)
            b.grid(row=1, column=0)

    def show_board(self):
        win = tk.Toplevel()
        win.wm_title("Leaderboard")
        win.wm_geometry('300x300+500+500')
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

