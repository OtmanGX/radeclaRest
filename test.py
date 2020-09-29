from core.models import *
import csv

membres = Membre.objects.values()
with open('file.csv', 'w') as csvfile:
    fieldnames = list(membres[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
    writer.writeheader()
    for membre in membres:
        writer.writerows(membres)

# write()