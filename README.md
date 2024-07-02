# space-shooter

## Overview
    This is simple space shooter game made using pygame. This project is create with intention of learning how to save and load game from local device. This game is still incompleted but is playable and contains 20 levels currently.
    **battle your way through galaxies filled with danger and excitement 😉.**

## Getting Started

To get started, you'll need to clone repo and create a virtual environment and install the required packages. Here are the steps:

**clone the repository"**
```bash
git clone https://github.com/FluffyRudy/space-shooter.git
```

**Create a virtual environment:**
Open a terminal and navigate to the directory where you cloned the repository. Then, run the following command to create a new virtual environment:
This will create a new virtual environment named `venv`.
```bash
cd space-shooter
python3 -m venv .env
```

**Activate the virtual environment:**

Depending on your operating system, activate virtual environment:
- **Linux/macOS:**

  ```
  source .env/bin/activate
  ```

- **Windows:**

  ```
  .env\Scripts\activate
  ```

**Install the required packages:**

Once the virtual environment is activated, you can install the required packages by running the following command:
```bash
pip install -r requirements.txt
```

**Running the game**

```bash
python3 main.py
```

## Current Features
    - Animated background
    - Simple animated text
    - Enemy spawning based on probability assigned to them
    - Obstacle occuring at random time
    - Difficulty increases as level increases
    - Can select any completed level
    - Simple enemy ai
    - Animated title
    - Loading levels from locally saved data
    - Generate level data from script itself
    - Custom widgets like button, state button and scrollbox

## Future Enhancements
    - Add boss
    - Add shop to purchase and upgrade
    - Add more obastacle
    - Add other different enemies
    - Improve the widgets UI

## Installation

## Credits
**Sound Effect from** <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=72679">Pixabay</a>

**Image assets from**
<ul>
    <li>
        <a href="https://foozlecc.itch.io/void-environment-pack">void-environment-pack</a>
    </li>
    <li>
        <a href="https://pixel-carvel.itch.io/shoot-em-up-enemies-ships-t1">Enemies ship and explosion</a>
    </li>
    <li>
        <a href="https://piiixl.itch.io/space/">Animated space background</a>
    </li>
    <li>
        <a href="https://free-game-assets.itch.io/free-space-shooter-game-user-interface">Menu UI</a>
    </li>
    
</ul>