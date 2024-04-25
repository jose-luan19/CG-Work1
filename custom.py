import tkinter
import tkinter.messagebox
import customtkinter
from matplotlib import pyplot as plt
import numpy as np
import curves.curves as curves
import polygons.polygons as polygons
import line.line as line
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageDraw

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.num_retas = 0
        self.entries = []
        self.entriesCurva = []
        self.mostrar_segunda_tabview = False

        # configure window
        self.title("Rasterização")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.canvas_widget = None

        # create sidebar frame with widgets
        
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.radio_var = tkinter.IntVar(value=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Rasterização:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
 
        
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))


        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=100)
        self.tabview.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        self.tabview.add("Linha")
        self.tabview.add("Curva")
        self.tabview.add("Poligono")
        self.tabview.tab("Linha").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Curva").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Poligono").grid_columnconfigure(0, weight=1)
        
        
        self.text_mode_labelRetas = customtkinter.CTkLabel(self.tabview.tab("Linha"), text="Número de Retas")
        self.text_mode_labelRetas.grid(row=0, column=0, pady=(0, 0))
        self.entryNumRetas = customtkinter.CTkEntry(self.tabview.tab("Linha"), placeholder_text="Nº", width=100, height=30)
        self.entryNumRetas.grid(row=1, column=0, pady=(10), padx=(10))
        self.mainReta_button_1 = customtkinter.CTkButton( master=self.tabview.tab("Linha"), text="Ok", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.create_entry_widgets_Retas())
        self.mainReta_button_1.grid(row=2, column=0, pady=(20, 20))
        
        self.text_mode_labelCurvas = customtkinter.CTkLabel(self.tabview.tab("Curva"), text="Número de Curvas")
        self.text_mode_labelCurvas.grid(row=0, column=0, pady=(0, 0))
        self.entryNumCurvas = customtkinter.CTkEntry(self.tabview.tab("Curva"), placeholder_text="Nº", width=100, height=30)
        self.entryNumCurvas.grid(row=1, column=0, pady=(10), padx=(10))
        self.mainCurva_button_1 = customtkinter.CTkButton( master=self.tabview.tab("Curva"), text="Ok", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.create_entry_widgets_Curva())
        self.mainCurva_button_1.grid(row=2, column=0, pady=(20, 20))
        
        self.mainPoligono_button_add = customtkinter.CTkButton( master=self.tabview.tab("Poligono"), text="+ Add Poligonos", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.criar_segunda_tabview())
        self.mainPoligono_button_add.grid(row=0, column=0, padx=(20, 20), pady=(10, 10))
        self.mainPoligono_button_3 = customtkinter.CTkButton( master=self.tabview.tab("Poligono"), text="Rasterizar", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.valuesPoligono(self.entryTrianguloX1.get(), self.entryTrianguloX2.get(), self.entryTrianguloX3.get(), self.entryTrianguloY1.get(), self.entryTrianguloY2.get(), self.entryTrianguloY3.get(), self.entryTriangulo2X1.get(), self.entryTriangulo2X2.get(), self.entryTriangulo2X3.get(), self.entryTriangulo2Y1.get(), self.entryTriangulo2Y2.get(), self.entryTriangulo2Y3.get(), self.entryQuadradoX1.get(), self.entryQuadradoX2.get(), self.entryQuadradoX3.get(), self.entryQuadradoX4.get(),  self.entryQuadradoY1.get(), self.entryQuadradoY2.get(), self.entryQuadradoY3.get(), self.entryQuadradoY4.get(), self.entryQuadrado2X1.get(), self.entryQuadrado2X2.get(), self.entryQuadrado2X3.get(), self.entryQuadrado2X4.get(),  self.entryQuadrado2Y1.get(), self.entryQuadrado2Y2.get(), self.entryQuadrado2Y3.get(), self.entryQuadrado2Y4.get(), self.entryHexX1.get(), self.entryHexX2.get(), self.entryHexX3.get(), self.entryHexX4.get(), self.entryHexX5.get(), self.entryHexX6.get(), self.entryHexY1.get(), self.entryHexY2.get(), self.entryHexY3.get(), self.entryHexY4.get(), self.entryHexY5.get(), self.entryHexY6.get(), self.entryHex2X1.get(), self.entryHex2X2.get(), self.entryHex2X3.get(), self.entryHex2X4.get(), self.entryHex2X5.get(), self.entryHex2X6.get(), self.entryHex2Y1.get(), self.entryHex2Y2.get(), self.entryHex2Y3.get(), self.entryHex2Y4.get(), self.entryHex2Y5.get(), self.entryHex2Y6.get()))
        self.mainPoligono_button_3.grid(row=2, column=0, padx=(20, 20), pady=(10))
     
        
        
        # create tabview

            
        

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=300, height=270)
        self.textbox.grid(row=0, column=2, padx=(2, 2), pady=(2, 2))
        
        self.textbox = customtkinter.CTkTextbox(self, width=300, height=270)
        self.textbox.grid(row=1, column=2, padx=(2, 2), pady=(2, 2))
        
        self.textbox = customtkinter.CTkTextbox(self,width=300, height=270)
        self.textbox.grid(row=0, column=3, padx=(2, 2), pady=(2, 2))
        
        self.textbox = customtkinter.CTkTextbox(self, width=300, height=270)
        self.textbox.grid(row=1, column=3, padx=(2, 2), pady=(2, 2))


        # set default values
        self.appearance_mode_optionemenu.set("Dark")
    
    def create_entry_widgets_Retas(self):
        
        self.text_mode_labelRetas.grid_forget()
        self.entryNumRetas.grid_forget()
        self.mainReta_button_1.grid_forget()
        
        self.num_retas = int(self.entryNumRetas.get())
        for i in range (self.num_retas):
            entry_x1 = customtkinter.CTkEntry(self.tabview.tab("Linha"), placeholder_text="X1", width=50)
            entry_y1 = customtkinter.CTkEntry(self.tabview.tab("Linha"), placeholder_text="Y1", width=50)
            entry_x2 = customtkinter.CTkEntry(self.tabview.tab("Linha"), placeholder_text="X2", width=50)
            entry_y2 = customtkinter.CTkEntry(self.tabview.tab("Linha"), placeholder_text="Y2", width=50)
            entry_x1.grid(row=i + 1, column=0, pady=(2))
            entry_y1.grid(row=i + 1, column=1, pady=(2))
            entry_x2.grid(row=i + 1, column=2, pady=(2))
            entry_y2.grid(row=i + 1, column=3, pady=(2))
            self.entries.append((entry_x1, entry_x2, entry_y1, entry_y2))
         # Botão de voltar
        self.back_button = customtkinter.CTkButton(self.tabview.tab("Linha"), text="Voltar", width=80, command=self.show_entry_widgets)
        self.back_button.grid(row=self.num_retas + 1, column=4)
        self.buttonPlotLine = customtkinter.CTkButton( master=self.tabview.tab("Linha"), text="Rasterizar", width=80, command=lambda: self.plot_lines())
        self.buttonPlotLine.grid(row=self.num_retas + 2, column=4)
        
    def create_entry_widgets_Curva(self):
        
        self.text_mode_labelCurvas.grid_forget()
        self.entryNumCurvas.grid_forget()
        self.mainCurva_button_1.grid_forget()
        
        self.num_curvas = int(self.entryNumCurvas.get())
        for i in range (self.num_curvas):
            entry_p0 = customtkinter.CTkEntry(self.tabview.tab("Curva"), placeholder_text="p0x, p0y", width=50)
            entry_p1 = customtkinter.CTkEntry(self.tabview.tab("Curva"), placeholder_text="p1x, p1y", width=50)
            entry_m0 = customtkinter.CTkEntry(self.tabview.tab("Curva"), placeholder_text="m0x, m0y", width=50)
            entry_m1 = customtkinter.CTkEntry(self.tabview.tab("Curva"), placeholder_text="m1x, m1y", width=50)
            entry_T = customtkinter.CTkEntry(self.tabview.tab("Curva"), placeholder_text="T", width=50)
            entry_p0.grid(row=i + 1, column=0, pady=(2))
            entry_p1.grid(row=i + 1, column=1, pady=(2))
            entry_m0.grid(row=i + 1, column=2, pady=(2))
            entry_m1.grid(row=i + 1, column=3, pady=(2))
            entry_T.grid(row=i + 1, column=4, pady=(2))
            self.entriesCurva.append((entry_p0, entry_p1, entry_m0, entry_m1, entry_T))
         # Botão de voltar
        self.back_buttonCurva = customtkinter.CTkButton(self.tabview.tab("Curva"), text="Voltar", width=80, command=self.show_entry_widgetsCurvas)
        self.back_buttonCurva.grid(row=self.num_curvas + 1, column=4)
        self.buttonPlotCurva = customtkinter.CTkButton( master=self.tabview.tab("Curva"), text="Rasterizar", width=80, command=lambda: self.plot_curvas())
        self.buttonPlotCurva.grid(row=self.num_curvas + 2, column=4)
    
    def show_entry_widgets(self):
        if hasattr(self, 'back_button') and self.back_button:
            self.back_button.grid_forget()
    
        if hasattr(self, 'buttonPlotLine') and self.buttonPlotLine:
            self.buttonPlotLine.grid_forget()
              
        self.text_mode_labelRetas.grid(row=0, column=0, pady=(0, 0))
        self.entryNumRetas.grid(row=1, column=0, pady=(10), padx=(10))
        self.mainReta_button_1.grid(row=2, column=0, pady=(20, 20))
        # Limpar entradas antigas
        for entry_set in self.entries:
            for entry in entry_set:
                entry.delete(0, 'end')  # Limpa as entradas de retas
                entry.grid_forget()
        self.entries = []
    
    def show_entry_widgetsCurvas(self):
        if hasattr(self, 'back_buttonCurva') and self.back_buttonCurva:
            self.back_buttonCurva.grid_forget()
    
        if hasattr(self, 'buttonPlotCurva') and self.buttonPlotCurva:
            self.buttonPlotCurva.grid_forget()
              
        self.text_mode_labelCurvas.grid(row=0, column=0, pady=(0, 0))
        self.entryNumCurvas.grid(row=1, column=0, pady=(10), padx=(10))
        self.mainCurva_button_1.grid(row=2, column=0, pady=(20, 20))
        # Limpar entradas antigas
        for entry_set in self.entriesCurva:
            for entry in entry_set:
                entry.delete(0, 'end')  # Limpa as entradas de retas
                entry.grid_forget()
        self.entriesCurva = []

        
    def plot_lines(self):
        coordenadas_retas = []

        for i in range(self.num_retas):
            x1 = float(self.entries[i][0].get())
            x2 = float(self.entries[i][1].get())
            y1 = float(self.entries[i][2].get())
            y2 = float(self.entries[i][3].get())
            coordenadas_retas.append((x1, y1, x2, y2))
            
            # Chame a função valuesLinha com as coordenadas retas como argumento
            self.valuesLinha(coordenadas_retas)
            
    def plot_curvas(self):
        p0_list = []
        p1_list = []
        m0_list = []
        m1_list = []
        T_list = []

        for i in range(self.num_curvas):
            p0 = [float(x) for x in self.entriesCurva[i][0].get().split(',')]
            p1 = [float(x) for x in self.entriesCurva[i][1].get().split(',')]
            m0 = [float(x) for x in self.entriesCurva[i][2].get().split(',')]
            m1 = [float(x) for x in self.entriesCurva[i][3].get().split(',')]
            T = [int(x) for x in self.entriesCurva[i][4].get().split(',')]

            p0x, p0y = p0[0], p0[1]
            p1x, p1y = p1[0], p1[1]
            m0x, m0y = m0[0], m0[1]
            m1x, m1y = m1[0], m1[1]
            T_value = T[0]

            p0_list.append(np.array([p0x, p0y, 0]))
            p1_list.append(np.array([p1x, p1y, 0]))
            m0_list.append(np.array([m0x, m0y, 0]))
            m1_list.append(np.array([m1x, m1y, 0]))
            T_list.append(T_value)

        p0_list, p1_list, m0_list, m1_list, T_list = zip(*zip(p0_list, p1_list, m0_list, m1_list, T_list))
        variaveis_curva = list(zip(p0_list, p1_list, m0_list, m1_list, T_list))

        self.valuesCurva(variaveis_curva)
    
    def criar_segunda_tabview (self):
            self.clear_graph()
            self.show_entry_widgets()
            self.tabview = customtkinter.CTkTabview(self, width=120)
            self.tabview.grid(row=1, column=1, padx=(10, 0), pady=(0, 0))
            self.tabview.add("Triângulo")
            self.tabview.add("Quadrado")
            self.tabview.add("Hexágono")
            self.tabview.tab("Triângulo").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
            self.tabview.tab("Quadrado").grid_columnconfigure(0, weight=1)
            self.tabview.tab("Hexágono").grid_columnconfigure(0, weight=1)
            
            self.appearance_mode_label = customtkinter.CTkLabel(self.tabview.tab("Triângulo"), text="Tri1:", anchor="w")
            self.appearance_mode_label.grid(row=0, column=0, padx=10, pady=(10, 0))
            self.entryTrianguloX1 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X1, Y1", width=60, height=30)
            self.entryTrianguloX1.grid(row=1, column=1, pady=(10), padx=(0))
            self.entryTrianguloX2 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X3,Y3", width=60, height=30)
            self.entryTrianguloX2.grid(row=1, column=2, pady=(10), padx=(0))
            self.entryTrianguloX3 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X5,Y5", width=60, height=30)
            self.entryTrianguloX3.grid(row=1, column=3, pady=(10), padx=(0))
            self.entryTrianguloY1 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X2, Y2", width=60, height=30)
            self.entryTrianguloY1.grid(row=2, column=1, pady=(10), padx=(0))
            self.entryTrianguloY2 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X4,Y4", width=60, height=30)
            self.entryTrianguloY2.grid(row=2, column=2, pady=(10), padx=(0))
            self.entryTrianguloY3 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X6,Y6", width=60, height=30)
            self.entryTrianguloY3.grid(row=2, column=3, pady=(10), padx=(0))
            
            self.appearance_mode_label = customtkinter.CTkLabel(self.tabview.tab("Triângulo"), text="Tri2:", anchor="w")
            self.appearance_mode_label.grid(row=3, column=0, padx=10, pady=(10, 0))
            self.entryTriangulo2X1 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X1, Y1", width=60, height=30)
            self.entryTriangulo2X1.grid(row=4, column=1, pady=(10), padx=(0))
            self.entryTriangulo2X2 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X3,Y3", width=60, height=30)
            self.entryTriangulo2X2.grid(row=4, column=2, pady=(10), padx=(0))
            self.entryTriangulo2X3 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X5,Y5", width=60, height=30)
            self.entryTriangulo2X3.grid(row=4, column=3, pady=(10), padx=(0))
            self.entryTriangulo2Y1 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X2, Y2", width=60, height=30)
            self.entryTriangulo2Y1.grid(row=5, column=1, pady=(10), padx=(0))
            self.entryTriangulo2Y2 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X4,Y4", width=60, height=30)
            self.entryTriangulo2Y2.grid(row=5, column=2, pady=(10), padx=(0))
            self.entryTriangulo2Y3 = customtkinter.CTkEntry(self.tabview.tab("Triângulo"), placeholder_text="X6,Y6", width=60, height=30)
            self.entryTriangulo2Y3.grid(row=5, column=3, pady=(10), padx=(0))     
            
            self.appearance_mode_label = customtkinter.CTkLabel(self.tabview.tab("Quadrado"), text="Quad1:", anchor="w")
            self.appearance_mode_label.grid(row=0, column=0, padx=0, pady=(10, 0))
            self.entryQuadradoX1 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X1, Y1", width=40, height=30)
            self.entryQuadradoX1.grid(row=1, column=1, pady=(10), padx=(0))
            self.entryQuadradoX2 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X3, Y3", width=40, height=30)
            self.entryQuadradoX2.grid(row=1, column=2, pady=(10), padx=(0))
            self.entryQuadradoX3 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X5, Y5",width=40, height=30)
            self.entryQuadradoX3.grid(row=1, column=3, pady=(10), padx=(0))
            self.entryQuadradoX4 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X7, Y7", width=40, height=30)
            self.entryQuadradoX4.grid(row=1, column=4, pady=(10), padx=(0))
            self.entryQuadradoY1 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X2, Y2", width=40, height=30)
            self.entryQuadradoY1.grid(row=2, column=1, pady=(10), padx=(0))
            self.entryQuadradoY2 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X4, Y4",width=40, height=30)
            self.entryQuadradoY2.grid(row=2, column=2, pady=(10), padx=(0))
            self.entryQuadradoY3 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X6, Y6", width=40, height=30)
            self.entryQuadradoY3.grid(row=2, column=3, pady=(10), padx=(0))
            self.entryQuadradoY4 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X8, Y8", width=40, height=30)
            self.entryQuadradoY4.grid(row=2, column=4, pady=(10), padx=(0))
            
            self.appearance_mode_label = customtkinter.CTkLabel(self.tabview.tab("Quadrado"), text="Quad2:", anchor="w")
            self.appearance_mode_label.grid(row=3, column=0, padx=0, pady=(10, 0))
            self.entryQuadrado2X1 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X1, Y1", width=40, height=30)
            self.entryQuadrado2X1.grid(row=4, column=1, pady=(10), padx=(0))
            self.entryQuadrado2X2 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X3, Y3", width=40, height=30)
            self.entryQuadrado2X2.grid(row=4, column=2, pady=(10), padx=(0))
            self.entryQuadrado2X3 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X5, Y5", width=40, height=30)
            self.entryQuadrado2X3.grid(row=4, column=3, pady=(10), padx=(0))
            self.entryQuadrado2X4 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X7, Y7", width=40, height=30)
            self.entryQuadrado2X4.grid(row=4, column=4, pady=(10), padx=(0))
            self.entryQuadrado2Y1= customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X2, Y2", width=40, height=30)
            self.entryQuadrado2Y1.grid(row=5, column=1, pady=(10), padx=(0))
            self.entryQuadrado2Y2 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X4, Y4", width=40, height=30)
            self.entryQuadrado2Y2.grid(row=5, column=2, pady=(10), padx=(0))
            self.entryQuadrado2Y3 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X6, Y6", width=40, height=30)
            self.entryQuadrado2Y3.grid(row=5, column=3, pady=(10), padx=(0))
            self.entryQuadrado2Y4 = customtkinter.CTkEntry(self.tabview.tab("Quadrado"), placeholder_text="X8, Y8", width=40, height=30)
            self.entryQuadrado2Y4.grid(row=5, column=4, pady=(10), padx=(0))     
            
            self.appearance_mode_label = customtkinter.CTkLabel(self.tabview.tab("Hexágono"), text="Hex1:", anchor="w")
            self.appearance_mode_label.grid(row=0, column=0, padx=10, pady=(10, 0))
            self.entryHexX1 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X1, Y1", width=40, height=30)
            self.entryHexX1 .grid(row=1, column=1, pady=(10), padx=(0))
            self.entryHexX2 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X3, Y3", width=40, height=30)
            self.entryHexX2.grid(row=1, column=2, pady=(10), padx=(0))
            self.entryHexX3= customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X5, Y5",width=40, height=30)
            self.entryHexX3.grid(row=1, column=3, pady=(10), padx=(0))
            self.entryHexX4 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X7, Y7", width=40, height=30)
            self.entryHexX4.grid(row=1, column=4, pady=(10), padx=(0))
            self.entryHexX5 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X9, Y9", width=40, height=30)
            self.entryHexX5.grid(row=1, column=5, pady=(10), padx=(0))
            self.entryHexX6 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X11, Y11", width=40, height=30)
            self.entryHexX6.grid(row=1, column=6, pady=(10), padx=(0))
            self.entryHexY1 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X2, Y2", width=40, height=30)
            self.entryHexY1.grid(row=2, column=1, pady=(10), padx=(0))
            self.entryHexY2 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X4, Y4",width=40, height=30)
            self.entryHexY2.grid(row=2, column=2, pady=(10), padx=(0))
            self.entryHexY3 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X6, Y6", width=40, height=30)
            self.entryHexY3.grid(row=2, column=3, pady=(10), padx=(0))
            self.entryHexY4 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X8, Y8", width=40, height=30)
            self.entryHexY4.grid(row=2, column=4, pady=(10), padx=(0))
            self.entryHexY5 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X10, Y10", width=40, height=30)
            self.entryHexY5.grid(row=2, column=5, pady=(10), padx=(0))
            self.entryHexY6 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X12, Y12", width=40, height=30)
            self.entryHexY6.grid(row=2, column=6, pady=(10), padx=(0))
            
            self.appearance_mode_label = customtkinter.CTkLabel(self.tabview.tab("Hexágono"), text="Hex2:", anchor="w")
            self.appearance_mode_label.grid(row=3, column=0, padx=10, pady=(10, 0))
            self.entryHex2X1 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X1, Y1", width=40, height=30)
            self.entryHex2X1.grid(row=4, column=1, pady=(10), padx=(0))
            self.entryHex2X2 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X3, Y3", width=40, height=30)
            self.entryHex2X2.grid(row=4, column=2, pady=(10), padx=(0))
            self.entryHex2X3 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X5, Y5",width=40, height=30)
            self.entryHex2X3.grid(row=4, column=3, pady=(10), padx=(0))
            self.entryHex2X4 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X7, Y7", width=40, height=30)
            self.entryHex2X4.grid(row=4, column=4, pady=(10), padx=(0))
            self.entryHex2X5 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X9, Y9", width=40, height=30)
            self.entryHex2X5.grid(row=4, column=5, pady=(10), padx=(0))
            self.entryHex2X6 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X11, Y11", width=40, height=30)
            self.entryHex2X6.grid(row=4, column=6, pady=(10), padx=(0))
            self.entryHex2Y1 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X2, Y2", width=40, height=30)
            self.entryHex2Y1.grid(row=5, column=1, pady=(10), padx=(0))
            self.entryHex2Y2 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X4, Y4",width=40, height=30)
            self.entryHex2Y2.grid(row=5, column=2, pady=(10), padx=(0))
            self.entryHex2Y3 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X6, Y6", width=40, height=30)
            self.entryHex2Y3.grid(row=5, column=3, pady=(10), padx=(0))
            self.entryHex2Y4 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X8, Y8", width=40, height=30)
            self.entryHex2Y4.grid(row=5, column=4, pady=(10), padx=(0))
            self.entryHex2Y5 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X10, Y10", width=40, height=30)
            self.entryHex2Y5.grid(row=5, column=5, pady=(10), padx=(0))
            self.entryHex2Y6 = customtkinter.CTkEntry(self.tabview.tab("Hexágono"), placeholder_text="X12, Y12", width=40, height=30)
            self.entryHex2Y6.grid(row=5, column=6, pady=(10), padx=(0))
    
    
    def show_tabviews_originals(self):
        self.tabview.grid_forget()
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=100)
        self.tabview.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        self.tabview.add("Linha")
        self.tabview.add("Curva")
        self.tabview.add("Poligono")
        self.tabview.tab("Linha").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Curva").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Poligono").grid_columnconfigure(0, weight=1)
        
        
        self.text_mode_labelRetas = customtkinter.CTkLabel(self.tabview.tab("Linha"), text="Número de Retas")
        self.text_mode_labelRetas.grid(row=0, column=0, pady=(0, 0))
        self.entryNumRetas = customtkinter.CTkEntry(self.tabview.tab("Linha"), placeholder_text="Nº", width=100, height=30)
        self.entryNumRetas.grid(row=1, column=0, pady=(10), padx=(10))
        self.mainReta_button_1 = customtkinter.CTkButton( master=self.tabview.tab("Linha"), text="Ok", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.create_entry_widgets_Retas())
        self.mainReta_button_1.grid(row=2, column=0, pady=(20, 20))
        
        self.text_mode_labelCurvas = customtkinter.CTkLabel(self.tabview.tab("Curva"), text="Número de Curvas")
        self.text_mode_labelCurvas.grid(row=0, column=0, pady=(0, 0))
        self.entryNumCurvas = customtkinter.CTkEntry(self.tabview.tab("Curva"), placeholder_text="Nº", width=100, height=30)
        self.entryNumCurvas.grid(row=1, column=0, pady=(10), padx=(10))
        self.mainCurva_button_1 = customtkinter.CTkButton( master=self.tabview.tab("Curva"), text="Ok", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.create_entry_widgets_Curva())
        self.mainCurva_button_1.grid(row=2, column=0, pady=(20, 20))
        
        self.mainPoligono_button_add = customtkinter.CTkButton( master=self.tabview.tab("Poligono"), text="+ Add Poligonos", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.criar_segunda_tabview())
        self.mainPoligono_button_add.grid(row=0, column=0, padx=(20, 20), pady=(10, 10))
        self.mainPoligono_button_3 = customtkinter.CTkButton( master=self.tabview.tab("Poligono"), text="Rasterizar", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.valuesPoligono(self.entryTrianguloX1.get(), self.entryTrianguloX2.get(), self.entryTrianguloX3.get(), self.entryTrianguloY1.get(), self.entryTrianguloY2.get(), self.entryTrianguloY3.get(), self.entryTriangulo2X1.get(), self.entryTriangulo2X2.get(), self.entryTriangulo2X3.get(), self.entryTriangulo2Y1.get(), self.entryTriangulo2Y2.get(), self.entryTriangulo2Y3.get(), self.entryQuadradoX1.get(), self.entryQuadradoX2.get(), self.entryQuadradoX3.get(), self.entryQuadradoX4.get(),  self.entryQuadradoY1.get(), self.entryQuadradoY2.get(), self.entryQuadradoY3.get(), self.entryQuadradoY4.get(), self.entryQuadrado2X1.get(), self.entryQuadrado2X2.get(), self.entryQuadrado2X3.get(), self.entryQuadrado2X4.get(),  self.entryQuadrado2Y1.get(), self.entryQuadrado2Y2.get(), self.entryQuadrado2Y3.get(), self.entryQuadrado2Y4.get(), self.entryHexX1.get(), self.entryHexX2.get(), self.entryHexX3.get(), self.entryHexX4.get(), self.entryHexX5.get(), self.entryHexX6.get(), self.entryHexY1.get(), self.entryHexY2.get(), self.entryHexY3.get(), self.entryHexY4.get(), self.entryHexY5.get(), self.entryHexY6.get(), self.entryHex2X1.get(), self.entryHex2X2.get(), self.entryHex2X3.get(), self.entryHex2X4.get(), self.entryHex2X5.get(), self.entryHex2X6.get(), self.entryHex2Y1.get(), self.entryHex2Y2.get(), self.entryHex2Y3.get(), self.entryHex2Y4.get(), self.entryHex2Y5.get(), self.entryHex2Y6.get()))
        self.mainPoligono_button_3.grid(row=2, column=0, padx=(20, 20), pady=(10))
            

        
    def change_default_tab(self, tab_name):
        # Esta função é chamada quando um dos botões de rádio é pressionado
        self.tabview.set(tab_name)
            

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def clear_graph(self):
        if self.canvas_widget:
            self.canvas_widget.destroy()
            self.canvas_widget = None

    def valuesLinha(self, coordenadas_retas):
        self.clear_graph()

        resolutions = [(100, 100), (300, 300), (800, 600), (1920, 1080)]
        matriz_pixels_list = []

        for i, (width, height) in enumerate(resolutions):

            matriz_combined = np.zeros((height, width), dtype=int)

            for X1, Y1, X2, Y2 in coordenadas_retas:
                scaled_x1, scaled_y1, scaled_x2, scaled_y2 = line.normalization(X1, Y1, X2, Y2, width, height)
                matriz_pixels = line.DDA(scaled_x1, scaled_y1, scaled_x2, scaled_y2, width, height)
                matriz_combined += matriz_pixels

            matriz_pixels_list.append(matriz_combined)



        for i, (width, height) in enumerate(resolutions):
                    canva_width = width
                    if canva_width == 100:
                        fig = plt.figure(figsize=[3, 3])
                        plt.imshow(matriz_pixels_list[i], cmap='Blues', origin='lower')
                        plt.rc('font', size=5)
                        plt.title(f'Resolução: {width}x{height}')
                        plt.xlabel('Eixo X')
                        plt.ylabel('Eixo Y')
                        plt.grid(True)
                        canvas = FigureCanvasTkAgg(fig, master=self)
                        self.canvas_widget = canvas.get_tk_widget()
                        self.canvas_widget.grid(row=0, column=2, padx=(2, 0), pady=(2, 0))

                    
                        
                    elif canva_width == 300:
                        fig = plt.figure(figsize=[3, 3])
                        plt.imshow(matriz_pixels_list[i], cmap='Blues', origin='lower')
                        plt.rc('font', size=5)
                        plt.title(f'Resolução: {width}x{height}')
                        plt.xlabel('Eixo X')
                        plt.ylabel('Eixo Y')
                        plt.grid(True)
                        canvas = FigureCanvasTkAgg(fig, master=self)
                        self.canvas_widget = canvas.get_tk_widget()
                        self.canvas_widget.grid(row=1, column=2, padx=(2, 0), pady=(2, 0))
                        
                    elif canva_width == 800:
                        fig = plt.figure(figsize=[3, 3])
                        plt.imshow(matriz_pixels_list[i], cmap='Blues', origin='lower')
                        plt.rc('font', size=5)
                        plt.title(f'Resolução: {width}x{height}')
                        plt.xlabel('Eixo X')
                        plt.ylabel('Eixo Y')
                        plt.grid(True)
                        canvas = FigureCanvasTkAgg(fig, master=self)
                        self.canvas_widget = canvas.get_tk_widget()
                        self.canvas_widget.grid(row=0, column=3, padx=(2, 0), pady=(2, 0))
                        
                    elif canva_width == 1920:
                        fig = plt.figure(figsize=[3, 3])
                        plt.imshow(matriz_pixels_list[i], cmap='Blues', origin='lower')
                        plt.rc('font', size=5)
                        plt.title(f'Resolução: {width}x{height}')
                        plt.xlabel('Eixo X')
                        plt.ylabel('Eixo Y')
                        plt.grid(True)
                        canvas = FigureCanvasTkAgg(fig, master=self)
                        self.canvas_widget = canvas.get_tk_widget()
                        self.canvas_widget.grid(row=1, column=3, padx=(2, 0), pady=(2, 0))
