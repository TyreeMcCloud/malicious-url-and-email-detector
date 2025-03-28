#!/bin/bash

# Navigate to the backend directory
cd backend || { echo "Backend directory not found"; exit 1; }

# Start the backend server
echo "Starting backend server..."
python3 -m uvicorn app:app --reload &

# Get the process ID of the backend server
BACKEND_PID=$!

# Wait a few seconds to ensure the server starts
sleep 3

# Navigate back to the project root
cd ..

# Restart Live Server (VS Code extension)
echo "Restarting Live Server..."
if pgrep -f "live-server"; then
    pkill -f "live-server"
    sleep 2
fi

# Start live server in the frontend directory
echo "Starting Live Server..."
cd frontend || { echo "Frontend directory not found"; exit 1; }
#npx live-server --port=5500 --open --root "$(pwd)" &

# Get the frontend server process ID
FRONTEND_PID=$!

# Wait for the frontend server to start
sleep 5

# Open the correct frontend URL
xdg-open http://127.0.0.1:5500/frontend/index.html 2>/dev/null || \
open http://127.0.0.1:5500/frontend/index.html 2>/dev/null || \
start http://127.0.0.1:5500/frontend/index.html 2>/dev/null

echo "Backend running on http://127.0.0.1:8000"
echo "Frontend running on http://127.0.0.1:5500/frontend/index.html"

# Cleanup processes on exit
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM
wait

