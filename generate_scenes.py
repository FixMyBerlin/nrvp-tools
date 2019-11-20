#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import csv
import os
import sys
import random
import rules_hvs
import rules_sr
from PIL import Image, ImageOps
from collections import defaultdict
from pprint import pprint

IMAGE_SIZE = (1240, 930)
IGNORE = (".DS_Store", "Icon\r")
SAVE_IMAGES = False

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

    if experiment == "SR":
        needs_layer = rules_sr.needs_layer
    elif experiment == "HVS":
        needs_layer = rules_hvs.needs_layer


    for i, row in enumerate(rows):
        layers = sorted(
            [lname for lname in layer_names if needs_layer(row, lname, experiment)], reverse=True
        )

        print("{} / {}: {}".format(i + 1, total, row["SceneID"]))
        pprint(row)
        print("Layers:")
        for lname in sorted(layer_names):
            print(needs_layer(row, lname, experiment), lname)
        
        if i >= 0:
            import pdb; pdb.set_trace()

        # if len(layers) == 0:
        #     continue

        for layer in layers:
            layers_used.add(layer)

        lset = frozenset(layers)
        # if lset in layersets:
        #     print(f"Layerset for Scene {row['SceneID']} already used in Scene {layersets[lset]}\n{lset}")
        layersets[lset].append(row["SceneID"])
        if SAVE_IMAGES:
            save_composite_image(layers, handles, row["SceneID"])

    for lname in layer_names:
        handles[lname].close()


def main():
    experiments = ["SR"]
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
                if base == "01" and perspective == "C":
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
        for lset in duplicate_layer_sets:
            print(f"Layerset: {lset}")
            print(f"Scenes: {', '.join(layersets[lset])}\n")

    # print(
    #     "Unused: {}".format(", ".join([l for l in layer_names if l not in layers_used]))
    # )


if __name__ == "__main__":
    main()
