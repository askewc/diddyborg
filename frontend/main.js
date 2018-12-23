const webCamImage = document.getElementById('web-cam');
let connected = false;

function updateWebCamImage() {
    webCamImage.src = 'cam.jpg?cache_buster=' + Date.now();
    requestAnimationFrame(updateWebCamImage);
}

let previousLeft = 0;
let previousRight = 0;

function moveRobot() {
    if (connected) {
        const gamepad = navigator.getGamepads()[0];
        const left = Math.round(100 * gamepad.axes[1]) / 100;
        const right = Math.round(100 * gamepad.axes[3]) / 100;

        if (previousLeft !== left || previousRight !== right) {
            console.log(left, gamepad.axes[1], right, gamepad.axes[3]);
        }
    }

    requestAnimationFrame(moveRobot);
}

window.addEventListener('gamepadconnected', (e) => {
    console.log('Gamepad connected!');

    connected = true;
});


window.addEventListener('gamepaddisconnected', (e) => {
    console.log('Gamepad disconnected!');
    connected = false;
});

updateWebCamImage();
moveRobot();