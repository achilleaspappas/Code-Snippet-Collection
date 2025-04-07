function Show-Menu
{
    param (
           [string]$Title = 'Welcome'
    )
    cls
    Write-Host "================ $Title ================"
    
    Write-Host "1: Enable Local Admin."
    Write-Host "2: Delete User."
    Write-Host "3: Configure Profile."
    Write-Host "4: Rename Computer."
    Write-Host "5: Join Active Directory."
    Write-Host "Q: Press 'Q' to quit."
}

function Enable-Local-Admin
{
    net user Administrator /active:yes
    net user Administrator "YOUR_PASSWORD_HERE"
    shutdown /l
}

function Delete-User 
{
    $username = "user"
    Remove-LocalUser -Name $username
    Remove-Item -Path "C:\Users\$username" -Recurse -Force  
}

function Configure-Profile
{
    # This PC
    New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" -Name "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" -Value 0 -Force

    # Network
    New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" -Name "{F02C1A0D-BE21-4350-88B0-7367FC96EF3C}" -Value 0 -Force

    # Recycle Bin
    #New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" -Name "{645FF040-5081-101B-9F08-00AA002F954E}" -Value 0 -Force

    # Control Panel
    New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" -Name "{21EC2020-3AEA-1069-A2DD-08002B30309D}" -Value 0 -Force

    # User Folder
    New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel" -Name "{59031a47-3f72-44a7-89c5-5595fe6b30ee}" -Value 0 -Force

    # Turn off "Hide empty drives"
    Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' -Name HideDrivesWithNoMedia -Value 0

    # Turn off "Hide extensions for known file types"
    Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' -Name HideFileExt -Value 0

    # Set Format to Greek
    Set-Culture el-GR
    #Set-WinUILanguageOverride el-GR

    # Set System Locale to Greek
    Set-WinSystemLocale el-GR

    # Set short date format
    Set-ItemProperty -Path 'HKCU:\Control Panel\International' -Name sShortDate -Value 'dd/MM/yyyy'

    # Set long date format
    Set-ItemProperty -Path 'HKCU:\Control Panel\International' -Name sLongDate -Value 'ddd, d MMMM yyyy'

    # Set short time format
    Set-ItemProperty -Path 'HKCU:\Control Panel\International' -Name sShortTime -Value 'HH:mm'

    # Set long time format
    Set-ItemProperty -Path 'HKCU:\Control Panel\International' -Name sTimeFormat -Value 'HH:mm:ss'

    # Hide Search
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Search" -Name SearchboxTaskbarMode -Value 0

    # Turn off Task View
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name ShowTaskViewButton -Value 0    

    # Turn off Widgets
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name TaskbarDa -Value 0

    # Turn off Automatic Restart on System Failure
    Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\CrashControl' -Name AutoReboot -Value 0

    # Set Write Debugging Information to None   
    Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\CrashControl' -Name CrashDumpEnabled -Value 0

    # Create Folder and Assign to TEMP and TMP for both User and System
    New-Item -Path "C:\" -Name "Temp" -ItemType "Directory"
    [Environment]::SetEnvironmentVariable("TEMP", "C:\Temp", "User")
    [Environment]::SetEnvironmentVariable("TMP", "C:\Temp", "User")
    [Environment]::SetEnvironmentVariable("TEMP", "C:\Temp", "Machine")
    [Environment]::SetEnvironmentVariable("TMP", "C:\Temp", "Machine")

    # Restart Windows Explorer
    Stop-Process -Name explorer -Force
    Start-Process explorer
}

function Rename-Computer
{
	# Ask for the new computer name
	$newName = Read-Host -Prompt "Enter the new computer name"
	# Confirm the rename
	Rename-Computer -NewName $newName -Force -Restart
}

function Join-Active-Directory
{	
    # Add the computer to a domain
    $domain = "DOMAIN_NAME_HERE
    $domainUser = "DOMAIN_USER_HERE" 
    $domainPassword = Read-Host -AsSecureString "Enter password for domain admin: "
    # Join the computer to the domain
    Add-Computer -DomainName $domain -Credential $domainUser -Force -Restart -Verbose
}

do
{
    Show-Menu
    $input = Read-Host "Give input: "
    switch ($input)
    {
        '1' {
                cls
                Enable-Local-Admin
        } '2' {
                cls
                Delete-User
        } '3' {
                cls
                Configure-Profile
	} '4' {
                cls
                Rename-Computer
	} '5' {
                cls
                Join-Active-Directory
        } 'q' {
                return
        }
    }
    pause
}
until ($input -eq 'q')