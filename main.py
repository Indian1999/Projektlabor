import tkinter as tk
import threading
import time

from genetic import Genetic
from mainGUI import MainGUI




if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    app.root.mainloop()
    #genetic = Genetic(n=15, population_size=60,  generations=None,
    #                   mutation_rate=0.01, accuracy=0, reach=None)
    #genetic.run(fitness_mode=2)