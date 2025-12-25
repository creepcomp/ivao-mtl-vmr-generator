import configparser
import os
from collections import defaultdict

MODELS_DIR = "./SimObjects/Airplanes"
OUTPUT_FILE = "ivaomtl.vmr"

def generate_rule(callsign, ac_type, models):
    rule = "<ModelMatchRule"
    if callsign:
        rule += f' CallsignPrefix="{callsign}"'
    rule += f' TypeCode="{ac_type}" ModelName="{models}" />\n'
    return rule

def get_callsign_prefix(texture):
    prefix = texture[1:4]
    return prefix if '"' not in prefix else ""

def generate_model_list():
    models = defaultdict(lambda: defaultdict(list))
    aircraft_count = 0
    texture_count = 0

    for aircraft in os.listdir(MODELS_DIR):
        cfg_path = f"{MODELS_DIR}/{aircraft}/aircraft.cfg"
        cfg = configparser.ConfigParser()

        try:
            cfg.read(cfg_path, encoding="utf-8")
        except Exception:
            continue

        aircraft_count += 1

        for section in cfg.sections():
            if not section.lower().startswith("fltsim"):
                continue

            ac_type = cfg[section].get("ui_type", "").strip('"')
            if not ac_type:
                continue

            title = cfg[section].get("title", "")
            title = title[1:-1] if title.startswith('"') else title

            texture = cfg[section].get("texture", "")
            callsign = get_callsign_prefix(texture)

            models[callsign][ac_type].append(title)
            texture_count += 1

    return models, aircraft_count, texture_count

def write_vmr(models):
    rule_count = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write("<ModelMatchRuleSet>\n")

        for airline in models:
            for ac_type in models[airline]:
                model_names = "//".join(
                    m for m in models[airline][ac_type] if "&" not in m
                )
                f.write(generate_rule(airline, ac_type, model_names))
                rule_count += 1

        f.write("</ModelMatchRuleSet>\n")
        f.write("<!-- Generated for IVAO MTL -->\n")

    return rule_count

print("Generating ivaomtl.vmr (this can take some time)...\n")

models, aircraft_count, texture_count = generate_model_list()
rule_count = write_vmr(models)

print(f"Aircraft folders processed: {aircraft_count}")
print(f"Textures extracted: {texture_count}")
print(f"Rules written: {rule_count}")
print(f"VMR file: {OUTPUT_FILE}")

input("\nPress Enter to exit...")
