# USAS Workspace Launcher - Capabilities & Awareness

## 1. What This Tool Does

The USAS Workspace Launcher is a lightweight, fully automated startup orchestrator capable of establishing a complete study environment with zero user interaction.

It works by launching a detached Python subprocess via robust batch scripting. This subprocess utilizes Selenium WebDriver to parse and manipulate DOM elements on Universiti Sultan Azlan Shah (USAS) login portals (Captive Portal, LMS, VCampus). Because it executes dynamic JavaScript injections and uses `eager` page loading strategies, it drastically outperforms human interaction and bypasses all CSS/UI animations.

It also creates a persistent Chrome Profile connection or seamlessly generates an ephemeral guest profile, ensuring it interacts correctly with existing authentication tokens or provides a sterile sandbox environment depending on user configuration. It handles dynamic network switching natively through the Windows API (`netsh`) to automatically resolve the `WIFI@USAS` BSSID broadcast.

---

## 2. Security & Access Considerations

If you are a network administrator or portal manager and wish to understand how to prevent automated logins or enforce distinct human interaction, be aware that this tool exclusively targets standard HTML forms and weak Captive Portal configurations.

### A. Implement CAPTCHA *(Most Effective)*
- Because this tool operates headless browser instances (or detached visible instances), integrating a Google reCAPTCHA or Cloudflare Turnstile directly on the login `POST` action is the single most effective deterrent against this explicit script.
- **Why it works:** The automation relies entirely on standard expected elements (`id="username"`, `id="password"`, `type="submit"`). A CAPTCHA halts the synchronous execution flow of the WebDriver, raising a `TimeoutException`.

### B. Two-Factor Authentication (2FA)
- Implementing standard SMS or Authenticator App protocols.
- **Why it works:** The script is hard-coded to pull static credentials from a localized `.env` file. It cannot intercept live OTP generation, causing the post-login verification step to fail.

### C. Dynamic DOM Elements
- Randomize the `id` and `name` attributes of the login form fields upon every request.
- **Why it works:** The current build of the USAS Workspace Launcher relies on discovering common static semantic identifiers (e.g., searching the DOM tree for elements named 'userid' or 'login_username'). Highly ephemeral forms break the selector logic.

---

## 3. Local Credential Security

The tool prioritizes local user security during the setup phase:
- **Masked Inputs**: Utilizing the `pwinput` module, password entries during the initial command-line setup are masked with asterisks to prevent shoulder-surfing.
- **Encrypted Storage**: Instead of storing credentials in plaintext `.env` files, the script exclusively leverages the `keyring` library to inject passwords directly into the host OS's native **Windows Credential Manager**.
- **Segregated Data**: Only non-sensitive User IDs are tracked in the `.env` configuration file, ensuring the repository remains sterile and user passwords are untouchable by local file-system scraping.

---

## Summary

This tool dramatically accelerates the daily workflow of USAS students by automating routine HTML forms and open network connections. Implementations of CAPTCHA, 2FA, or heavily obfuscated login endpoints are required if the goal is to enforce manual, non-automated human presence at the time of login.
