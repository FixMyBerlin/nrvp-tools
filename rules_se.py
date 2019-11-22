#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils


def needs_layer(data, lname, experiment):
    if not utils.check_base_data(data, lname, experiment):
        return False

    if "Konsole" in lname:
        return data["Kamera"] == "A"

    if "Lenker" in lname:
        return data["Kamera"] == "C"

     # Symbole auf Fahrbahn
        
    if lname.endswith("Fahrrad.png"):
        rv = data["besondere Merkmale"] == "Fahrradstraße"
        return rv

    if "Spiel" in lname:
        rv = data["besondere Merkmale"] == "Spielstraße"
        return rv
        
    # Basis
    
    if "Basis-Regulaer" in lname:
        rv= (
            data["FS-Art"] == "Kfz"
            and data["Verkehrsaufkommen"] == "normal"
        )
        return rv
        
        
    if "Fahrrad-Sonderzeichen-Regulaer" in lname:
        rv = (
            data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
            and data["Verkehrsaufkommen"] == "normal"
            and data["FS-Art"] == "Kfz"
        )
        return rv
        
    # Basis ohne Verkehr
    
    if "Basis-Ohne-Verkehr" in lname:
        rv = data["Verkehrsaufkommen"] == "autofrei"
        return rv 	
    
    if "Fahrrad-Sonderzeichen-Ohne-Verkehr" in lname:
        rv = (
            (data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
            and data["Verkehrsaufkommen"] == "autofrei") 
            or data["besondere Merkmale"] == "Fahrradstraße-Hollandaise"
        )
        return rv
        
    if "Aufpflasterung-Mitte" in lname:
        rv = data["besondere Merkmale"] == "Fahrradstraße-Hollandaise"
        return rv
        

    if "RVA-Farbig" in lname:
        rv = data["besondere Merkmale"] == "Fahrradstraße-Hollandaise"
        return rv
    
    # Basis Einbahn
    
    if "Basis-Einbahn" in lname:
        rv = data["FS-Art"] == "Einbahnstraße"
        return rv
        
    if "Fahrrad-Sonderzeichen-Einbahn" in lname:
        rv = (
            data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
            and data["FS-Art"] == "Einbahnstraße"
        )
        return rv
        
    # Basis Gegenverkehr
        
    if "Basis-Gegenverkehr" in lname:
        rv = data["FS-Art"] == "Einbahnstraße-Gegenverkehr"
        return rv

    if "Fahrrad-Sonderzeichen-Gegenverkehr" in lname:
        rv = (
            data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
            and data["FS-Art"] == "Einbahnstraße-Gegenverkehr"
        )
        return rv



    return False
