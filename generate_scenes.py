import csv
import os
import random
from PIL import Image
from pprint import pprint

IMAGE_SIZE = (1280, 720)

layer_names = ["blumenkasten", "01_MS_C__0019_Basis"]


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


def save_composite_image(layers, sceneID):
    handles = [
        Image.open(os.path.join("./layers/HVS-04_C_Test", layer + ".png"))
        for layer in reversed(layers)
    ]
    image = merge_images(handles)
    new_fname = os.path.join("./out", sceneID + ".jpg")
    image = image.resize(IMAGE_SIZE, Image.ANTIALIAS)
    image.save(new_fname, quality=60)
    for handle in handles:
        handle.close()


def needs_layer(data, lname):
    if lname.endswith("Basis"):
        return True

    if lname == "01_MS_C__0000_HVS-04-Trli-bauliTrennung-Sperrpfosten-hochB":
        if data["Tr_li-Art"] == "Aufpflasterung":
            return True

    if lname == "01_MS_C__0001_FS-Aufkommen-hochA":
        pass

    if lname == "01_MS_C__0002_FS-Aufkommen-hochB":
        pass

    if lname == "01_MS_C__0003_FS-Aufkommen-hochC":
        pass

    if lname == "01_MS_C__0004_HVS-04-Trli-bauliTrennung-Sperrpfosten-hochA":
        pass

    if lname == "01_MS_C__0005_HVS-04-Trli-Breit-Pflanzenbeete":
        pass

    if lname == "01_MS_C__0006_HVS-04-Trli-bauliTrennung-Sperrpfosten-niedrig":
        pass

    if lname == "01_MS_C__0007_TrRe__SchmalDurchgezogen":
        pass

    if lname == "01_MS_C__0008_Tempo30":
        pass

    if lname == "01_MS_C__0009_Tempo50":
        pass

    if lname == "01_MS_C__0010_HVS-04-Trli-Schmal-unterbrochen":
        pass

    if lname == "01_MS_C__0011_HVS-04-Trli-Schmal-durchgezogen":
        pass

    if lname == "01_MS_C__0012_HVS-04-Trli-Breit-Doppellinie":
        pass

    if lname == "01_MS_C__0013_HVS-04-Trli-Breit-schraffiert":
        pass

    if lname == "01_MS_C__0014_RVA-Farbig-Schraffur":
        pass

    if lname == "01_MS_C__0015_RVA-Farbig":
        pass

    if lname == "01_MS_C__0016_Kurven-1":
        pass

    if lname == "01_MS_C__0017_HVS-04-Einbahnstraße":
        pass

    if lname == "01_MS_C__0018_Kurven-1-Kopie":
        pass

    if lname == "01_MS_C__0019_Basis":
        pass

    return False


def make_images(rows):
    total = len(rows)
    for i, row in enumerate(rows):
        print("{} / {}: {}".format(i, total, row["SceneID"]))
        layers = [lname for lname in layer_names if needs_layer(row, lname)]
        save_composite_image(layers, row["SceneID"])


def main():
    with open("tabelle.csv") as f:
        csv_reader = csv.DictReader(f, delimiter=",")
        rows = [row for row in csv_reader if row["Basisszenario"] == "4"]

    make_images(rows[:10])

    # im = Image.open("")


if __name__ == "__main__":
    main()
