# USAS Workspace Launcher

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Selenium](https://img.shields.io/badge/Selenium-Async-2C5BB4?logo=python&logoColor=white)
![Batch](https://img.shields.io/badge/Batch-CLI-blueviolet)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)

<p align="center">
  <img src="preview.png" alt="USAS Workspace Launcher Preview" width="600">
</p>

A high-performance, automated workspace initialization suite built with Python and Selenium. Capable of instantly connecting to the campus network and securely authenticating into essential academic platforms without user interaction.

> [!WARNING]
> **Educational Purposes Only**: This tool is designed to optimize personal workflow. The authors are not responsible for any misuse.

## Features

- 🚀 **High Performance**: `eager` page loading strategies and direct JavaScript execution for instantaneous portal bypasses.
- 🎨 **Modern UI**: Beautiful, color-coded ANSI terminal interface mimicking a CLI environment.
- 🖥️ **Persistent Profiles**: Integrates seamlessly with your primary Google Chrome profile, ensuring extensions remain intact.
- 🔄 **Smart Handling**: Automatically handles locked Chrome profiles with interactive retry loops.
- 🛡️ **Secure Credentials**: Credentials are encrypted locally via `.env` files and never hard-coded.
- 🤖 **Auto-Discovery**: Automatically parses generic login fields (username, userid, email, password, etc) for robust compatibility.
- 💻 **CLI & Interactive**: Run it fully automated via the one-click Batch script.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/zis3c/USAS-Launcher
   cd USAS-Launcher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
USAS-Launcher/
├── usas_auth_controller.py     # Main Python engine - browser automation, credential management
├── USAS_Workspace_Launcher.bat # System orchestrator - handles WiFi, Python venv, and execution
├── requirements.txt            # Python dependencies (Selenium, python-dotenv, colorama)
├── .env.example                # Template for credentials
├── preview.png                 # CLI preview screenshot
├── TOOL_DOCUMENTATION.md       # Capabilities and awareness guide
└── CONTRIBUTING.md             # Contribution guidelines
```

## Usage

### Interactive Mode
Simply execute `USAS_Workspace_Launcher.bat`. On the first run, the script will securely prompt you for your credentials. These are saved to a hidden local `.env` file.

### Daily Automation
For every subsequent run, simply execute `USAS_Workspace_Launcher.bat` and watch it automatically:
1. Connect to the university WiFi.
2. Setup the Python environment.
3. Launch a background Chrome Service.
4. Auto-login to the Captive Portal.
5. Auto-login to LMS.
6. Auto-login to VCampus (Portal Pelajar 1).
7. Open a new tab for ChatGPT.
8. Automatically open your local USAS OneDrive folder.

## How It Works

1. **Network Layer**: Uses native Windows `netsh` commands to force connections to specific SSIDs.
2. **Setup Layer**: Uses Windows Batch scripting to orchestrate Python `venv` creation, dependency injection, and cleanup.
3. **Execution Layer**: Uses Selenium WebDriver with detached creation flags so it runs completely independent of the command console.
4. **Automation**: Analyzes the DOM for common semantic login markers and leverages `implicitly_wait` for robust loading.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reporting bugs, suggesting enhancements, and submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
