from server_application import ServerApplication
from fastapi import FastAPI

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