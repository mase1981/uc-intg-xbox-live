# Unfolded Circle - Xbox Presence Widget

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A standalone integration for the Unfolded Circle Remote that displays the current game or app you are using on your Xbox as a media widget.

This integration connects to the Xbox Live services to see your "presence" and updates a widget on your remote in near real-time, showing the game title and cover art.

## Features

* **Now Playing Widget**: Displays the current Xbox game and cover art.
* **Real-time Status**: Shows if you are Online, Playing, or Offline.
* **Standalone**: Does not require any other Xbox integration to be installed.
* **Easy Setup**: Simple authentication flow with your Microsoft account.

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

#### Understanding the Docker Compose File
The `docker-compose.yml` is pre-configured for easy use:
```yaml
version: '3.8'
services:
  uc-intg-xbox-widget:
    build: .
    container_name: uc-intg-xbox-widget
    restart: unless-stopped
    # Host network mode is required for mDNS auto-discovery
    network_mode: host
    environment:
      # Sets a non-standard port to avoid conflicts
      - UC_INTEGRATION_HTTP_PORT=9094
      # Sets the directory for config files inside the container
      - UC_CONFIG_HOME=/config
    volumes:
      # Mounts the host's ./config dir to the container's /config dir
      - ./config:/config
```

## Configuration

1.  On your Unfolded Circle remote, go to `Settings > Integrations` and tap `+ Add New`.
2.  The **"Xbox Presence Widget"** should be listed as a discovered "External" integration. Select it.
3.  You will be prompted to enter your **Xbox Live Device ID**.
4.  Follow the on-screen instructions to log in with your Microsoft account and paste the final redirect URL back into the setup screen.
5.  Once setup is complete, the "Xbox Presence" media widget will be available to add to your user interfaces.

## Development

1.  Clone the repository: `git clone https://github.com/mase1981/uc-intg-xbox-widget.git`
2.  Navigate to the directory: `cd uc-intg-xbox-widget`
3.  Create a virtual environment: `python -m venv .venv`
4.  Activate it: `.\.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (macOS/Linux).
5.  Install in editable mode: `pip install -e .`
6.  Run the driver: `python -m uc_intg_xbox_widget.driver`

## License

This project is licensed under the MIT License.