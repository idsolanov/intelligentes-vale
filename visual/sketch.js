const ROWS = 25;
const COLS = 25;
const LENGTH = 25;
let quadrille;
let row0, col0, row1, col1, row2, col2;
let v0color, v1color, v2color;

function setup() {
  createCanvas(COLS * LENGTH, ROWS * LENGTH);
  quadrille = createQuadrille(25, 25);
  v0color = createColorPicker(color('yellow'));
  v1color = createColorPicker(color('fuchsia'));
  v2color = createColorPicker(color('cyan'));
  v0color.position(410, 580);
  v1color.position(480, 580);
  v2color.position(550, 580);
  v0color.input(() => { quadrille.colorizeTriangle(row0, col0, row1, col1, row2, col2, v0color.color(), v1color.color(), v2color.color()) });
  v1color.input(() => { quadrille.colorizeTriangle(row0, col0, row1, col1, row2, col2, v0color.color(), v1color.color(), v2color.color()) });
  v2color.input(() => { quadrille.colorizeTriangle(row0, col0, row1, col1, row2, col2, v0color.color(), v1color.color(), v2color.color()) });
  rdm();
}

function draw() {
  background('white');
  drawQuadrille(quadrille, { cellLength: LENGTH, outlineWeight: 1, outline: 'blue', board: true });
  bdt();
}

function bdt() {
  push();
  stroke('black');
  strokeWeight(3);
  noFill();
  triangle(col0 * LENGTH + LENGTH / 2, row0 * LENGTH + LENGTH / 2, col1 * LENGTH + LENGTH / 2, row1 * LENGTH + LENGTH / 2, col2 * LENGTH + LENGTH / 2, row2 * LENGTH + LENGTH / 2);
  pop();
}

function keyPressed() {
  rdm();
}

function rdm() {
  row0 = int(random(0, ROWS));
  col0 = int(random(0, COLS));
  row1 = int(random(0, ROWS));
  col1 = int(random(0, COLS));
  row2 = int(random(0, ROWS));
  col2 = int(random(0, COLS));
  quadrille.clear();
  quadrille.colorizeTriangle(row0, col0, row1, col1, row2, col2, v0color.color(), v1color.color(), v2color.color());
}