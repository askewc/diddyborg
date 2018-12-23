const webCamImage = document.getElementById('web-cam');
let axes = undefined;

function update() {
    if (axes) {
        webCamImage.onload = undefined;

        fetch('api/move', {
            method: 'POST',
            cache: 'no-cache',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(axes),
        }).then(() => {
            webCamImage.onload = update;
            requestAnimationFrame(() => webCamImage.src = 'cam.jpg?cache_buster=' + Date.now());
        });
    }
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
    if (axes) fetch('api/stop');

    console.log('Gamepad disconnected!');
    axes = undefined;
});

update();
