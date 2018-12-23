const webCamImage = document.getElementById('web-cam');
let axes = undefined;

function update() {
    webCamImage.src = 'cam.jpg?cache_buster=' + Date.now();
}

webCamImage.onload = update;

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