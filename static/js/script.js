//=nb
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext("2d");
const btn = document.getElementById("btn");
ctx.fillStyle = 'white';
ctx.fillRect(0, 0, canvas.width, canvas.height);

let drawColor = 'black';
let drawWidth = "5";
let isDrawing = false;

canvas.addEventListener("touchstart", start, false);
canvas.addEventListener("touchmove", draw, false);
canvas.addEventListener("mousedown", start, false);
canvas.addEventListener("mousemove", draw, false);
canvas.addEventListener("touchend", () => isDrawing = false, false);
canvas.addEventListener("mouseup", () => isDrawing = false, false);
btn.addEventListener('click', save, false);

function start(event) {
    isDrawing = true;
    let rect = canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;
    ctx.beginPath();
    ctx.moveTo(x, y);
    event.preventDefault();
}

function draw(event){
     if(isDrawing){
        let rect = canvas.getBoundingClientRect();
        let x = event.clientX - rect.left;
        let y = event.clientY - rect.top;
        
        ctx.lineTo(x, y);
        ctx.strokeStyle = drawColor;
        ctx.linewidth = drawWidth;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.stroke();
     }    
}

function save(event) {
    const data = ctx.getImageData(0,0,canvas.width, canvas.height);
    const send = fetch('/api/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            width: canvas.width,
            height: canvas.height,
            data: Array.from(data.data)
        })
    })
}
console.log("Script loaded successfully");