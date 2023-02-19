import turtle
from tkinter import *
from PIL import ImageTk,Image
from pygments import highlight
from pygments.lexers import PythonLexer, PythonConsoleLexer
from pygments.token import Number
from pygments.formatters import RawTokenFormatter
import math

        
class App(Frame,object):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #self.pack()
        #self.create_widgets()
        
        root.configure(background='black')
        root.title('Partie Programmation - Mission1')
        root.iconbitmap('images/car.ico')
        root.attributes('-fullscreen', True)
        #Zone de texte
        self.label_text = Label (text = "Allons découvrir les programmes",bg="black", fg="white")
        self.label_text.config(font=("Times New Roman", 30))
        self.label_text.grid(row=0,column=0,columnspan=4)
        self.zone_de_saisie=Text  (padx=10,pady=5)
        
        self.zone_de_saisie.config (width = 50, height = 10,font= ('Courier 15 bold'))

        self.zone_de_saisie.grid(row=1,column=0,columnspan=4,padx=10)
        self.zone_de_saisie.bind("<KeyRelease-Return>", self.insert_tab)
        self.label_compil = Label (text = "",bg="black", fg="white")
        self.label_compil.config(font=("Times New Roman", 14))
        self.label_compil.grid(row=2,column=0,columnspan=4)
        # Créer un objet photoimage pour utiliser l'image
        self.photo = PhotoImage(file = "images/btnExec.png")
        self.photo1 = PhotoImage(file = "images/btnCancel.png")
        self.photoreset = PhotoImage(file = "images/btnReset.png")
    
        self.Bouton_Executer=Button(root, image=self.photo,relief="flat",activebackground="black", activeforeground="black",bg="black",bd=0,command =lambda: self.executionCode(0))
        self.Bouton_Reset=Button(root, image=self.photoreset,relief="flat",activebackground="black", activeforeground="black",bg="black",bd=0,command =lambda: self.reset())
        self.Bouton_Cancel=Button(root, image=self.photo1,relief="flat",activebackground="black", activeforeground="black",bg="black",bd=0,command =lambda: self.cancel())
        
        #On ajoute l'affichage du bouton dans la fenêtre tk:
        self.Bouton_Executer.grid(row=3,column=0,columnspan=1)
        self.Bouton_Reset.grid(row=3,column=1,columnspan=1)
        self.Bouton_Cancel.grid(row=3,column=3,columnspan=1)
        ''' canenva pour mission '''
        self.imgmission = ImageTk.PhotoImage(Image.open("images/mission1.png"))
        self.canvasM = Canvas(root, width = 600, height = 325, bd=5, bg="black")
        self.canvasM.grid(row=4,column=0,columnspan=4)       
        self.canvasM.create_image(0, 0, anchor=NW, image=self.imgmission)
        # canvas for image
        # Dans root creaton  d'un objet type Canvas qui se nomme canvas
        self.canvas = Canvas(root, width = 900, height = 900, bd=5, bg="black")
        #Affiche le Canvas
        self.canvas.grid(row=0, rowspan=20,column=4)

        # Créez un canvas Turtle et attachez-le au canvas Tkinter
        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.turtle_screen.bgpic("images/taxi1.png")
        self.turtle_screen.register_shape("images/taxis.gif")
        self.turtle_canvas = turtle.RawTurtle(self.turtle_screen)
        self.turtle_canvas.shape("images/taxis.gif")
        self.turtle_canvas.up()
        self.turtle_canvas.goto(-330,100)
        #self.turtle.shape("taxis")
        self.turtle_canvas.speed(0)
    def colorize_text(self,event=None):
        tags = {
        'keyword': 'purple',
        'builtin': 'dark blue',
        'comment': 'forest green',
        'string': 'red',
        'number': 'blue'
        }
        code = self.zone_de_saisie.get('1.0', 'end-1c')
        for tag in tags:
            self.zone_de_saisie.tag_configure(tag, foreground=tags[tag])
        
        # Get the text from the entry
        text = self.zone_de_saisie.get("insert linestart-1l", "insert linestart-1l lineend")
        
        # Define the regular expressions for each syntax element
        keyword_re = re.compile(r'\b(and|as|assert|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b')
        builtin_re = re.compile(r'\b(abs|all|any|bin|bool|bytearray|bytes|callable|chr|classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|eval|exec|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip)\b')
        comment_re = re.compile(r'#.*')
        string_re = re.compile(r'(["\'])(?:(?=(\\?))\2.)*?\1')
        number_re = re.compile(r'\b(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?\b')
        
        # Colorize the text using the regular expressions
        start = 0
        for match in keyword_re.finditer(text):
            self.zone_de_saisie.tag_add('keyword', f'{match.start()}.0', f'{match.end()}.0')
        
        start = 0
        for match in builtin_re.finditer(text):
            self.zone_de_saisie.tag_add('builtin', f'{match.start()}.0', f'{match.end()}.0')
        
        start = 0
        for match in comment_re.finditer(text):
            self.zone_de_saisie.tag_add('comment', f'{match.start()}.0', f'{match.end()}.0')
        
        start = 0
        for match in string_re.finditer(text):
            self.zone_de_saisie.tag_add('string', f'{match.start()}.0', f'{match.end()}.0')
    def executionCode(self,indexCode):
        instructions=[]
        # retourne le texte entre deux positions
        codes = self.zone_de_saisie.get('1.0', END).splitlines()
        code = self.zone_de_saisie.get('1.0', END)
        try:
            compiled_code = compile(code, "<string>", "exec")
            self.label_compil.configure(text="")
            for line in codes:
                line = line.rstrip()
                if line[0]=='\t':
                    line=line[1:]
                
                instructions.append(line)
            while indexCode < len(instructions):
                    if instructions[indexCode]=='avant()':
                        eval(str(self.avant()))
                        #time.sleep(0.005)
                        indexCode+=1
                    elif instructions[indexCode]=='droite()':
                        eval(str(self.droite()))
                        indexCode+=1
                    elif instructions[indexCode]=='gauche()':
                        eval(str(self.left()))
                        indexCode+=1
                    elif instructions[indexCode].find("for")==0:
                        range1=0
                        range2=0
                        if instructions[indexCode].find(',')==-1:
                            range1=instructions[indexCode][instructions[indexCode].find('range')+6:instructions[indexCode].find(')')]
                        else:
                            range1=instructions[indexCode][instructions[indexCode].find('range')+6:instructions[indexCode].find(',')]
                            range2=instructions[indexCode][instructions[indexCode].find(',')+1:instructions[indexCode].find(')')]
                        if range2==0:
                            for i in range(int(range1)):
                                if instructions[indexCode+1]=='avant()':
                                    eval(str(self.avant()))
                                    #time.sleep(0.5)
                                elif instructions[indexCode+1]=='gauche()':
                                    eval(str(self.gauche()))
                                elif instructions[indexCode+1]=='droite()':
                                    eval(str(self.droite()))
                        else:
                            for i in range(int(range1),int(range2)):
                                if instructions[indexCode+1]=='avant()':
                                    eval(str(self.avancer()))
                                elif instructions[indexCode+1]=='gauche()':
                                    eval(str(self.gauche()))
                                elif instructions[indexCode+1]=='droite()':
                                    eval(str(self.droite()))
                        indexCode+=2
        except SyntaxError as e:
            self.label_compil.configure(text="Erreur de syntaxe : {}".format(e), fg="red")
            
    
    def avant(self):
        self.turtle_canvas.forward(38)
        
    def gauche(self):
    
        self.turtle_canvas.tilt(90)
        self.turtle_canvas.left(90)
        if self.turtle_canvas.tiltangle()==90:
            self.turtle_screen.register_shape("images/taxis_up.gif")  #Enregistre d'après une image
            self.turtle_canvas.shape("images/taxis_up.gif")
        elif self.turtle_canvas.tiltangle()==180:
            self.turtle_screen.register_shape("images/taxis_left.gif")  #Enregistre d'après une image
            self.turtle_canvas.shape("images/taxis_left.gif")
        elif self.turtle_canvas.tiltangle()==270:
            self.turtle_screen.register_shape("images/taxis_down.gif")  #Enregistre d'après une image
            self.turtle_canvas.shape("images/taxis_down.gif")
        else:
            self.turtle_screen.register_shape("images/taxis.gif")  #Enregistre d'après une image
            self.turtle_canvas.shape("images/taxis.gif")
        
    def droite(self):
        self.turtle_canvas.tilt(90)
        self.turtle_canvas.right(90)
        if self.turtle_canvas.tiltangle()==90:
            self.turtle_screen.register_shape("images/taxis_down.gif")  #Enregistre d'après une image
            self.turtle_canvas.shape("images/taxis_down.gif")
        elif self.turtle_canvas.tiltangle()==180:
            self.turtle_screen.register_shape("images/taxis_left.gif")  #Enregistre d'après une image
            self.turtle_canvas.shape("images/taxis_left.gif")
        elif self.turtle_canvas.tiltangle()==270:
            self.turtle_screen.register_shape("images/taxis_up.gif")  #Enregistre d'après une image
            self.turtle_canvas.shape("images/taxis_up.gif")
        else:
            self.turtle_screen.register_shape("images/taxis.gif")  #Enregistre d'après une image
            self.turtle_canvas.shape("images/taxis.gif")
    def insert_tab(self,event):
        
        # Récupérer la position de début et de fin de la ligne précédente
        current_line = self.zone_de_saisie.get("insert linestart-1l", "insert linestart-1l lineend")
        
        self.colorize_text(current_line)
        last_char=current_line[-1]
        # Compter le nombre de tabulations dans la ligne précédente
        num_tabs = current_line.count("\t")
        if last_char==":":
            self.zone_de_saisie.insert(float(math.floor(float(self.zone_de_saisie.index(INSERT)))+1.3),"\t"*(num_tabs+1))
        else:
            self.zone_de_saisie.insert(float(math.floor(float(self.zone_de_saisie.index(INSERT)))+1.3),"\t"*(num_tabs))
    def cancel(self):
        root.destroy()
    def reset(self):
        self.zone_de_saisie.delete("1.0","end")
        self.label_compil = Label (text = "",bg="black", fg="white")
        self.canvas = Canvas(root, width = 900, height = 900, bd=5, bg="black")
        #Affiche le Canvas
        self.canvas.grid(row=0, rowspan=20,column=4)

        # Créez un canvas Turtle et attachez-le au canvas Tkinter
        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.turtle_screen.bgpic("images/taxi1.png")
        self.turtle_screen.register_shape("images/taxis.gif")
        self.turtle_canvas = turtle.RawTurtle(self.turtle_screen)
        self.turtle_canvas.shape("images/taxis.gif")
        self.turtle_canvas.up()
        self.turtle_canvas.goto(-330,100)
        #self.turtle.shape("taxis")
        self.turtle_canvas.speed(0)
root = Tk()
app = App(root)
app.mainloop()