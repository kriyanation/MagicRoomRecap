import tkinter as tk
from tkinter import ttk
import DataCapture

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
                                            text="Choose Lessons", borderwidth=0,relief=tk.RIDGE,style="Red.TLabelframe")

        self.choice_label = ttk.Label(self.labelframeone, text="Select your lessons for the flash card game ",
                                      font=("Comic Sans",14,'bold'),background='beige',foreground='brown')
        self.scroll_frame = ttk.Frame(self.labelframeone)
        self.choice_list = tk.Listbox(self.scroll_frame,selectmode=tk.MULTIPLE,background='beige',selectbackground='sienna',selectforeground='white',bd=0)
        self.lesson_button = ttk.Button(self.labelframeone,text="Select Lessons",command = self.start_flashcards,style='Blue.TButton')
        self.lesson_list = DataCapture.get_Lessons()
        for element in self.lesson_list:
            self.choice_list.insert(tk.END,str(element[0])+' : '+element[1])
        self.labelframeone.grid(row = 0,sticky=tk.EW,padx=self.screen_width/3)
        self.choice_label.grid(row=0,column=0)
        self.scroll_frame.grid(row=1,column=0)
        self.choice_list.grid(row=0,column=0,sticky=tk.NSEW)
        self.lesson_button.grid(row=2,column=0)
        self.scrollbar = ttk.Scrollbar(self.scroll_frame,style='TScrollbar')
        self.choice_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.choice_list.yview)
        self.scrollbar.grid(row = 0,column=1,sticky=tk.NSEW)



    def start_flashcards(self):
        self.labelframetwo = ttk.Labelframe(self, width=self.screen_width - 40, height=self.screen_height /1.5,
                                            text="Flash Cards", borderwidth=0,relief=tk.RIDGE,style="Red.TLabelframe")


        lesson_list = []
        items = self.choice_list.curselection()
        for item in items:
            self.data = self.choice_list.get(item)
            index = self.data[0:self.data.index(':')-1]
            lesson_list.append(int(index.strip()))
        self.term_text_list = DataCapture.get_Fact_Terms(lesson_list)
        self.description_text_list = DataCapture.get_Fact_Descriptions(lesson_list)
        self.image_list = DataCapture.get_Images(lesson_list)




if __name__ == "__main__":
    app = MagicFlashApplication()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    app.geometry(str(screen_width)+'x'+str(screen_height)+'+5+5')
    app.mainloop()

