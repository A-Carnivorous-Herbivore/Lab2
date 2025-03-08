document.onkeydown = updateKey;
document.onkeyup = resetKey;

var wifi_server_port = 65432;
var wifi_server_addr = "192.168.1.47"; // The IP address of your Raspberry Pi

function bluetoothClient() {
    console.log("Spawning Bluetooth client process");

    const { spawn } = require('child_process');    
    ls = spawn('python',['bt_client.py']);

    ls.stdout.on('data', function (data) {

        console.log(data.toString());
        
        const carStats = JSON.parse(data.toString());
        document.getElementById("speed").innerHTML = carStats.carSpeed.toString();
        document.getElementById("turning").innerHTML = carStats.turning.toString();
        document.getElementById("cpu-temp").innerHTML = carStats.cpuTemp.toString();
    });
}

function client(command) {
    const net = require('net');

    const client = net.createConnection({ port: wifi_server_port, host: wifi_server_addr }, () => {
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

bluetoothClient();

function updateKey(e) {
    e = e || window.event;
        
    if (e.keyCode == '87' || e.keyCode == '38') { // 'W' key or Up Arrow
      document.querySelector("#upArrow span").style.color = "green";
      client("FORWARD");
    } else if (e.keyCode == '83' || e.keyCode == '40') { // 'S' key or Down Arrow
      document.querySelector("#downArrow span").style.color = "green";
      client("BACKWARD");
    } else if (e.keyCode == '65' || e.keyCode == '37') { // 'A' key or Left Arrow
      document.querySelector("#leftArrow span").style.color = "green";
      client("LEFT");
    } else if (e.keyCode == '68' || e.keyCode == '39') { // 'D' key or Right Arrow
      document.querySelector("#rightArrow span").style.color = "green";
      client("RIGHT");
    }
  }
  
  function resetKey(e) {
    e = e || window.event;
    
    // Reset all arrows to their original color
    document.querySelector("#upArrow span").style.color = "#333";
    document.querySelector("#downArrow span").style.color = "#333";
    document.querySelector("#leftArrow span").style.color = "#333";
    document.querySelector("#rightArrow span").style.color = "#333";
    
    client("STOP");
  } 


