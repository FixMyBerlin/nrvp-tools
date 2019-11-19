import csv
import os
import sys
import random
from PIL import Image, ImageOps
from collections import defaultdict
from pprint import pprint

IMAGE_SIZE = (1240, 930)
IGNORE = (".DS_Store", "Icon\r")

layers_used = set()
missing_base = set()
layer_ids = set()
layersets = defaultdict(list)

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
    image = merge_images([handles[layer] for layer in layers])
    new_fname = os.path.join("./out", sceneID + ".jpg")
    image_cropped = ImageOps.fit(image, IMAGE_SIZE, centering=(0.5, 0.5))
    image_cropped.save(new_fname, quality=60)


def needs_layer(data, lname):
    if lname.endswith("Basis.png"):
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


def get_layer_names(experiment, base, perspective):
    basepath = os.path.abspath(
        "./layers/{}/{:02d}/{}".format(experiment, int(base), perspective)
    )

    layer_names = [
        f
        for f in os.listdir(basepath)
        if f not in IGNORE and os.path.isfile(os.path.join(basepath, f))
    ]
    for layer in layer_names:
        layer_ids.add(layer.split("_", 5)[-1])

    return basepath, layer_names


def make_images(experiment, base, perspective, rows):
    total = len(rows)
    try:
        basepath, layer_names = get_layer_names(experiment, base, perspective)
    except FileNotFoundError as e:
        return

    handles = {}
    for lname in layer_names:
        try:
            handles[lname] = Image.open(os.path.join(basepath, lname))
        except FileNotFoundError as e:
            print("Error loading layer", e)
            sys.exit()

    for i, row in enumerate(rows):
        if (i + 1) % 25 == 0:
            print("{} / {}: {}".format(i + 1, total, row["SceneID"]))
        # pprint(row)
        layers = sorted(
            [lname for lname in layer_names if needs_layer(row, lname)], reverse=True
        )

        if len(layers) == 0:
            return

        for layer in layers:
            layers_used.add(layer)

        lset = frozenset(layers)
        # if lset in layersets:
        #     print(f"Layerset for Scene {row['SceneID']} already used in Scene {layersets[lset]}\n{lset}")
        layersets[lset].append(row["SceneID"])
        save_composite_image(layers, handles, row["SceneID"])

    for lname in layer_names:
        handles[lname].close()


def main():
    experiments = ["HVS", "SR"]
    for experiment in experiments:
        with open("Szenarienübersicht_{}.csv".format(experiment)) as f:
            csv_reader = csv.DictReader(f, delimiter=",")
            rows = [row for row in csv_reader]
        total = len(rows)
        scenes_grouped = defaultdict(lambda: defaultdict(list))
        for row in rows:
            scenes_grouped[row["Basisszenario"]][row["Kamera"]].append(row)

        for base in scenes_grouped.keys():
            for perspective in scenes_grouped[base].keys():
                print(
                    "\n{}\tSzenen für Experiment {}\tBasisszenario {}\tPerspektive {}".format(
                        len(scenes_grouped[base][perspective]),
                        experiment,
                        base,
                        perspective,
                    )
                )
                make_images(
                    experiment, base, perspective, scenes_grouped[base][perspective]
                )

    print("All layer ids:")
    pprint(sorted(layer_ids))
    print()

    duplicate_layer_sets = [
        lset for lset in layersets.keys() if len(layersets[lset]) > 0
    ]
    if len(duplicate_layer_sets) > 0:
        print(f"Duplicate layersets: {len(duplicate_layer_sets)}")
        # for lset in duplicate_layer_sets:
        #     print(f"Layerset: {lset}")
        #     print(f"Scenes: {', '.join(layersets[lset])}\n")

    # print(
    #     "Unused: {}".format(", ".join([l for l in layer_names if l not in layers_used]))
    # )


if __name__ == "__main__":
    main()
