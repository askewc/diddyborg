const webCamImage = document.getElementById('web-cam');
let connected = false;

function updateWebCamImage() {
    webCamImage.src = 'cam.jpg?cache_buster=' + Date.now();
    requestAnimationFrame(updateWebCamImage);
}

let previousLeft = undefined;
let previousRight = undefined;

function moveRobot() {
    if (connected) {
        const gamepad = navigator.getGamepads()[0];
        const left = Math.round(10 * gamepad.axes[1]) / -10;
        const right = Math.round(10 * gamepad.axes[3]) / -10;

        if (previousLeft !== left || previousRight !== right) {
            // noinspection JSIgnoredPromiseFromCall
            fetch('api/move', {
                method: 'POST',
                cache: 'no-cache',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    left: left,
                    right: right,
                }),
            }).then(moveRobot);

            previousLeft = left;
            previousRight = right;
        } else {
            requestAnimationFrame(moveRobot);
        }
    } else {
        requestAnimationFrame(moveRobot);
    }
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