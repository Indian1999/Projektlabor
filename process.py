from cubesolver import CubeSolver
import os
import threading

class Process:
    def __init__(self, solver: CubeSolver, priority = 0):
        self.solver = solver
        self.running = False
        self.finished = False
        self.priority = priority
        self.on_terminate: function = None 
        self.thread = threading.Thread(target=self.run_solver, daemon=True)
        self.thread.start()
        path = os.path.join(os.path.dirname(__file__))
        os.makedirs(os.path.join(path, "output_logs"), exist_ok=True)
        filename = "Process_" + self.solver.get_params_string() + ".txt"
        path = os.path.join(path, "output_logs", filename)
        self.file = open(path, "w", encoding="utf-8")

    def to_json(self):
        return self.solver.to_json()

    def run_solver(self):
        for msg in self.solver.run():
            self.file.write(msg + "\n")
        self.terminate()

    def pause(self):
        self.solver.pause()
        self.running = False
    
    def resume(self):
        self.solver.resume()
        self.running = True

    def terminate(self): 
        """Terminates the process"""
        self.solver.stop()
        self.running = False
        self.finished = True
        self.file.close()
        self.on_terminate(self)





