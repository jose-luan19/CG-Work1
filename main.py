import tkinter as tk
from tkinter import messagebox
import subprocess
import json

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Input Interface")

        self.create_widgets()

    def create_widgets(self):
        # Create frames
        self.inputs_frame = tk.Frame(self.root)
        self.inputs_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Setup layout
        self.figura_var = tk.StringVar(value="Line")
        self.setup_controls()
        self.update_inputs()

        for col in range(4):
            self.root.grid_columnconfigure(col, weight=1)

    def setup_controls(self):
        # Radio buttons for selection
        tk.Label(self.inputs_frame, text="Figura:").grid(row=0, column=0, columnspan=4, pady=10)
        figuras = ["Line", "Curve", "Polygon"]
        for idx, figura in enumerate(figuras):
            rb = tk.Radiobutton(self.inputs_frame, text=figura, variable=self.figura_var, value=figura, command=self.update_inputs)
            rb.grid(row=1, column=idx, padx=10)

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
        
    def create_line_inputs(self):
        num_inputs = 16  # Default for Line

        self.points_entries = []
        title = "Line"

        for i in range(num_inputs // 4):
            # col_start = i * 2  # Define o espaçamento de 2 colunas entre cada conjunto de entradas

            # Adiciona um título para cada linha
            tk.Label(self.inputs_frame, text=f"{title} {i+1}").grid(row=2 + i * 5, column=0, columnspan=4, pady=10)

            # Adiciona os campos de entrada para o ponto de início (Start X e Start Y)
            tk.Label(self.inputs_frame, text="Start X:").grid(row=3 + i * 5, column=0, pady=5)
            start_x_entry = tk.Entry(self.inputs_frame, width=5)
            start_x_entry.grid(row=3 + i * 5, column=1, padx=6, pady=5)
            self.points_entries.append(start_x_entry)

            tk.Label(self.inputs_frame, text="Start Y:").grid(row=3 + i * 5, column=2, pady=5)
            start_y_entry = tk.Entry(self.inputs_frame, width=5)
            start_y_entry.grid(row=3 + i * 5, column=3, padx=6, pady=5)
            self.points_entries.append(start_y_entry)

            # Adiciona os campos de entrada para o ponto de fim (End X e End Y)
            tk.Label(self.inputs_frame, text="End X:").grid(row=4 + i * 5, column=0, pady=5)
            end_x_entry = tk.Entry(self.inputs_frame, width=5)
            end_x_entry.grid(row=4 + i * 5, column=1, padx=6, pady=5)
            self.points_entries.append(end_x_entry)

            tk.Label(self.inputs_frame, text="End Y:").grid(row=4 + i * 5, column=2, pady=5)
            end_y_entry = tk.Entry(self.inputs_frame, width=5)
            end_y_entry.grid(row=4 + i * 5, column=3, padx=6, pady=5)
            self.points_entries.append(end_y_entry)

        self.row_count = (num_inputs // 4) * 5 + 2  # Atualiza a contagem
        
    def create_curve_inputs(self):
        num_inputs = 32  # Agora são 8 entradas por conjunto, então 32 no total

        self.points_entries = []
        title = "Curve"

        for i in range(num_inputs // 8):
            # Adiciona um título para cada conjunto de entradas
            tk.Label(self.inputs_frame, text=f"{title} {i+1}").grid(row=2 + i * 7, column=0, columnspan=4, pady=10)

            # Adiciona os campos de entrada para o ponto de início (Start X e Start Y)
            tk.Label(self.inputs_frame, text="Start X:").grid(row=3 + i * 7, column=0, pady=5)
            start_x_entry = tk.Entry(self.inputs_frame, width=5)
            start_x_entry.grid(row=3 + i * 7, column=1, padx=6, pady=5)
            self.points_entries.append(start_x_entry)

            tk.Label(self.inputs_frame, text="Start Y:").grid(row=3 + i * 7, column=2, pady=5)
            start_y_entry = tk.Entry(self.inputs_frame, width=5)
            start_y_entry.grid(row=3 + i * 7, column=3, padx=6, pady=5)
            self.points_entries.append(start_y_entry)

            # Adiciona os campos de entrada para o ponto de fim (End X e End Y)
            tk.Label(self.inputs_frame, text="End X:").grid(row=4 + i * 7, column=0, pady=5)
            end_x_entry = tk.Entry(self.inputs_frame, width=5)
            end_x_entry.grid(row=4 + i * 7, column=1, padx=6, pady=5)
            self.points_entries.append(end_x_entry)

            tk.Label(self.inputs_frame, text="End Y:").grid(row=4 + i * 7, column=2, pady=5)
            end_y_entry = tk.Entry(self.inputs_frame, width=5)
            end_y_entry.grid(row=4 + i * 7, column=3, padx=6, pady=5)
            self.points_entries.append(end_y_entry)

            # Adiciona os campos de entrada para o ponto M_0 (M_0 X e M_0 Y)
            tk.Label(self.inputs_frame, text="M_0 X:").grid(row=5 + i * 7, column=0, pady=5)
            m0_x_entry = tk.Entry(self.inputs_frame, width=5)
            m0_x_entry.grid(row=5 + i * 7, column=1, padx=6, pady=5)
            self.points_entries.append(m0_x_entry)

            tk.Label(self.inputs_frame, text="M_0 Y:").grid(row=5 + i * 7, column=2, pady=5)
            m0_y_entry = tk.Entry(self.inputs_frame, width=5)
            m0_y_entry.grid(row=5 + i * 7, column=3, padx=6, pady=5)
            self.points_entries.append(m0_y_entry)

            # Adiciona os campos de entrada para o ponto M_1 (M_1 X e M_1 Y)
            tk.Label(self.inputs_frame, text="M_1 X:").grid(row=6 + i * 7, column=0, pady=5)
            m1_x_entry = tk.Entry(self.inputs_frame, width=5)
            m1_x_entry.grid(row=6 + i * 7, column=1, padx=6, pady=5)
            self.points_entries.append(m1_x_entry)

            tk.Label(self.inputs_frame, text="M_1 Y:").grid(row=6 + i * 7, column=2, pady=5)
            m1_y_entry = tk.Entry(self.inputs_frame, width=5)
            m1_y_entry.grid(row=6 + i * 7, column=3, padx=6, pady=5)
            self.points_entries.append(m1_y_entry)

        self.row_count = (num_inputs // 8) * 7 + 2  # Atualiza a contagem de linhas


    def create_polygon_inputs(self):
        num_points = [3, 4, 6]  # Número de pontos para Triângulo, Quadrado e Hexágono
        titles = ["Triangle", "Square", "Hexagon"]
        column_offset = [0, 4, 8]  # Deslocamento da coluna para cada tipo de polígono

        self.points_entries = []

        for j, title in enumerate(titles):
            # Título do polígono
            tk.Label(self.inputs_frame, text=title).grid(row=2, column=column_offset[j], columnspan=4, pady=10)

            for i in range(num_points[j]):
                row = 3 + i * 2  # Calcula a linha baseada no índice do ponto e do tipo de polígono

                # Labels e entradas para X e Y
                tk.Label(self.inputs_frame, text=f"Point {i+1} X:").grid(row=row, column=column_offset[j], pady=5)
                x_entry = tk.Entry(self.inputs_frame, width=5)
                x_entry.grid(row=row, column=column_offset[j] + 1, padx=6, pady=5)
                self.points_entries.append(x_entry)

                tk.Label(self.inputs_frame, text=f"Point {i+1} Y:").grid(row=row, column=column_offset[j] + 2, pady=5)
                y_entry = tk.Entry(self.inputs_frame, width=5)
                y_entry.grid(row=row, column=column_offset[j] + 3, padx=6, pady=5)
                self.points_entries.append(y_entry)

        # Atualiza a contagem de linhas considerando o maior número de pontos e espaçamento
        self.row_count = max(num_points) * 2 + 3

    def submit(self):
        figura = self.figura_var.get()
        if figura == "Polygon":
            points = {
                "Triangle": [],
                "Square": [],
                "Hexagon": []
            }

            num_points = [3, 4, 6]  # Número de pontos para Triângulo, Quadrado e Hexágono
            titles = ["Triangle", "Square", "Hexagon"]
            # column_offset = [0, 4, 8]  # Deslocamento da coluna para cada tipo de polígono

            try:
                entry_index = 0
                for j, title in enumerate(titles):
                    for i in range(num_points[j]):
                        # Obtém as entradas de x e y na ordem correta
                        x = self.points_entries[entry_index].get()
                        y = self.points_entries[entry_index + 1].get()

                        if x == '' or y == '':
                            entry_index += 2
                            continue

                        points[title].append((int(x), int(y)))
                        entry_index += 2
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid integer points for x and y")
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
                    if len(self.points_entries) - entry_index >= 4 and all(self.points_entries[entry_index + i].get() != '' for i in range(4)):
                        line = [
                            (int(self.points_entries[entry_index].get()), int(self.points_entries[entry_index + 1].get())),
                            (int(self.points_entries[entry_index + 2].get()), int(self.points_entries[entry_index + 3].get()))
                        ]
                        points.append(line)
                        entry_index += 4
                    else:
                        entry_index += 2

            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid integer points for all coordinates")
                return

            data = {
                "figura": figura,
                "points": points
            }

        elif figura == "Curve":
            points = []
            try:
                entry_index = 0
                while entry_index < len(self.points_entries):
                    if len(self.points_entries) - entry_index >= 8 and all(self.points_entries[entry_index + i].get() != '' for i in range(8)):
                        curve = [
                            (int(self.points_entries[entry_index].get()), int(self.points_entries[entry_index + 1].get())),
                            (int(self.points_entries[entry_index + 2].get()), int(self.points_entries[entry_index + 3].get())),
                            (int(self.points_entries[entry_index + 4].get()), int(self.points_entries[entry_index + 5].get())),
                            (int(self.points_entries[entry_index + 6].get()), int(self.points_entries[entry_index + 7].get()))
                        ]
                        points.append(curve)
                        entry_index += 8
                    else:
                        entry_index += 2

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
