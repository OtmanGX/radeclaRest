from core.models import *
import csv


def export_membres_toexcel():
    membres = Membre.objects.values()
    with open('file.csv', 'w') as csvfile:
        fieldnames = list(membres[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        writer.writerows(membres)
# write()