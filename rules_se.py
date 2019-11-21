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

    if "Aufpflasterung-Mitte" in lname:
        rv = data["besondere Merkmale"] == "Fahrradstraße-Hollandaise"
        return rv

    if "Einbahn-Gegenverkehr" in lname:
        rv = data["FS-Art"] == "Einbahnstraße-Gegenverkehr" and data["besondere Merkmale"] == "-"
        return rv

    if "Einbahn" in lname:
        rv = data["FS-Art"] == "Einbahnstraße"
        return rv

    if lname.endswith("Fahrrad.png"):
        rv = data["besondere Merkmale"] == "Fahrradstraße"
        return rv

    if "Fahrrad-Sonderzeichen-Einbahn-Gegenverkehr" in lname:
        rv = data["FS-Art"] == "Einbahnstraße-Gegenverkehr" and data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
        return rv

    if  lname.endswith("Fahrrad-Sonderzeichen-Einbahn.png"):
        rv = data["FS-Art"] == "Einbahnstraße" and data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
        return rv

    if "Fahrrad-Sonderzeichen-Ohne-Verkehr" in lname:
        rv = data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung" and data["Verkehrsaufkommen"] == "autofrei"
        return rv

    if "Fahrrad-Sonderzeichen-Regulaer" in lname:
        rv = data["besondere Merkmale"] == 'Fahrradstraße-Sondermarkierung' and data["Verkehrsaufkommen"] == "normal"
        return rv

    if "Fahrrad-Sonderzeichen" in lname:
        rv = data["FS-Art"] == "KFZ" and data["besondere Merkmale"] == "Fahrradstraße-Sondermarkierung"
        return rv

    if "Gegenverkehr" in lname:
        rv = data["FS-Art"] == "Einbahnstraße-Gegenverkehr"
        return rv

    if "Ohne-Verkehr" in lname:
        rv = data["Verkehrsaufkommen"] == 'autofrei'
        return rv

    if "RVA-Farbig-Einbahn-Gegenverkehr" in lname:
        rv = data["besondere Merkmale"] == "Fahrradstraße-Hollandaise" and data["FS-Art"] == "Einbahnstraße-Gegenverkehr"
        return rv

    if "RVA-Farbig-Einbahn" in lname:
        rv = data["besondere Merkmale"] == "Fahrradstraße-Hollandaise" and data["FS-Art"] == "Einbahnstraße"
        return rv

    if "RVA-Farbig-Ohne-Verkehr" in lname:
        rv = data["besondere Merkmale"] == "Fahrradstraße-Hollandaise" and data["Verkehrsaufkommen"] == "autofrei"
        return rv

    if "RVA-Farbig-Regulaer" in lname:
        rv = data["besondere Merkmale"] == "Fahrradstraße-Hollandaise"  and data["Verkehrsaufkommen"] == "normal"
        return rv

    if "Spiel" in lname:
        rv = data["besondere Merkmale"] == "Spielstraße"
        return rv

        return False