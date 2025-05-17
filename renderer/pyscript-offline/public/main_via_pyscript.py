from pyscript import document
from canvas import HTMLDOMCanvas
from main import Main

board_div = document.body.querySelector("#svgboard")

# Create a subclass with the necessary methods for using Main through Pyscript
class Main_Via_Pyscript(Main):
  def append_canvas(self):
    sub_board = document.createElement("div")
    board_div.append(sub_board)
    canvas = HTMLDOMCanvas(sub_board)
    canvas.parent = sub_board
    return canvas

  def append_text(self, container, text):
    p = document.createElement("p")
    p.innerText = text
    container.appendChild(p)
    p.parent = container
    return p

main_obj = Main_Via_Pyscript(document)

main_obj.main() # Finally call the main method