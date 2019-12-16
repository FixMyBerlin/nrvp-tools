def translate_from_heiko_to_reality(heiko):
    return {
        "SR": "CP",
        "HVS": "MS",
        "NVS": "SE"
    }[heiko]

def check_base_data(data, lname, experiment):
    # if lname == "HVS_01_C__0006_Basis.png":
    #     import pdb; pdb.set_trace()

    if lname.endswith("raus.png"):
        return False

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

    if int(data["Basisszenario"]) != int(layer_base):
        return False

    if experiment != layer_experiment:
        return False
        
    return True