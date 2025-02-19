import xml.dom.minidom as minidom
from canvas import XMLCanvas
from main import Main

document = minidom.parse("index.html")

# FIXME: This assumes a pretty specific template for index.html
# The child node indexes are n*2+1 from what you might expect, because newlines are treated as text nodes.
html = document.childNodes[1]
head = html.childNodes[1]
for node in head.childNodes: # Remove the pyscript import
  if node.nodeName == "script" and "src" in node.attributes and node.attributes["src"].value == "./pyscript/core.js":
    head.removeChild(node)
body = html.childNodes[3]
board_div = body.childNodes[1]
script_node = body.childNodes[5]
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
  output.write(document.toprettyxml())

# TODO: somehow automatically open and/or refresh the file? opening it is still a bit of a hassle
