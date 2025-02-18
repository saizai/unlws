from pyscript import document
from canvas import HTMLDOMCanvas
from main import Main

board_div = document.body.querySelector("#svgboard")

def append_canvas():
  sub_board = document.createElement("div")
  board_div.append(sub_board)
  canvas = HTMLDOMCanvas(sub_board)
  canvas.parent = sub_board
  return canvas

def append_text(container, text):
  node = document.createTextNode(text)
  container.appendChild(node)

main_obj = Main(document, append_canvas, append_text)

main_obj.main()