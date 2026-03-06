# System Commands Module
# Handles PC control and automation using subprocess, os, pyautogui, webbrowser

import subprocess
import os
import sys
import webbrowser
import pyautogui
import json

class SystemCommands:
    """Execute system commands on Windows/Mac/Linux"""
    
    def __init__(self):
        """Initialize system commands"""
        self.system = sys.platform
        self.command_log = []
        print(f"✓ System Commands initialized (Platform: {self.system})")
        
        self.applications = self._get_applications_map()
    
    def _get_applications_map(self):
        """Map common application names to executables"""
        if self.system == 'win32':
            return {
                'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
                'vscode': r'C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe',
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'spotify': 'spotify.exe',
                'discord': r'C:\Users\{username}\AppData\Local\Discord\app-*\Discord.exe',
                'telegram': 'telegram.exe',
                'obs': r'C:\Program Files\obs-studio\bin\64bit\obs.exe',
                'vlc': r'C:\Program Files\VideoLAN\VLC\vlc.exe',
                'blender': r'C:\Program Files\Blender Foundation\Blender 3.5\blender.exe',
                'gimp': r'C:\Program Files\GIMP 2\bin\gimp-2.10.exe',
                'atom': 'atom.exe',
                'sublime': r'C:\Program Files\Sublime Text\sublime_text.exe',
                'python': 'python.exe',
                'powershell': 'powershell.exe',
            }
        elif self.system == 'darwin':  # macOS
            return {
                'chrome': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                'firefox': '/Applications/Firefox.app/Contents/MacOS/firefox',
                'vscode': '/Applications/Visual Studio Code.app/Contents/MacOS/Code',
                'spotify': '/Applications/Spotify.app/Contents/MacOS/Spotify',
                'discord': '/Applications/Discord.app/Contents/MacOS/Discord',
                'safari': '/Applications/Safari.app/Contents/MacOS/Safari',
            }
        else:  # Linux
            return {
                'chrome': 'google-chrome',
                'firefox': 'firefox',
                'vscode': 'code',
                'spotify': 'spotify',
                'discord': 'discord',
            }
    
    def open_application(self, app_name):
        """
        Open an application
        
        Args:
            app_name: Application name (chrome, vscode, spotify, etc)
            
        Returns:
            Success message or error
        """
        app_name = app_name.lower().strip()
        
        if app_name not in self.applications:
            return f"✗ Application '{app_name}' not recognized. Try: chrome, firefox, vscode, spotify, discord, etc"
        
        app_path = self.applications[app_name]
        
        try:
            if self.system == 'win32':
                subprocess.Popen(app_path)
            elif self.system == 'darwin':
                subprocess.Popen(['open', '-a', app_path])
            else:  # Linux
                subprocess.Popen([app_path])
            
            message = f"✓ Opening {app_name.capitalize()}"
            self._log_command('open_app', app_name, True)
            return message
        except Exception as e:
            message = f"✗ Error opening {app_name}: {e}"
            self._log_command('open_app', app_name, False)
            return message
    
    def open_website(self, website_url):
        """
        Open a website in default browser
        
        Args:
            website_url: URL of the website
            
        Returns:
            Success message
        """
        try:
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url
            
            webbrowser.open(website_url)
            message = f"✓ Opening {website_url}"
            self._log_command('open_website', website_url, True)
            return message
        except Exception as e:
            message = f"✗ Error opening website: {e}"
            self._log_command('open_website', website_url, False)
            return message
    
    def search_google(self, query):
        """
        Search Google for a query
        
        Args:
            query: Search query
            
        Returns:
            Success message
        """
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return self.open_website(search_url)
    
    def open_youtube(self, query=""):
        """
        Open YouTube or search for video
        
        Args:
            query: Optional search query
            
        Returns:
            Success message
        """
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        else:
            url = "https://www.youtube.com"
        
        return self.open_website(url)
    
    def shutdown_computer(self, delay=60):
        """
        Shutdown computer
        
        Args:
            delay: Delay in seconds before shutdown (default: 60)
            
        Returns:
            Confirmation message
        """
        try:
            if self.system == 'win32':
                subprocess.run(['shutdown', '/s', '/t', str(delay)])
            else:
                subprocess.run(['shutdown', '-h', f'+{delay//60}'])
            
            message = f"✓ Computer will shutdown in {delay} seconds"
            self._log_command('shutdown', '', True)
            return message
        except Exception as e:
            message = f"✗ Error initiating shutdown: {e}"
            self._log_command('shutdown', '', False)
            return message
    
    def restart_computer(self, delay=60):
        """
        Restart computer
        
        Args:
            delay: Delay in seconds before restart
            
        Returns:
            Confirmation message
        """
        try:
            if self.system == 'win32':
                subprocess.run(['shutdown', '/r', '/t', str(delay)])
            else:
                subprocess.run(['shutdown', '-r', f'+{delay//60}'])
            
            message = f"✓ Computer will restart in {delay} seconds"
            self._log_command('restart', '', True)
            return message
        except Exception as e:
            message = f"✗ Error initiating restart: {e}"
            self._log_command('restart', '', False)
            return message
    
    def execute_command(self, command):
        """
        Execute custom shell command
        
        Args:
            command: Shell command to execute
            
        Returns:
            Command output or error
        """
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            self._log_command('execute', command, True)
            return result.stdout if result.stdout else "Command executed"
        except subprocess.TimeoutExpired:
            message = "✗ Command timed out"
            self._log_command('execute', command, False)
            return message
        except Exception as e:
            message = f"✗ Error: {e}"
            self._log_command('execute', command, False)
            return message
    
    def get_system_info(self):
        """Get system information"""
        import platform
        info = {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
        }
        return info
    
    def _log_command(self, cmd_type, cmd_text, success):
        """Log executed command"""
        self.command_log.append({
            'type': cmd_type,
            'command': cmd_text,
            'success': success
        })
    
    def get_command_log(self):
        """Get command log"""
        return self.command_log


if __name__ == "__main__":
    # Test system commands
    cmds = SystemCommands()
    
    # Test opening website
    print(cmds.open_website("google.com"))
    
    # Test search
    print(cmds.search_google("Python programming"))
    
    # Test opening YouTube
    print(cmds.open_youtube("machine learning"))
    
    # Test system info
    print(cmds.get_system_info())
