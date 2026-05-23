<div align="center">

# PyRoll Engine

[![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/sha-wrks/PyRoll-Engine)](LICENSE)
[![Redis](https://img.shields.io/badge/storage-Redis-DC382D?logo=redis&logoColor=white)](https://redis.io)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#installation)

A lightweight desktop payroll management system built with Python and Tkinter.

[Getting Started](#getting-started) · [Features](#features) · [Configuration](#configuration) · [Contributing](#contributing)

</div>

---

## Overview

PyRoll Engine is a cross-platform desktop application for calculating and managing employee payroll. Enter hours worked, hourly rate, deductions, tax rate, and bonus to instantly compute gross and net pay. Records can be saved to Redis for persistence, with a seamless in-memory fallback when Redis is unavailable.

The UI is inspired by Claude's design language - dark backgrounds, a coral accent color - built entirely with Python's built-in `tkinter` library (no external UI dependencies).

## Features

| Feature | Description |
|---|---|
| **Payroll Calculator** | Computes gross pay, tax, deductions, bonus, and net pay in real time |
| **Employee Records** | Save and view all employee payroll records in a sortable table |
| **Redis Storage** | Persists records across sessions when a Redis server is available |
| **In-Memory Fallback** | Runs fully offline with no Redis required - data lives in memory for the session |
| **Demo Data** | Pre-seeded with two sample employees so the app is useful immediately |
| **Connection Status** | Status bar shows Redis vs. in-memory mode at a glance |

## Screenshots

> *Calculate tab - enter employee details and compute net pay instantly.*

> *Employees tab - full payroll table with all computed values.*

## Getting Started

### Prerequisites

- Python **3.10** or later
- `pip`
- *(Optional)* A running Redis server on `localhost:6379`

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/sha-wrks/PyRoll-Engine.git
cd PyRoll-Engine

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Running

```bash
python main.py
```

The app opens immediately. If Redis is not running, it silently falls back to in-memory storage and two demo employees are available right away.

## Redis Setup *(optional)*

Redis is only needed if you want payroll records to persist between sessions.

**Windows** - install [Memurai Community Edition](https://www.memurai.com/) or run Redis via WSL/Ubuntu:

```bash
# WSL / Ubuntu
sudo apt update && sudo apt install redis-server
sudo service redis-server start
```

**macOS**

```bash
brew install redis
brew services start redis
```

**Linux (Ubuntu / Debian)**

```bash
sudo apt update && sudo apt install redis-server
sudo systemctl enable --now redis-server
```

## Configuration

Redis connection settings are controlled via environment variables. The app uses these defaults when variables are not set:

| Variable | Default | Description |
|---|---|---|
| `REDIS_HOST` | `localhost` | Redis server hostname |
| `REDIS_PORT` | `6379` | Redis server port |
| `REDIS_DB` | `0` | Redis database index |

**Example** - connect to a remote Redis instance:

```bash
REDIS_HOST=192.168.1.100 REDIS_PORT=6380 python main.py
```

## Project Structure

```
PyRoll-Engine/
├── main.py                  # Entry point
├── requirements.txt         # Runtime dependencies
├── pyproject.toml           # Build metadata (PEP 517/518)
└── src/
    ├── ui/
    │   ├── gui.py           # Main window, widgets, user actions
    │   └── theme.py         # Design tokens (colors, fonts, spacing)
    ├── engine/
    │   └── payroll.py       # Pure payroll calculation logic
    └── database/
        └── database.py      # Redis + in-memory storage abstraction
```

## How It Works

```
User Input  ->  PayrollCalculator.calculate_salary()  ->  Display result
                        |
                   (on save)
                        v
              Database.save_employee()  ->  Redis  or  In-Memory list
```

- **`PayrollCalculator`** is a pure, stateless utility - `gross = hours * rate`, `tax = gross * (rate/100)`, `net = gross - deductions - tax + bonus`.
- **`Database`** attempts a Redis connection on startup. If it fails, it falls back transparently and sets a `using_redis` flag that the status bar reads.
- Demo records are seeded only when storage is empty, so restarting the app never creates duplicates.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes, then push
git push origin feature/your-feature-name

# Open a pull request on GitHub
```

Please follow the existing code style (type hints, no unnecessary comments) and open an issue first for significant changes.

## Security

To report a vulnerability, see [SECURITY.md](SECURITY.md). Do not open a public issue for security concerns.

## License

Distributed under the terms of the [LICENSE](LICENSE) file in this repository.
