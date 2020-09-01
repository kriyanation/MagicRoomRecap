import os
import tkinter as tk
import random
from tkinter import ttk

import LessonListFlash
import LessonListNinja
import data_capture_flashcard, FlashUtils, FlashLeaderBoard

import tooltip
from PIL import ImageTk, Image
import tkinter.scrolledtext as sText

class MagicNinja(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s = ttk.Style(self)
        s.theme_use('clam')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        s.configure('Red.TLabelframe', background='deepskyblue4', bordercolor="royalblue4")
        s.configure('Red.TLabelframe.Label', font=('helvetica', 15, 'bold'))
        s.configure('Red.TLabelframe.Label', foreground='white')
        s.configure('Red.TLabelframe.Label', background='deepskyblue4')
        s.configure('Blue.TButton', background='deepskyblue4', foreground='snow', font=('helvetica', 12, 'bold'),
                    bordercolor="royalblue4")
        s.map('Blue.TButton', background=[('active', '!disabled', 'cyan'), ('pressed', 'white')],
              foreground=[('pressed', 'royalblue4'), ('active', 'royalblue4')])
        s.configure('TScrollbar', background='royalblue4', foreground='deepskyblue4')
        s.map('TScrollbar', background=[('active', '!disabled', 'deepskyblue4'), ('pressed', 'white')],
              foreground=[('pressed', 'royalblue4'), ('active', 'royalblue4')])

        self.title("Lesson Flashcards")
        self.configure(background='deepskyblue4')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()



        app = LessonListNinja.MagicLessonListNinja(parent=self)
        app.geometry("350x700+50+50")
        self.wait_window(app)
        if hasattr(self, "selected_lessons") is False:
            self.destroy()
        print(self.selected_lessons)
        experiment_steps, experiment_images, number_steps = data_capture_flashcard.get_experiment_content(self.selected_lessons[0])

        self.restart_button = ttk.Button(self, text="Restart",
                                         width=16,
                                         command=lambda: self.restart(experiment_images, experiment_steps),
                                         style='Blue.TButton')
        self.restart_button.pack()
        self.start_ninja(experiment_images,experiment_steps)
    def restart(self,experiment_images,experiment_steps):
        self.canvas.pack_forget()
        self.start_ninja(experiment_images, experiment_steps)
    def start_ninja(self,images,texts):
                # provide a list of images(full directory) and list of texts
        self.images = images
        self.texts = texts
        self.score = 0

        self.activeLeftBlock = 0
        self.activeRightBlock = 4
        self.ninjaStatus = 'walking'  # Keep track of ninja
        self.winHeight = self.winfo_screenheight()
        self.winWidth = self.winfo_screenwidth()
        # self.attributes('-fullscreen',True)
        self.ninjaWidth = 58
        self.ninjaHeight = 110
        self.xrameHeight = 115
        self.xrameWidth = 335
        self.leftstackx = 500  # coord of the left blocks
        self.ninjaTime = 0
        self.mainCount = 0  # current count
        self.leftBlocksCoords = []  # Track of the coords of left blocks
        self.rightBlocksCoords = []  # right
        self.leftstacky = self.winHeight - 115 - 80
        self.rightstackx = 500 + self.xrameWidth
        self.rightstacky = self.winHeight - 115 - 80
        self.leftstackx1 = self.leftstackx - self.xrameWidth
        print(self.winfo_vrootheight(), self.winfo_vrootwidth())
        print(self.winHeight, self.winWidth)
        self.spriteData()  # Loads the sprites
        self.gui()
        self.geometry('1200x720')
        #self.mainloop()

    def spriteData(self):
        self.ninjaImage = tk.PhotoImage(file='../images/ninja/ninja.png')
        self.ninjaImage2 = tk.PhotoImage(file='../images/ninja/ninja2.png')
        self.ladderImage = tk.PhotoImage(file='../images/ninja/rLadder.png')
        self.climbImage = tk.PhotoImage(file='../images/ninja/climb1.png')
        self.climbImage2 = tk.PhotoImage(file='../images/ninja/climb2.png')
        print(self.ninjaImage)

    def gui(self):
        self.canvas = tk.Canvas(self,
                             bg='deepskyblue4')
        self.canvas.pack(fill=tk.BOTH, expand=2)
        self.base = self.canvas.create_rectangle(0, self.winHeight, self.winWidth, self.winHeight - 80, fill='cyan')
        # grid1->left grid grid2->right
        self.grid1 = self.canvas.create_rectangle(0, self.winHeight - 50, 500, (self.winHeight - 115 - 80),
                                                  fill='tomato2')
        self.grid2 = self.canvas.create_rectangle(500 + self.xrameWidth, self.winHeight - 50, self.winWidth,
                                                  (self.winHeight - 115 - 80), fill='tomato2')
        self.image = tk.PhotoImage(file='../images/ninja/one.png')
        self.stack_left()
        self.stack_right()
        self.roof = self.winHeight - 150 - 40
        # Stack the ladder
        for x in range(4):
            self.canvas.create_image(500 - self.xrameWidth + 10, self.roof, image=self.ladderImage, anchor=tk.SE)
            self.roof -= 140
        self.roof = self.winHeight - 150 - 40
        for x in range(4):
            self.canvas.create_image(500 + self.xrameWidth * 2 - 20, self.roof, image=self.ladderImage, anchor=tk.SW)
            self.roof -= 140
        self.ninja = self.canvas.create_image(58, self.winHeight - 115 - 80, image=self.ninjaImage, anchor=tk.SE)
        self.scoreBoard = self.canvas.create_text(self.rightstackx, self.rightstacky-100, text='SCORE:000',
                                                  anchor=tk.SW, font=('TlwgTypist', 25, 'bold'),fill="snow")
        # self.canvas.create_image(58, 110, image = self.ninjaImage, anchor = SE)
        self.bind('<Left>', self.ninjaMoveLeft)
        self.bind('<Right>', self.ninjaMoveRight)
        self.verticalBindings()

    # self.widget = Xrame(self, image, 'freuhhiu Hai Hello')
    # self.wid = self.canvas.create_window(335,  115,  window =self.widget)
    # print(self.canvas.coords(self.wid))

    def verticalBindings(self):
        self.bind('<Up>', self.ninjaMoveUp)
        self.bind('<Down>', self.ninjaMoveDown)

    def stackBlocks(self):
        self.loadedImages = []
        for j in self.images:
            try:
                img = ImageTk.PhotoImage((Image.open(j)).resize((100, 100)))
                self.loadedImages.append(img)
            except:
                print("Image not valid")



        # photoimages for all the input images
        self.xrameData = []  # will store all the xrame objects
        null = tk.PhotoImage(file='../images/ninja/null.png')
        for x in range(len(self.loadedImages)):
            xrameInstance = Xrame(self, self.loadedImages[x], self.texts[x], x)
            self.xrameData.append(xrameInstance)
        # less than 8 scnarieo
        while (len(self.xrameData) < 8):
            self.xrameData.append(Xrame(self, null, 'No Text', len(self.xrameData)))
        # print(self.xrameData)
        random.shuffle(self.xrameData)

    def stack_left(self):
        self.leftCanvasBlocks = []  #
        null = tk.PhotoImage(file='../images/ninja/null.png')  # default image
        self.stackBlocks()  #
        # self.canvas.create_window(165, self.leftstacky, window = Xrame(self, null, 'NULL', len(self.xrameData)))
        for x in range(4):
            wid = self.canvas.create_window(self.leftstackx, self.leftstacky, window=self.xrameData[x], anchor=tk.SE)
            self.leftCanvasBlocks.append(wid)
            self.leftBlocksCoords.append(
                {'x1': self.leftstackx - self.xrameWidth, 'y1': self.leftstacky - self.xrameHeight,
                 'x2': self.leftstackx, 'y2': self.leftstacky})
            self.leftstacky -= 115

    def stack_right(self):
        self.rightCanvasBlocks = []
        for x in range(4):
            wid = self.canvas.create_window(self.rightstackx, self.rightstacky, window=self.xrameData[x + 4],
                                            anchor=tk.SW)
            self.rightCanvasBlocks.append(wid)
            self.rightBlocksCoords.append({'x1': self.rightstackx, 'y1': self.rightstacky - self.xrameHeight,
                                           'x2': self.rightstackx + self.xrameWidth, 'y2': self.rightstacky})
            self.rightstacky -= 115

    def ninjaMoveRight(self, *args):
        ninjaX2, ninjaY2 = self.canvas.coords(self.ninja)
        ninjaX1, ninjaY1 = ninjaX2 - 58, ninjaY2 - 110
        # if self.ninjaStatus != 'walking':
        self.canvas.itemconfigure(self.ninja, {'image': self.ninjaImage})
        self.ninjaStatus = 'walking'
        if ninjaX1 >= self.winWidth:
            # Teleporting from most right x coordinate
            self.canvas.move(self.ninja, -self.winWidth, 0)
            if self.xrameData[self.activeRightBlock].txt['bg'] == 'sea green':
                self.xrameData[self.activeRightBlock - 4].txt['bg'] = 'sea green'
                self.xrameData[self.activeRightBlock - 4].txt['foreground'] = "snow"
            for x in self.xrameData[4:]:
                x.txt['bg'] = 'white'
                x.txt['foreground'] = 'royalblue'

            return None
        for x in range(4):
            # print(self.leftBlocksCoords[x])
            # print(ninjaX1, ninjaY1, ninjaX2, ninjaY2)
            if 500 <= ninjaX2 <= 500 + self.xrameWidth:
                return None
            if ninjaY1 >= self.leftBlocksCoords[x]['y1'] and ninjaY2 <= self.leftBlocksCoords[x]['y2']:
                #  print('Entered')
                if ninjaX2 >= self.leftBlocksCoords[x]['x1'] and ninjaX2 < self.leftBlocksCoords[x]['x2']:
                    #  print('2')
                    self.moveLeftBlockRight(self.leftCanvasBlocks[x], x)
            elif self.leftBlocksCoords[x]['y1'] < ninjaY1 < self.leftBlocksCoords[x]['y2'] or \
                    self.leftBlocksCoords[x]['y1'] < ninjaY2 < self.leftBlocksCoords[x]['y2']:
                if ninjaX2 >= self.leftBlocksCoords[x]['x1'] and ninjaX2 < self.leftBlocksCoords[x]['x2']:
                    return None
        self.canvas.move(self.ninja, 5, 0)

    def moveLeftBlockRight(self, num, x):
        self.canvas.move(num, 5, 0)
        self.leftBlocksCoords[x]['x1'] += 5
        self.leftBlocksCoords[x]['x2'] += 5
        if self.leftBlocksCoords[x]['x1'] >= 500:
            self.leftBlockGoDown(num, x)

    def leftBlockGoDown(self, canvasId, listId):
        y2 = self.leftBlocksCoords[listId]['y2']
        if y2 < self.winHeight - 80:
            #    print('Entered')
            self.canvas.move(canvasId, 0, 5)
            self.leftBlocksCoords[listId]['y2'] += 5
            self.after(50, lambda: self.leftBlockGoDown(canvasId, listId))
        else:
            #  print('This also')
            # order checker
            if self.xrameData[listId].identity == self.mainCount:
                self.mainCount += 1
                self.score += 100
                self.canvas.itemconfigure(self.grid1, {'fill': 'sea green'})
                self.canvas.itemconfigure(self.grid2, {'fill': 'sea green'})
            else:
                self.score -= 100
                self.mainCount += 1
                self.canvas.itemconfigure(self.grid1, {'fill': 'tomato2'})
                self.canvas.itemconfigure(self.grid2, {'fill': 'tomato2'})
            self.canvas.delete(canvasId)
            self.canvas.itemconfigure(self.scoreBoard, {'text': f'SCORE:{self.score}'})

    def ninjaMoveLeft(self, *args):
        ninjaX2, ninjaY2 = self.canvas.coords(self.ninja)
        ninjaX1, ninjaY1 = ninjaX2 - 58, ninjaY2 - 110
        # if self.ninjaStatus != 'walking':
        self.canvas.itemconfigure(self.ninja, {'image': self.ninjaImage2})
        self.ninjaStatus = 'walking'
        if ninjaX2 <= 0:
            self.canvas.move(self.ninja, self.winWidth, 0)
            if self.xrameData[self.activeLeftBlock].txt['bg'] == 'sea green':
                self.xrameData[self.activeLeftBlock + 4].txt['bg'] = 'sea green'
                self.xrameData[self.activeLeftBlock + 4].txt['foreground'] = "snow"
            for x in self.xrameData[:4]:
                x.txt['bg'] = 'white'
                x.txt['foreground'] = 'royalblue'
            return None
        for x in range(4):
            # print(self.rightBlocksCoords[x])
            #    print(ninjaX1, ninjaY1, ninjaX2, ninjaY2)
            if ninjaX1 <= self.xrameWidth + 500 and ninjaX1 > 500:
                return None
            if ninjaY1 >= self.rightBlocksCoords[x]['y1'] and ninjaY2 <= self.rightBlocksCoords[x]['y2']:
                # print('Entered')
                if ninjaX1 <= self.rightBlocksCoords[x]['x2'] and ninjaX1 > self.rightBlocksCoords[x]['x1']:
                    #  print('2')
                    self.moveRightBlockLeft(self.rightCanvasBlocks[x], x)
            elif self.rightBlocksCoords[x]['y1'] < ninjaY1 < self.rightBlocksCoords[x]['y2'] or \
                    self.rightBlocksCoords[x]['y1'] < ninjaY2 < self.rightBlocksCoords[x]['y2']:
                if ninjaX1 <= self.rightBlocksCoords[x]['x2'] and ninjaX1 > self.rightBlocksCoords[x]['x1']:
                    print('Stopped')
                    return None
        self.canvas.move(self.ninja, -5, 0)

    def moveRightBlockLeft(self, num, x):
        self.canvas.move(num, -5, 0)
        self.rightBlocksCoords[x]['x1'] -= 5
        self.rightBlocksCoords[x]['x2'] -= 5
        if self.rightBlocksCoords[x]['x2'] <= self.xrameWidth + 500:
            self.rightBlockGoDown(num, x)

    def rightBlockGoDown(self, canvasId, listId):
        y2 = self.rightBlocksCoords[listId]['y2']
        if y2 < self.winHeight - 80:
            # print('Entered')
            self.canvas.move(canvasId, 0, 5)
            self.rightBlocksCoords[listId]['y2'] += 5
            self.after(50, lambda: self.rightBlockGoDown(canvasId, listId))
        else:
            #  print('This also')
            if self.xrameData[listId + 4].identity == self.mainCount:
                self.canvas.itemconfigure(self.grid1, {'fill': 'sea green'})
                self.canvas.itemconfigure(self.grid2, {'fill': 'sea green'})
                self.mainCount += 1
                self.score += 100
            else:
                self.canvas.itemconfigure(self.grid1, {'fill': 'tomato2'})
                self.canvas.itemconfigure(self.grid2, {'fill': 'tomato2'})
                self.score -= 100
                self.mainCount += 1
            self.canvas.delete(canvasId)
            self.canvas.itemconfigure(self.scoreBoard, {'text': f'SCORE:{self.score}'})

    def ninjaMoveUp(self, *args):
        ninjaX2, ninjaY2 = self.canvas.coords(self.ninja)
        ninjaX1, ninjaY1 = ninjaX2 - 58, ninjaY2 - 110
        ladderX1, ladderX2 = 500 - self.xrameWidth + 10 - 100, 500 - self.xrameWidth + 10
        ladder2X1, ladder2X2 = 500 + self.xrameWidth * 2 - 20, 500 + self.xrameWidth * 2 - 20 + 100
        if ninjaY1 <= self.roof:
            return None
        if (ninjaX1 > ladderX1 and ninjaX2 < ladderX2) or (ninjaX1 > ladder2X1 and ninjaX2 < ladder2X2):
            if self.ninjaStatus == 'walking':
                self.canvas.itemconfigure(self.ninja, {'image': self.climbImage})
                self.ninjaStatus = 'climb1'
                self.ninjaTime = 0
            elif self.ninjaStatus == 'climb1' and self.ninjaTime == 5:
                # selfninjatime = FPS
                self.canvas.itemconfigure(self.ninja, {'image': self.climbImage2})
                self.ninjaStatus = 'climb2'
                self.ninjaTime = 0
            elif self.ninjaStatus == 'climb2' and self.ninjaTime == 5:
                self.canvas.itemconfigure(self.ninja, {'image': self.climbImage})
                self.ninjaStatus = 'climb1'
                self.ninjaTime = 0
            self.canvas.move(self.ninja, 0, -5)
            ninjaY1 -= 5
            ninjaY2 -= 5
            # Active Green color for left blocks
            for x in range(4):
                if ninjaY1 >= self.leftBlocksCoords[x]['y1'] and ninjaY2 <= self.leftBlocksCoords[x][
                    'y2'] and ninjaX1 < 500:
                    self.xrameData[self.activeLeftBlock].txt['bg'] = 'white'
                    self.xrameData[x].txt['bg'] = 'sea green'
                    self.xrameData[x].txt['foreground'] = "snow"
                    self.activeLeftBlock = x
                    break
                else:
                    self.xrameData[self.activeLeftBlock].txt['bg'] = 'white'
                    self.xrameData[self.activeLeftBlock].txt['foreground'] = 'royalblue'
            for x in range(4):
                if ninjaY1 >= self.rightBlocksCoords[x]['y1'] and ninjaY2 <= self.rightBlocksCoords[x][
                    'y2'] and ninjaX1 > 500:
                    self.xrameData[self.activeRightBlock].txt['bg'] = 'white'
                    self.xrameData[x + 4].txt['bg'] = 'sea green'
                    self.xrameData[x + 4].txt['foreground'] = "snow"
                    self.activeRightBlock = x + 4
                    break
                else:
                    self.xrameData[self.activeRightBlock].txt['bg'] = 'white'
                    self.xrameData[self.activeRightBlock].txt['foreground'] = 'royalblue'
            self.ninjaTime += 1

    def ninjaMoveDown(self, *args):
        ninjaX2, ninjaY2 = self.canvas.coords(self.ninja)
        ninjaX1, ninjaY1 = ninjaX2 - 58, ninjaY2 - 110
        ladderX1, ladderX2 = 500 - self.xrameWidth + 10 - 100, 500 - self.xrameWidth + 10
        ladder2X1, ladder2X2 = 500 + self.xrameWidth * 2 - 20, 500 + self.xrameWidth * 2 - 20 + 100
        if ninjaY2 >= self.winHeight - 115 - 80:
            #   print(ninjaY2, self.winHeight - 115 - 80)
            # print('ergrthrhbt')
            return None
        if (ninjaX1 > ladderX1 and ninjaX2 < ladderX2) or (ninjaX1 > ladder2X1 and ninjaX2 < ladder2X2):
            if self.ninjaStatus == 'walking':
                self.canvas.itemconfigure(self.ninja, {'image': self.climbImage})
                self.ninjaStatus = 'climb1'
                self.ninjaTime = 0
            elif self.ninjaStatus == 'climb1' and self.ninjaTime == 5:
                self.canvas.itemconfigure(self.ninja, {'image': self.climbImage2})
                self.ninjaStatus = 'climb2'
                self.ninjaTime = 0
            elif self.ninjaStatus == 'climb2' and self.ninjaTime == 5:
                self.canvas.itemconfigure(self.ninja, {'image': self.climbImage})
                self.ninjaStatus = 'climb1'
                self.ninjaTime = 0
            self.canvas.move(self.ninja, 0, 5)
            ninjaY1 += 5
            ninjaY2 += 5
            for x in range(4):
                if ninjaY1 >= self.leftBlocksCoords[x]['y1'] and ninjaY2 <= self.leftBlocksCoords[x][
                    'y2'] and ninjaX1 < 500:
                    self.xrameData[self.activeLeftBlock].txt['bg'] = 'white'
                    self.xrameData[x].txt['bg'] = 'sea green'
                    self.xrameData[x].txt['foreground'] = "snow"
                    self.activeLeftBlock = x
                    break
                else:
                    self.xrameData[self.activeLeftBlock].txt['bg'] = 'white'
                    self.xrameData[self.activeLeftBlock].txt['foreground'] = 'royalblue'

            for x in range(4):
                if ninjaY1 >= self.rightBlocksCoords[x]['y1'] and ninjaY2 <= self.rightBlocksCoords[x][
                    'y2'] and ninjaX1 > 500:
                    self.xrameData[self.activeRightBlock].txt['bg'] = 'white'
                    self.xrameData[x + 4].txt['bg'] = 'sea green'
                    self.xrameData[x + 4].txt['foreground'] = "snow"
                    self.activeRightBlock = x + 4
                    break
                else:
                    self.xrameData[self.activeRightBlock].txt['bg'] = 'white'
                    self.xrameData[self.activeRightBlock].txt['foreground'] = 'royalblue'
            self.ninjaTime += 1

    '''


        def stack_left(self):
            self.widget = Xrame(self, self.image, 'freuhhiu Hai Hello', 0)
            self.wid = self.canvas.create_window(self.leftstackx, self.leftstacky, window=self.widget, anchor=NW)
            for x in range(4):
                self.widget = Xrame(self, self.image, 'freuhhiu Hai Hello', 0)
                self.wid = self.canvas.create_window(self.leftstackx,  self.leftstacky,  window =self.widget, anchor = SE)
                self.leftstacky -= 115
        def stack_right(self):
            for x in range(4):
                self.widget = Xrame(self, self.image, 'freuhhiu Hai Hello')
                self.wid = self.canvas.create_window(self.rightstackx,  self.rightstacky,  window =self.widget, anchor = SW)
                self.rightstacky -= 115'''

class Xrame(tk.Frame):
    '''Classs  of the block.thIS CLASS contains the main object.'''

    def __init__(self, root, image, text, identity=0):
        self.image = image  # Photoimage of the respecive image
        self.text = text  # inpu text
        self.identity = identity  # the order of the block(0 - 8)
        super().__init__(root,
                         height=1000,
                         width=5000)
        self.gui()
        self['bd'] = 5
        self['bg'] = 'deepskyblue4'
        self['relief'] = tk.RIDGE


    def gui(self):
        # Create the button(image)
        self.img = tk.Button(self,
                          image=self.image,bg="deepskyblue4")
        self.img.pack(side=tk.LEFT)
        self.img['image'] = self.image
        # Scrolled text
        self.txt = sText.ScrolledText(self,
                                      height=6,
                                      width=25,wrap=tk.WORD,foreground="royalblue",font=('helvetica', 11, 'bold'))
        self.txt.vbar.configure(background="deepskyblue4")

        self.txt.insert('insert', self.text)
        self.txt.pack(side=tk.RIGHT)