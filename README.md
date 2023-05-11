# Game 2048
Game 2048 with manual and AI play options. Implemented with 3-layer expectimax algorithm with AI player modeled as max player and computer as chance player.

## Files
**main.py**: 2048 Game UI  
**game.py**: 2048 game engine  
**ai.py**: AI simulator  
**test.py**: Automated testing suites  
**test_states, test_sols**: test case parameters  

## Usage
To run the program:  
```
python main.py
```

To run automated tests:
```
python main -t 1
python main -t 2
```

## in-game keyboard options
* keyboard actions up, down, left, right: sliding direction
* keyboard enter: starts/stop AI player
* 'r': restart game
* 'u': undo a move
* '3'-'7': change board size
* 'g': toggle grayscale
* 'e': switch to stronger AI player
