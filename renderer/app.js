class Drawer {
	constructor(canvas, ctx) {
		this.canvas = canvas;
		this.ctx = ctx;
	}

	drawGlyph(glyph, x=0, y=0, angle=0) {
		let baseTransform = this.ctx.getTransform();
		this.ctx.translate(x, y);
		this.ctx.rotate(angle);

		glyph.lineCoordinates().forEach((coords) => {
			this.ctx.beginPath();
	    this.ctx.moveTo(coords[0][0], coords[0][1]);
	    this.ctx.lineTo(coords[1][0], coords[1][1]);
	    this.ctx.stroke();
		});
    glyph.bezierCoordinates().forEach((coords) => {
      this.ctx.beginPath();
      this.ctx.moveTo(coords[0][0], coords[0][1]);
      this.ctx.bezierCurveTo(coords[1][0], coords[1][1],
                             coords[2][0], coords[2][1],
                             coords[3][0], coords[3][1]);
      this.ctx.stroke();
    });
    
		this.ctx.setTransform(baseTransform);
	}
}

class App {
	constructor(params) {
		// crude.  will be replaced when we start on the sentence level
		this.glyphs = params.glyphs || [];

		this.setupDrawing(params)

    this.glyphs.forEach((garray) => {
      this.drawer.drawGlyph(garray[0], garray[1] || 0, garray[2] || 0, garray[3] || 0);

    });
	}

	setupDrawing(params) {
		this.canvas = params.canvas_element || document.getElementById("board").firstElementChild;
		this.ctx = this.canvas.getContext("2d", {
			alpha: false,
			desynchronized: true,
			powerPreference: "high-performance",
			failIfMajorPerformanceCaveat: true,
			antialias: params.antialias || false
		});

		this.resetCanvas(params.emSize || 48);
		this.drawer = new Drawer(this.canvas, this.ctx);

		this.ctx.strokeStyle = params.strokeStyle || '#153360';
		this.ctx.lineWidth = params.lineWidth || 1/12;
	}

	resetCanvas(emSize) {
		// HiDPI canvas adapted from http://www.html5rocks.com/en/tutorials/canvas/hidpi/
		const devicePixelRatio = window.devicePixelRatio || 1;
		this.canvas.width = window.innerWidth*devicePixelRatio;
		this.canvas.height = window.innerHeight*devicePixelRatio;
		this.canvas.style.width = window.innerWidth + 'px';
		this.canvas.style.height = window.innerHeight + 'px';
    // put the origin at centre
    this.ctx.translate(this.canvas.width/2, this.canvas.height/2);
    // use the "em" as unit.
		// This is our analogue of font size for glyphs.
		this.ctx.scale(devicePixelRatio * emSize, devicePixelRatio * emSize);
	}
}
