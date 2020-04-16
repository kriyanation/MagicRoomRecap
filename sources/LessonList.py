import tkinter as tk
from tkinter import ttk, Toplevel
import DataCapture


class MagicLessonList(Toplevel):
    def __init__(self, bg,fg,buttonbg,buttonfg,selectmode,parent,*args, **kwargs):
        Toplevel.__init__(self,parent,*args, **kwargs)
        self.transient(parent)
        self.parent = parent

        s = ttk.Style(self)
        s.configure('Red.TLabelframe', background=bg)
        s.configure('Red.TLabelframe.Label', font=('courier', 14, 'bold', 'italic'))
        s.configure('Red.TLabelframe.Label', foreground=fg)
        s.configure('Red.TLabelframe.Label', background=bg)
        s.configure('Blue.TButton', background=buttonbg, foreground=buttonfg)
        s.map('Blue.TButton', background=[('active', '!disabled', 'peru'), ('pressed', buttonbg)],
              foreground=[('pressed', buttonfg), ('active', buttonfg)])
        s.configure('TScrollbar', background=buttonbg, foreground=buttonfg)
        self.configure(background=bg)
        self.grab_set()

        self.choice_label = ttk.Label(self, text="Select your lessons for the flash card game ",
                                      font=("Comic Sans", 14, 'bold'), background=bg, foreground=fg)
        self.scroll_frame = ttk.Frame(self)
        self.choice_list = tk.Listbox(self.scroll_frame, selectmode=selectmode, background=bg,
                                      selectbackground='sienna', selectforeground='white',foreground=fg)
        self.lesson_button = ttk.Button(self, text="Select Lessons",
                                        style='Blue.TButton',command=self.select_lesson)

        self.lesson_list = DataCapture.get_Lessons()
        for element in self.lesson_list:
            self.choice_list.insert(tk.END, str(element[0]) + ' : ' + element[1])
        self.choice_label.grid(row=0, column=0)
        self.scroll_frame.grid(row=1, column=0)
        self.choice_list.grid(row=0, column=0, sticky=tk.NSEW)
        self.lesson_button.grid(row=2, column=0)
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, style='TScrollbar')
        self.choice_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.choice_list.yview)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

    def select_lesson(self):
        self.parent.selected_lessons = self.choice_list.curselection()
        self.destroy()


#if __name__ == "__main__":
    #app = MagicLessonList(bg='dark slate gray',fg='white',buttonbg='dark olive green',selectmode=tk.MULTIPLE,buttonfg='snow')
    #screen_width = app.winfo_screenwidth()
    #screen_height = app.winfo_screenheight()
    #app.geometry(str(screen_width) + 'x' + str(screen_height) + '+5+5')
    #app.mainloop()