import tkinter as tk
from tkinter import ttk
import LessonList

if __name__ == "__main__":
    root = tk.Tk()
    def launch_selector():
        global root
        app = LessonList.MagicLessonList(bg='dark slate gray', fg='white', buttonbg='dark olive green', selectmode=tk.MULTIPLE,
                                         buttonfg='snow', parent=root)
        root.wait_window(app)
        print(root.selected_lessons)




    buttona = ttk.Button(text="Click Me!", command=launch_selector)
    buttona.pack()
    root.mainloop()

