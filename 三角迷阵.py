# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, ttk


class TrianglePathSolver:
    def __init__(self, root):
        self.root = root
        self.points = []
        self.buttons = []

        # Input for row count and control buttons
        self.input_frame = tk.Frame(root, bg="lightgray")
        self.input_frame.pack(pady=10)

        self.row_entry = tk.Entry(self.input_frame, width=5, font=('Arial', 14))
        self.row_entry.insert(0, "12")  # Default row count
        self.row_entry.grid(row=0, column=0)

        self.generate_button = tk.Button(self.input_frame, text="生成三角形", command=self.generate_triangle,
                                         font=('Arial', 12))
        self.generate_button.grid(row=0, column=1, padx=10)

        self.calculate_button = tk.Button(self.input_frame, text="计算最优路径", command=self.calculate_path,
                                          font=('Arial', 12))
        self.calculate_button.grid(row=0, column=2)

        # Canvas for triangle layout with scrollbar
        self.canvas_frame = tk.Frame(root, bg="lightgray")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg="lightgray")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def generate_triangle(self):
        # Clear previous points and buttons if they exist
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.points = []
        self.buttons = []

        # Get the number of rows from the entry
        try:
            self.rows = int(self.row_entry.get())
            if self.rows < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的行数（正整数）")
            return

        # Create buttons in a centered, isosceles triangle layout
        for i in range(self.rows):
            row_points = []
            row_buttons = []

            # Frame for each row, to help with centering
            row_frame = tk.Frame(self.inner_frame, bg="lightgray")
            row_frame.pack()

            # Label to indicate the row number
            row_label = tk.Label(row_frame, text=f"第{i + 1}行", font=('Arial', 12), bg="lightgray")
            row_label.grid(row=0, column=0, padx=5, pady=5)

            # Create buttons centered in each row
            for j in range(i + 1):
                point = 0  # Initial state (not highlighted)
                row_points.append(point)

                # Create a button styled to look like a circular point
                button = tk.Button(
                    row_frame,
                    text="●",
                    font=('Arial', 16),
                    width=2,
                    height=1,
                    fg="black",
                    bg="black",
                    command=lambda x=i, y=j: self.toggle_point(x, y)
                )

                # Position the button in the correct column within the row frame
                button.grid(row=0, column=j + 1, padx=5, pady=5)  # Shift column index by 1 to accommodate row label
                row_buttons.append(button)
            self.points.append(row_points)
            self.buttons.append(row_buttons)

    def toggle_point(self, row, col):
        # Toggle between a highlighted state (red with star) and normal state (black)
        self.points[row][col] = 1 - self.points[row][col]
        if self.points[row][col] == 1:
            self.buttons[row][col].config(text="★", fg="yellow", bg="red")
        else:
            self.buttons[row][col].config(text="●", fg="black", bg="black")

    def calculate_path(self):
        # Apply dynamic programming to find the path with maximum highlights
        dp = [[0 for _ in range(i + 1)] for i in range(self.rows)]
        path = [[None for _ in range(i + 1)] for i in range(self.rows)]

        # Initialize DP table
        dp[0][0] = self.points[0][0]

        # Fill DP table from top to bottom
        for i in range(1, self.rows):
            for j in range(i + 1):
                if j == 0:
                    # Only one way to get here, from directly above
                    dp[i][j] = dp[i - 1][j] + self.points[i][j]
                    path[i][j] = "左"  # 从用户视角来看，这是向左走
                elif j == i:
                    # Only one way to get here, from the left above
                    dp[i][j] = dp[i - 1][j - 1] + self.points[i][j]
                    path[i][j] = "右"  # 从用户视角来看，这是向右走
                else:
                    # Two ways to get here, choose the one with the maximum score
                    if dp[i - 1][j - 1] > dp[i - 1][j]:
                        dp[i][j] = dp[i - 1][j - 1] + self.points[i][j]
                        path[i][j] = "右"
                    else:
                        dp[i][j] = dp[i - 1][j] + self.points[i][j]
                        path[i][j] = "左"

        # Find maximum score in the last row
        max_score = max(dp[-1])
        max_index = dp[-1].index(max_score)

        # Reconstruct the path from bottom to top
        directions = []
        current_row, current_col = self.rows - 1, max_index

        while current_row > 0:
            direction = path[current_row][current_col]
            directions.append(direction)

            # Update button to show the path
            self.buttons[current_row][current_col].config(bg="blue", fg="white")

            if direction == "右":
                current_col -= 1
            current_row -= 1

        # Update button at the start of the path
        self.buttons[0][0].config(bg="blue", fg="white")

        directions.reverse()  # Reverse to get the path from top to bottom

        # Display result
        path_str = " -> ".join(directions)
        messagebox.showinfo("结果", f"最高得分: {max_score}\n路径: {path_str}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("三角迷阵得分最高路径")
    root.geometry("600x600")  # Set a reasonable default size
    TrianglePathSolver(root)
    root.mainloop()
