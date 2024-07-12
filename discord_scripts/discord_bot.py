import discord
import os
import json
import time
from websocket import WebSocketApp, WebSocket
from dotenv import load_dotenv, dotenv_values

# Set the WebSocket URL to the server's address
bot_url = "wss://deepwoke.com/ws"

# Function to connect to the WebSocket
def connect_to_websocket():
    global ws
    try:
        ws = WebSocketApp(bot_url,
                          on_message=on_message,
                          on_error=on_error,
                          on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
    except Exception as e:
        print(f"WebSocket connection failed: {e}")
        time.sleep(5)
        connect_to_websocket()

# WebSocket event handlers
def on_open(ws):
    print("WebSocket connection opened")

def on_message(ws, message):
    print("Received message from server:", message)

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed. Reconnecting...")
    time.sleep(5)
    connect_to_websocket()

def send_to_websocket(message):
    message_data = {
        "type": "inbound",
        "id": str(message.id),
        "text": str(message.content),
        "user": str(message.author),
        "is_hateful": 0
    }
    try:
        ws.send(json.dumps(message_data))
    except Exception as e:
        print(f"Failed to send message: {e}")
        connect_to_websocket()

# Load environment variables
load_dotenv()
token = os.getenv("DISCORD_API")

# Initialize WebSocket connection
ws = WebSocket()
ws.connect(bot_url)

# Set up Discord client with all intents
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Discord event handlers
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.author)
    print(message.content)
    send_to_websocket(message)

# Run the Discord client
client.run(token)
