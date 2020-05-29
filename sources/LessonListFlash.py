import tkinter as tk
from tkinter import ttk, Toplevel
import data_capture_flashcard

class MagicLessonList(Toplevel):
    def __init__(self,parent,*args, **kwargs):
        Toplevel.__init__(self,parent,*args, **kwargs)
        self.transient(parent)
        self.parent = parent

        s = ttk.Style(self)
        s.theme_use('clam')
        s.configure('Red.TLabelframe', background="deepskyblue4")
        s.configure('Red.TLabelframe.Label', font=('helvetica', 14, 'bold'))
        s.configure('Red.TLabelframe.Label', foreground="white")
        s.configure('Red.TLabelframe.Label', background="deepskyblue4")
        s.configure('Blue.TButton', background="white", foreground="royalblue4")
        s.map('Blue.TButton', background=[('active', '!disabled', 'cyan'), ('pressed', "white")],
              foreground=[('pressed', "royalblue4"), ('active', "royalblue4")])
        s.configure('TScrollbar', background='royalblue4', foreground='steelblue4')
        s.map('TScrollbar', background=[('active', '!disabled', 'steelblue4'), ('pressed', 'white')],
              foreground=[('pressed', 'royalblue4'), ('active', 'royalblue4')])
        self.configure(background="steelblue4")
        self.grab_set()

        self.choice_label = ttk.Label(self, text="Select the Lesson to Learn",
                                      font=("helvetica", 14, 'bold'), background="steelblue4", foreground="white")
        self.scroll_frame = ttk.Frame(self)
        self.choice_list = tk.Listbox(self.scroll_frame, selectmode=tk.MULTIPLE, background="white",font=("helvetica",10,"bold"),
                                      selectbackground='royalblue4', selectforeground='white',foreground="royalblue4", width=40,height=25, bd=0)
        self.lesson_button = ttk.Button(self, text="Select Lesson",
                                        style='Blue.TButton',command=lambda:self.select_lesson(parent))

        self.lesson_list = data_capture_flashcard.get_Lessons()
        for element in self.lesson_list:
            self.choice_list.insert(tk.END, str(element[0]) + ' : ' + element[1])
        self.choice_label.grid(row=0, column=0)
        self.scroll_frame.grid(row=1, column=0,sticky=tk.NSEW,padx=10)
        self.choice_list.grid(row=0, column=0, sticky=tk.NSEW)
        self.lesson_button.grid(row=2, column=0,pady=5)
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, style='TScrollbar')
        self.choice_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.choice_list.yview)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

    def select_lesson(self,parent):
        items = self.choice_list.curselection()
        for item in items:
            self.data = self.choice_list.get(item)
            index = self.data[0:self.data.index(':') - 1]
            parent.lesson_list.append(int(index.strip()))

        self.destroy()


#if __name__ == "__main__":
    #app = MagicLessonList(bg='dark slate gray',fg='white',buttonbg='dark olive green',selectmode=tk.MULTIPLE,buttonfg='snow')
    #screen_width = app.winfo_screenwidth()
    #screen_height = app.winfo_screenheight()
    #app.geometry(str(screen_width) + 'x' + str(screen_height) + '+5+5')
    #app.mainloop()