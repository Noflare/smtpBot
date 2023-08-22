import asyncio
from aiosmtpd.controller import Controller
from email import message_from_bytes
import re
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

latest_link = ""

class MailHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        # ... (votre code de gestion des emails)
        pass

    async def handle_DATA(self, server, session, envelope):
        plain_text_part = None
        email_message = message_from_bytes(envelope.content)
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                plain_text_part = part.get_payload(decode=True).decode('utf-8')
                break

        if plain_text_part:
            # Extract links using regular expression
            links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', plain_text_part)

            if links:
                global latest_link
                latest_link = links[-1]  # Update with the latest link
                socketio.emit('latest_link', {"latest_link": latest_link})

        print()
        print('End of message')
        return '250 Message accepted for delivery'

controller = Controller(MailHandler(), hostname='10.0.0.4', port=25)
controller.start()
asyncio.get_event_loop().run_forever()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('latest_link', {"latest_link": latest_link})

if __name__ == '__main__':
    socketio.run(app, host='10.0.0.4', port=5000)
