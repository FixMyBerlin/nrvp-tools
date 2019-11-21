#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
import utils
 
def needs_layer(data, lname, experiment):
    if not utils.check_base_data(data, lname, experiment):
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