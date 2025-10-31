from cubesolver import CubeSolver
import threading

class Process:
    def __init__(self, solver: CubeSolver):
        self.solver = solver
        self.running = False
        self.finished = False
        self.pause_event = threading.Event()
        self.pause_event.clear()

    def pause(self):
        self.running = False
        self.pause_event.clear() 

    def resume(self):
        self.pause_event.set()

    def terminate(self): 
        """Terminates the process"""
        self.solver.stop()
        self.running = False
        self.finished = True





