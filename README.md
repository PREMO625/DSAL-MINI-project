# Snake and Ladder Game

A classic Snake and Ladder board game implemented in Python using Pygame.

## Features

- Interactive game board with snakes and ladders
- Support for 2-4 players
- Animated dice rolling
- Particle effects for movement
- Clean and intuitive UI
- Player turn indicators
- Win condition detection

## Gameplay Demo

### Option 1: Download and View Locally

You can download the gameplay video directly from the repository and play it on your device: [Download Gameplay Video](Untitled%20video%20-%20Made%20with%20Clipchamp%20(1).mp4)

### Option 2: Direct Embed (Works in local Markdown viewers, may not work on GitHub for large videos)

<video width="640" height="360" controls>
  <source src="Untitled video - Made with Clipchamp (1).mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

*Note: This direct embed may not work on GitHub for videos around 60MB in size.*

### Option 3: Watch on GitHub

The video is available in the GitHub repository. You can view it directly at:

[View Gameplay Video on GitHub](https://github.com/PREMO625/DSAL-MINI-project/blob/main/Untitled%20video%20-%20Made%20with%20Clipchamp%20(1).mp4)

For embedding in GitHub markdown (may not display properly for videos around 60MB):

```markdown
![Gameplay Demo](https://github.com/PREMO625/DSAL-MINI-project/raw/main/Untitled%20video%20-%20Made%20with%20Clipchamp%20(1).mp4)
```

Or using GitHub's video tag format:

```html
<video src="https://github.com/PREMO625/DSAL-MINI-project/raw/main/Untitled%20video%20-%20Made%20with%20Clipchamp%20(1).mp4" controls="controls" muted="muted" style="max-width:100%;"></video>
```

## Prerequisites

- Python 3.7 or higher
- Pygame library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/snake-and-ladder.git
cd snake-and-ladder
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python snake_and_ladder.py
```

2. Game Rules:
   - Players take turns rolling the dice
   - Move your piece according to the dice roll
   - Land on a ladder to climb up
   - Land on a snake head to slide down
   - First player to reach position 100 wins

## Controls

- Mouse click to roll dice and interact with buttons
- ESC to quit game
- ENTER to confirm selections
- BACKSPACE to delete text in input fields

## Game Elements

- **Snakes**: Positions 16→4, 47→26, 49→11, 65→53, 62→19, 64→60, 87→24, 93→73, 95→75, 98→78
- **Ladders**: Positions 1→38, 4→14, 9→31, 21→42, 28→84, 36→44, 51→67, 71→91, 80→100

## Project Structure

```
snake-and-ladder/
│
├── snake_and_ladder.py    # Main game file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .gitignore           # Git ignore file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Pygame
- Inspired by the classic Snake and Ladder board game