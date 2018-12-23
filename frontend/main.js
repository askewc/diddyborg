const webCamImage = document.getElementById('web-cam');

function update() {
    webCamImage.src = 'cam.jpg?cache_buster=' + Date.now();
    requestAnimationFrame(update);
}

update();