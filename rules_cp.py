#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

def translate_from_heiko_to_reality(heiko):
    return {
        "SR": "CP",
        "HVS": "MS",
        "NVS": "SE"
    }[heiko]
 
def needs_layer(data, lname, experiment):
    layer_info = lname.split("_", 5)
    try:
        layer_experiment  = translate_from_heiko_to_reality(layer_info[0])
        layer_base  = layer_info[1]
        layer_perspective  = layer_info[2]
    except (IndexError, KeyError):
        layer_experiment  = experiment
        layer_base  = data["Basisszenario"]
        layer_perspective  = data["Kamera"]

    if data["Kamera"] != layer_perspective:
        return False

    if data["Basisszenario"] != layer_base:
        return False

    if experiment != layer_experiment:
        return False

    if lname.endswith("Basis.png"):
        return True

    if "Konsole" in lname:
        return data["Kamera"] == "A"

    if "Lenker" in lname:
        return data["Kamera"] == "C"

    # Aufpflasterung
    if "TrLi-Aufpflasterung-Breit" in lname:
        rv = data["Tr_li-Breite"] == "breit" and data["Tr_li-Art"] == "Aufpflasterung"
        return rv
    
    if "TrLi-Aufpflasterung-Schmal" in lname:
        rv = (data["Tr_li-Breite"] == "schmal" and data["Tr_li-Art"] == "Aufpflasterung")
        return rv
    
    if "TrRe-Aufpflasterung-Breit" in lname:
        rv = data["Tr_re-Breite"] == "breit" and data["Tr_re-Art"] == "Aufpflasterung"
        return rv
    
    if lname.endswith("Aufpflasterung-Schmal.png"):
        rv = data["Tr_re-Breite"] == "schmal" and data["Tr_re-Art"] == "Aufpflasterung"
        return rv

    if "Aufpflasterung-Schmal-Hecke" in lname:
        rv = data["Tr_re-Breite"] == "schmal" and data["Tr_re-Art"] == "Aufpflasterung"
        rv = rv and data["Haeuserfront"] == "Gruenanlage"
        return rv

    # Grünfläche und Grasfläche

    if "TrLi-Gruenstreifen-Breit" in lname:
        rv = data["Tr_li-Breite"] == "breit" and data["Tr_li-Art"] == "Gruenstreifen"
        return rv
    
    if "TrLi-Gruenstreifen-Schmal" in lname:
        rv = data["Tr_li-Breite"] == "schmal" and data["Tr_li-Art"] == "Gruenstreifen"
        return rv
    
    if "TrRe-Gruenstreifen-Breit" in lname:
        rv = data["Tr_re-Breite"] == "breit" and data["Tr_re-Art"] == "Gruenstreifen"
        return rv
    
    if "TrRe-Gruenstreifen-Schmal" in lname:
        rv = data["Tr_re-Breite"] == "schmal" and data["Tr_re-Art"] == "Gruenstreifen"
        return rv

    # Hecke

    if "TrLi-Hecke" in lname:
        rv = data["Links_RVA"] == "Gruenanlage"
        return rv

    if "TrRe-Hecke" in lname:
        rv = data["Haeuserfront"] == "Gruenanlage"
        return rv

    # Poller

    if "Poller"  in lname:
        rv = data["Tr_li_baulTrennung"] == "Sperrpfosten"
        return rv

    # Auslage

    if "Auslage" in lname:
        rv = data["GW-Geschaeftsnutzung"] == "ja"
        return rv

    return False