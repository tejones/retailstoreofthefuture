import csv


names = []

with open('NationalNames.csv', 'r') as s:
    reader = csv.DictReader(s)
    for row in reader:
        if int(row['Year']) > 2010:
            name = row['Name']
            gender = row['Gender']
            names.append(name + "," + gender + "\n")

names = set(names)

print(names)

with open('names.txt', 'w') as t:
    t.write('name,gender\n')
    t.writelines(names)
