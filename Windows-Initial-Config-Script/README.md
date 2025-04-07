# Windows Config Script

This PowerShell script simplifies the configuration of new Windows PCs by automating common administrative tasks. It provides a menu-driven interface for enabling the local administrator account, deleting users, configuring user profiles, renaming the computer, and joining an Active Directory domain.

## Prerequisites
  - [PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.4)
  - Administrative privileges for running configurations on new PCs
  - Active Directory credentials for joining the domain

## Getting Started
1. **Clone the Repository** ```git clone https://github.com/achilleaspappas/Code-Snippet-Collection.git```
2. **Run Script**: Open PowerShell as Administrator, navigate to the folder where the script is located, run the script.
3. **Use Menu Interface**: Simply enter the corresponding number to select the action you want to perform. After each action, the script will prompt you to return to the menu or exit.

## How It Works
The script includes the following functions:
1. **Enable Local Admin**: Enables the built-in local administrator account, sets a password, and forces a logoff.
2. **Delete User**: Deletes a specified local user account and removes its corresponding user folder.
3. **Configure Profile**: Configures various system and user settings, such as:
   - Hides or shows icons on the desktop (e.g., "This PC", "Network", "Control Panel").
   - Sets the system locale to Greek and configures date and time formats.
   - Configures system-wide settings like "Hide empty drives" and "Hide file extensions".
4. **Rename Computer**: Renames the computer and restarts it.
5. **Join Active Directory**: Adds the computer to an Active Directory domain using provided credentials.

## Authors
[Achilleas Pappas] - Created the script.

## License
This project is provided as-is for personal use and development.

## Acknowledgments
This project was developed as part of my work and experience.