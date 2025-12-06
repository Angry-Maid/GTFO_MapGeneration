key_count = 0
name_dict = {
    "BulkKey": "Key0",
    "CELL": "Cell",
    "ArtifactContainer": "artifact",
    "ConsumableContainer": "consumable",
    "ArtifactWorldspawn": "artifact", 
    "ConsumableWorldspawn": "consumable"
}


def convert_name(name: str):
    global key_count

    if name.startswith("Key"):
        return f"Key{key_count}"

    if name in name_dict:
        name = name_dict[name]

    return name


def reset_keys():
    global key_count
    key_count = 0
