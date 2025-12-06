from src.data_loading.deserializer import load_data_binary
from src.mesh_handling.svg import get_svg
import trimesh

level_cache = {}


def load_level(level_name, marker):
    if (level_name, marker) in level_cache:
        return level_cache[(level_name, marker)]

    print(f"fed marker {marker}")

    loaded = load_data_binary(f"resources/levels/{level_name}_{marker}.bin")

    if loaded is None:
        loaded = load_data_binary(f"resources/levels/{level_name}_0.bin")

    if loaded is not None:
        loaded["dimensions_svgs"] = build_loaded_extra_data(loaded)

    level_cache[(level_name, marker)] = loaded
    return loaded


def show_svg(vertices, triangles):
    print(len(vertices))
    print(len(triangles))
    
    mesh = trimesh.Trimesh(vertices=vertices, faces=triangles, process=False)
    mesh.show()


def build_loaded_extra_data(loaded):
    meshes_per_dimension = loaded["meshes"]
    items_per_dimension = loaded["static_items"]

    svgs = []

    for mesh, items in zip(meshes_per_dimension, items_per_dimension):
        vertices = mesh["vertices"]
        triangles = mesh["triangles"]
        
        # show_svg(vertices, triangles)

        svg = get_svg(vertices, triangles, items)
        svgs.append(svg)

    return svgs