#---------------------------------------------------------------------------------------


#-------------------------------Plot de Poligonos---------------------------------------

    def valuesPoligono(self, tx1, tx2, tx3, ty1, ty2, ty3, t2x1, t2x2, t2x3, t2y1, t2y2, t2y3, qx1, qx2, qx3, qx4, qy1, qy2, qy3, qy4, q2x1, q2x2, q2x3, q2x4, q2y1, q2y2, q2y3, q2y4, hx1, hx2, hx3, hx4, hx5, hx6, hy1, hy2, hy3, hy4, hy5, hy6, h2x1, h2x2, h2x3, h2x4, h2x5, h2x6, h2y1, h2y2, h2y3, h2y4, h2y5, h2y6):
        self.show_tabviews_originals()

        def parse_coordinates(coords_str):
            if coords_str:
                x, y = map(float, coords_str.split(','))
                return (x, y)
            else:
                return (0.0, 0.0)

        # Agora, podemos utilizar a função parse_coordinates para extrair as coordenadas.
        triangle1 = [parse_coordinates(tx1), parse_coordinates(ty1), parse_coordinates(tx2), parse_coordinates(ty2), parse_coordinates(tx3), parse_coordinates(ty3)]
        triangle2 = [parse_coordinates(t2x1), parse_coordinates(t2y1), parse_coordinates(t2x2), parse_coordinates(t2y2), parse_coordinates(t2x3), parse_coordinates(t2y3)]
        square1 = [parse_coordinates(qx1), parse_coordinates(qy1), parse_coordinates(qx2), parse_coordinates(qy2), parse_coordinates(qx3), parse_coordinates(qy3), parse_coordinates(qx4), parse_coordinates(qy4)]
        square2 = [parse_coordinates(q2x1), parse_coordinates(q2y1), parse_coordinates(q2x2), parse_coordinates(q2y2), parse_coordinates(q2x3), parse_coordinates(q2y3), parse_coordinates(q2x4), parse_coordinates(q2y4)]
        hexagon1 = [parse_coordinates(hx1), parse_coordinates(hy1), parse_coordinates(hx2), parse_coordinates(hy2), parse_coordinates(hx3), parse_coordinates(hy3), parse_coordinates(hx4), parse_coordinates(hy4), parse_coordinates(hx5), parse_coordinates(hy5), parse_coordinates(hx6), parse_coordinates(hy6)]
        hexagon2 = [parse_coordinates(h2x1), parse_coordinates(h2y1), parse_coordinates(h2x2), parse_coordinates(h2y2), parse_coordinates(h2x3), parse_coordinates(h2y3), parse_coordinates(h2x4), parse_coordinates(h2y4), parse_coordinates(h2x5), parse_coordinates(h2y5), parse_coordinates(h2x6), parse_coordinates(h2y6)]
        
        # Lista de resoluções
        resolutions = [(100, 100), (300, 300), (800, 600), (1920, 1080)]

        # Cores para cada forma geométrica
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        
        # Rasteriza as formas geométricas em cada resolução e exibe em janelas separadas
        for width, height in resolutions:
            canva_width = width
            image = np.full((height, width, 3), 255, dtype=np.uint8)           #cria uma matriz nova para cada resolução
            shapes = [triangle1, triangle2, square1, square2, hexagon1, hexagon2]
            for i, shape in enumerate(shapes):
                color = colors[i]
                adjusted_shape = [polygons.map_coordinates(x, y, width, height) for x, y in shape]  #lista que armazena as coordenada ajustadas dos vértices da forma geometrica .usada para a resolução atual (ajuda a escalonar)
                polygons.rasterize_polygon(adjusted_shape, image, color)
                
            

        # PLOT DO QUARTO GRÁFICO RASTERIZADO 
            if(canva_width == 100):
                fig1 = plt.figure(figsize=[3, 3])
                plt.imshow(image, extent=(0, width, 0, height), origin="upper")
                plt.rc('font', size=5)
                plt.title(f'Resolução: {width}x{height}')
                plt.xlabel('Eixo X')
                plt.ylabel('Eixo Y')
                plt.grid(True)
                
                canvas = FigureCanvasTkAgg(fig1, master=self)
                self.canvas_widget = canvas.get_tk_widget()
                self.canvas_widget.grid(row=0, column=2, padx=(2, 0), pady=(2, 0))
                
            if(canva_width == 300):
                fig2 = plt.figure(figsize=[3, 3])
                plt.imshow(image, extent=(0, width, 0, height), origin="upper")
                plt.rc('font', size=5)
                plt.title(f'Resolução: {width}x{height}')
                plt.xlabel('Eixo X')
                plt.ylabel('Eixo Y')
                plt.grid(True)
                canvas = FigureCanvasTkAgg(fig2, master=self)
                self.canvas_widget = canvas.get_tk_widget()
                self.canvas_widget.grid(row=1, column=2, padx=(2, 0), pady=(2, 0))
                
            if(canva_width == 800):
                fig3 = plt.figure(figsize=[3, 3])
                plt.imshow(image, extent=(0, width, 0, height), origin="upper")
                plt.rc('font', size=5)
                plt.title(f'Resolução: {width}x{height}')
                plt.xlabel('Eixo X')
                plt.ylabel('Eixo Y')
                plt.grid(True)
                canvas = FigureCanvasTkAgg(fig3, master=self)
                self.canvas_widget = canvas.get_tk_widget()
                self.canvas_widget.grid(row=0, column=3, padx=(2, 0), pady=(2, 0))
                
            if(canva_width == 1920):
                fig4 = plt.figure(figsize=[3, 3])
                plt.imshow(image, extent=(0, width, 0, height), origin="upper")
                plt.rc('font', size=5)
                plt.title(f'Resolução: {width}x{height}')
                plt.xlabel('Eixo X')
                plt.ylabel('Eixo Y')
                plt.grid(True)
                canvas = FigureCanvasTkAgg(fig4, master=self)
                self.canvas_widget = canvas.get_tk_widget()
                self.canvas_widget.grid(row=1, column=3, padx=(2, 0), pady=(2, 0))
            
