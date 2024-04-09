#pragma once
#include "Constants.h"
#include "Board.h"
#include <vector>
#include "Move.h"
#include <string>



class Board {
private:
    std::vector<std::vector<int>> gameBoard;
    int numOfRows;
    int numOfColumns;
    int checkersInARow;
    Move lastMove;
    int lastPlayer;
    int winner;
    bool overflow;
    bool gameOver;
    int turn;

public:
    Board();
    Board(int numOfRows, int numOfColumns, int checkersInARow);
    Board(const Board& board);
    int getLastPlayer() const;
    int getNumOfColumns() const;
    int getWinner() const;
    void makeMove(int col, int player);
    bool canMove(int row, int col);
    bool checkFullColumn(int col);
    int getEmptyRowPosition(int col);
    std::vector<Board> getChildren(int player);
    int evaluate();
    bool checkForDraw();
    bool checkWinState();
    int countNInARow(int n, int player);
    bool checkForGameOver();
    std::string getGameBoardAsString();
};
