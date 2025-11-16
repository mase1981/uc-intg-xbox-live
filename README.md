# Xbox Live Integration for Unfolded Circle Remote Two/3

![xbox](https://img.shields.io/badge/Xbox-Live-green)
[![GitHub Release](https://img.shields.io/github/v/release/mase1981/uc-intg-xbox-live?style=flat-square)](https://github.com/mase1981/uc-intg-xbox-live/releases)
![License](https://img.shields.io/badge/license-MPL--2.0-blue)
[![GitHub issues](https://img.shields.io/github/issues/mase1981/uc-intg-xbox-live?style=flat-square)](https://github.com/mase1981/uc-intg-xbox-live/issues)
[![Community Forum](https://img.shields.io/badge/community-forum-blue?style=flat-square)](https://community.unfoldedcircle.com/)
[![Discord](https://badgen.net/discord/online-members/zGVYf58)](https://discord.gg/zGVYf58)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/mase1981/uc-intg-xbox-live/total)
[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-donate-blue.svg)](https://paypal.me/mmiyara)
[![Github Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-30363D?&logo=GitHub-Sponsors&logoColor=EA4AAA)](https://github.com/sponsors/mase1981/button)

Display what you're playing on Xbox Live with beautiful game artwork directly on your Unfolded Circle Remote Two/3!

This integration connects to Xbox Live services to show your gaming presence in real-time with cover art, creating a rich media experience on your UC Remote.

# MAJOR UPDATE: THIS INTEGRATION HAS BEEN OFFICIALLY MERGED INTO A SINGLE INTEGRATION: https://github.com/mase1981/uc-intg-xbox WHICH WILL PROVIDE BOTH CONTROLS AS WELL AS MEDIA PLAYER - THIS XBOX-LIVE INTEGRATION WILL NO LONGER BE MAINTAINED AND OFFICIALLY REPLACED WITH THE XBOX INTEGRATION #
---

## 🌟 What This Integration Does

### Real-Time Gaming Presence

The Xbox Live integration displays your current gaming activity with stunning visuals:

- 🎮 **Current Game Display** - See what you're playing with official game artwork
- 👤 **Gamertag Display** - Your Xbox gamertag shown as entity name
- 🖼️ **Game Cover Art** - High-quality game artwork pulled from Xbox Live
- 🟢 **Live Presence Status** - Online, Playing, or Offline states
- ⚡ **Real-Time Updates** - Updates every 60 seconds automatically
- 📱 **Media Player Widget** - Beautiful presentation on UC Remote UI

### How It Works

The integration authenticates with your Microsoft account and monitors your Xbox Live presence:

1. **Authenticate** - Secure OAuth2 login with Microsoft
2. **Monitor** - Checks your Xbox Live presence every 60 seconds
3. **Display** - Updates media player entity with:
   - Game title as media title
   - Game artwork as media image
   - Current state (Playing/Online/Offline)

---

## ✨ Features

- 🎨 **Beautiful Game Artwork** - Official high-resolution game covers
- 🏷️ **Automatic Gamertag Detection** - Entity named with your Xbox gamertag
- 🔄 **Auto-Updating Presence** - Real-time game tracking (60s refresh)
- 🔐 **Secure OAuth2 Authentication** - Microsoft account login
- 💾 **Persistent Configuration** - One-time setup, works across reboots
- 🌐 **Cloud-Based** - Works via Xbox Live API (no console access needed)
- 📊 **Rich Status Display** - Playing, Online, or Offline states

---

## 📋 Requirements

### Hardware
- Xbox One, Xbox Series S, or Xbox Series X console
- Unfolded Circle Remote Two or Remote 3
- Active internet connection

### Software
- Microsoft account with Xbox Live access
- Xbox Live Device ID (from console settings)
- UC Remote firmware 1.7.0+

### Xbox Console Setup
- Xbox Live Device ID found at: **Settings > Devices & connections > Remote features**

---

## 🚀 Installation

### Option 1: GitHub Release (Recommended)

1. Download latest `.tar.gz` from [Releases](https://github.com/mase1981/uc-intg-xbox-live/releases)
2. Open UC Remote configurator: `http://your-remote-ip/configurator`
3. **Integrations** → **Add Integration** → **Upload driver**
4. Select downloaded file
5. Follow setup wizard

### Option 2: Docker

```bash
docker run -d --name uc-intg-xbox-live --restart unless-stopped --network host -v $(pwd)/data:/data -e UC_CONFIG_HOME=/data -e UC_INTEGRATION_INTERFACE=0.0.0.0 -e UC_INTEGRATION_HTTP_PORT=9090 -e UC_DISABLE_MDNS_PUBLISH=false ghcr.io/mase1981/uc-intg-xbox-live:latest
```

**Or with Docker Compose:**

```yaml
version: '3.8'

services:
  xbox-live-integration:
    image: ghcr.io/mase1981/uc-intg-xbox-live:latest
    container_name: uc-intg-xbox-live
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./data:/data
    environment:
      - UC_CONFIG_HOME=/data
      - UC_INTEGRATION_INTERFACE=0.0.0.0
      - UC_INTEGRATION_HTTP_PORT=9090
      - UC_DISABLE_MDNS_PUBLISH=false
```

```bash
docker-compose up -d
```

### Option 3: Development

```bash
git clone https://github.com/mase1981/uc-intg-xbox-live.git
cd uc-intg-xbox-live
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uc_intg_xbox_live.driver
```

---

## ⚙️ Setup

### Step 1: Get Xbox Live Device ID

1. On your Xbox console:
   - Navigate to **Settings > Devices & connections > Remote features**
2. **Copy the Xbox Live Device ID** (long alphanumeric string)
3. Keep it handy for setup

### Step 2: Add Integration

1. UC Remote configurator → **Integrations** → **Add**
2. Select **Xbox Live**
3. Enter **Xbox Live Device ID** from Step 1
4. Click **Next**

### Step 3: Microsoft Authentication

1. **Copy the login URL** displayed in setup
2. **Open URL in web browser**
3. **Login with Microsoft account** (same account linked to Xbox)
4. After successful login, **copy the entire redirect URL** from browser address bar
5. **Paste URL** back into integration setup
6. Click **Complete**

### Done! ✅

- Xbox Live entity appears with your gamertag
- Configuration saved permanently
- No re-authentication needed (tokens auto-refresh)

---

## 🎮 Entity Display

### Media Player Entity

**Entity Name:** `Gamertag: [Your Xbox Gamertag]`

**Displays:**
- **Media Title:** Current game name or status
- **Media Artist:** "Xbox Live"
- **Media Image:** Game cover artwork
- **State:** 
  - 🟢 **PLAYING** - Actively playing a game
  - 🟢 **ON** - Online but not gaming
  - ⚫ **OFF** - Offline

### Widget Appearance

The media player widget on your UC Remote shows:
- Large game artwork thumbnail
- Game title text
- "Xbox Live" as artist
- Current state indicator

Perfect for display on:
- Main dashboard
- Gaming activities
- Media widget pages

---

## 📊 What Gets Displayed

### Game Information

When you're playing an Xbox game, the integration shows:

- **Game Title** - Official game name from Xbox database
- **Game Artwork** - High-resolution box art/cover image
- **Status** - "Playing" state indicator

### Online Status

When you're online but not gaming:

- **Status Text** - Your Xbox presence text
- **State** - "Online" indicator
- **No Artwork** - Blank image (not playing)

### Offline Status

When you're offline:

- **Status Text** - "Offline"
- **State** - "Off" indicator
- **No Artwork** - Blank image

---

## 🔄 How Updates Work

### Automatic Polling

The integration checks Xbox Live every **60 seconds** for:
- Current gaming activity
- Presence state changes
- Game artwork updates

### What Triggers Updates

- Starting a new game
- Switching games
- Going online/offline
- Changing presence status

### Update Frequency

- **Default:** 60 seconds
- **Can be adjusted** in code if needed
- **Balance:** Responsiveness vs API load

---

## ⚠️ Important Limitations

### Display Only - No Control

This integration is **presence display only**:

- ✅ Shows what you're playing
- ✅ Displays game artwork
- ✅ Updates presence status
- ❌ **Cannot control Xbox console**
- ❌ **Cannot launch games**
- ❌ **Cannot navigate menus**

**For Xbox control**, see: [Xbox Integration](https://github.com/mase1981/uc-intg-xbox) (separate project)

### Cloud API Dependency

- Requires active internet connection
- Depends on Xbox Live services
- Updates are not instant (60s refresh)
- Some games may not have artwork

### Token Management

- OAuth tokens expire periodically (~90 days)
- Integration auto-refreshes tokens
- May need re-authentication if tokens expire
- Handled automatically in most cases

---

## 🛠 Troubleshooting

### No Entity Appears

**Symptoms:** Integration installs but no entity shows up

**Solutions:**
- ✅ Verify Xbox Live Device ID is correct
- ✅ Check authentication completed successfully
- ✅ View integration logs for errors
- ✅ Restart UC Remote
- ✅ Reconfigure integration if needed

### Entity Shows "Xbox User"

**Symptoms:** Entity name is generic "Xbox User" instead of gamertag

**Solutions:**
- ✅ Ensure Microsoft account is linked to Xbox Live
- ✅ Check Xbox profile has gamertag set
- ✅ View logs for profile fetch errors
- ✅ Wait for profile data to load (may take 1-2 minutes)

### Entity Stuck Offline

**Symptoms:** Entity always shows "Offline" even when gaming

**Solutions:**
- ✅ Verify correct Microsoft account used
- ✅ Check Xbox console is online
- ✅ Ensure privacy settings allow presence sharing
- ✅ View logs for API errors
- ✅ Re-authenticate if tokens expired

### No Game Artwork

**Symptoms:** Game title shows but no artwork appears

**Possible Causes:**
- Game is too new (artwork not in Xbox database yet)
- Indie/smaller game without official artwork
- API rate limiting or errors
- Network connectivity issues

**Solutions:**
- ✅ Check logs for titlehub API errors
- ✅ Verify game is recognized by Xbox
- ✅ Try switching to different game
- ✅ Wait a few minutes and check again

### Authentication Failed

**Symptoms:** Setup fails during Microsoft login

**Solutions:**
- ✅ Use correct Microsoft account (linked to Xbox)
- ✅ Copy **entire** redirect URL including all parameters
- ✅ Don't modify URL - paste exactly as shown
- ✅ Ensure Xbox Live access on account
- ✅ Try logging out and back in to Microsoft

### Entity Unavailable After Reboot

**Symptoms:** Integration works but entity unavailable after UC Remote restart

**Solutions:**
- ✅ Wait 30-60 seconds for initialization
- ✅ Check that config file exists
- ✅ View logs for token refresh errors
- ✅ Reconfigure if tokens corrupted
- ✅ Integration includes reboot survival features

---

## 📊 Technical Details

### Architecture

- **API:** Xbox Live REST API via `pythonxbox` library
- **Auth:** OAuth2 with token refresh
- **Protocol:** HTTPS to Xbox Live services
- **Entity Type:** Media Player (display only)
- **Update Interval:** 60 seconds

### API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `people.get_friends_by_xuid()` | Get user profile and presence |
| `titlehub.get_title_info()` | Fetch game artwork and metadata |
| `auth.refresh_tokens()` | Maintain authentication |

### Data Flow

```
Xbox Live → pythonxbox → Integration → UC Remote Entity
          ↓
     [Gamertag]
     [Presence State]
     [Game Title]
     [Game Artwork]
```

---

## 🛠️ Development

### Project Structure

```
uc-intg-xbox-live/
├── uc_intg_xbox_live/
│   ├── __init__.py           # Version from driver.json
│   ├── auth.py               # OAuth2 authentication
│   ├── config.py             # Persistent configuration
│   ├── driver.py             # Main integration driver
│   ├── media_player_entity.py # Media player entity
│   └── setup.py              # Setup flow handler
├── driver.json               # Integration metadata
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker image
├── docker-compose.yml        # Docker Compose config
└── README.md                 # This file
```

### Key Dependencies

```python
ucapi==0.3.1              # UC integration framework
python-xbox==0.1.0        # Xbox API wrapper
xbox-webapi==2.1.0        # Xbox authentication
httpx                     # Async HTTP client
platformdirs==4.5.0       # Config directories
```

### Modify Update Interval

Edit `uc_intg_xbox_live/driver.py`:

```python
UPDATE_INTERVAL_SECONDS = 60  # Change to desired seconds
```

**Recommendations:**
- **30s** - More responsive, higher API load
- **60s** - Balanced (default)
- **120s** - Conservative, lower API load

### Build Release

```bash
git tag v3.0.1
git push origin v3.0.1
# GitHub Actions builds automatically
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

### Reporting Issues

[Report Bug](https://github.com/mase1981/uc-intg-xbox-live/issues) · [Request Feature](https://github.com/mase1981/uc-intg-xbox-live/issues)

When reporting issues, please include:
- Integration version
- UC Remote firmware version
- Xbox console model
- Detailed error description
- Relevant log excerpts

---

## 💰 Support

If you find this integration useful, please consider supporting its development:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/mase1981)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/mmiyara)

Your support helps maintain this integration and develop new features. Thank you! ❤️

---

## 📄 License

This project is licensed under the **Mozilla Public License 2.0** (MPL-2.0).

See the [LICENSE](LICENSE) file for full details.

```
Copyright (c) 2025 Meir Miyara

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
```

---

## 🙏 Credits & Acknowledgments

### Developer
- **Meir Miyara** - [LinkedIn](https://www.linkedin.com/in/meirmiyara/) | [GitHub](https://github.com/mase1981)

### Special Thanks
- **[bjw-s](https://github.com/bjw-s)** - Code assistance and identifying removal of GiantBomb dependency
- **[Unfolded Circle](https://unfoldedcircle.com)** - For creating an amazing open platform
- **[OpenXbox](https://github.com/OpenXbox)** - For xbox-webapi-python library
- **UC Community** - For testing and feedback

### Libraries & Frameworks
- **[ucapi](https://github.com/unfoldedcircle/integration-python-library)** - Unfolded Circle Integration API
- **[python-xbox](https://github.com/OpenXbox/xbox-webapi-python)** - Xbox Live API wrapper
- **[xbox-webapi-python](https://github.com/OpenXbox/xbox-webapi-python)** - Xbox authentication

---

## 📞 Support & Links

### Getting Help
- 🐛 [GitHub Issues](https://github.com/mase1981/uc-intg-xbox-live/issues)
- 💬 [Discussions](https://github.com/mase1981/uc-intg-xbox-live/discussions)
- 👥 [UC Community Forum](https://community.unfoldedcircle.com/)
- 💬 [Discord Server](https://discord.gg/zGVYf58)

### Related Projects
- **[Xbox Integration](https://github.com/mase1981/uc-intg-xbox)** - Full Xbox console control
- **[Fire TV Integration](https://github.com/mase1981/uc-intg-firetv)** - Fire TV control
- **[WiiM Integration](https://github.com/mase1981/uc-intg-wiim)** - WiiM audio control

### Resources
- [UC Developer Documentation](https://github.com/unfoldedcircle/core-api)
- [UC Integration Examples](https://github.com/unfoldedcircle)
- [Xbox Live API Docs](https://github.com/OpenXbox/xbox-webapi-python)

---

## ⚠️ Disclaimer

This is an **unofficial integration** and is not affiliated with, endorsed by, or connected to Microsoft Corporation, Xbox, or Unfolded Circle ApS.

- **Xbox** and **Xbox Live** are trademarks of Microsoft Corporation
- **Unfolded Circle**, **Remote Two**, and **Remote 3** are trademarks of Unfolded Circle ApS
- Use this integration at your own risk
- No warranty provided, express or implied
- Developer not responsible for any issues arising from use

**Privacy Note:** This integration uses your Microsoft account credentials solely for Xbox Live API authentication. Credentials are never stored - only OAuth tokens are saved locally on your UC Remote.

---

<div align="center">

Made with ❤️ by [Meir Miyara](https://www.linkedin.com/in/meirmiyara/)

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/mase1981/uc-intg-xbox-live/issues) · [Request Feature](https://github.com/mase1981/uc-intg-xbox-live/issues) · [Discussions](https://github.com/mase1981/uc-intg-xbox-live/discussions)

</div>
