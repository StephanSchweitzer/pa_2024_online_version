# Start the Python script in a new screen session
screen -dmS python_session bash -c 'python3 discord_bot.py > python_output.log 2>&1'

# Save the screen session name
echo "python_session" > python_screen_name.txt

echo "Python script started."