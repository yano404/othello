|[English](README_en.md)|[日本語](README.md)|

# Othello
This is the Othello game (Human vs Computer).
Computer uses αβmethod or minmax method.

## How to play
You can start the game by `python3 run.py`.

```
$ python3 run.py
Your stone is Black(B)
====================================
Turn Count: 0
Turn:  B
====================================
     1   2   3   4   5   6   7   8  
   +---+---+---+---+---+---+---+---+
 1 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 2 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 3 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 4 |   |   |   | W | B |   |   |   |
   +---+---+---+---+---+---+---+---+
 5 |   |   |   | B | W |   |   |   |
   +---+---+---+---+---+---+---+---+
 6 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 7 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 8 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
Enter the position you want to put the stone.
row > 3 ↵
col > 4 ↵
====================================
Turn Count: 1
Turn:  W
====================================
     1   2   3   4   5   6   7   8  
   +---+---+---+---+---+---+---+---+
 1 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 2 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 3 |   |   |   | B |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 4 |   |   |   | B | B |   |   |   |
   +---+---+---+---+---+---+---+---+
 5 |   |   |   | B | W |   |   |   |
   +---+---+---+---+---+---+---+---+
 6 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 7 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 8 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
score: 0
====================================
Turn Count: 2
Turn:  B
====================================
     1   2   3   4   5   6   7   8  
   +---+---+---+---+---+---+---+---+
 1 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 2 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 3 |   |   |   | B |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 4 |   |   |   | B | B |   |   |   |
   +---+---+---+---+---+---+---+---+
 5 |   |   | W | W | W |   |   |   |
   +---+---+---+---+---+---+---+---+
 6 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 7 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 8 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
Enter the position you want to put the stone.
row >
```
