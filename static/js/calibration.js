let canvas = document.getElementById("myCanvas");

let width = window.innerWidth
let height = window.innerHeight

canvas.width = width;
canvas.height = height;

const ctx = canvas.getContext("2d");

window.addEventListener('resize', () => {
    width = window.innerWidth
    height = window.innerHeight

    canvas.width = width;
    canvas.height = height;

    arucoImageDraw()
})


function arucoImageDraw() {
    const img_0 = new Image();
    const img_1 = new Image();
    const img_2 = new Image();
    const img_3 = new Image();

    img_0.src = './static/ArucoMarkers/marker_0.png';
    img_1.src = './static/ArucoMarkers/marker_1.png';
    img_2.src = './static/ArucoMarkers/marker_2.png';
    img_3.src = './static/ArucoMarkers/marker_3.png';

    img_0.onload = () => ctx.drawImage(img_0, 10, 10)
    img_1.onload = () => ctx.drawImage(img_1, width - 210, 10)
    img_2.onload = () => ctx.drawImage(img_2, width - 210, height - 210)
    img_3.onload = () => ctx.drawImage(img_3, 10, height - 210)
}

arucoImageDraw()
