import csv
import os
import sys
import random
from PIL import Image
from pprint import pprint

IMAGE_SIZE = (1280, 720)

layers_used = set()

layer_names = [
    "01_MS_C__0000_Lenker",
    "01_MS_C__0001_HVS-04-Trli-baulTrennung-Sperrpfosten_hoch_B",
    "01_MS_C__0002_FS-Aufkommen-hochA",
    "01_MS_C__0003_FS-Aufkommen-hochB",
    "01_MS_C__0004_FS-Aufkommen-hochC",
    "01_MS_C__0005_HVS-04-Trli-baulTrennung-Sperrpfosten_hochA",
    "01_MS_C__0006_HVS-04-Trli-Breit-Pflanzenbeete",
    "01_MS_C__0007_HVS-04-Trli-baulTrennung-Sperrpfosten-niedrig",
    "01_MS_C__0008_TrRe__SchmalDurchgezogen",
    "01_MS_C__0009_Tempo30",
    "01_MS_C__0010_Tempo50",
    "01_MS_C__0011_HVS-04-Trli-Schmal-unterbrochen",
    "01_MS_C__0012_HVS-04-Trli-Schmal-durchgezogen",
    "01_MS_C__0013_HVS-04-Trli-Breit-Doppellinie",
    "01_MS_C__0014_HVS-04-Trli-Breit-schraffiert",
    "01_MS_C__0015_RVA-Farbig-Schraffur",
    "01_MS_C__0016_RVA-Farbig_abgeschnitten (1)",
    "01_MS_C__0017_RVA-Farbig_ganz",
    "01_MS_C__0018_HVS-04-Einbahnstraße",
    "01_MS_C__0019_Basis",
]
csv.field_size_limit(sys.maxsize)


def merge_images(images):
    rv = None
    for image in images:
        image = image.convert("RGBA")
        if rv is None:
            rv = image
        else:
            # rv.paste(image, (0, 0))
            rv = Image.alpha_composite(rv, image)
    return rv.convert("RGB")


def save_composite_image(layers, handles, sceneID):
    image = merge_images([handles[layer] for layer in reversed(layers)])
    new_fname = os.path.join("./out", sceneID + ".jpg")
    image = image.resize(IMAGE_SIZE, Image.ANTIALIAS)
    image.save(new_fname, quality=60)


def needs_layer(data, lname):
    if lname.endswith("Basis"):
        return True

    if "Trli-baulTrennung-Sperrpfosten_hoch" in lname:
        return data["Tr_li-baulTrennung"] == "Sperrpfosten_hoch"

    if "Trli-baulTrennung-Sperrpfosten-niedrig" in lname:
        return data["Tr_li-baulTrennung"] == "Sperrpfosten_niedrig"

    if "FS-Aufkommen-hoch" in lname:
        return data["FS-Aufkommen"] == "hoch"

    if "Trli-Breit-Pflanzenbeete" in lname:
        return data["Tr_li-baulTrennung"] == "Blumenkasten"

    if "TrRe__SchmalDurchgezogen" in lname:
        return False

    if "Tempo30" in lname:
        return data["FS-Geschwindigkeit"] == "30"

    if "Tempo50" in lname:
        return data["FS-Geschwindigkeit"] == "50"

    if "Trli-Schmal-unterbrochen" in lname:
        return data["Tr_li-Markierung"] == "unterbrochen"

    if "Trli-Schmal-durchgezogen" in lname:
        return data["Tr_li-Markierung"] == "durchgezogen"

    if "Trli-Breit-Doppellinie" in lname:
        return data["Tr_li-Markierung"] == "Doppellinie"

    if "Trli-Breit-schraffiert" in lname:
        return data["Tr_li-Markierung"] == "Schraffiert"

    if "RVA-Farbig-Schraffur" in lname:
        return data["RVA-Oberfläche"] == "Asphalt - farbig Schraffur"

    if "RVA-Farbig_ganz" in lname:
        return (
            data["RVA-Oberfläche"] == "Asphalt - farbig"
            and data["Tr_li-Breite"] == "schmal"
        )

    if "RVA-Farbig_abgeschnitten" in lname:
        return (
            data["RVA-Oberfläche"] == "Asphalt - farbig"
            and data["Tr_li-Breite"] == "breit"
        )

    if "Einbahnstraße" in lname:
        return data["FS-Art"] == "Einbahn"

    if "Tram" in lname:
        return data["FS-Art"] == "Tram"

    if "Lenker" in lname:
        return data["Kamera"] == "C"

    return False


def make_images(rows):
    total = len(rows)
    # print(rows[0])

    handles = {}
    for lname in layer_names:
        try:
            handles[lname] = Image.open(
                os.path.join("./layers/HVS-04_C_Test", lname + ".png")
            )
        except FileNotFoundError as e:
            print("Error loading layer", e)
            sys.exit()

    for i, row in enumerate(rows):
        print("{} / {}: {}".format(i, total, row["SceneID"]))
        print(row)
        layers = [lname for lname in layer_names if needs_layer(row, lname)]
        print("\n - ".join(layers))
        for layer in layers:
            layers_used.add(layer)
        save_composite_image(layers, handles, row["SceneID"])

    for lname in layer_names:
        handles[lname].close()


def main():
    with open("Szenarienübersicht_HVS.csv") as f:
        csv_reader = csv.DictReader(f, delimiter=",")
        rows = [
            row
            for row in csv_reader
            if (row["Basisszenario"] == "4" and row["Kamera"] == "C")
        ]

    make_images(rows)

    print(
        "Unused: {}".format(", ".join([l for l in layer_names if l not in layers_used]))
    )


if __name__ == "__main__":
    main()
