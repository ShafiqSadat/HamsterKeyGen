# HamsterKeyGen

This is an asynchronous Python script to generate Hamster Kombat Keys.

## Features
- Generate unique client IDs.
- Authenticate and obtain client tokens.
- Emulate user progress and register events.
- Generate and retrieve promo keys.
- Optional proxy support.
- Save keys into file.

## Requirements
- Python 3.7+
- `httpx`
- `asyncio`
- `loguru`

## Installation

1. Clone the repository or download the script.
    ```sh
    git clone https://github.com/ShafiqSadat/HamsterKeyGen.git
    ```
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
3. Follow the prompts to enter the game number and the number of keys you want to generate.

### Using Proxies

You can optionally use a proxy by specifying a proxy file. If no proxy file is provided, the script will look for `proxy.txt` in the same directory.

1. Create a file named `proxy.txt` in the same directory as the script.
2. Add your proxy URL to the `proxy.txt` file. For example:

#### HTTP Proxy
```
http://proxy-server:8080
```

#### HTTPS Proxy
```
https://proxy-server:8080
```

#### SOCKS5 Proxy
```
socks5://proxy-server:1080
```

#### SOCKS4 Proxy
```
socks4://proxy-server:1080
```

When running the script, you can specify the path to your proxy file:

```sh
python main.py
```

If you do not specify a proxy file, the script will attempt to use `proxy.txt` by default.

### Script Details

- **generate_client_id**: Generates a unique client ID.
- **login**: Authenticates using the client ID and returns a client token.
- **emulate_progress**: Simulates user progress and registers an event.
- **generate_key**: Generates a promo key using the client token.
- **generate_key_process**: Orchestrates the process of generating a key.
- **main**: Main function to generate multiple keys concurrently.

## License
This project is licensed under the GPL-3.0 license.
