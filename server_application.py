import os
import json
from process import Process
import time

class ServerApplication():
    def __init__(self):
        self.results = []
        self.processes = []
        self.active_process_index = None
        self.log("Server started")

    def __del__(self):
        self.log("Server stopped")

    def log(self, message: str):
        with open("server_log.txt", "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+f" {message}\n")

    def add_process(self, process: Process, start_immediately: bool = False):
        process.on_terminate = self.on_terminate
        self.processes.append(process)
        if start_immediately:
            if self.active_process_index is not None:
                self.processes[self.active_process_index].pause()
            self.active_process_index = len(self.processes) - 1
            self.processes[self.active_process_index].resume()
        self.log(f"Process {process.solver.get_params_string()} added, immedietly: {start_immediately}, priority: {process.priority}")

    def get_processes(self, format = None):
        """
        Retrieve processes in the specified format.

        Args:
            format (str, optional): The desired output format. If set to "json", 
                returns a list of process objects serialized to JSON format. 
                Defaults to None, which returns the raw process objects.

        Returns:
            list: If format is "json", returns a list of dictionaries containing 
                JSON-serialized process data. Otherwise, returns the list of 
                process objects directly.
        """
        if format == "json":
            processes = []
            for process in self.processes:
                processes.append(process.to_json())
            return processes
        else:
            return self.processes

    def change_active_process(self, index: int):
        if self.active_process_index:
            self.processes[self.active_process_index].pause()
        self.active_process_index = index
        self.processes[self.active_process_index].resume()
        self.log(f" Active process changed to {index} index.")

    def highest_priority_process_index(self):
        highest = 0
        for i in range(1, len(self.processes)):
            if self.processes[i].priority > self.processes[highest].priority:
                highest = i
        return highest

    def on_terminate(self, process: Process):
        self.log(f"Process {process.solver.get_params_string()} terminated")
        self.results.extend(process.solver.results)
        self.processes.remove(process)
        if len(self.processes) != 0:
            self.active_process_index = self.highest_priority_process_index()
            self.processes[self.active_process_index].resume()
            self.log(f"Active process changed to {self.active_process_index} index.")
        else:
            self.active_process_index = None
            self.log("No active process.")


    def terminate_process(self, index: int):
        self.log_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+f" Process {self.processes[index].solver.get_params_string()} terminated\n")
        self.processes[index].terminate()

    def get_best_space(self, n:int):
        best = None
        for result in self.results:
            if result["n"] == n:
                if best == None or result["result"] > best["result"]:
                    best = result
        return best

    def load_results(self):
        self.log("Loading results")
        results = os.listdir("results")
        for dir in results:
            spaces = os.listdir(os.path.join("results", dir, "spaces"))
            for space in spaces:
                path = os.path.join("results", dir, "spaces", space)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.results.append(data)
                self.log(f" Loaded space from {path}")
        self.log(f"Loaded {len(self.results)} results in total")