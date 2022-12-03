const canvas = document.getElementById("myCanvas");

let width = window.innerWidth
let height =  window.innerHeight * 0.9

canvas.width = width;
canvas.height = height;

const ctx = canvas.getContext("2d");

const img_0 = new Image();      
const img_1 = new Image();      
const img_2 = new Image();      
const img_3 = new Image();

img_0.src = './static/4x4_1000-0.svg';     
img_1.src = './static/4x4_1000-1.svg';     
img_2.src = './static/4x4_1000-2.svg';     
img_3.src = './static/4x4_1000-3.svg';

img_0.onload = () => {          
    ctx.drawImage(img_0, 0, 0);        
};
img_1.onload = () => {          
    ctx.drawImage(img_1, width-377, 0);     
};
img_2.onload = () => {          
    ctx.drawImage(img_2, width-377, height-377);        
};
img_3.onload = () => {          
    ctx.drawImage(img_3, 0, height-377);        
};
