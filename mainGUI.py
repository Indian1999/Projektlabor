import tkinter as tk
from genetic import Genetic
from tkinter import scrolledtext
import threading
import time

FONT = ("Arial", 20)
class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kockapakolás")

        tk.Label(self.root, text="N:", font=FONT).grid(row=0, column=0)
        self.n_entry = tk.Entry(self.root)
        self.n_entry.insert(0, "20")
        self.n_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Population size:", font=FONT).grid(row=1,column=0)
        self.population_entry = tk.Entry(self.root)
        self.population_entry.insert(0, "50")
        self.population_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Generations (0 for infinite):", font=FONT).grid(row=2, column=0,)
        self.generations_entry = tk.Entry(self.root)
        self.generations_entry.insert(0, "100")
        self.generations_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Mutation rate:", font=FONT).grid(row=3, column=0)
        self.mutation_rate_entry = tk.Entry(self.root)
        self.mutation_rate_entry.insert(0, "0.1")
        self.mutation_rate_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Accuracy:", font=FONT).grid(row=4, column=0)
        self.accuracy_entry = tk.Entry(self.root)
        self.accuracy_entry.insert(0, "0")
        self.accuracy_entry.grid(row=4, column=1)

        tk.Button(self.root, text="Start", command=self.start, font=FONT).grid(row=5, column=0, columnspan=2)
        
        tk.Button(self.root, text="Stop", command=self.stop, font=FONT).grid(row=6, column=0, columnspan=2)

        self.output = tk.scrolledtext.ScrolledText(self.root, width = 100, height = 30, font=("Arial", 12))
        self.output.grid(row=0, column=2, rowspan=7)
        self.output.config(state="disabled")

    def start(self):
        n = int(self.n_entry.get())
        population_size = int(self.population_entry.get())
        generations = int(self.generations_entry.get())
        mutation_rate = float(self.mutation_rate_entry.get())
        accuracy = int(self.accuracy_entry.get())
        self.genetic = Genetic(n=n, population_size=population_size,  generations=generations, mutation_rate=mutation_rate, accuracy=accuracy, reach=None, fitness_mode=2)
        self.thread = threading.Thread(target=self.run_genetic, daemon=True)
        self.thread.start()

    def run_genetic(self):
        for msg in self.genetic.run():
            self.append_output(msg)

    def append_output(self, msg):
        self.output.config(state="normal")
        self.output.insert("end", msg + "\n")
        self.output.see("end")
        self.output.config(state="disabled")

    def stop(self):
        if self.genetic:
            self.genetic.stop()

