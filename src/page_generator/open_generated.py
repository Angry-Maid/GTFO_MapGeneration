
import webbrowser
from PIL.Image import tempfile

def open_generated_svg(svg: str):
    # Create a temporary SVG file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".svg")
    tmp.write(svg.encode("utf-8"))
    tmp.close()

    # Open it in the default web browser
    webbrowser.open("file://" + tmp.name)
