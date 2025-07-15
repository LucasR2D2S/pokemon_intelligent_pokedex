import csv
from .backend.database import models

def import_pokemon_from_csv(db, csv_path):
    with open(csv_path, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            pokemon = models.Pokemon(
                name=row["name"],
                type=row["type"],
                hp=int(row["hp"]),
                attack=int(row["attack"]),
                defense=int(row["defense"]),
                speed=int(row["speed"]),
                image_url=row["image_url"]
            )
            db.add(pokemon)
        db.commit()