# Unfolded Circle - Xbox Live Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A standalone integration for the Unfolded Circle Remote that displays the current game or app you are using on your Xbox.

This integration connects to the Xbox Live services to see your "presence" and updates a media player entity on your remote in near real-time, showing your gamertag, the game title, and cover art.

## Features

* **Dynamic Entity Name**: The entity is automatically named after your Xbox Gamertag.
* **Now Playing**: Displays the current Xbox game and its cover art.
* **Real-time Status**: Shows if you are Online, Playing, or Offline.
* **Standalone**: Does not require any other Xbox integration to be installed.
* **Easy Setup**: Simple and secure authentication flow with your Microsoft account.

## Prerequisites

1.  An Unfolded Circle Remote (RC2 or RC3).
2.  An Xbox One, Xbox Series S, or Xbox Series X console.
3.  Your console's **Xbox Live Device ID**. To find it, go to `Settings > Devices & connections > Remote features` on your Xbox.
4.  An active **internet connection** for the machine running this integration, as it needs to communicate with Xbox Live servers.

## Installation (Docker)

The recommended way to run this integration is using Docker on a home server or Synology NAS.

### Method 1: Docker Compose (Easiest)

1.  **Download Files**: Clone or download the project files from this GitHub repository.
2.  **Run Docker Compose**: From a terminal in the project's root directory, run the following single command:
    ```bash
    docker-compose up --build -d
    ```
3.  The integration will build, start, and be discoverable on your network.

#### Docker Compose File
The `docker-compose.yml` is pre-configured for your convenience:
```yaml
version: '3.8'
services:
  uc-intg-xbox-live:
    build: .
    container_name: uc-intg-xbox-live
    restart: unless-stopped
    network_mode: host
    environment:
      # Sets a non-standard port to avoid conflicts
      - UC_INTEGRATION_HTTP_PORT=9098
      - UC_CONFIG_HOME=/config
    volumes:
      - ./config:/config
```
> **Note on Port**: This integration uses port **9098** by default to avoid conflicts with the Unfolded Circle remote's default port (9090). If port 9098 is already in use on your network, you can edit the `docker-compose.yml` file and change `9098` to another unused port.

### Method 2: Manual Docker Run (Single Command)

If you don't use `docker-compose`, you can build and run the container with these commands.

1.  **Build the Image**: First, navigate to the project's root directory in your terminal and build the Docker image:
    ```bash
    docker build -t uc-intg-xbox-live .
    ```

2.  **Run the Container**: After the build is complete, use the command for your operating system to run the container.

    * **For Linux, macOS, or Windows PowerShell:**
        ```bash
        docker run -d --name uc-intg-xbox-live --network host -e "UC_INTEGRATION_HTTP_PORT=9098" -v "$(pwd)/config:/config" --restart unless-stopped uc-intg-xbox-live
        ```

    * **For Windows Command Prompt (cmd.exe):**
        ```bash
        docker run -d --name uc-intg-xbox-live --network host -e "UC_INTEGRATION_HTTP_PORT=9098" -v "%cd%/config:/config" --restart unless-stopped uc-intg-xbox-live
        ```

## Configuration

1.  On your Unfolded Circle remote, go to `Settings > Integrations` and tap `+ Add New`.
2.  The **"Xbox Live"** integration should be listed as a discovered "External" integration. Select it.
3.  You will be prompted to enter your **Xbox Live Device ID**.
4.  Follow the on-screen instructions to log in with your Microsoft account and paste the final redirect URL back into the setup screen.
5.  Once setup is complete, the entity with your gamertag will be available to add to your user interfaces.

## Development

1.  Clone the repository: `git clone https://github.com/mase1981/uc-intg-xbox-live.git`
2.  Navigate to the directory: `cd uc-intg-xbox-live`
3.  Create a virtual environment: `python -m venv .venv`
4.  Activate it: `.\.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (macOS/Linux).
5.  Install in editable mode: `pip install -e .`
6.  Run the driver: `python -m uc_intg_xbox_live.driver`

## Acknowledgements
* This project is powered by the [xbox-webapi](https://github.com/OpenXbox/xbox-webapi-python) library.
* Thanks to [JackJPowell](https://github.com/JackJPowell) for the PSN integration which served as an excellent reference point.
* Special thanks to the [Unfolded Circle](https://www.unfoldedcircle.com/) team for creating a remote with an open API.

## License

This project is licensed under the MIT License.