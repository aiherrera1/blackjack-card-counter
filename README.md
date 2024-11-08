# Blackjack Card Counting and Strategy Interface

This project provides a graphical user interface (GUI) for simulating and analyzing blackjack strategies using card counting techniques. The interface is built using Python's `tkinter` library and allows users to interact with a virtual shoe of cards, update counts, and observe optimal moves based on the current card composition.

**Disclaimer:** This project is intended for educational purposes only, focusing on the mathematical and statistical aspects of blackjack. It does not promote or endorse gambling in any form.

## Features

- **Card Input:** Buttons and key bindings to simulate drawing cards from the shoe.
- **Counts Display:** Real-time updates of card counts, running count, true count, and expectation.
- **Strategy Board:** Dynamic strategy recommendations (Hit, Stand, Double, Split) based on the current card composition.
- **Controls:** Option to set the number of decks and shuffle the shoe.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- The `tkinter` library (usually included with Python installations).
- Clone or download this repository.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/blackjack-strategy-interface.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd blackjack-strategy-interface
   ```

3. **Ensure all Python files (`main.py`, `interface.py`, `shoe.py`, `stats.py`) are in the same directory.**

### Running the Application

Execute the following command in your terminal:

```bash
python main.py
```

This will launch the GUI application.

## File Structure

- `main.py`: The main script to run the application.
- `interface.py`: Contains the `Interface` class that builds the GUI.
- `shoe.py`: Contains the `Shoe` class representing the deck(s) of cards.
- `stats.py`: Contains the `Stats` class for calculating strategy recommendations.
