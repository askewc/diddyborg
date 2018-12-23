const webCamImage = document.getElementById('web-cam');
let gamepad;

function updateWebCamImage() {
    webCamImage.src = 'cam.jpg?cache_buster=' + Date.now();
    requestAnimationFrame(updateWebCamImage);
}

function moveRobot() {
    if (gamepad) {
        const left = Math.round(100 * gamepad.axes[1]) / 100;
        const right = Math.round(100 * gamepad.axes[3]) / 100;
        console.log(left, right);
    }

    requestAnimationFrame(moveRobot);
}

window.addEventListener('gamepadconnected', (e) => {
    console.log('Gamepad connected!');

    gamepad = navigator.getGamepads()[0];
});


window.addEventListener('gamepaddisconnected', (e) => {
    console.log('Gamepad disconnected!');
    gamepad = undefined;
});

updateWebCamImage();
moveRobot();