# NeuroFusion AI + Siri Clone v9.0

![NeuroFusion AI Screenshot](https://images.pexels.com/photos/3495603/pexels-photo-3495603.jpeg)

Enhanced hybrid voice assistant with web interface and desktop integration.

## Features

- 🎙️ Voice command recognition
- 🌐 Web-based control panel
- 🖥️ Desktop application integration
- 🎨 Light/dark mode
- 📝 Command history
- 📊 System monitoring
- 🌦️ Weather forecasts
- 🎵 Media control
- 📸 Screenshot capture
- 🔒 System controls (lock, shutdown)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/neurofusion-ai.git
cd neurofusion-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys:
- Create/edit `config.json`
```json
{
  "wake_word": "neuro",
  "openweather_api_key": "your_api_key_here",
  "theme": "light"
}
```

## Usage

### Running the Application
```bash
python neurofusion_ai.py
```

### Voice Commands
- "Neuro open [application/website]"
- "Neuro search for [query]"
- "Neuro play [song/video] on YouTube"
- "Neuro weather in [location]"
- "Neuro system info"
- "Neuro lock screen"
- "Neuro tell me a joke"
- "Neuro what's the time"

### Web Interface
Access the web interface at: `http://localhost:8000`

## Configuration

Edit `config.json` to customize:
- Wake word
- Theme (light/dark)
- API keys
- Logging preferences

## Requirements

- Python 3.8+
- Modern web browser (Chrome/Firefox/Edge recommended)
- Microphone for voice commands

## Troubleshooting

**Voice recognition not working:**
- Ensure microphone access is granted
- Try using Chrome/Edge for best results
- Check console for errors

**Weather commands failing:**
- Verify OpenWeatherMap API key in config.json
- Check internet connection

## License

MIT License

## Screenshots

![Web Interface Light Mode](screenshots/light-mode.png)
![Web Interface Dark Mode](screenshots/dark-mode.png)

## Roadmap

- [ ] Mobile app integration
- [ ] Natural language processing
- [ ] Plugin system
- [ ] Multi-language support