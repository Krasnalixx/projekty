# Chess Game

Welcome to my Chess Game, a fully interactive digital chess experience built with PyQt5. This project consists of three main modules that handle everything from the graphical user interface to the game mechanics.

## Modules

1. **main.py**: This is the core file of the game, where the main application is run. It includes the rules of the game and sets up the graphical user interface (GUI). It utilizes PyQt5 to manage game windows, dialogs, and other GUI components.

2. **figury.py**: This file contains the definitions of the chess pieces and classes related to piece promotion and reviewing past moves. It plays a crucial role in defining the behavior of each piece on the chessboard.

3. **zasoby_rc.py**: This module handles the graphical resources, storing representations of the chess pieces used in the game's GUI.

## Dependencies

To run this game, you will need Python and PyQt5. Here's how you can install PyQt5 if you haven't done so yet:

```bash
pip install PyQt5
```
## Running the game

To start the game, navigate to the directory containing the game's files and run the following command:
``` bash
python main.py
```

## Gameplay

The game follows standard chess rules. You can move pieces by clicking on them and then clicking on the destination square. Special game options like piece promotion are handled via dialog boxes that appear when necessary.

## Contributions

Contributions to this project are welcome. Please feel free to fork the repository, make changes, and submit a pull request.

## License

This project is open-source and available under the MIT License.

