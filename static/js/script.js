//=nb
const canvas = document.getElementById('canvas');
canvas.width = 28;
canvas.height = 28;
const ctx = canvas.getContext("2d");
const btn = document.getElementById("btn");
ctx.fillStyle = 'white';
ctx.fillRect(0, 0, canvas.width, canvas.height);

let drawColor = 'black';
let drawWidth = "6";
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

function reshape_image(data){    
   let row =  0;
   let image = [];
   for(let i = 0; i < 28; i++){
        rowData = data.slice(row,  row+(28*4));
        row += 28*4;
        let col = 0;
        let column = [];
        for(let i = 0; i < 28; i++){
            colData = rowData.slice(col, col + 4);
            col += 4;
            column.push(colData.reduce((acc, curr) => acc + curr, 0)/ 4);
        }
        image.push(column);
    }
    return image;
}
let g = document.getElementById("a");
function save(event) {
    let res = "";
    const data = ctx.getImageData(0,0,canvas.width, canvas.height);
    const send = fetch('/api/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: Array.from(reshape_image(data.data))
        }),
    }).then(Response => Response.json())
    .then(data => g.innerHTML = data.response)
    .catch(error =>  console.error("Error", error)
    )
}
