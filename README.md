# PyRoll Engine

PyRoll Engine is a simple payroll calculator application with a desktop GUI built using Tkinter. It supports salary calculations with hours worked, hourly rate, deductions, tax rate, and bonus. The app uses Redis as the primary data store and provides an in-memory fallback when Redis is not available.

## Features

- Employee salary calculation
- Tax and bonus support
- Save employee records to Redis
- View saved employee list
- Dummy initial data for demonstration
- Redis fallback mode when Redis is unavailable

## Project Structure

- `main.py` — application entry point
- `src/engine/` — payroll calculation logic
- `src/ui/` — user interface implementation
- `src/database/` — data storage and Redis integration

## Prerequisites

- Python 3.10 or later
- `pip`
- Redis server on `localhost:6379` (recommended)
- Optional: Memurai on Windows or Redis via WSL if native Redis is not installed

## Installation

### 1. Install Python

Install Python from the official website or package manager:

- Windows: https://www.python.org/downloads/
- macOS: `brew install python` or download from python.org
- Linux: `sudo apt install python3 python3-pip`

### 2. Install dependencies

From the project root:

```bash
pip install -r requirements.txt
```

If you want to use a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Install Redis

#### Windows

Recommended: install Memurai Community Edition or another Redis-compatible Windows server. Start the service and ensure it listens on `localhost:6379`.

Alternative: use WSL/Ubuntu and install Redis there.

#### macOS

```bash
brew install redis
brew services start redis
```

#### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### 4. Run the application

From the project root:

```bash
python main.py
```

## Notes

- The app uses Redis if available. If Redis is not running, it falls back to in-memory storage and still runs.
- Dummy employee data is loaded on first run.
- `requirements.txt` currently includes `redis`.

## Troubleshooting

- If the app cannot connect to Redis, make sure Redis or Memurai is running on `localhost:6379`.
- For Windows, verify the Redis service is active in Services or Memurai UI.
- If you see `ConnectionRefusedError`, start Redis and rerun the app.