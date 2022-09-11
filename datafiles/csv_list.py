import csv


city_values = []
state_values = []
with open("city-state.csv",encoding="utf-8") as cityfile:
    csvreader = csv.reader(cityfile)
    header = next(csvreader)
    for row in csvreader:
        city_values.append(
            tuple((row[0],row[0]))
            )
        state_values.append(
            tuple((row[-1],row[-1]))
        )
# print(type(city_values[10][0]),city_values[10][1])
# print(state_values[10])
print(city_values[0],city_values.next())
def get_city_values():
    return city_values

def get_state_values():
    return state_values