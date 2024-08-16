import tkinter as tk
from tkinter import messagebox
import subprocess
import json

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Input Interface")
        self.root.state('zoomed')

        self.create_widgets()
        # # Mapeamento da tecla Enter para o método submit
        self.root.bind('<Return>', lambda event: self.submit())

    def create_widgets(self):
        # Criar frames
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Criar canvas e scrollbar
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # Bind scroll event
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Frame para inputs
        self.inputs_frame = tk.Frame(self.scrollable_frame)
        self.inputs_frame.pack(fill="both", expand=True)

        # Configurar layout
        self.figura_var = tk.StringVar(value="Line")
        self.setup_controls()
        self.update_inputs()

        # Configura o peso das colunas e linhas
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
    def on_mouse_wheel(self, event):
        # Rola o canvas quando a rotação do mouse é detectada
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def setup_controls(self):
        # Radio buttons for selection
        tk.Label(self.inputs_frame, text="Figura:").grid(row=0, column=0, columnspan=4, pady=5)
        tk.Label(self.inputs_frame, text="Pode por entradas para o plano 100x100 e será feito a normalização para as outras resoluções").grid(row=1, column=0, columnspan=4, padx=10, pady=1)
        figuras = ["Line", "Curve", "Polygon"]
        for idx, figura in enumerate(figuras):
            rb = tk.Radiobutton(self.inputs_frame, text=figura, variable=self.figura_var, value=figura, command=self.update_inputs)
            rb.grid(row=2, column=idx, padx=10, pady=3)

    def update_inputs(self):
        # Remove todos os widgets do frame
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()

        self.setup_controls()

        # Recria os inputs conforme a figura selecionada
        figura = self.figura_var.get()
        if figura == "Line":
            self.create_line_inputs()
        elif figura == "Curve":
            self.create_curve_inputs()
        elif figura == "Polygon":
            self.create_polygon_inputs()

        # Adiciona o botão de submissão ao final
        tk.Button(self.inputs_frame, text="Submit", command=self.submit).grid(row=self.row_count, column=0, columnspan=4, pady=15)
        
        if figura == "Polygon":
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        else:
            self.canvas.config(scrollregion=(0, 0, 1, 1))  # Esconde a barra de rolagem quando não necessário
    
        
    def create_line_inputs(self):
        num_inputs = 20  # Default for Line

        self.points_entries = []
        title = "Line"

        for i in range(num_inputs // 4):
            # col_start = i * 2  # Define o espaçamento de 2 colunas entre cada conjunto de entradas

            # Adiciona um título para cada linha
            tk.Label(self.inputs_frame, text=f"{title} {i+1}").grid(row=3 + i * 5, column=0, columnspan=4, pady=10)

            # Adiciona os campos de entrada para o ponto de início (Start X e Start Y)
            tk.Label(self.inputs_frame, text="Start X:").grid(row=4 + i * 5, column=0, pady=5)
            start_x_entry = tk.Entry(self.inputs_frame, width=5)
            start_x_entry.grid(row=4 + i * 5, column=1, padx=6, pady=5)
            self.points_entries.append(start_x_entry)

            tk.Label(self.inputs_frame, text="Start Y:").grid(row=4 + i * 5, column=2, pady=5)
            start_y_entry = tk.Entry(self.inputs_frame, width=5)
            start_y_entry.grid(row=4 + i * 5, column=3, padx=6, pady=5)
            self.points_entries.append(start_y_entry)

            # Adiciona os campos de entrada para o ponto de fim (End X e End Y)
            tk.Label(self.inputs_frame, text="End X:").grid(row=5 + i * 5, column=0, pady=5)
            end_x_entry = tk.Entry(self.inputs_frame, width=5)
            end_x_entry.grid(row=5 + i * 5, column=1, padx=6, pady=5)
            self.points_entries.append(end_x_entry)

            tk.Label(self.inputs_frame, text="End Y:").grid(row=5 + i * 5, column=2, pady=5)
            end_y_entry = tk.Entry(self.inputs_frame, width=5)
            end_y_entry.grid(row=5 + i * 5, column=3, padx=6, pady=5)
            self.points_entries.append(end_y_entry)

        self.row_count = (num_inputs // 4) * 5 + 2  # Atualiza a contagem
        
    def create_curve_inputs(self):
        num_inputs = 40  # Agora são 8 entradas por conjunto, então 32 no total

        self.points_entries = []
        title = "Curve"

        for i in range(num_inputs // 8):
            # Adiciona um título para cada conjunto de entradas
            tk.Label(self.inputs_frame, text=f"{title} {i+1}").grid(row=3 + i * 7, column=0, columnspan=4, pady=10)

            # Adiciona os campos de entrada para o ponto de início (Start X e Start Y)
            tk.Label(self.inputs_frame, text="Start X:").grid(row=4 + i * 7, column=0, pady=5)
            start_x_entry = tk.Entry(self.inputs_frame, width=5)
            start_x_entry.grid(row=4 + i * 7, column=1, padx=6, pady=5)
            self.points_entries.append(start_x_entry)

            tk.Label(self.inputs_frame, text="Start Y:").grid(row=4 + i * 7, column=2, pady=5)
            start_y_entry = tk.Entry(self.inputs_frame, width=5)
            start_y_entry.grid(row=4 + i * 7, column=3, padx=6, pady=5)
            self.points_entries.append(start_y_entry)

            # Adiciona os campos de entrada para o ponto de fim (End X e End Y)
            tk.Label(self.inputs_frame, text="End X:").grid(row=5 + i * 7, column=0, pady=5)
            end_x_entry = tk.Entry(self.inputs_frame, width=5)
            end_x_entry.grid(row=5 + i * 7, column=1, padx=6, pady=5)
            self.points_entries.append(end_x_entry)

            tk.Label(self.inputs_frame, text="End Y:").grid(row=5 + i * 7, column=2, pady=5)
            end_y_entry = tk.Entry(self.inputs_frame, width=5)
            end_y_entry.grid(row=5 + i * 7, column=3, padx=6, pady=5)
            self.points_entries.append(end_y_entry)

            # Adiciona os campos de entrada para o ponto M_0 (M_0 X e M_0 Y)
            tk.Label(self.inputs_frame, text="M_0 X:").grid(row=6 + i * 7, column=0, pady=5)
            m0_x_entry = tk.Entry(self.inputs_frame, width=5)
            m0_x_entry.grid(row=6 + i * 7, column=1, padx=6, pady=5)
            self.points_entries.append(m0_x_entry)

            tk.Label(self.inputs_frame, text="M_0 Y:").grid(row=6 + i * 7, column=2, pady=5)
            m0_y_entry = tk.Entry(self.inputs_frame, width=5)
            m0_y_entry.grid(row=6 + i * 7, column=3, padx=6, pady=5)
            self.points_entries.append(m0_y_entry)

            # Adiciona os campos de entrada para o ponto M_1 (M_1 X e M_1 Y)
            tk.Label(self.inputs_frame, text="M_1 X:").grid(row=7 + i * 7, column=0, pady=5)
            m1_x_entry = tk.Entry(self.inputs_frame, width=5)
            m1_x_entry.grid(row=7 + i * 7, column=1, padx=6, pady=5)
            self.points_entries.append(m1_x_entry)

            tk.Label(self.inputs_frame, text="M_1 Y:").grid(row=7 + i * 7, column=2, pady=5)
            m1_y_entry = tk.Entry(self.inputs_frame, width=5)
            m1_y_entry.grid(row=7 + i * 7, column=3, padx=6, pady=5)
            self.points_entries.append(m1_y_entry)

        self.row_count = (num_inputs // 8) * 7 + 2  # Atualiza a contagem de linhas


    def create_polygon_inputs(self):
        num_points = [3, 4, 6]  # Número de pontos para Triângulo, Quadrado e Hexágono
        titles = ["Triangle", "Square", "Hexagon"]

        self.points_entries = []

        current_row = 3  # Linha inicial para o primeiro polígono

        for j, title in enumerate(titles):
            for k in range(2):  # Loop para criar dois conjuntos de entradas
                # Título do polígono
                tk.Label(self.inputs_frame, text=f"{title} {k+1}").grid(row=current_row, column=0, columnspan=4, pady=10)

                for i in range(num_points[j]):
                    row = current_row + 1 + i * 2  # Calcula a linha baseada no índice do ponto e do tipo de polígono

                    # Labels e entradas para X e Y
                    tk.Label(self.inputs_frame, text=f"Point {i+1} X:").grid(row=row, column=0, pady=5)
                    x_entry = tk.Entry(self.inputs_frame, width=5)
                    x_entry.grid(row=row, column=1, padx=6, pady=5)
                    self.points_entries.append(x_entry)

                    tk.Label(self.inputs_frame, text=f"Point {i+1} Y:").grid(row=row, column=2, pady=5)
                    y_entry = tk.Entry(self.inputs_frame, width=5)
                    y_entry.grid(row=row, column=3, padx=6, pady=5)
                    self.points_entries.append(y_entry)

                # Incrementa a linha atual para o próximo conjunto de inputs
                current_row += num_points[j] * 2 + 2  # Move para a linha após o último ponto do polígono atual

        # Atualiza a contagem de linhas
        self.row_count = current_row + 1

    def submit(self):
        figura = self.figura_var.get()
        if figura == "Polygon":
            points = {
                "Triangle": [[], []],
                "Square": [[], []],
                "Hexagon": [[], []]
            }

            num_points = [3, 4, 6]  # Número de pontos para Triângulo, Quadrado e Hexágono
            titles = ["Triangle", "Square", "Hexagon"]

            all_empty = True
            incomplete_polygon = False

            try:
                entry_index = 0
                for j, title in enumerate(titles):
                    for k in range(2):  # Loop para criar dois conjuntos de entradas
                        polygon_points = []
                        polygon_complete = True
                        
                        for i in range(num_points[j]):
                            # Obtém as entradas de x e y na ordem correta
                            x = self.points_entries[entry_index].get()
                            y = self.points_entries[entry_index + 1].get()

                            # Se ambos X e Y estiverem vazios, continua verificando
                            if x == '' and y == '':
                                polygon_complete = False
                            elif x == '' or y == '':
                                # Se apenas um dos campos estiver vazio, considera como incompleto
                                incomplete_polygon = True
                                polygon_complete = False
                            else:
                                # Se ambos estão preenchidos corretamente, adiciona ao polígono
                                polygon_points.append((int(x), int(y)))

                            # Se qualquer campo não estiver vazio, não está tudo vazio
                            if x != '' or y != '':
                                all_empty = False

                            entry_index += 2

                        if polygon_complete and len(polygon_points) == num_points[j]:
                            points[title][k].extend(polygon_points)
                        elif len(polygon_points) > 0:
                            incomplete_polygon = True

                if all_empty:
                    messagebox.showwarning("Input Warning", "Não pode ser tudo vazio.")
                    return

                if incomplete_polygon:
                    messagebox.showwarning("Input Warning", "Por favor, preencha todos os campos para os polígonos incompletos.")
                    return
                
            except ValueError:
                messagebox.showerror("Input Error", "Por favor, insira valores inteiros válidos para x e y.")
                return

            data = {
                "figura": figura,
                "points": points
            }
            
        elif figura == "Line":
            points = []
            try:
                entry_index = 0
                while entry_index < len(self.points_entries):
                    start_x = self.points_entries[entry_index].get()
                    start_y = self.points_entries[entry_index + 1].get()
                    end_x = self.points_entries[entry_index + 2].get()
                    end_y = self.points_entries[entry_index + 3].get()

                    if start_x == '' or start_y == '' or end_x == '' or end_y == '':
                        # Se qualquer campo estiver vazio, gera um alerta
                        if any([start_x, start_y, end_x, end_y]):
                            messagebox.showwarning("Incomplete Input", "Please fill in all fields for the current line.")
                            return
                    else:
                        line = [
                            (int(start_x), int(start_y)),
                            (int(end_x), int(end_y))
                        ]
                        points.append(line)
                    
                    entry_index += 4

                if not points:
                    messagebox.showwarning("No Input", "No complete line data entered.")
                    return

            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid integer points for all coordinates")
                return

            data = {
                "figura": figura,
                "points": points
            }

        else:
            points = []
            try:
                entry_index = 0
                while entry_index < len(self.points_entries):
                    start_x = self.points_entries[entry_index].get()
                    start_y = self.points_entries[entry_index + 1].get()
                    end_x = self.points_entries[entry_index + 2].get()
                    end_y = self.points_entries[entry_index + 3].get()
                    m0_x = self.points_entries[entry_index + 4].get()
                    m0_y = self.points_entries[entry_index + 5].get()
                    m1_x = self.points_entries[entry_index + 6].get()
                    m1_y = self.points_entries[entry_index + 7].get()

                    if (start_x == '' or start_y == '' or end_x == '' or end_y == '' or
                        m0_x == '' or m0_y == '' or m1_x == '' or m1_y == ''):
                        # Se qualquer campo estiver vazio, gera um alerta
                        if any([start_x, start_y, end_x, end_y, m0_x, m0_y, m1_x, m1_y]):
                            messagebox.showwarning("Incomplete Input", "Please fill in all fields for the current curve.")
                            return
                    else:
                        curve = [
                            (int(start_x), int(start_y)),
                            (int(end_x), int(end_y)),
                            (int(m0_x), int(m0_y)),
                            (int(m1_x), int(m1_y))
                        ]
                        points.append(curve)

                    entry_index += 8

                if not points:
                    messagebox.showwarning("No Input", "No complete curve data entered.")
                    return

            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid integer points for all coordinates")
                return

            data = {
                "figura": figura,
                "points": points
            }

        with open("data.json", "w") as f:
            json.dump(data, f)

        script_map = {
            "Line": "line.py",
            "Curve": "curve.py",
            "Polygon": "polygon.py"
        }

        try:
            subprocess.run(["python", script_map[figura]], check=True)
            messagebox.showinfo("Success", "Images generated successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
