import xml.dom.minidom as minidom
from canvas import XMLCanvas
from main import Main

document = minidom.getDOMImplementation().createDocument("https://www.w3.org/1999/xhtml/", "html", None) # TODO: add doctype

# TODO: add style, encoding etc.
# (Should this be done some other way? Maybe making a template HTML file and using that for both ./index.html and this?)

html = document.childNodes[0] # TODO: bad style?
body = html.appendChild(document.createElement("body"))

board_div = document.createElement("div")
body.appendChild(board_div)

body.appendChild(document.createElement("hr"))

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
