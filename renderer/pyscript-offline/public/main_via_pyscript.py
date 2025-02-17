from pyscript import document
from canvas import HTMLDOMCanvas
import main

board = document.querySelector("#svgboard")
canvas = HTMLDOMCanvas(board)

append_text = lambda x: document.body.append(x)

main.main(canvas=canvas, append_text=append_text)