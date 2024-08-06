from telethon import TelegramClient, events
from telethon.sessions import StringSession
import re
import asyncio
from flask import Flask
import threading
import os

# Your Telegram session string
session_str = os.getenv('string')

# Initialize the Telegram client
client = TelegramClient(StringSession(session_str), 28213805, '8f80142dfef1a696bee7f6ab4f6ece34')

# Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

async def send_riddle(chat_id):
    while True:
        await client.send_message(chat_id, '/riddle')
        await asyncio.sleep(10)  # Wait for 8 seconds before sending again

@client.on(events.NewMessage)
async def my_event_handler(event):
    if "Answer in 15 sec." in event.message.message:  # check if the message contains "Answer in 15 sec."
        if event.is_private:  # only respond in private messages
            message = event.message.message
            message = re.sub(r'[^\d\s\+\-\*\/]', '', message)  # remove unwanted characters
            message = message.replace(" ", "")  # remove whitespace
            message = message.replace("15", "")  # remove '15' from the message
            try:
                result = eval(message)  # evaluate the expression
                buttons = await event.get_buttons()
                for row in buttons:
                    for button in row:
                        if button.button.text == str(result):
                            # Create and start 10 tasks for clicking the button
                            tasks = [asyncio.create_task(button.click()) for _ in range(10)]
                            await asyncio.gather(*tasks)
                            break
            except SyntaxError:
                print("Invalid expression. Please check your syntax.")  # print error message to console
            except Exception as e:
                print(str(e))  # print the error message to console

@client.on(events.NewMessage)
async def respond_to_wait_message(event):
    # Check if the received message exactly matches the specific text
    if event.raw_text == "Please wait 0 seconds before starting a new riddle.":
        # Respond with the /riddle command
        await event.respond("/riddle")

@client.on(events.NewMessage)
async def respond_to_wait_message(event):
    # Check if the received message exactly matches the specific text
    if event.raw_text == "Please wait 1 seconds before starting a new riddle.":
        # Respond with the /riddle command
        await event.respond("/riddle")

@client.on(events.NewMessage)
async def respond_to_wait_message(event):
    # Check if the received message exactly matches the specific text
    if event.raw_text == "Please wait 2 seconds before starting a new riddle.":
        # Respond with the /riddle command
        await event.respond("/riddle")

@client.on(events.NewMessage)
async def respond_to_wait_message(event):
    # Check if the received message exactly matches the specific text
    if event.raw_text == "Please wait 3 seconds before starting a new riddle.":
        # Respond with the /riddle command
        await event.respond("/riddle")

async def main():
    chat_id = 'lustXcatcherrobot'  # Replace with the actual chat ID or username
    # Start the riddle sending task
    asyncio.create_task(send_riddle(chat_id))
    await client.run_until_disconnected()

def run_flask_app():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    client.start()
    client.loop.create_task(main())
    client.run_until_disconnected()
