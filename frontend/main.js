const webCamImage = document.getElementById('web-cam');
let connected = false;
const MIN_X_Y = 0.1;

function updateWebCamImage() {
    webCamImage.src = 'cam.jpg?cache_buster=' + Date.now();
    requestAnimationFrame(updateWebCamImage);
}

let previousLeft = undefined;
let previousRight = undefined;

const getLeftAndRight = (x, y) => {
    let left = 0;
    let right = 0;

    if (Math.abs(x) <= MIN_X_Y && Math.abs(y) <= MIN_X_Y) return { left: left, right: right };

    const z = Math.sqrt(x * x + y * y);
    const rad = Math.acos(Math.abs(x) / z);
    const deg = rad * 180 / Math.PI;

    const turnCoefficient = -1 + (deg / 90) * 2;
    let turn = turnCoefficient * Math.abs(Math.abs(y) - Math.abs(x));
    turn = Math.round(turn * 100) / 100;

    const movement = Math.max(Math.abs(y), Math.abs(x));

    if (Math.sign(x) == Math.sign(y)) {
        left = movement;
        right = turn;
    } else {
        left = turn;
        right = movement;
    }

    left *= Math.sign(y);
    right *= Math.sign(y);

    return { left: left, right: right };
};

function move() {
    if (connected) {
        const gamepad = navigator.getGamepads()[0];
        const x = Math.round(10 * gamepad.axes[0]) / 10;
        const y = Math.round(10 * gamepad.axes[1]) / -10;

        const sides = getLeftAndRight(x, y);
        const left = sides.left;
        const right = sides.right;

        if (previousLeft !== left || previousRight !== right) {
            // noinspection JSIgnoredPromiseFromCall
            fetch('api/move', {
                method: 'POST',
                cache: 'no-cache',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(sides),
            }).then(move);

            previousLeft = left;
            previousRight = right;
        } else {
            requestAnimationFrame(move);
        }
    } else {
        requestAnimationFrame(move);
    }
}

function getStatus() {
    requestAnimationFrame(() => {
        fetch('api/distances', {
            method: 'GET',
            cache: 'no-cache',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then((response) => {
            return response.json();
        }).then((distances) => {
            const distancesElement = document.getElementById('distances');
            distancesElement.innerText = distances.toString();
            console.log(distances);
            setTimeout(getStatus, 2000);
        });
    });
}

window.addEventListener('gamepadconnected', (e) => {
    console.log('Gamepad connected!');
    connected = true;
});


window.addEventListener('gamepaddisconnected', (e) => {
    console.log('Gamepad disconnected!');
    connected = false;
});

//updateWebCamImage();
move();
//getStatus();
