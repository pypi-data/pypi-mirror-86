# tictactoe-abhay

## Installation

```
pip install tictactoe-abhay
```
## Example

```
from tic_tac_toe.TicTacToe import TicTacToe
game = TicTacToe("player 1", "player 2")
game.play_turn(5)
print(game.get_board())
```
```
>>>|1|2|3|
   -------
   |4|x|6|
   -------
   |7|8|9|
```

## Methods and Attributes
### Attributes
```
    player_1:str name of player 1 (Default "player_1")
    player_2:str name of player 2 (Default "player_2")
    winner:str name of player if winner (Default "")
    player_1_turn:bool priorty bit to keep track of player order(Init true)
    board:list stores the state of the board
```
### Methods
#### get_winner()
```get the name of the winner```
#### get_board()
```return a str state of the board```
#### play_turn(spot:int)
```
updates the board based on the spot and return status
status(int):
   +1  : game has ended
   +0  : successful in placing the spot
   -1 : filled spot was selected
```
