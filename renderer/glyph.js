class Glyph {
  constructor(params) {
    this.vertices = params.vertices || {};
    this.paths = params.paths || [];
  }

  lineCoordinates() {
    return this.paths.filter(
      path => path["type"] == "line"
    ).map(
      path => [this.vertices[path["from"]]["position"], this.vertices[path["to"]]["position"]]
    );
  }
}
