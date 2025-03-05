document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.1.35"; // The IP address of your Raspberry Pi

function client(command) {
    const net = require('net');

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        console.log('Connected to server!');
        client.write(`${command}\r\n`); // Send command
    });

    client.on('data', (data) => {
        console.log("Response from server:", data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('Disconnected from server');
    });
}

// Detect key presses and send movement commands
function updateKey(e) {
    e = e || window.event;

    if (e.keyCode == '87' || e.keyCode == '38') { // 'W' key or Up Arrow
        document.getElementById("upArrow").style.color = "green";
        client("FORWARD");
    } else if (e.keyCode == '83' || e.keyCode == '40') { // 'S' key or Down Arrow
        document.getElementById("downArrow").style.color = "green";
        client("BACKWARD");
    } else if (e.keyCode == '65' || e.keyCode == '37') { // 'A' key or Left Arrow
        document.getElementById("leftArrow").style.color = "green";
        client("LEFT");
    } else if (e.keyCode == '68' || e.keyCode == '39') { // 'D' key or Right Arrow
        document.getElementById("rightArrow").style.color = "green";
        client("RIGHT");
    }
}

// Reset key styles when released
function resetKey(e) {
    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";

    client("STOP"); // Stop the car when the key is released
}
