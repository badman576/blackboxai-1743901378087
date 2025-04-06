#!/usr/bin/env python3
"""
NEUROFUSION AI + SIRI CLONE v9.0
Enhanced Hybrid Web/Desktop Edition
"""

import os
import sys
import json
import re
import time
import logging
import threading
import webbrowser
import subprocess
try:
    import pyautogui
    GUI_AVAILABLE = True
except (ImportError, KeyError):
    GUI_AVAILABLE = False
    import warnings
    warnings.warn("GUI functions disabled - running in headless environment")
import psutil
import speech_recognition as sr
from typing import Optional, Dict, List, Deque, Tuple, Any
from collections import deque
from pathlib import Path
import platform
import datetime
import pyjokes

class SystemCapabilities:
    @staticmethod
    def check():
        capabilities = {
            'gui': False,
            'microphone': False,
            'youtube': False,
            'screenshots': False,
            'system_controls': False
        }
        
        try:
            import pyautogui
            capabilities['gui'] = True
            capabilities['screenshots'] = True
        except:
            pass
            
        try:
            import pyaudio
            capabilities['microphone'] = True
        except:
            pass
            
        try:
            import pywhatkit
            capabilities['youtube'] = True
        except:
            pass
            
        if platform.system() == "Windows":
            capabilities['system_controls'] = True
            
        return capabilities
try:
    import pywhatkit
    WHATKIT_AVAILABLE = True
except (ImportError, KeyError):
    WHATKIT_AVAILABLE = False
    import warnings
    warnings.warn("YouTube playback disabled - running in headless environment")
import requests
import pyperclip
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO

# Constants
MAX_COMMAND_LENGTH = 1000
DEFAULT_WAKE_WORD = "neuro"
CONFIG_FILE = "config.json"
LOG_DIR = "logs"

