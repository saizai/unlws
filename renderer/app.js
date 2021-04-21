class App {
	constructor(params) {
    // "font size" for glyphs
    this.emSize = params.emSize || 48;

		this.setupDrawing(params)

    // check if I got the coordinates right
    this.ctx.strokeStyle = '#153360';
    this.ctx.lineWidth = this.emSize/12;
    this.ctx.beginPath();
    this.ctx.moveTo(-this.emSize/2, 0);
    this.ctx.lineTo(this.emSize/2, 0);
    this.ctx.stroke();
	}

	setupDrawing({canvas_element, antialias=false}) {
		this.canvas = canvas_element || document.getElementById("board").firstElementChild;
		this.ctx = this.canvas.getContext("2d", {
			alpha: false,
			desynchronized: true,
			powerPreference: "high-performance",
			failIfMajorPerformanceCaveat: true,
			antialias: antialias
		});

		this.resetCanvas()
	}

	resetCanvas() {
		// HiDPI canvas adapted from http://www.html5rocks.com/en/tutorials/canvas/hidpi/
		const devicePixelRatio = window.devicePixelRatio || 1;
		this.canvas.width = window.innerWidth*devicePixelRatio;
		this.canvas.height = window.innerHeight*devicePixelRatio;
		this.canvas.style.width = window.innerWidth + 'px';
		this.canvas.style.height = window.innerHeight + 'px';
    // put the origin at centre
    this.ctx.translate(this.canvas.width/2, this.canvas.height/2);
    // use the logical pixel as unit
		this.ctx.scale(devicePixelRatio, devicePixelRatio);
	}
}
