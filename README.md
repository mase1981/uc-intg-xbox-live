# Xbox Live Integration for Unfolded Circle Remote 2/3

Display your current Xbox Live gaming activity with **beautiful game artwork** directly on your Unfolded Circle Remote 2 or Remote 3. This integration shows **real-time presence**, **game titles**, and **official cover art** from Xbox Live.

![xbox](https://img.shields.io/badge/Xbox-Live-green)
[![GitHub Release](https://img.shields.io/github/v/release/mase1981/uc-intg-xbox-live?style=flat-square)](https://github.com/mase1981/uc-intg-xbox-live/releases)
![License](https://img.shields.io/badge/license-MPL--2.0-blue?style=flat-square)
[![GitHub issues](https://img.shields.io/github/issues/mase1981/uc-intg-xbox-live?style=flat-square)](https://github.com/mase1981/uc-intg-xbox-live/issues)
[![Community Forum](https://img.shields.io/badge/community-forum-blue?style=flat-square)](https://unfolded.community/)
[![Discord](https://badgen.net/discord/online-members/zGVYf58)](https://discord.gg/zGVYf58)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/mase1981/uc-intg-xbox-live/total?style=flat-square)
[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat-square)](https://buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-donate-blue.svg?style=flat-square)](https://paypal.me/mmiyara)
[![Github Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-30363D?&logo=GitHub-Sponsors&logoColor=EA4AAA&style=flat-square)](https://github.com/sponsors/mase1981)

---
## ⚠️ IMPORTANT NOTICE ⚠️

**THIS INTEGRATION HAS BEEN OFFICIALLY MERGED INTO THE [XBOX INTEGRATION](https://github.com/mase1981/uc-intg-xbox)**

The new Xbox integration provides **BOTH** remote control and media player (presence display) functionality in a single integration.

**This Xbox Live integration will no longer be maintained.** Please use the [Xbox Integration](https://github.com/mase1981/uc-intg-xbox) instead for:
- Full Xbox console control
- Live gaming presence display with artwork
- Power management
- All features from this integration and more

---

## Features

This integration displays your current gaming activity with stunning visuals through the Xbox Live API, delivering seamless integration with your Unfolded Circle Remote for real-time presence monitoring.

---
## ❤️ Support Development ❤️

If you find this integration useful, consider supporting development:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/mase1981)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/mmiyara)

Your support helps maintain this integration. Thank you! ❤️
---

### 🎮 **Real-Time Gaming Presence**

#### **Current Game Display**
- **Game Title** - See what you're playing with official game artwork
- **Gamertag Display** - Your Xbox gamertag shown as entity name
- **Game Cover Art** - High-quality game artwork from Xbox Live
- **Live Presence Status** - Online, Playing, or Offline states
- **Real-Time Updates** - Updates every 60 seconds automatically
- **Media Player Widget** - Beautiful presentation on UC Remote UI

#### **Display Information**
- **Media Title**: Current game name or status
- **Media Artist**: "Xbox Live"
- **Media Image**: Game cover artwork
- **State**: Playing (in-game), On (online), Off (offline)

### **Supported Consoles**

- **Xbox One** (Original, S, X)
- **Xbox Series S**
- **Xbox Series X**

### **Protocol Requirements**

- **Protocol**: Xbox Live REST API
- **Microsoft Account**: With Xbox Live access
- **Xbox Live Device ID**: Found in console settings
- **Internet Connectivity**: Required for Xbox Live API
- **Authentication**: OAuth2 with token refresh

### **Network Requirements**

- **Internet Access** - Required for Xbox Live API communication
- **HTTPS Protocol** - Integration uses secure HTTPS to Xbox Live servers
- **Firewall** - Ensure outbound HTTPS traffic is permitted
- **Cloud-Based** - Works via Xbox Live API (no console access needed)

## Installation

### Option 1: Remote Web Interface (Recommended)
1. Navigate to the [**Releases**](https://github.com/mase1981/uc-intg-xbox-live/releases) page
2. Download the latest `uc-intg-xbox-live-<version>-aarch64.tar.gz` file
3. Open your remote's web interface (`http://your-remote-ip`)
4. Go to **Settings** → **Integrations** → **Add Integration**
5. Click **Upload** and select the downloaded `.tar.gz` file

### Option 2: Docker (Advanced Users)

The integration is available as a pre-built Docker image from GitHub Container Registry:

**Image**: `ghcr.io/mase1981/uc-intg-xbox-live:latest`

**Docker Compose:**
```yaml
services:
  uc-intg-xbox-live:
    image: ghcr.io/mase1981/uc-intg-xbox-live:latest
    container_name: uc-intg-xbox-live
    network_mode: host
    volumes:
      - </local/path>:/data
    environment:
      - UC_CONFIG_HOME=/data
      - UC_INTEGRATION_HTTP_PORT=9090
      - UC_INTEGRATION_INTERFACE=0.0.0.0
      - PYTHONPATH=/app
    restart: unless-stopped
```

**Docker Run:**
```bash
docker run -d --name uc-intg-xbox-live --restart unless-stopped --network host -v xbox-live-config:/data -e UC_CONFIG_HOME=/data -e UC_INTEGRATION_INTERFACE=0.0.0.0 -e UC_INTEGRATION_HTTP_PORT=9090 -e PYTHONPATH=/app ghcr.io/mase1981/uc-intg-xbox-live:latest
```

## Configuration

### Step 1: Get Xbox Live Device ID

**IMPORTANT**: You need your Xbox Live Device ID before setup.

#### On Your Xbox Console:
1. Navigate to **Settings** → **Devices & connections** → **Remote features**
2. Copy the **Xbox Live Device ID** (long alphanumeric string)
3. Keep it handy for setup

### Step 2: Setup Integration

1. After installation, go to **Settings** → **Integrations**
2. The Xbox Live integration should appear in **Available Integrations**
3. Click **"Configure"** to begin setup:

#### **Configuration:**
- **Xbox Network Device ID**: Enter the ID from your Xbox console
- Click **Next**

#### **Microsoft Authentication:**
1. **Copy the login URL** displayed in setup
2. **Open URL in web browser**
3. **Login with Microsoft account** (same account linked to Xbox)
4. After successful login, **copy the entire redirect URL** from browser address bar
5. **Paste URL** back into integration setup
6. Click **Complete**

#### **Connection Test:**
- Integration authenticates with Xbox Live
- Fetches your Xbox gamertag
- Verifies presence data access
- Setup fails if authentication unsuccessful

4. Integration will create entity:
   - **Gamertag: [Your Xbox Gamertag]**: Media player entity showing gaming activity

## Using the Integration

### Media Player Entity

The media player entity displays live Xbox gaming activity:

**Entity Name:** `Gamertag: [Your Xbox Gamertag]`

**Displays:**
- **Media Title**: Current game name or status
- **Media Artist**: "Xbox Live"
- **Media Image**: Game cover artwork
- **State**: Playing (actively gaming), On (online), Off (offline)

**Automatic Updates:**
- Status refreshes every 60 seconds
- Game changes detected automatically
- Presence updates in real-time
- No manual refresh needed

### What Gets Displayed

**When Playing:**
- Game title (official game name)
- Game artwork (high-resolution cover art)
- "Playing" state indicator

**When Online (Not Gaming):**
- Xbox presence text
- "Online" indicator
- No artwork

**When Offline:**
- "Offline" status
- "Off" indicator
- No artwork

## Important Limitations

### Display Only - No Control

This integration is **presence display only**:

- Shows what you're playing
- Displays game artwork
- Updates presence status
- **Cannot control Xbox console**
- **Cannot launch games**
- **Cannot navigate menus**

**For Xbox control**, use the [Xbox Integration](https://github.com/mase1981/uc-intg-xbox) which includes both control and presence display.

### Cloud API Dependency

- Requires active internet connection
- Depends on Xbox Live services
- Updates are not instant (60s refresh)
- Some games may not have artwork

## Credits

- **Developer**: Meir Miyara
- **[bjw-s](https://github.com/bjw-s)**: Code assistance and identifying removal of GiantBomb dependency
- **[OpenXbox](https://github.com/OpenXbox)**: For xbox-webapi-python library
- **Unfolded Circle**: Remote 2/3 integration framework (ucapi)
- **Protocol**: Xbox Live REST API
- **Community**: Testing and feedback from UC community

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0) - see LICENSE file for details.

## Disclaimer

This is an **unofficial integration** and is not affiliated with, endorsed by, or connected to Microsoft Corporation, Xbox, or Unfolded Circle ApS.

- **Xbox** and **Xbox Live** are trademarks of Microsoft Corporation
- **Unfolded Circle**, **Remote Two**, and **Remote 3** are trademarks of Unfolded Circle ApS
- Use this integration at your own risk
- No warranty provided, express or implied
- Developer not responsible for any issues arising from use

**Privacy Note:** This integration uses your Microsoft account credentials solely for Xbox Live API authentication. Credentials are never stored - only OAuth tokens are saved locally on your UC Remote.

## Support & Community

- **GitHub Issues**: [Report bugs and request features](https://github.com/mase1981/uc-intg-xbox-live/issues)
- **GitHub Discussions**: [General discussion and support](https://github.com/mase1981/uc-intg-xbox-live/discussions)
- **UC Community Forum**: [Unfolded Circle community](https://unfolded.community/)
- **Discord**: [Unfolded Circle Discord](https://discord.gg/zGVYf58)
- **Developer**: [Meir Miyara](https://github.com/mase1981)

## Related Projects

- **[Xbox Integration](https://github.com/mase1981/uc-intg-xbox)** - Full Xbox console control (RECOMMENDED)
- **[Fire TV Integration](https://github.com/mase1981/uc-intg-firetv)** - Fire TV control
- **[WiiM Integration](https://github.com/mase1981/uc-intg-wiim)** - WiiM audio control

---

**Made with ❤️ for the Unfolded Circle and Xbox Gaming Communities**

**Thank You**: Meir Miyara
