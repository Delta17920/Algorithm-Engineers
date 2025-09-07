/*
  A* Pathfinding on Arduino Nano (10x10 grid)
  - 0 = free, 1 = obstacle
  - 4-connected neighbors, cost = 1 per move
  - Manhattan heuristic
  - Linear-scan open list to save RAM
  - Prints path coordinates, turn instructions, and ASCII map

  Notes:
  - Uses uint8_t for costs (good up to grids where max path < 255)
  - Fits within 2KB SRAM on Nano for 10x10
*/

#include <Arduino.h>

static const uint8_t W = 10;
static const uint8_t H = 10;
static const uint8_t INF8 = 255;

// Maze grid (edit obstacles for different tests).
// S = (0,0), G = (9,9) in this example.
uint8_t grid[H][W] = {
  {0,0,0,0,0, 0,1,0,0,0},
  {0,1,1,0,1, 0,1,0,1,0},
  {0,0,0,0,1, 0,0,0,1,0},
  {1,1,0,1,0, 0,1,0,1,0},
  {0,0,0,1,0, 1,0,0,0,0},

  {0,1,0,0,0, 1,0,1,1,0},
  {0,1,1,1,0, 0,0,0,1,0},
  {0,0,0,1,0, 1,1,0,1,0},
  {0,1,0,0,0, 0,0,0,1,0},
  {0,0,0,1,1, 0,0,0,0,0}
};

// Cost arrays
uint8_t gScore[H][W];
uint8_t fScore[H][W];

// Parent map
struct Parent { int8_t px, py; };
Parent cameFrom[H][W];

// Bookkeeping
bool closedSet[H][W];
bool inOpen[H][W];

// Open list (linear scan)
struct OpenEntry { uint8_t x, y; };
OpenEntry openList[W * H];
uint8_t openCount = 0;

// Heuristic: Manhattan distance
inline uint8_t manhattan(uint8_t x1, uint8_t y1, uint8_t x2, uint8_t y2) {
  return (uint8_t)(abs((int)x1 - (int)x2) + abs((int)y1 - (int)y2));
}

void openClear() { openCount = 0; }
void openPush(uint8_t x, uint8_t y) {
  if (!inOpen[y][x]) {
    openList[openCount++] = {x, y};
    inOpen[y][x] = true;
  }
}

// Pop the cell with the lowest fScore via linear scan
bool openPopLowest(uint8_t &x, uint8_t &y) {
  if (openCount == 0) return false;
  uint8_t bestIdx = 0;
  uint8_t bx = openList.x, by = openList.y;
  uint8_t bestF = fScore[by][bx];
  for (uint8_t i = 1; i < openCount; i++) {
    uint8_t ox = openList[i].x, oy = openList[i].y;
    uint8_t f  = fScore[oy][ox];
    if (f < bestF) {
      bestF = f; bestIdx = i;
    }
  }
  x = openList[bestIdx].x; y = openList[bestIdx].y;
  // remove best by swapping with last
  inOpen[y][x] = false;
  openList[bestIdx] = openList[openCount - 1];
  openCount--;
  return true;
}

void printGrid() {
  Serial.println(F("Grid (0=free, 1=wall):"));
  for (uint8_t y = 0; y < H; y++) {
    for (uint8_t x = 0; x < W; x++) {
      Serial.print(grid[y][x]); Serial.print(' ');
    }
    Serial.println();
  }
}

// Reconstruct path into tmp[] with length len (start->goal order)
bool reconstructPath(uint8_t sx, uint8_t sy, uint8_t gx, uint8_t gy,
                     OpenEntry *tmp
