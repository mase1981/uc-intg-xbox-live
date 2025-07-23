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
3.  You will need your console's **Xbox Live Device ID**. To find it, go to `Settings > Devices & connections > Remote features` on your Xbox.

## Installation (Docker - Recommended)

This is the easiest and most stable way to run the integration on a home server or Synology NAS.

1.  **Download Files**: Clone or download the project files from this GitHub repository. Make sure you have both `docker-compose.yml` and the `Dockerfile`.
2.  **Run Docker Compose**: From a terminal in the project's root directory, run the following command:
    ```bash
    docker-compose up --build -d
    ```
3.  The integration will build, start, and be discoverable on your network.

#### Docker Compose File
The `docker-compose.yml` is pre-configured for easy use:
```yaml
version: '3.8'
services:
  uc-intg-xbox-live:
    build: .
    container_name: uc-intg-xbox-live
    restart: unless-stopped
    network_mode: host
    environment:
      - UC_INTEGRATION_HTTP_PORT=9094
      - UC_CONFIG_HOME=/config
    volumes:
      - ./config:/config
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