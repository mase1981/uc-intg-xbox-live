# Unfolded Circle - Xbox Live Integration

[![Discord](https://badgen.net/discord/online-members/zGVYf58)](https://discord.gg/zGVYf58)
![GitHub Release](https://img.shields.io/github/v/release/mase1981/uc-intg-xbox-live)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/mase1981/uc-intg-xbox-live/total)
![License](https://img.shields.io/badge/license-MPL--2.0-blue)
[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-donate-blue.svg)](https://paypal.me/mmiyara)
[![Github Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-30363D?&logo=GitHub-Sponsors&logoColor=EA4AAA)](https://github.com/sponsors/mase1981/button)

A standalone integration for the Unfolded Circle Remote that displays the current game you are playing on your xBox, complete with cover art.

This integration connects to the Xbox Live services to see your "presence" and updates a media player entity on your remote in near real-time, showing your gamertag, the game title, and the game's artwork.

Hope you enjoy this integration, thank you so much - Meir Miyara.

## Features

- **Now Playing**: Displays the current Xbox game and its cover art on the media widget.
- **Real-time Status**: Shows if you are Online, Playing, or Offline.
- **Dynamic Entity Name**: The entity is automatically named after your Xbox Gamertag.
- **Standalone**: Does not require any other Xbox integration to be installed.
- **Easy Setup**: Simple and secure authentication flow with your Microsoft account.

---

## Prerequisites

1.  An Unfolded Circle Remote 2 or Remote 3.
2.  An Xbox One, Xbox Series S, or Xbox Series X console.
3.  Your console's **Xbox Live Device ID**. To find it, go to `Settings > Devices & connections > Remote features` on your Xbox.
4.  An active **internet connection** for the device running this integration.

---

## Installation

You can run this integration in two ways: as a `tar.gz` archive on an Unfolded Circle Hub, or as a Docker container on a home server.

### Method 1: Manual Installation (`.tar.gz`)

This is the recommended method for users running the Unfolded Circle Hub software.

1.  Go to the [**Releases**](https://github.com/mase1981/uc-intg-xbox-live/releases) page of this repository.
2.  Download the latest `uc-intg-xbox-live-x.x.x-aarch64.tar.gz` file and the corresponding `.hash` file.
3.  On your Unfolded Circle remote or web configurator, go to `Settings > Integrations > + Add New`.
4.  Select **"Install from file (.tar.gz)"** and upload the archive you downloaded.
5.  The integration will install and become discoverable.

### Method 2: Docker Installation

This is the recommended method for users with a home server or Synology NAS.

1.  **Download Files**: Clone or download the `docker-compose.yml` file from this GitHub repository.
2.  **Run Docker Compose**: From a terminal in the same directory as the file, run the following command:
    ```bash
    docker-compose up -d
    ```
3.  The integration will build, start, and be discoverable on your network.

### Docker Compose File

Create a `docker-compose.yml` file with the following content:

```
version: '3.8'
services:
  uc-intg-xbox-live:
    build: .
    container_name: uc-intg-xbox-live
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./config:/app/uc_intg_xbox_live/config
```

**Note** on network_mode: host: This is required for the Unfolded Circle remote to discover the integration on your local network.

## Configuration

1.  On your Unfolded Circle remote, go to `Settings > Integrations` and tap `+ Add New`.
2.  The **"Xbox Live Presence"** integration should be listed as a discovered integration. Select it.
3.  You will be prompted to enter your **Xbox Live Device ID**.
4.  Follow the on-screen instructions to log in with your Microsoft account and paste the final redirect URL back into the setup screen.
5.  Once setup is complete, the entity with your gamertag will be available to add to your user interfaces as a **Media Widget**.

## Development

1.  Clone the repository: `git clone https://github.com/mase1981/uc-intg-xbox-live.git`
2.  Navigate to the directory: `cd uc-intg-xbox-live`
3.  Create a virtual environment: `python -m venv .venv`
4.  Activate it: `.\.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (macOS/Linux).
5.  Install dependencies: `pip install -r requirements.txt`
6.  Run the driver: `python -m uc_intg_xbox_live.driver`

## Acknowledgements

- This project is powered by the [xbox-webapi-python](https://github.com/OpenXbox/xbox-webapi-python) library.
- Thanks to [JackJPowell](https://github.com/JackJPowell) for the PSN integration which served as an excellent reference point.
- Special thanks to the [Unfolded Circle](https://www.unfoldedcircle.com/) team for creating a remote with an open API.

## License

This project is licensed under the MIT License.
