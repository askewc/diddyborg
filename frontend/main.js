const webCamImage = document.getElementById('web-cam');
let axes = undefined;

function update() {
    if (axes) {
        fetch('api/move', {
            method: 'POST',
            cache: 'no-cache',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(axes),
        }).then(() => {
            webCamImage.src = 'cam.jpg?cache_buster=' + Date.now();
            requestAnimationFrame(update);
        });
    } else {
        requestAnimationFrame(update);
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
    console.log('Gamepad disconnected!');
    axes = undefined;
    fetch('api/stop');

});

update();
