# Teachemon
Teachemon is a card-based game that uses concepts from Pokemon, to make a video game that connects the Newport High School Community.

The cards consist of teachers from the school, and each teachers have their own unique abilities that are associated with their identity. 

The game is built mainly using python and socket, with other python dependencies.

## Overview

In Teachemon, two trainers face off in tactical turn-based combat.
Each player brings a team of 4 Teachemon cards, each with unique stats, types, and moves.

During a turn, the player can:
- **Attack** - Use the current Teachemon's moves to deal damage
- **Use Item** - Use items that can enhance your current Teachemon (this includes increased attack, increased defense, and gaining more energy.
- **Swap** - Switch to another Teachemon in the team.

Both players choose their actions simultaneously, so prediction and strategy is key.

## Game Rules

Each Teachmon has HP, Type, and 3 moves with different:
 - Damage
 - Speed
 - Energy Cost

The move with faster speed executes first.
When a Teachemon's HP reaches 0, it dies.
The first player to knock out all 4 opponent Teachemon wins.

## Game Modes

- **Singleplayer** - Fight against the AI powered by 'MaskablePPO' reinforcement learning.
- **Multiplayer** - Connect to the server over sockets to battle a real player.

## Instructions to run the code:
/server is independent from rest of the code, as it is a code for server host.

1. Make sure the server is hosted. Run server.py in the server directory, and the code should print "Listening..." when it is connected

2. Run main game code, by running main.py in the main directory. 




Developed by:
- Henry (Hyeoncheol) Yang
- Esther Carl
- Daniel Choi
- Jessica Ni
- Cassidy Tran

