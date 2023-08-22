import asyncio
from aiosmtpd.controller import Controller
from email import message_from_bytes
import re

class MailHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address.endswith('@besavvy.fr'):
            print("Address does not end with @besavvy.fr")
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'
    
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
                with open('links.txt', 'w') as file:
                    file.write('')
                with open('links.txt', 'w') as file:
                    link = links[0]  # Only take the first link
                    print("Extracted link:")
                    print(link)
                    file.write(link)

        print()
        print('End of message')
        return '250 Message accepted for delivery'

controller = Controller(MailHandler(), hostname='10.0.0.4', port=25)
controller.start()
asyncio.get_event_loop().run_forever()
