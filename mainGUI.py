import tkinter as tk
import threading
import time


class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kockapakolás")

        tk.Label(self.root, text="N:").grid(row=0, column=0)
        self.n_entry = tk.Entry(self.root)
        self.n_entry.insert(0, "10")
        self.n_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Population size:").grid(row=1,column=0)
        self.population_entry = tk.Entry(self.root)
        self.population_entry.insert(0, "50")
        self.population_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Generations (0 for infinite):").grid(row=2, column=0,)
        self.generations_entry = tk.Entry(self.root)
        self.generations_entry.insert(0, "100")
        self.generations_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Mutation rate:").grid(row=3, column=0)
        self.mutation_rate_entry = tk.Entry(self.root)
        self.mutation_rate_entry.insert(0, "0.1")
        self.mutation_rate_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Accuracy:").grid(row=4, column=0)
        self.accuracy_entry = tk.Entry(self.root)
        self.accuracy_entry.insert(0, "0")
        self.accuracy_entry.grid(row=4, column=1)

        tk.Button(self.root, text="Start", command=self.start).grid(row=6, column=0, columnspan=2)

    def start(self):
        pass

