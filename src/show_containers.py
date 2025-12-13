import argparse

from src.data_loading.item import load_item_svg
from src.data_loading.level import load_level
from src.mesh_handling.load_mesh import get_bounds_svg, get_bounds_svg_multi, to_svg_pos
from src.mesh_handling.svg import add_item, extract_inner_svg
from src.page_generator.open_generated import open_generated_svg


def add_text(svg, pos, bounds, text):
    (pos_x, pos_y) = pos

    try:
        item_svg = load_item_svg("text")
        inner = extract_inner_svg(item_svg)
        inner = inner.format(text=text)

        pos_x, pos_y = to_svg_pos([pos_x, pos_y], bounds[0][0], bounds[1][1])

        group = f"""
        <g transform="translate({pos_x}, {pos_y}) rotate(0)">
            {inner}
        </g>
        """

        svg = svg.replace("</svg>", group + "</svg>")
    except Exception as e:
        print(f"got error: {e}")

    return svg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("level_name")
    parser.add_argument("marker", type=str, nargs="?", default=0)

    parser.add_argument("-c", "--container-show", action="store_false", default=True, help="stop showing containers")
    parser.add_argument("-s", "--small-pickup-show", action="store_true", default=False, help="show small pickups")
    parser.add_argument("-b", "--big-pickup-show", action="store_true", default=False, help="show big pickups")

    args = parser.parse_args()
    
    level_name = args.level_name.upper()
    marker = args.marker
    
    show_containers = args.container_show
    show_small_pickups = args.small_pickup_show
    show_big_pickups = args.big_pickup_show

    level_data = load_level(level_name, marker)
    if level_data is None:
        print("Failed to load level data")
        return

    container_map = level_data["container_map"]
    small_pickups_map = level_data["small_pickups_map"]
    big_pickups_map = level_data["big_pickups_map"]

    for i in range(len(level_data["dimensions_svgs"])):
        svg = level_data["dimensions_svgs"][i][:]
        bounds = get_bounds_svg_multi(level_data["meshes"][i])

        if show_containers:
            for _, containers_in_zone in container_map.get(i, {}).items():
                for id, container in containers_in_zone.items():
                    pos = container["position"]
                    name = container["image"].split("_")[0]
    
                    svg = add_item(svg, name, pos, 0, bounds)
                    pos = (pos[0], pos[1] + 10)
                    svg = add_text(svg, pos, bounds, str(id))

        if show_small_pickups:
            for _, small_pickups_in_zone in small_pickups_map.get(i, {}).items():
                for id, pickup in small_pickups_in_zone.items():
                    pos = pickup["position"]
                    name = "small_pickup"
    
                    svg = add_item(svg, name, pos, 0, bounds)
                    pos = (pos[0], pos[1] + 10)
                    svg = add_text(svg, pos, bounds, str(id))

        if show_big_pickups:
            for _, big_pickups_in_zone in big_pickups_map.get(i, {}).items():
                for id, pickup in big_pickups_in_zone.items():
                    pos = pickup["position"]
                    name = "big_pickup"
    
                    svg = add_item(svg, name, pos, 0, bounds)
                    pos = (pos[0], pos[1] + 10)
                    svg = add_text(svg, pos, bounds, str(id))

        open_generated_svg(svg)


if __name__ == "__main__":
    main()
