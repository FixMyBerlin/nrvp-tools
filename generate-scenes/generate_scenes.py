#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import sys
import random
import rules_ms
import rules_cp
import rules_se
import json
from PIL import Image, ImageOps
from collections import defaultdict
from pprint import pprint

DEBUG = False
SAVE_IMAGES = False

FNAME_SCENE_LIST = "out/KatasterKI_scene_list.csv"
IGNORE = (".DS_Store", "Icon\r")
IMAGE_SIZE = (1240, 930)

have_images = set()
have_data = set()

all_layer_names = set()
layer_ids = set()
layers_used = set()
layersets = defaultdict(list)
missing_base = set()

csv.field_size_limit(sys.maxsize)


def merge_images(images):
    rv = None
    for image in images:
        image = image.convert("RGBA")
        if rv is None:
            rv = image
        else:
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


def log_debug_info(iteration, row, total, experiment, layer_names, needs_layer):
    if iteration % 25 == 0 and DEBUG is False and SAVE_IMAGES is True:
        print("\t{} / {}: {}".format(iteration + 1, total, row["SceneID"]))
    elif DEBUG:
        print("\t{} / {}: {}".format(iteration + 1, total, row["SceneID"]))
        pprint(row)
        print("Layers:")
        for lname in sorted(layer_names):
            head = "--> " if needs_layer(row, lname, experiment) else "    "
            print(head, lname)

        # if row["Basisszenario"] != "1":
        import pdb

        pdb.set_trace()


def log_duplicate_layersets(fname):
    duplicate_layer_sets = [
        lset for lset in layersets.keys() if len(layersets[lset]) > 1
    ]
    if len(duplicate_layer_sets) > 0:
        print(f"Duplicate layersets: {len(duplicate_layer_sets)}")
        with open(fname, "w") as f:
            for lset in duplicate_layer_sets:
                f.write(f"Layerset: {', '.join(lset)}\n")
                for field in layersets[lset][0].keys():
                    val = layersets[lset][0][field]
                    for scene in layersets[lset]:
                        if scene[field] != val:
                            f.write(f"{field}:\n{scene[field]} != {val}\n\n")
                            val = scene[field]

                # for scene in layersets[lset]:
                #     f.write(json.dumps(scene, indent=2))
                f.write("\n\n")


def reset_scene_list():
    with open(FNAME_SCENE_LIST, "w") as f:
        f.write("SceneID,Weight")


def append_scene_list(sceneID, weight):
    with open(FNAME_SCENE_LIST, "a") as f:
        f.write(f"\n{sceneID},{weight}")


def make_images(experiment, base, perspective, rows):
    global have_images

    total = len(rows)
    try:
        basepath, layer_names = get_layer_names(experiment, base, perspective)
    except FileNotFoundError as e:
        return

    all_layer_names.update(layer_names)

    handles = {}
    for lname in layer_names:
        try:
            handles[lname] = Image.open(os.path.join(basepath, lname))
        except FileNotFoundError as e:
            print("Error loading layer", e)
            sys.exit()

    if experiment == "CP":
        needs_layer = rules_cp.needs_layer
    elif experiment == "MS":
        needs_layer = rules_ms.needs_layer
    elif experiment == "SE":
        needs_layer = rules_se.needs_layer
    else:
        raise Exception(f"Experiment {experiment} not defined")

    for i, row in enumerate(rows):
        layers = sorted(
            [lname for lname in layer_names if needs_layer(row, lname, experiment)],
            reverse=True,
        )

        log_debug_info(i, row, total, experiment, layer_names, needs_layer)

        layers_used.update(layers)
        layersets[frozenset(layers)].append(row)

        if SAVE_IMAGES:
            save_composite_image(layers, handles, row["SceneID"])
            append_scene_list(row["SceneID"], row["weight"])

        have_images.add(row["SceneID"])

    for lname in layer_names:
        handles[lname].close()


def main():
    global have_data

    experiments = ["MS", "CP", "SE"]

    if SAVE_IMAGES:
        reset_scene_list()
        
    for experiment in experiments:
        with open("Szenarienübersicht_{}.csv".format(experiment)) as f:
            csv_reader = csv.DictReader(f, delimiter=",")
            rows = [row for row in csv_reader]
        total = len(rows)
        scenes_grouped = defaultdict(lambda: defaultdict(list))
        for row in rows:
            scenes_grouped[row["Basisszenario"]][row["Kamera"]].append(row)
            have_data.add(row["SceneID"])

        for base in scenes_grouped.keys():
            for perspective in scenes_grouped[base].keys():
                print(
                    "{}_{}_{}  \t{} Szenen".format(
                        experiment,
                        base,
                        perspective,
                        len(scenes_grouped[base][perspective])
                    )
                )

                make_images(
                    experiment, base, perspective, scenes_grouped[base][perspective]
                )

    log_duplicate_layersets("duplicate_layersets.txt")

    print(
        "\nUnused layer names (without 'raus'):\n- {}\n".format(
            "\n- ".join(sorted([l for l in all_layer_names if (l not in layers_used and "_raus" not in l)]))
        )
    )

    print("{} / {} Szenen generiert".format(len(have_images), len(have_data)))

    missing_sids = [sid for sid in have_data if sid not in have_images]
    print("\nMissing SceneIDs:\n- {}\n".format(
        "\n- ".join(sorted(missing_sids)))
    )


if __name__ == "__main__":
    main()