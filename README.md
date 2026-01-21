# Tetris in Arcade

A barebones version of tetris made with the python **arcade** framework.

## Controls

- ← → Move
- ↑ Rotate
- ↓ Acclerate
- <kbd>SPACE</kbd> Pause/Play
- <kbd>ENTER</kbd> Restart

## How to Run (executable)

- Download a release your system can run & start the executable(EXE or ELF).
- If there is an executable in the *dist* folder, run it from there.

## Run from Source 

1. Install Python 3.10+
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:

   ```bash
   python game.py
   ```

## Build Instructions

You will be needing **pyinstaller** for this. Run the following in project directory:

  ```bash
  pyinstaller --clean game.py --onefile --add-data "assets;assets" --name tetris-game --icon="assets\icon.ico" --windowed
  ```

Result should appear in *dist* folder.

## Assets & Credits

- Game Framework: <u>Python Arcade</u>
- Fonts: PixelMix, Noto Sans Math
