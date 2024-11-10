from pyscript import document
document.body.append("Before importing... ")
from canvas import HTMLDOMCanvas
from emictext import EmicText

board = document.querySelector("#svgboard")
canvas = HTMLDOMCanvas(board)
text = EmicText() # currently has test logic in it
canvas.render(text)

#e = document.createElementNS("http://www.w3.org/2000/svg", "use")
#e.setAttribute("href", "#firstsg")
#e.setAttribute("transform", "translate(-2 0) rotate(-90)")
#board.appendChild(e)
#f = document.createElementNS("http://www.w3.org/2000/svg", "circle")
#f.setAttribute("cx", "0")
#f.setAttribute("cy", "0")
#f.setAttribute("r", "1")
#f.setAttribute("fill", "red")
#board.appendChild(f)
