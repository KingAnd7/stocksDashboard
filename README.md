# Financial Dashboard TUI

A real-time financial market monitor that runs in your terminal. This project uses a Python Textual interface to display live stock data, moving averages, and price changes, backed by a PostgreSQL database for persistent storage.

## Features

-   **Live Data Ingestion:** Fetches real-time stock data using `yfinance`.
-   **SQL Backend:** robust data storage using PostgreSQL.
-   **Terminal UI:** Beautiful, interactive TUI built with Textual.
-   **Watchlist Management:** Add and remove stock tickers dynamically directly from the UI.
-   **Metrics:** Displays Price, 5-minute Moving Average, and Percentage Change.

## Prerequisites

-   **Python 3.8+**
-   **Docker & Docker Compose** (for the database)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KingAnd7/financialDashboard.git
    cd financialDashboard
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

This application consists of three parts: the database, the data ingestion script, and the user interface. You will need to run them in parallel.

### 1. Start the Database
Start the PostgreSQL container using Docker Compose:

```bash
docker-compose up -d
```

### 2. Start Data Ingestion
Open a terminal and run the ingestion script. This fetches data for your watched tickers and updates the database.

```bash
# Make sure your venv is active
python ingest.py
```
*Note: This script runs indefinitely. Press `Ctrl+C` to stop it.*

### 3. Launch the Dashboard
Open a **new** terminal window (activate the venv there too) and launch the TUI:

```bash
# Make sure your venv is active
python tui.py
```

## Controls

| Key | Action |
| :--- | :--- |
| **`a`** | **Add Ticker**: Open a modal to add a new stock symbol (e.g., AAPL, TSLA) to your watchlist. |
| **`r`** | **Remove Ticker**: Open a modal to remove a stock symbol from your watchlist. |
| **`q`** | **Quit**: Exit the application. |

## Project Structure

-   `tui.py`: Main application entry point handling the User Interface.
-   `ingest.py`: Background service that fetches market data and updates the DB.
-   `database.py`: Data Access Object (DAO) handling all database interactions.
-   `docker-compose.yml`: Configuration for the PostgreSQL database container.
-   `requirements.txt`: Python dependencies.