#-------------------------------Plot das Curvas---------------------------------------

    def valuesCurva(self, variaveis_curva):

                M = np.array([[2, -2, 1, 1],
                [-3, 3, -2, -1],
                [0, 0, 1, 0],
                [1, 0, 0, 0]])

                # Defina as resoluções desejadas
                resolutions = [(100, 100), (300, 300), (800, 600), (1920, 1080)]

                # Lista de cores para as curvas
                colors = ['red', 'green', 'blue', 'purple', 'orange']

                for i, (width, height) in enumerate(resolutions):
                    canva_width = width
                    image = Image.new('RGB', (width, height), color=(0, 0, 0))
                    draw = ImageDraw.Draw(image)
                    
                    p0_list, p1_list, m0_list, m1_list, T_list = zip(*variaveis_curva)

                    for i in range(len(p0_list)):
                        p0 = p0_list[i]
                        p1 = p1_list[i]
                        m0 = m0_list[i]
                        m1 = m1_list[i]
                        T_values = T_list[i]
                        # Após calcular as coordenadas da curva
                        x_curve, y_curve = curves.rasterize_hermite_curve(p0, p1, m0, m1, T_values, M)

                        x_scale = width / 2
                        y_scale = height / 2

                        for j in range(1, len(x_curve)):
                            x0 = int(round(x_curve[j - 1] * x_scale + width / 2))
                            y0 = int(round(-y_curve[j - 1] * y_scale + height / 2))  # Inverter a coordenada Y
                            x1 = int(round(x_curve[j] * x_scale + width / 2))
                            y1 = int(round(-y_curve[j] * y_scale + height / 2))  # Inverter a coordenada Y

                            draw.line((x0, y0, x1, y1), fill=(255, 255, 255), width=1)

                # PLOT DO QUARTO GRÁFICO RASTERIZADO 
                    if(canva_width == 100):
                        fig1 = plt.figure(figsize=[3, 3])
                        plt.imshow(image, extent=(0, width, 0,height), origin="upper")
                        plt.rc('font', size=5)
                        plt.title(f'Resolução: {width}x{height}')
                        plt.xlabel('Eixo X')
                        plt.ylabel('Eixo Y')
                        plt.grid(True)
                        
                        canvas = FigureCanvasTkAgg(fig1, master=self)
                        self.canvas_widget = canvas.get_tk_widget()
                        self.canvas_widget.grid(row=0, column=2, padx=(2, 0), pady=(2, 0))
                        
                    if(canva_width == 300):
                        fig2 = plt.figure(figsize=[3, 3])
                        plt.imshow(image, extent=(0, width, 0, height), origin="upper")
                        plt.rc('font', size=5)
                        plt.title(f'Resolução: {width}x{height}')
                        plt.xlabel('Eixo X')
                        plt.ylabel('Eixo Y')
                        plt.grid(True)
                        canvas = FigureCanvasTkAgg(fig2, master=self)
                        self.canvas_widget = canvas.get_tk_widget()
                        self.canvas_widget.grid(row=1, column=2, padx=(2, 0), pady=(2, 0))
                        
                    if(canva_width == 800):
                        fig3 = plt.figure(figsize=[3, 3])
                        plt.imshow(image, extent=(0, width, 0, height), origin="upper")
                        plt.rc('font', size=5)
                        plt.title(f'Resolução: {width}x{height}')
                        plt.xlabel('Eixo X')
                        plt.ylabel('Eixo Y')
                        plt.grid(True)
                        canvas = FigureCanvasTkAgg(fig3, master=self)
                        self.canvas_widget = canvas.get_tk_widget()
                        self.canvas_widget.grid(row=0, column=3, padx=(2, 0), pady=(2, 0))
                        
                    if(canva_width == 1920):
                        fig4 = plt.figure(figsize=[3, 3])
                        plt.imshow(image, extent=(0, width, 0, height), origin="upper")
                        plt.rc('font', size=5)
                        plt.title(f'Resolução: {width}x{height}')
                        plt.xlabel('Eixo X')
                        plt.ylabel('Eixo Y')
                        plt.grid(True)
                        canvas = FigureCanvasTkAgg(fig4, master=self)
                        self.canvas_widget = canvas.get_tk_widget()
                        self.canvas_widget.grid(row=1, column=3, padx=(2, 0), pady=(2, 0))


if __name__ == "__main__":
    app = App()
    app.mainloop()