import os
import json

class ServerApplication():
    def __init__(self):
        self.results = []

    def get_best_space(self, n:int):
        best = None
        for result in self.results:
            if result["n"] == n:
                if best == None or result["result"] > best["result"]:
                    best = result
        return best

    def load_results(self):
        results = os.listdir("results")
        for dir in results:
            spaces = os.listdir(os.path.join("results", dir, "spaces"))
            for space in spaces:
                path = os.path.join("results", dir, "spaces", space)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.results.append(data)