# USAS Workspace Launcher

A professional, zero-interaction automation suite designed for students and staff at Universiti Sultan Azlan Shah (USAS). This tool streamlines your study workflow by instantly connecting to the campus network, bypassing captive portals, and securely authenticating into essential university academic platforms.

## Overview

The USAS Workspace Launcher is built to eliminate the tedious daily process of logging into multiple university systems. With a single execute of the Batch launcher, the suite handles network configuration, dependency management, and browser automation to launch a fully authenticated workspace.

### Core Features

- **Automated Network Authentication:** Instantly connects to the `WIFI@USAS` network and automatically bypasses the Mikrotik captive portal.
- **Academic Portal Integration:** Automatically logs into LMS (`https://lms.usas.edu.my/my/`) and the VCampus Student Portal (`http://vcampus.usas.edu.my/`).
- **Additional Tools Integration:** Automatically opens supplemental productivity tools like ChatGPT alongside academic portals.
- **Local Application Launching:** Triggers the opening of local synced workspace folders (e.g., USAS OneDrive).
- **Persistent Profile Sessions:** Integrates seamlessly with your primary Google Chrome profile, ensuring your extensions, bookmarks, and standard logins remain intact.
- **Smart Credential Management:** Enforces a secure, encrypted one-time setup using localized `.env` variables ensuring passwords are never hardcoded.

## Technical Architecture

- **Language:** Python 3.10+
- **Automation Framework:** Selenium WebDriver
- **Orchestration:** Windows Batch Scripting
- **UI:** ANSI True-Color Terminal Interface

The suite runs entirely detached from the terminal instance, spawning an independent Chrome subprocess to prevent console hangups.

## Installation & Setup

1. Clone the repository to your local machine:
   ```cmd
   git clone https://github.com/YOUR_USERNAME/usas-workspace-launcher.git
   cd usas-workspace-launcher
   ```
2. Double-click the `USAS_Workspace_Launcher.bat` file.
3. On the first run, the terminal will prompt you for your university credentials. These are securely saved locally to an encrypted `.env` file and **will never be sent anywhere.**
4. The system will automatically build a Python virtual environment, download driver dependencies, and launch your authenticated workspace.

## Notice regarding Chrome Profiles

This automation integrates with your active operating system Chrome profile. If Chrome is already running, the tool features a smart-lock retry system that will safely pause execution until background Chrome processes are closed, preventing profile database corruption.

## Disclaimer

This software is an independent productivity tool and is not officially affiliated with, endorsed by, or integrated with Universiti Sultan Azlan Shah. Credentials are processed locally on the user's host machine.
