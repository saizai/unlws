import xml.dom.minidom as minidom
from canvas import XMLCanvas
import main

document = minidom.getDOMImplementation().createDocument("https://www.w3.org/1999/xhtml/", "html", None) # TODO: add doctype

# TODO: add style, encoding etc.
# (Should this be done some other way? Maybe making a template HTML file and using that for both ./index.html and this?)

html = document.childNodes[0] # TODO: bad style?
body = html.appendChild(document.createElement("body"))

canvas_div = document.createElement("div")
body.appendChild(canvas_div)
canvas = XMLCanvas(canvas_div)

body.appendChild(document.createElement("hr"))

def append_text(text):
    node = document.createTextNode(text)
    body.appendChild(node)

main.main(canvas=canvas, append_text=append_text)

with open("output.html", mode="w", encoding="utf-8") as output:
    output.write(document.toprettyxml())

# TODO: somehow automatically open and/or refresh the file? opening it is still a bit of a hassle
