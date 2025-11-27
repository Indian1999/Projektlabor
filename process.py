from cubesolver import CubeSolver
import os
import threading
import time

class Process:
    def __init__(self, solver: CubeSolver, priority = 0):
        self.solver = solver
        self.running = False
        self.finished = False
        self.priority = priority
        self.on_terminate: function = lambda p: None
        self.path = os.path.join(os.path.dirname(__file__), "server_log.txt")
        #os.makedirs(os.path.join(self.path, "output_logs"), exist_ok=True)
        #filename = "Process_" + self.solver.get_params_string() + ".txt"
        #self.path = os.path.join(self.path, "output_logs", filename)
        self.thread = threading.Thread(target=self.run_solver, daemon=True)
        # A konstruktorból indítás problémás -> start() feladata legyen

    def start(self):
        self.thread.start()

    def log(self, message: str):
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+f" {message}\n")

    def get_log_info(self):
        return f"""
        Priority: {self.priority}
        Running: {self.running}
        Finished: {self.finished}
        {self.solver.get_log_info()}
        """

    def to_json(self):
        return self.solver.to_json()

    def run_solver(self):
        for msg in self.solver.run():
            self.log(msg)
        self.log("Calling terminate() from run_solver()...")
        self.terminate()
        self.log("terminate() completed in run_solver()")

    def pause(self):
        self.solver.pause()
        self.running = False
    
    def resume(self):
        self.solver.resume()
        self.running = True

    def terminate(self):
        """Terminates the process"""
        self.log("Process:terminate() started")
        self.solver.stop()
        self.log("Process:terminate() - solver.stop() called")
        self.running = False
        self.finished = True
        self.log(f"Process:terminate() - About to call on_terminate callback: {self.on_terminate}")
        self.on_terminate(self)
        self.log("Process:terminate() - on_terminate callback completed")





