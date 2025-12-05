# Dragons & Dungeons - Full Stack Game

A complete D&D-style RPG game with AI Dungeon Master powered by Ollama.

## 🚀 Tech Stack

- **Backend**: Python + Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **AI**: Ollama (Llama 3.2)

## 📁 Project Structure

```
dnd-game/
├── app.py                 # Flask backend
├── database.sql           # Database schema & data
├── requirements.txt       # Python dependencies
├── static/
│   ├── style.css         # Main stylesheet
│   ├── characters.js     # Characters page logic
│   ├── adventure.js      # Combat system
│   └── dm.js             # AI chat logic
└── templates/
    ├── index.html        # Home page
    ├── characters.html   # Character management
    ├── adventure.html    # Combat/adventure
    ├── dm.html           # AI Dungeon Master chat
    └── shop.html         # Shop (TODO)
```

## 🔧 Setup Instructions

### 1. Install MySQL

```bash
# Ubuntu/Debian
sudo apt install mysql-server

# macOS
brew install mysql

# Windows: Download from mysql.com
```

### 2. Setup Database

```bash
# Login to MySQL
mysql -u root -p

# Run the database.sql file
source database.sql

# Or copy-paste the SQL commands
```

### 3. Install Python Dependencies

```bash
pip install flask flask-cors mysql-connector-python requests
```

### 4. Install & Run Ollama

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull the model
ollama pull llama3.2

# Run Ollama (keep this running in a terminal)
ollama run llama3.2
```

### 5. Configure Database Connection

Edit `app.py` line 10-15:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD',  # Change this!
    'database': 'dnd_game'
}
```

### 6. Run the Application

```bash
python app.py
```

Visit: `http://localhost:5000`

## 🎮 Features

### ✅ Working Features

- **Character Creation**: Create heroes with races & classes
- **Dynamic Stats**: Race + Class + Base stats calculation
- **Health Bars**: Real-time animated HP bars
- **Combat System**: Turn-based fighting with damage calculation
- **XP & Gold**: Earn rewards from victories
- **AI Dungeon Master**: Chat with AI for storytelling
- **Responsive UI**: Works on desktop & mobile

### 🎯 Game Flow

1. **Home** → Choose what to do
2. **Characters** → Create/view heroes
3. **Adventure** → Select character → Start combat
4. **Combat** → Attack/Defend/Skill/Flee
5. **Victory** → Earn XP & Gold
6. **Shop** → Buy items (coming soon)
7. **DM Chat** → Talk to AI anytime

## 🗃️ Database Tables

- **races** - Character races (Human, Elf, Orc, etc.)
- **classes** - Character classes (Fighter, Sorcerer, etc.)
- **characters** - Player characters
- **items** - Weapons, armor, artifacts, consumables
- **inventory** - Character items
- **combat_log** - Battle history

## 🤖 Ollama Integration

The AI Dungeon Master:
- Knows your character details
- Responds contextually
- Creates immersive stories
- Helps with game questions

**Make sure Ollama is running before using DM chat!**

## 🎨 Customization

### Change Colors

Edit `static/style.css`:
- `.home-bg` - Home page gradient
- `.characters-bg` - Characters page
- `.adventure-bg` - Adventure page
- `.dm-bg` - DM chat page

### Add New Items

Edit `database.sql` items section and re-run SQL.

### Change AI Model

In `app.py` line 40, change `'model': 'llama3.2'` to any Ollama model.

## 🐛 Troubleshooting

**Database Connection Error**
- Check MySQL is running: `sudo systemctl status mysql`
- Verify credentials in `app.py`

**Ollama Not Working**
- Ensure Ollama is running: `ollama run llama3.2`
- Check URL: `http://localhost:11434`

**Health Bars Not Updating**
- Clear browser cache
- Check browser console for errors

**Characters Not Loading**
- Verify database has data: `SELECT * FROM characters;`
- Check Flask console for errors

## 📝 TODO Features

- [ ] Shop system with buying/selling
- [ ] Equipment system (equip items)
- [ ] More enemy types
- [ ] Boss battles
- [ ] Skill/spell system
- [ ] Party system (multiple characters)
- [ ] Save/load game states
- [ ] Achievement system

## 🎓 Learning Resources

- Flask: https://flask.palletsprojects.com/
- MySQL: https://dev.mysql.com/doc/
- Ollama: https://ollama.ai/
- JavaScript: https://developer.mozilla.org/

## 📄 License

Free to use and modify for learning purposes!

## 🤝 Contributing

Feel free to fork and improve! Some ideas:
- Add sound effects
- Implement shop system
- Create more item types
- Add multiplayer features
- Improve AI prompts

---

**Enjoy your adventure! 🐉⚔️**
