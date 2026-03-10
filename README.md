# USAS Workspace Launcher

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Selenium](https://img.shields.io/badge/Selenium-Automation-43B02A?logo=selenium&logoColor=white)
![Batch](https://img.shields.io/badge/Batch-Scripting-4EAA25)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)

A high-performance, automated workspace initialization suite built with Python and Selenium. Capable of instantly connecting to the USAS campus network, bypassing captive portals, and securely authenticating into essential academic platforms without user interaction.

> [!WARNING]
> **Educational Purposes Only**: This tool is designed to optimize personal workflow. The authors are not responsible for any misuse.

## Features

- 🚀 **High Performance**: `eager` page loading strategies and direct JavaScript execution for instantaneous portal bypasses.
- 🎨 **Modern UI**: Beautiful, color-coded ANSI terminal interface.
- 🖥️ **Persistent Profiles**: Integrates seamlessly with your primary Google Chrome profile, ensuring your extensions, bookmarks, and standard logins remain intact.
- 🔄 **Smart Handling**: Automatically handles locked Chrome profiles with interactive retry loops.
- 🛡️ **Secure Credentials**: Credentials are encrypted locally via `.env` files and never hard-coded.
- 🤖 **Auto-Discovery**: Automatically parses generic login fields (username, userid, email, password, etc) for robust portal compatibility.
- 💻 **CLI & Interactive**: Run it fully automated via the one-click Batch script.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/zis3c/USAS-Launcher.git
   cd USAS-Launcher
   ```

2. **Run Initialization**
   Double-click `USAS_Workspace_Launcher.bat` to automatically install dependencies and build the virtual environment.

## Project Structure

```
USAS-Launcher/
├── usas_auth_controller.py     # Main Python engine - browser automation, credential management
├── USAS_Workspace_Launcher.bat # System orchestrator - handles WiFi, Python venv, and execution
├── requirements.txt            # Python dependencies (Selenium, python-dotenv, colorama)
├── .env.example                # Template for credentials
├── TOOL_DOCUMENTATION.md       # Capabilities and awareness guide
└── CONTRIBUTING.md             # Contribution guidelines
```

## Usage

### Interactive First-Run
Simply execute `USAS_Workspace_Launcher.bat`. On the first run, the script will securely prompt you for your `WIFI@USAS`, LMS, and VCampus credentials. These are saved to a hidden local `.env` file.

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
