#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils


def needs_layer(data, lname, experiment):
    if not utils.check_base_data(data, lname, experiment):
        return False

    # Basis

    if lname.endswith("Basis.png"):
        return True

    if "Konsole" in lname:
        return data["Kamera"] == "A"

    if "Lenker" in lname:
        return data["Kamera"] == "C"

    # Tempo

    if "Tempo-30" in lname:
        return data["FS-Geschwindigkeit"] == "30"

    if "Tempo-50" in lname:
        return data["FS-Geschwindigkeit"] == "50"

    # Tram und Einbahn

    if "Einbahn" in lname:
        return data["FS-Art"] == "Einbahn"

    if "Tram" in lname:
        return data["FS-Art"] == "Tram"

    # Bauliche Trennung

    if "PollerHoch" in lname:
        return data["Tr_li-baulTrennung"] == "Sperrpfosten-hoch"

    if "PollerNiedrig" in lname:
        return data["Tr_li-baulTrennung"] == "Sperrpfosten-niedrig"

    if "Blumenkasten" in lname:
        return data["Tr_li-baulTrennung"] == "Blumenkasten"

    # Trennungen links

    if "TrLi-Schmal-Unterbrochen" in lname:
        return data["Tr_li-Markierung"] == "unterbrochen"

    if "TrLi-Schmal-Durchgezogen" in lname:
        return data["Tr_li-Markierung"] == "durchgezogen"

    if "TrLi-Breit-Doppellinie" in lname:
        return data["Tr_li-Markierung"] == "Doppellinie"

    if "TrLi-Breit-Sperrflaeche" in lname:
        return data["Tr_li-Markierung"] == "Sperrfläche"

    # Trennungen rechts

    if "TrRe-Schmal-Unterbrochen" in lname:
        return data["Tr_re-Markierung"] == "unterbrochen"

    if "TrRe-Schmal-Durchgezogen" in lname:
        return data["Tr_re-Markierung"] == "durchgezogen"

    if "TrRe-Breit-Doppellinie" in lname:
        return data["Tr_re-Markierung"] == "Doppellinie"

    if "TrRe-Breit-Sperrflaeche" in lname:
        return data["Tr_re-Markierung"] == "Sperrfläche"

    # Verkehrsaufkommen

    if "Viel-Verkehr" in lname:
        return data["FS-Aufkommen"] == "viel"

    # Oberfläche

    if "Anschraffiert" in lname:
        return data["RVA-Oberfläche"] == "Asphalt-Farbig Schraffur"

    if "RVA-Farbig-TrLi-Breit" in lname:
        return (
            data["RVA-Oberfläche"] == "Asphalt-Farbig"
            and data["Tr_li-Breite"] == "breit"
        )

    if "RVA-Farbig-TrRe-Breit" in lname:
        return (
            data["RVA-Oberfläche"] == "Asphalt-Farbig"
            and data["Tr_re-Breite"] == "breit"
        )

    if "RVA-Farbig-Tr-Schmal" in lname:
        return data["RVA-Oberfläche"] == "Asphalt-Farbig" and (
            data["Tr_re-Breite"] == "schmal" or data["Tr_li-Breite"] == "schmal"
        )

    # Radwegsymbol

    if "Radwegmarkierung" in lname:
        return True

    if "radwegsymbol-Rechts" in lname:
        return data["Tr_li-Breite"] == "breit"

    if "radwegsymbol-Mittig" in lname:
        return (data["Tr_li-Breite"] == "schmal" and data["Tr_re-Breite"] == "-") or (
            data["Tr_li-Breite"] == "-" and data["Tr_re-Breite"] == "schmal"
        )

    if "radwegsymbol-Links" in lname:
        return data["Tr_re-Breite"] == "breit"

    return False
