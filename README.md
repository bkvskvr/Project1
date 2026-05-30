🎮 **Pygame Battleship (Морський бій)**

This is a classic Battleship game implemented in Python using the Pygame library. 
The project features a complete Player vs. Bot gameplay loop, interactive ship placement, smart AI logic, sound effects, and visual animations.

🌟 **Key Features**

* **Interactive Ship Placement:** A visual arsenal to select ships and place them on the grid, complete with hover shadows and orientation controls.
* **Smart AI Opponent:** The bot features a strategic algorithm to hunt down and sink ships logically after a successful initial hit.
* **Game Logic:**
  * Strict collision detection (ships cannot overlap or touch each other).
  * Automatic perimeter marking (water/misses) around destroyed ships for both the player and the bot.
  * Turn-based mechanics with extra moves upon successful hits.
* **Interface and Rendering:**
  * Clean UI with custom assets for ships and destroyed states.
  * Frame-by-frame explosion animations when a ship is sunk.
  * A "Game Over" overlay showing the final result with options to restart or exit.
* **Sound Management:** Integrated audio feedback for hits, misses, and sinking ships.

❓ **How to Play**

* **Placement Phase:**
  * `Left Click` : Select a ship from the right panel and place it on your left grid.
  * `Arrow Keys` : Precisely control the ship's orientation:
    * `Right` / `Left` : Horizontal orientations.
    * `Up` / `Down` : Vertical orientations.
  * `R` : Quick toggle between horizontal and vertical.
* **Battle Phase:**
  * `Left Click` : Fire at the opponent's grid on the right side of the screen.
* **Game Control:**
  * `R` : Restart the game (available on the Game Over screen).
  * `ESC` : Exit the game.
    
🛠 **Installation and Setup**

To run the game, you will need Python and the `pygame` library.
1. **Clone the repository:**
   ```bash
   git clone https://github.com/bkvskvr/Project1.git
   cd Project1
2. **Install dependencies: You will only need pygame.**
   ```bash
   pip install pygame
3. **Run the game: The main entry point is main.py.**
   ```bash
   python main.py
   
📍 **Project structure**

```mermaid
classDiagram
    class Ship {
        +int length
        +String orientation
        +List coordinates
        +int lives
        +set_coordinates(x, y)
        +hit()
        +defeated() bool
    }

    class Board {
        +List~List~int~~ field
        +List~Ship~ ships
        +add_ship(ship) bool
        +shot(x, y) bool/None
        +auto_place_ships()
        +mark_destroyed_perimeter(ship)
    }

    class Player {
        +String name
        +Board board
        +Board enemy_board
        +make_shot(x, y) bool
        +is_defeated() bool
    }

    class Bot {
        +Set shoted
        +List possible_opt
        +get_move() tuple
        +register_hit(row, col)
        +make_turn(player_board, destroyed_ships) String
    }

    class Audio {
        +load_sound(name, path)
        +play(name)
    }

    %% Зв'язки між класами (Relationships)
    Player <|-- Bot : Успадкування (Inheritance)
    Player --> Board : Використовує (Association)
    Board "1" *-- "*" Ship : Містить (Composition)
