#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    # Hollandaise
    
    if "Aufpflasterung-Mitte" in lname:
        rv = data["besondere Merkmale"] == "Fahrradstraße-Hollandaise"
        return rv
        
    if lname.endswith("Fahrrad-Sonderzeichen.png"):
        rv = data["besondere Merkmale"] == "Fahrradstraße-Hollandaise"
        return rv
        
    if "RVA-Farbig-Ohne-Verkehr" in lname:
        rv = data["besondere Merkmale"] == "Fahrradstraße-Hollandaise"
        return rv
    
    # normal
    
    if lname.endswith("Einbahn-Gegenverkehr.png"):
        rv = (
            data["FS-Art"] == "Einbahnstraße-Gegenverkehr"
            and data["besondere Merkmale"] == "-"
        )
        return rv
        
    if lname.endswith("Einbahn.png"):
        rv = (
            data["FS-Art"] == "Einbahnstraße"
            and data["besondere Merkmale"] == "-"
        )
        return rv
        
    if lname.endswith("Fahrrad.png"):
        rv = (
            data["besondere Merkmale"] == "Fahrradstraße"
            and data["besondere Merkmale"] == "-"
        )
        return rv
        
    if lname.endswith("Gegenverkehr.png"):
        rv = (
            data["FS-Art"] == "Einbahnstraße-Gegenverkehr"
            and data["besondere Merkmale"] == "-"
        )
        return rv

  #  if "Ohne-Verkehr" in lname:
   #     rv = data["Verkehrsaufkommen"] == "autofrei"
    #    return rv
        
    if "Spiel" in lname:
        rv = data["besondere Merkmale"] == "Spielstraße"
        return rv

    # Fahrradstraße-Sondermarkierung

    if "Fahrrad-Sonderzeichen-Regulaer" in lname:
        rv = (
            data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
            and data["Verkehrsaufkommen"] == "normal"
            and data["FS-Art"] == "Kfz"
        )
        return rv
        
    if lname.endswith("Fahrrad-Sonderzeichen-Einbahn.png"):
        rv = (
            data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
            and data["Verkehrsaufkommen"] == "normal"
            and data["FS-Art"] == "Einbahnstraße"
        )
        return rv

    if "Fahrrad-Sonderzeichen-Einbahn-Gegenverkehr" in lname:
        rv = (
            data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
            and data["Verkehrsaufkommen"] == "normal"
            and data["FS-Art"] == "Einbahnstraße-Gegenverkehr"
        )
        return rv

    if "Fahrrad-Sonderzeichen-Ohne-Verkehr" in lname:
        rv = (
            data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
            and data["Verkehrsaufkommen"] == "autofrei"
        )
        return rv

    return False
