const webCamImage = document.getElementById('web-cam');
let axes = undefined;

function update() {
    webCamImage.src = 'cam.jpg?cache_buster=' + Date.now();

    if (axes) {
        fetch('api/move', {
            method: 'POST',
            cache: 'no-cache',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(axes),
        }).then(response => console.log(response))
    } else {
        fetch('api/stop');
    }

    requestAnimationFrame(update);
}

window.addEventListener('gamepadconnected', (e) => {
    console.log('Gamepad connected!');

    const gamepad = navigator.getGamepads()[0];

    axes = {
        LEFT: gamepad.axes[1],
        RIGHT: gamepad.axes[3],
    };
});

window.addEventListener('gamepaddisconnected', (e) => {
    console.log('Gamepad disconnected!');

    axes = undefined;
});

update();
