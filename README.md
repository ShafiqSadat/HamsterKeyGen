# HamsterKeyGen

This is an asynchronous Python script to generate Hamster Kombat Keys.

## Features
- Generate unique client IDs.
- Authenticate and obtain client tokens.
- Emulate user progress and register events.
- Generate and retrieve promo keys.

## Requirements
- Python 3.7+
- `httpx`
- `asyncio`

## Installation

1. Clone the repository or download the script.
2. Create a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Open a terminal and navigate to the directory containing the script.
2. Run the script:
    ```sh
    python main.py
    ```
3. Enter the number of keys you want to generate when prompted.

## Script Details

- **generate_client_id**: Generates a unique client ID.
- **login**: Authenticates using the client ID and returns a client token.
- **emulate_progress**: Simulates user progress and registers an event.
- **generate_key**: Generates a promo key using the client token.
- **generate_key_process**: Orchestrates the process of generating a key.
- **main**: Main function to generate multiple keys concurrently.

## License
This project is licensed under the GPL-3.0 license.

