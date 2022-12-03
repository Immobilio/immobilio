import json
import random
import sys



# Read the dataset
with open("datasetHouses.json", "r") as f:
    data = json.loads(f.read())

# Initiliate false max/min possible value
min_price = sys.float_info.max
max_price = 0

# loop to get the max and min price from the dataset
for price in data:
    if price["price"] > max_price:
        max_price = price["price"]
    if price["price"] < min_price:
        min_price = price["price"]

# get the range between the real and our limit ([80000.. 300000])
leftSpan = 300000 - 80000
rightSpan = max_price - min_price

programs = []
programe_names= []

# Basic loop to refine house informations
for iter in range(10):

    program = {
        "name":f"Coralio-Immobilier {len(programs)}",
        "state": random.choice([False, True]),
        "buildings": []
    }
    #each programme contains 20 immobilier
    for house in data[iter * 20:iter * 20+20]:

        valueScaled = float(house["price"] - min_price) / float(rightSpan)
        immo = {
            "surface": house["area"] / 10  if len(str(house["area"])) > 3 else house["area"],
            "prix": 80000 + (valueScaled * leftSpan),
            "nb_pieces": house["bedrooms"],
            "caracteristic": []
        }

        caracteristic = ["proche station ski", "piscine", "jardin", "cave", "parking", "concierge", "proche magasin"]
        immo["caracteristic"].append(random.choices(caracteristic, k=1)[0])
        caracteristic.remove(immo["caracteristic"][0])
        immo["caracteristic"].append(random.choices(caracteristic, k=1)[0])

        program["buildings"].append(immo)        

    programs.append(program)
    


for program in programs:
    # assert if each program contains 20 buildins
    assert len(program["buildings"]) == 20
    # assert if all prices are between 80000..300000
    for buildings in program["buildings"]:
        assert buildings["prix"] <= 300000
        assert buildings["prix"] >= 80000


# Save the refined information into a jsonfile
with open("sample.json", "w") as writer:
    writer.write(json.dumps(programs))
