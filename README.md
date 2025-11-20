# 🧩2048 – Python Pygame Edition

A polished, animated, and fully modular recreation of the classic 2048 game using Pygame.
Features smooth tile movement, merge animations, clean architecture, and a customizable renderer.
## ✨Features

- Smooth animations (sliding + merge pop-effects)
- Dynamic tile rendering with smaller, auto-scaling numbers
- Scoring system
- Clean color palette and polished UI
- Modular codebase (logic, rendering, constants separated)
- Easily extendable (add textures, themes, grid sizes)
- Uses an assets/ folder for icons or future tile images
- Restart and ❌ Quit support


## 📁Folder Structure

```
project/
│
├── assets/
│     └── logo.png
├── doc/
│     └── Python Project.pptx
├── constants.py
├── game_logic.py
├── render.py
├── main.py
├── requirements.txt
└── run.bat
```
## 🛠️Tech Stack
- Python 3.10+
- Pygame
- pygame-menu (optional, if menu used)
- NumPy
## 🚀Run Locally

1. Clone the repository
```bash
git clone https://github.com/NirajPujari/Python-Game
cd Python-Game
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the game
    ```bash
    python main.py
    ```
    Windows users
    - Double-click:
        ```
        run.bat
        ```
    - Run on cmd:
        ```
        ./run.bat
        ```

## 📖About the Project / Details

This project is a clean and extendable re-implementation of 2048, designed specifically for readability and modding.
All visuals, logic, movement, animation timing, and grid calculations are separated into individual modules for maximum clarity.
The game includes fluid tile sliding, merge animations, and a polished UI—providing a more modern feel compared to beginner-level Pygame projects.

It serves both as:
- a fun playable game, and
- a high-quality reference for structuring Pygame applications.
## License
MIT


## Authors

- [@Niraj Pujari](https://github.com/NirajPujari)