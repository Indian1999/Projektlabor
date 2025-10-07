import json
from space import Space

path = "spaces/1990_gen_best.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
space = Space.from_json(data, accuracy=1)
value = space.n * 2
while not space.check_grid_coverage(value):
    print(value, space.delta)
    value -= space.delta
    value = round(value, space.accuracy)
print("result:",value)