const express = require('express');
const http = require('http');
const fs = require('fs');
const socketIO = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

const SERVER_PORT = 3000; // Port du serveur WebSocket

io.on('connection', socket => {
    console.log('Client connected');

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

fs.watch('links.txt', (event, filename) => {
    if (event === 'change') {
        fs.readFile('links.txt', 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading links.txt:', err);
                return;
            }
            const link = data.trim();
            if (link) {
                io.emit('link', link);
            }
        });
    }
});

server.listen(SERVER_PORT, () => {
    console.log(`Server listening on port ${SERVER_PORT}`);
});
