import tkinter as tk
from tkinter import ttk,StringVar
from sources import DataCapture


class MagicLeaderBoard(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(background='')
        s = ttk.Style(self)
        s.configure('Red.TLabelframe', background='beige')
        s.configure('Red.TLabelframe.Label', font=('courier', 12, 'bold','italic'))
        s.configure('Red.TLabelframe.Label', foreground='brown')
        s.configure('Red.TLabelframe.Label', background='beige')

        s.configure('Blue.TButton', background='firebrick', foreground='snow')
        s.map('Blue.TButton', background=[('active', '!disabled', 'peru'), ('pressed', 'firebrick')],
              foreground=[('pressed', 'snow'), ('active', 'snow')])
        s.configure('TScrollbar', background='firebrick', foreground='beige')



       # self.leaderboard = ttk.LabelFrame(self, text = "Class Leaderboard", width=parent.screen_width/4, height=parent.screen_height,borderwidth=8,relief=tk.GROOVE,style='Red.TLabelframe')
        self.leaderboard = tk.Text(self, width=100,
                                          height=300, borderwidth=8, relief=tk.GROOVE,
                                          background='beige', foreground='brown')
        self.dataframe= tk.Frame(self.leaderboard)
        self.dataframe.configure(background='beige')
        self.refreshbutton = ttk.Button(self.dataframe,text="Refresh",style='Blue.TButton',command=self.refresh_data,cursor="arrow")
        self.savebutton = ttk.Button(self.dataframe,text="Save",style='Blue.TButton',command=self.save_data,cursor="arrow")
        self.dataframe.grid(row=0,column=0,columnspan=3)
        self.refreshbutton.grid(row=0,column=0)
        self.savebutton.grid(row=0,column=1,padx=5)

        self.scrollbar = ttk.Scrollbar(self)
        self.leaderboard.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0,column=3,sticky="nsew")

        self.scrollbar.config(command=self.leaderboard.yview, style='TScrollbar')
        self.leaderboard.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.headernamelabel = ttk.Label(self.leaderboard, text="Name", font = ('TkDefaultFont', 16),background='beige', foreground = 'brown')
        self.headerbadgelabel = ttk.Label(self.leaderboard, text="Badge", font=('TkDefaultFont', 16),background='beige', foreground='brown')
        self.headerpointslabel = ttk.Label(self.leaderboard, text="Points", font=('TkDefaultFont', 16),background='beige', foreground='brown')

        self.headernamelabel.grid(row=1, column=0, padx=10, pady=2)
        self.headerbadgelabel.grid(row=1, column=1,padx=10, pady=2)
        self.headerpointslabel.grid(row=1, column=2,padx=10, pady=2)
        self.refresh_data()

    def refresh_data(self):

        self.spinboxvalue = []
        self.list_points = []
        self.leaderboard.configure(state="normal")
        list_names = DataCapture.class_info()
        rowindex = 2
        self.badge_image_medala = tk.PhotoImage(file= '../images/medala.png' )
        self.badge_image_medalb = tk.PhotoImage(file= '../images/medalb.png' )
        self.badge_image_medalc = tk.PhotoImage(file='../images/medalc.png')
        for element in list_names:
            self.datanamelabel = ttk.Label(self.leaderboard, text=element[0].strip(), font = ('TkDefaultFont', 12),
                                           foreground = 'brown',wraplength = 100,background='beige')
            if element[1].strip() == 'a':
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medala,background='beige')
            elif element[1].strip() == 'b':
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medalb,background='beige')
            else:
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medalc,
                                                background='beige')

            points = StringVar()
            points.set(str(element[2]))
            self.spinboxvalue.append(points)
            print("rowindex"+str(rowindex))
            self.datapointspinner = ttk.Spinbox(self.leaderboard,background='beige',foreground='brown',font=('TkDefaultFont', 12),
                                                from_=0,to=100,textvariable=self.spinboxvalue[rowindex-2],wrap=True,width=2)

            self.list_points.append((element[0],self.spinboxvalue[rowindex-2]))

           # self.datapointslabel = ttk.Label(self.leaderboard, text=element[2], font=('TkDefaultFont', 12),
           #                                foreground='PeachPuff2',background='dark slate gray')
            self.datanamelabel.grid(row=rowindex, column=0, padx=10, pady=3,sticky=tk.W)
            self.databadgelabel.grid(row=rowindex, column=1, padx=10, pady=3)
            self.datapointspinner.grid(row=rowindex, column=2, padx=10, pady=3)
            rowindex += 1
            self.leaderboard.configure(state="disabled")

    def save_data(self):
        DataCapture.save_leader_board_data(self.list_points)




