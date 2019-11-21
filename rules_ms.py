#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
def needs_layer(data, lname, experiment):
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

    if "Auslage" in lname:
        return data["GW-Geschäftsnutzung"] == "ja"

    return False