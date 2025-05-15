import xml.dom.minidom as minidom
from minidom_extras import remove_whitespace_nodes
from canvas import XMLCanvas
from main import Main

document = minidom.parse("index.html")

remove_whitespace_nodes(document)

# FIXME: This assumes a pretty specific template for index.html
html = document.childNodes[1]
head = html.childNodes[0]
for node in head.childNodes: # Remove the pyscript import
  if node.nodeName == "script" and "src" in node.attributes and node.attributes["src"].value == "./pyscript/core.js":
    head.removeChild(node)
body = html.childNodes[1]
board_div = body.childNodes[0]
script_node = body.childNodes[2]
body.removeChild(script_node) # Remove the pyscript call

def append_canvas():
  sub_board = document.createElement("div")
  board_div.appendChild(sub_board)
  canvas = XMLCanvas(sub_board)
  canvas.parent = sub_board
  return canvas

def append_text(container, text):
  node = document.createTextNode(text)
  container.appendChild(node)


# Adding properties to make the minidom objects behave more like HTML DOM objects.
# This might get ugly if we want more features like this.
document.body = body


main_obj = Main(document, append_canvas, append_text)

main_obj.main()

with open("output.html", mode="w", encoding="utf-8") as output:
  pretty_output = document.toprettyxml()
  pretty_output = pretty_output.removeprefix('<?xml version="1.0" ?>\n')
  output.write(pretty_output)

# TODO: somehow automatically open and/or refresh the file? opening it is still a bit of a hassle
