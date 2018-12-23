const webCamImage = document.getElementById('web-cam');
let axes;

function updateWebCamImage() {
    webCamImage.src = 'cam.jpg?cache_buster=' + Date.now();
    requestAnimationFrame(updateWebCamImage);
}

function moveRobot() {
    if (axes) {
        console.log(axes);
    }

    requestAnimationFrame(moveRobot);
}

window.addEventListener('gamepadconnected', (e) => {
    console.log('Gamepad connected!');

    const gamepad = navigator.getGamepads()[0];

    axes = {
        left: gamepad.axes[1],
        right: gamepad.axes[3],
    };
});


window.addEventListener('gamepaddisconnected', (e) => {
    console.log('Gamepad disconnected!');
    axes = undefined;
});

updateWebCamImage();
moveRobot();