const webCamImage = document.getElementById('web-cam');

function updateWebCamImage() {
    webCamImage.src = 'cam.jpg?cache_buster=' + Date.now();
    requestAnimationFrame(updateWebCamImage)
}

updateWebCamImage();
