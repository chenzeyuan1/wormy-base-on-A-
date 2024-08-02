# Automatic Pathfinding System Based on A* Algorithm with Snake Game as the Carrier
This is an automatic pathfinding system that leverages the A* algorithm, utilizing the classic Snake game as its platform. By building upon open-source code for a Snake game, I have designed an automatic control system based on the A* algorithm. When an optimal path to the apple exists, the system directs the snake to move directly towards the apple. However, if there is no optimal path to the apple, the system first identifies the optimal path to the snake's tail, and then proceeds to find the optimal path from the tail to the apple.
## System Functionality
- Direct Path to Apple: If an optimal path from the snake's current position to the apple exists, the system directs the snake to follow this path to reach and eat the apple promptly.
- Tail Priority Strategy: In cases where a direct optimal path to the apple is obstructed (e.g., by walls or the snake's own body), the system prioritizes finding an optimal path to the snake's tail first. This serves as a preliminary strategy to navigate around obstacles or reposition itself. Subsequently, it seeks an optimal path from the tail to the apple, allowing the snake to successfully consume the apple.
## Technical Implementation
-  A\* Algorithm: As the core algorithm, A employs heuristic search to find the lowest-cost path between a start node and a goal node within a graph. In this system, it computes the optimal path for the snake to reach the apple (or its tail).
- Open-Source Snake Game: Serving as the foundation, this platform provides a visual game environment that showcases the effectiveness of the A* algorithm's application.
- Automatic Control System: Based on the computed paths from the A* algorithm, the automatic control system generates a series of control commands, such as moving up, down, left, or right, to guide the snake along the optimal path.
## Application Value
This system not only demonstrates the efficacy of the A* algorithm in solving complex pathfinding problems but also enhances the educational fun and practicality of algorithm learning through a real-world game application. Furthermore, it serves as a starting point for further research and development of intelligent game AIs, offering insights and technical support for designing more sophisticated game strategies.
## How to Run the Program
This program relies on pygame, a popular Python library for creating video games. Before running the program, it is necessary to install pygame using pip, the Python package installer. Additionally, the program is compatible with Python versions 3.12.4 and above. Below are the steps to follow to successfully run the program:
Install Python (If Not Already Installed):
Ensure you have Python installed on your system, with a version of 3.12.4 or higher. You can check your Python version by opening a terminal or command prompt and typing python **version or python3** version (depending on your system configuration). If you do not have Python installed, download and install it from the official Python website.
- Download or Clone the Program:
Obtain the program files.You can download the source code as a zip file,or clone the repository using Git.
- Navigate to the Program Directory:
In your terminal or command prompt, change the current directory to the one containing the program files. Use the cd command followed by the path to the directory, e.g., cd /path/to/your/program.
- Run the Program:
Once you are in the correct directory, execute the 毛毛虫.py Python script file to run the program. 
If python points to the wrong version or if you're using a system where python3 is the standard command for Python 3.
- Verify the Program is Running:
Depending on the program's design, you should see a window or a graphical interface appear, indicating that the program is successfully running. If the program does not behave as expected, check the terminal or command prompt for any error messages that may provide clues on how to resolve the issue.
By following these steps, you should be able to run the program successfully, assuming all the necessary dependencies are met and the program files are intact.
