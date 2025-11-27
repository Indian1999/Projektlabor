from server_application import ServerApplication
from fastapi import FastAPI
from pydantic import BaseModel
from genetic import Genetic
from typing import Optional
from process import Process

"""
This runs the FastAPI server for the Unity app specifically.
"""

class GeneticProcessItem(BaseModel):
    n:int
    population_size:int
    generations:int
    mutation_rate:float
    accuracy: Optional[int] = 0
    reach: Optional[float] = None
    fitness_mode: Optional[int] = 2
    priority: Optional[int] = 0
    start_immediately: Optional[bool] = False

app = FastAPI()

server_app = ServerApplication()
server_app.load_results()

@app.get("/")
async def root():
    return {"message": "The server is running."}

@app.get("/results/{n}")
async def get_results(n: int):
    result = server_app.get_best_space(n)
    return result

@app.post("/add_genetic_process")
async def add_process(process: GeneticProcessItem):
    genetic = Genetic(process.n, process.population_size,
                      process.generations, process.mutation_rate, process.accuracy,
                      process.reach, process.fitness_mode)
    
    server_app.add_process(Process(genetic, process.priority), 
                           start_immediately=process.start_immediately)
    
    return {"message": "Process added successfully."}
    
@app.post("/terminate_process/{index}")
async def terminate_process(index: int):
    server_app.terminate_process(index)

@app.post("/change_active_process/{index}")
async def change_active_process(index: int):
    server_app.change_active_process(index)

@app.get("/processes")
async def get_processes():
    return server_app.get_processes(format = "json")