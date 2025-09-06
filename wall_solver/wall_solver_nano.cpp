// =======================================================================
//   PATH OPTIMIZATION MODULE (for Algorithm Engineer)
//   Platform: Arduino Nano
// =======================================================================

#include <cstdint> 
typedef uint8_t byte; 

// --- Configuration & Data Structures ---
#define MAZE_WIDTH 16
#define MAZE_HEIGHT 16
#define GOAL_X 7
#define GOAL_Y 7

#define NORTH 1
#define EAST  2
#define SOUTH 4
#define WEST  8
#define EXPLORED 16

// INPUT: The map of the known world. The hardware/exploration team updates this array.
byte maze[MAZE_WIDTH][MAZE_HEIGHT];

// INTERNAL: Grid to store shortest path distances, calculated by your algorithm.
int distances[MAZE_WIDTH][MAZE_HEIGHT];

// Helper struct and queue for the BFS algorithm.
struct Point {
  int x;
  int y;
};
Point queue[MAZE_WIDTH * MAZE_HEIGHT];
int queueHead = 0;
int queueTail = 0;

/**
 * Main algorithm (Flood Fill/BFS) to calculate the shortest path to the goal.
 * This is called every time the main loop gets new map data.
 */
void recomputePath_FloodFill() {
  for (int i = 0; i < MAZE_WIDTH; i++) {
    for (int j = 0; j < MAZE_HEIGHT; j++) {
      distances[i][j] = -1; // -1 means unvisited
    }
  }
  queueHead = 0;
  queueTail = 0;

  // Start the flood from the goal center (assuming a 2x2 goal)
  distances[GOAL_X][GOAL_Y] = 0;
  distances[GOAL_X + 1][GOAL_Y] = 0;
  distances[GOAL_X][GOAL_Y + 1] = 0;
  distances[GOAL_X + 1][GOAL_Y + 1] = 0;
  
  queue[queueTail++] = {GOAL_X, GOAL_Y};
  queue[queueTail++] = {GOAL_X + 1, GOAL_Y};
  queue[queueTail++] = {GOAL_X, GOAL_Y + 1};
  queue[queueTail++] = {GOAL_X + 1, GOAL_Y + 1};

  while (queueHead < queueTail) {
    Point current = queue[queueHead++];

    if (current.y > 0 && !(maze[current.x][current.y] & NORTH) && distances[current.x][current.y - 1] == -1) {
      distances[current.x][current.y - 1] = distances[current.x][current.y] + 1;
      queue[queueTail++] = {current.x, current.y - 1};
    }
    if (current.x < MAZE_WIDTH - 1 && !(maze[current.x][current.y] & EAST) && distances[current.x + 1][current.y] == -1) {
      distances[current.x + 1][current.y] = distances[current.x][current.y] + 1;
      queue[queueTail++] = {current.x + 1, current.y};
    }
    if (current.y < MAZE_HEIGHT - 1 && !(maze[current.x][current.y] & SOUTH) && distances[current.x][current.y + 1] == -1) {
      distances[current.x][current.y + 1] = distances[current.x][current.y] + 1;
      queue[queueTail++] = {current.x, current.y + 1};
    }
    if (current.x > 0 && !(maze[current.x][current.y] & WEST) && distances[current.x - 1][current.y] == -1) {
      distances[current.x - 1][current.y] = distances[current.x][current.y] + 1;
      queue[queueTail++] = {current.x - 1, current.y};
    }
  }
}

/**
 * Provides the optimal direction for the next move based on the re-computed distances.
 * @param currentX The robot's current X position.
 * @param currentY The robot's current Y position.
 * @return The best direction (NORTH, EAST, SOUTH, WEST), or 0 if stuck.
 */
byte getOptimalMove(int currentX, int currentY) {
  int currentDist = distances[currentX][currentY];
  if(currentDist == -1) return 0; // No known path from this cell

  int minDist = currentDist;
  byte bestDir = 0;

  if (currentY > 0 && !(maze[currentX][currentY] & NORTH)) {
    int neighborDist = distances[currentX][currentY - 1];
    if (neighborDist != -1 && neighborDist < minDist) {
      minDist = neighborDist;
      bestDir = NORTH;
    }
  }
  if (currentX < MAZE_WIDTH - 1 && !(maze[currentX][currentY] & EAST)) {
    int neighborDist = distances[currentX + 1][currentY];
    if (neighborDist != -1 && neighborDist < minDist) {
      minDist = neighborDist;
      bestDir = EAST;
    }
  }
  if (currentY < MAZE_HEIGHT - 1 && !(maze[currentX][currentY] & SOUTH)) {
    int neighborDist = distances[currentX][currentY + 1];
    if (neighborDist != -1 && neighborDist < minDist) {
      minDist = neighborDist;
      bestDir = SOUTH;
    }
  }
  if (currentX > 0 && !(maze[currentX][currentY] & WEST)) {
    int neighborDist = distances[currentX - 1][currentY];
    if (neighborDist != -1 && neighborDist < minDist) {
      minDist = neighborDist;
      bestDir = WEST;
    }
  }

  return bestDir;
}