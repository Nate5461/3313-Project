#include "Constants.h"
#include "Board.h"

Board::Board() {
    // Initialize the board with the default values
    // ...
}

Board::Board(int numOfRows, int numOfColumns, int checkersInARow) {
    // Initialize the board with the given values
    // ...
}

Board::Board(const Board& board) {
    // Copy the values from the given board
    // ...
}

void Board::makeMove(int col, int player) {
    // Make a move
    // ...
}

bool Board::canMove(int row, int col) {
    // Check if a move can be made
    // ...
}

bool Board::checkFullColumn(int col) {
    // Check if a column is full
    // ...
}

int Board::getEmptyRowPosition(int col) {
    // Get the position of the first empty row in a column
    // ...
}

std::vector<Board> Board::getChildren(int player) {
    // Generate the children of the state
    // ...
}

int Board::evaluate() {
    // Evaluate the board
    // ...
}

bool Board::checkWinState() {
    // Check if someone has won the game
    // ...
}
