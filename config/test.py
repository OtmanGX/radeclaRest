# from core.models import *
import csv
import json


# def export_membres_toexcel():
#     membres = Membre.objects.values()
#     with open('file.csv', 'w') as csvfile:
#         fieldnames = list(membres[0].keys())
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
#         writer.writeheader()
#         writer.writerows(membres)


# write()

with open('config.json', 'w') as f:
    config = {'rule1': {
        'from': 17,
        'to': 23,
        'age': 30,
        'nb': 1
    }}
    f.write(json.dumps(config, indent=2))
