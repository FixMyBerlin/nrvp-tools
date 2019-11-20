#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
 
def needs_layer(data, lname, experiment):
    layer_info = lname.split("_", 5)
    try:
        layer_experiment  = layer_info[0]
        layer_base  = layer_info[1]
        layer_perspective  = layer_info[2]
    except IndexError:
        layer_experiment  = experiment
        layer_base  = data["Basisszenario"]
        layer_perspective  = data["Kamera"]

    if data["Kamera"] != layer_perspective:
        return False

    if data["Basisszenario"] != layer_base:
        return False

    if experiment != layer_experiment:
        return False

    # Aufpflasterung
    if "TrLi_Aufpflasterung" in lname and "Breit" in lname:
        rv = data["Tr_li-Breite"] == "breit" and data["Tr_li-Art"] == "Aufpflasterung"
        return rv
    
    if "TrLi_Aufpflasterung" in lname and "Schmal" in lname:
        rv = (data["Tr_li-Breite"] == "schmal" and data["Tr_li-Art"] == "Aufpflasterung")
        return rv
    
    if "TrRe_Aufpflasterung" in lname and "Breit" in lname:
        rv = data["Tr_re-Breite"] == "breit" and data["Tr_re-Art"] == "Aufpflasterung"
        return rv
    
    if "TrRe_Aufpflasterung" in lname and "Schmal" in lname:
        rv = data["Tr_re-Breite"] == "schmal" and data["Tr_re-Art"] == "Aufpflasterung"
        return rv

    # Grünfläche und Grasfläche

    if "TrLi_Gruenstreifen" in lname and "Breit" in lname:
        rv = data["Tr_li-Breite"] == "breit" and data["Tr_li-Art"] == "Gruenstreifen"
        return rv
    
    if "TrLi_Gruenstreifen" in lname and "Schmal" in lname:
        rv = data["Tr_li-Breite"] == "schmal" and data["Tr_li-Art"] == "Gruenstreifen"
        return rv
    
    if "TrRe_Gruenstreifen" in lname and "Breit" in lname:
        rv = data["Tr_re-Breite"] == "breit" and data["Tr_re-Art"] == "Gruenstreifen"
        return rv
    
    if "TrRe_Gruenstreifen" in lname and "Schmal" in lname:
        rv = data["Tr_re-Breite"] == "schmal" and data["Tr_re-Art"] == "Gruenstreifen"
        return rv

    # Hecke

    if "TrLi_Hecke" in lname:
        rv = data["Links_RVA"] == "Gruenanlage"
        return rv

    if data["SceneID"].endswith("A_258"):
        print(lname)

    if "TrRe_Hecke" in lname:
        # print(lname, data["Haeuserfront"])
        rv = data["Haeuserfront"] == "Gruenanlage"
        if rv:
            print(data["SceneID"])
        return rv



    # Poller

    # Auslage

    return False