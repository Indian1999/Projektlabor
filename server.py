from server_application import ServerApplication
from fastapi import FastAPI
from pydantic import BaseModel
from genetic import Genetic
from process import Process

class GeneticProcessItem(BaseModel):
    n:int
    population_size:int
    generations:int
    mutation_rate:float
    accuracy: int
    reach:float = None
    fitness_mode:int = None
    priority:int = 0


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
    process = Process(genetic, process.priority)
    server_app.add_process(process)