# Setup logging
def setup_logging() -> logging.Logger:
    logger = logging.getLogger('NeuroFusion')
    logger.setLevel(logging.DEBUG)
    
    logs_dir = Path(LOG_DIR)
    logs_dir.mkdir(exist_ok=True)
    
    # File handler
    file_handler = logging.FileHandler(
        logs_dir/'neurofusion.log',
        encoding='utf-8'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

class CommandProcessor:
    @staticmethod
    def process(command: str) -> Tuple[str, str]:
        command = command.strip().lower()
        
        # Enhanced command patterns
        patterns = [
            (r'open\s+(?:the\s+)?(.+)', 'open'),
            (r'search\s+(?:for\s+)?(.+)', 'search'),
            (r'(?:volume|turn)\s+(up|down|mute)', 'volume'),
            (r'(exit|quit|shutdown|restart)', 'system'),
            (r'play\s+(.+)', 'media'),
            (r'play\s+(.+)\s+on\s+youtube', 'youtube'),
            (r'remind\s+me\s+to\s+(.+)', 'reminder'),
            (r'(tell me a )?joke( of the day)?', 'joke'),
            (r'screenshot', 'screenshot'),
            (r'weather\s+(?:in|for|at)?\s*(.+)', 'weather'),
            (r'calculate\s+(.+)', 'calculate'),
            (r'system\s+info', 'system_info'),
            (r'lock\s+screen', 'lock'),
            (r'what\'?s? time', 'time'),
            (r'what\'?s? date', 'date')
        ]
        
        for pattern, action in patterns:
            match = re.search(pattern, command)
            if match:
                return action, match.group(1) if match.groups() else ''
        
        return 'unknown', command

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            self.mic_available = True
        except (AttributeError, OSError):
            self.mic_available = False
            import warnings
            warnings.warn("Microphone access unavailable - running in limited mode")
        self.command_history = deque(maxlen=10)
        self.running = True
        self.load_config()
        
    def load_config(self):
        try:
            with open(CONFIG_FILE) as f:
                self.config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.config = {
                "wake_word": DEFAULT_WAKE_WORD,
                "theme": "light"
            }
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f)
    
    def listen(self) -> Optional[str]:
        try:
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio).lower()
                if self.config['wake_word'] in text:
                    return text.replace(self.config['wake_word'], '').strip()
                return text
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out")
            return None
        except Exception as e:
            logger.error(f"Voice recognition error: {e}")
            return None

    def execute_command(self, command: str) -> str:
        if not command or len(command) > MAX_COMMAND_LENGTH:
            return "Invalid command"
            
        action, param = CommandProcessor.process(command)
        self.command_history.append((command, datetime.datetime.now()))
        
        try:
            if action == 'open':
                return self._handle_open(param)
            elif action == 'search':
                return self._handle_search(param)
            elif action == 'volume':
                return self._adjust_volume(param)
            elif action == 'system':
                return self._handle_system_command(param)
            elif action == 'media':
                return f"Playing {param}"
            elif action == 'youtube':
                return self._play_youtube(param)
            elif action == 'reminder':
                return f"I'll remind you to {param}"
            elif action == 'joke':
                return pyjokes.get_joke()
            elif action == 'screenshot':
                return self._take_screenshot()
            elif action == 'weather':
                return self._get_weather(param)
            elif action == 'calculate':
                return self._calculate(param)
            elif action == 'system_info':
                return self._get_system_info()
            elif action == 'lock':
                return self._lock_screen()
            elif action == 'time':
                return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"
            elif action == 'date':
                return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
            else:
                return f"I don't understand: {command}"
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return f"Error executing command: {str(e)}"

    def _handle_open(self, param: str) -> str:
        try:
            os.startfile(param)
            return f"Opened {param}"
        except OSError:
            try:
                webbrowser.open(f"https://{param}")
                return f"Opened {param} in browser"
            except Exception as e:
                return f"Couldn't open {param}: {str(e)}"

    def _handle_search(self, query: str) -> str:
        webbrowser.open(f"https://google.com/search?q={query}")
        return f"Searching for {query}"

    def _adjust_volume(self, direction: str) -> str:
        if not GUI_AVAILABLE:
            return "Volume control unavailable in this environment"
        try:
            if direction == 'mute':
                pyautogui.press('volumemute')
                return "Toggled mute"
            else:
                key = 'volumeup' if direction == 'up' else 'volumedown'
                pyautogui.press(key)
                return f"Volume turned {direction}"
        except Exception as e:
            return f"Couldn't adjust volume: {str(e)}"

    def _handle_system_command(self, command: str) -> str:
        if command in ('exit', 'quit'):
            self.running = False
            return "Goodbye"
        elif command == 'shutdown':
            if platform.system() == "Windows":
                os.system("shutdown /s /t 30")
            return "Shutting down in 30 seconds"
        elif command == 'restart':
            if platform.system() == "Windows":
                os.system("shutdown /r /t 30")
            return "Restarting in 30 seconds"
        return "Unknown system command"

    def _play_youtube(self, query: str) -> str:
        if not WHATKIT_AVAILABLE:
            return "YouTube playback unavailable in this environment"
        try:
            pywhatkit.playonyt(query)
            return f"Playing {query} on YouTube"
        except Exception as e:
            return f"Couldn't play video: {str(e)}"

    def _take_screenshot(self) -> str:
        if not GUI_AVAILABLE:
            return "Screenshot functionality unavailable in this environment"
        try:
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = screenshot_dir / f"screenshot_{timestamp}.png"
            pyautogui.screenshot(str(filename))
            return f"Screenshot saved as {filename}"
        except Exception as e:
            return f"Couldn't take screenshot: {str(e)}"

    def _get_weather(self, location: str) -> str:
        try:
            if not location:
                location = "current location"
                ip_url = "https://ipinfo.io/json"
                response = requests.get(ip_url)
                location = response.json().get('city', 'current location')
            
            url = f"https://wttr.in/{location}?format=%C+%t+%w"
            response = requests.get(url)
            return f"Weather in {location}: {response.text.strip()}"
        except Exception as e:
            return f"Couldn't get weather: {str(e)}"

    def _calculate(self, expression: str) -> str:
        try:
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Couldn't calculate: {str(e)}"

    def _get_system_info(self) -> str:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            return (
                f"System Information:\n"
                f"OS: {platform.system()} {platform.release()}\n"
                f"CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%"
            )
        except Exception as e:
            return f"Couldn't get system info: {str(e)}"

    def _lock_screen(self) -> str:
        if not GUI_AVAILABLE:
            return "Screen lock unavailable in this environment"
        try:
            if platform.system() == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return "Screen locked"
            else:
                return "Screen lock not supported on this OS"
        except Exception as e:
            return f"Couldn't lock screen: {str(e)}"

# Web Interface
app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
assistant = VoiceAssistant()

@app.route('/')
def index():
    return render_template('index.html', theme=assistant.config.get('theme', 'light'))

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command', '')
    response = assistant.execute_command(command)
    return jsonify({'response': response})

@app.route('/settings')
def settings():
    return render_template('settings.html', config=assistant.config)

@socketio.on('connect')
def handle_connect():
    logger.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Client disconnected')

def run_web_interface():
    socketio.run(app, port=8000, debug=False)

if __name__ == "__main__":
    print("""
    NEUROFUSION AI + SIRI CLONE v9.0
    Enhanced Hybrid Web/Desktop Edition
    """)
    
    # Start web interface in background
    web_thread = threading.Thread(target=run_web_interface, daemon=True)
    web_thread.start()
    
    # Main voice loop
    try:
        while assistant.running:
            command = assistant.listen()
            if command:
                response = assistant.execute_command(command)
                print(f"AI: {response}")
                socketio.emit('command_response', {'command': command, 'response': response})
    except KeyboardInterrupt:
        print("\nShutting down...")