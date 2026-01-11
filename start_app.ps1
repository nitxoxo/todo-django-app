# Navigate to your project directory (adjust if needed)
cd "C:\Users\avija\todo_site"

# Activate virtual environment
& "C:\Users\avija\todoproject\myenv\Scripts\Activate.ps1"

# Start Django server in the background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python manage.py runserver"

# Wait a few seconds to ensure server is up
Start-Sleep -Seconds 5

# Start ngrok tunnel
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http 8000"
