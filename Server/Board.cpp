#include "Constants.h"
#include "Board.h"
#include "Move.h"
#include <iostream>
#include <vector>
#include <cmath>
#include <climits>


Board::Board(int numOfRows, int numOfColumns, int checkersInARow) {
    this->numOfRows = numOfRows;
    this->numOfColumns = numOfColumns;
    this->checkersInARow = checkersInARow;
    lastMove = Move();
    lastPlayer = P2;
    winner = EMPTY;
    overflow = false;
    gameOver = false;
    turn = 1;
    gameBoard = std::vector<std::vector<int>>(numOfRows, std::vector<int>(numOfColumns, EMPTY));
}

Board::Board(){
    this->numOfRows = CONNECT_4_NUM_OF_ROWS;
    this->numOfColumns = CONNECT_4_NUM_OF_COLUMNS;
    this->checkersInARow = CONNECT_4_CHECKERS_IN_A_ROW;
    lastMove = Move();
    lastPlayer = P2;
    winner = EMPTY;
    overflow = false;
    gameOver = false;
    turn = 1;
    gameBoard = std::vector<std::vector<int>>(numOfRows, std::vector<int>(numOfColumns, EMPTY));

}

Board::Board(const Board& board) {
    numOfRows = board.numOfRows;
    numOfColumns = board.numOfColumns;
    checkersInARow = board.checkersInARow;
    lastMove = board.lastMove;
    lastPlayer = board.lastPlayer;
    winner = board.winner;
    overflow = board.overflow;
    gameOver = board.gameOver;
    turn = board.turn;
    gameBoard = board.gameBoard;
}

int Board::getLastPlayer() const {
    return lastPlayer;
}

int Board::getNumOfColumns() const {
    return numOfColumns;
}



void Board::makeMove(int col, int player) {
    try {
        int row = getEmptyRowPosition(col);
        lastMove = Move(row, col);
        lastPlayer = player;
        gameBoard[row][col] = player;
        turn++;
    } catch (std::out_of_range& ex) {
        std::cerr << "Column " << (col + 1) << " is full!" << std::endl;
        overflow = true;
    }
}

bool Board::canMove(int row, int col) {
    return (row >= 0) && (col >= 0) && (row < numOfRows) && (col < numOfColumns);
}


bool Board::checkFullColumn(int col) {
    return gameBoard[0][col] != EMPTY;
}

int Board::getEmptyRowPosition(int col) {
    int rowPosition = -1;
    for (int row = 0; row < numOfRows; row++) {
        if (gameBoard[row][col] == EMPTY) {
            rowPosition = row;
        }
    }
    return rowPosition;
}



bool Board::checkForGameOver() {
    if (checkWinState()) {
        return true;
    }

    return checkForDraw();
}

bool Board::checkWinState() {
    int counter = countNInARow(checkersInARow, P1);
    if (counter > 0) {
        winner = P1;
        return true;
    }

    counter = countNInARow(checkersInARow, P2);
    if (counter > 0) {
        winner = P2;
        return true;
    }

    winner = EMPTY;
    return false;
}

std::vector<Board> Board::getChildren(int player) {
    std::vector<Board> children;
    for (int col = 0; col < numOfColumns; col++) {
        if (!checkFullColumn(col)) {
            Board child(*this);
            child.makeMove(col, player);
            children.push_back(child);
        }
    }
    return children;
}

int Board::countNInARow(int N, int player) {
    int times = 0;

    for (int i = 0; i < numOfRows; i++) {
        for (int j = 0; j < numOfColumns; j++) {
            if (canMove(i, j + checkersInARow - 1)) {
                int k = 0;
                while (k < N && gameBoard[i][j + k] == player) {
                    k++;
                }
                if (k == N) {
                    while (k < checkersInARow && (gameBoard[i][j + k] == player || gameBoard[i][j + k] == EMPTY)) {
                        k++;
                    }
                    if (k == checkersInARow) times++;
                }
            }
        }
    }

    for (int i = 0; i < numOfRows; i++) {
        for (int j = 0; j < numOfColumns; j++) {
            if (canMove(i - checkersInARow + 1, j)) {
                int k = 0;
                while (k < N && gameBoard[i - k][j] == player) {
                    k++;
                }
                if (k == checkersInARow) {
                    while (k < checkersInARow && (gameBoard[i - k][j] == player || gameBoard[i - k][j] == EMPTY)) {
                        k++;
                    }
                    if (k == checkersInARow) times++;
                }
            }
        }
    }

    for (int i = 0; i < numOfRows; i++) {
        for (int j = 0; j < numOfColumns; j++) {
            if (canMove(i + checkersInARow - 1, j + checkersInARow - 1)) {
                int k = 0;
                while (k < N && gameBoard[i + k][j + k] == player) {
                    k++;
                }
                if (k == checkersInARow) {
                    while (k < checkersInARow && (gameBoard[i + k][j + k] == player || gameBoard[i + k][j + k] == EMPTY)) {
                        k++;
                    }
                    if (k == checkersInARow) times++;
                }
            }
        }
    }

    for (int i = 0; i < numOfRows; i++) {
        for (int j = 0; j < numOfColumns; j++) {
            if (canMove(i - checkersInARow + 1, j + checkersInARow - 1)) {
                int k = 0;
                while (k < N && gameBoard[i - k][j + k] == player) {
                    k++;
                }
                if (k == checkersInARow) {
                    while (k < checkersInARow && (gameBoard[i - k][j + k] == player || gameBoard[i - k][j + k] == EMPTY)) {
                        k++;
                    }
                    if (k == checkersInARow) times++;
                }
            }
        }
    }

    return times;
}

int Board::evaluate() {
    int player1Score = 0;
    int player2Score = 0;

    if (checkWinState()) {
        if (winner == P1) {
            return INT_MAX;
        } else if (winner == P2) {
            return INT_MIN;
        }
    }

    for (int i = 2; i < checkersInARow; i++) {
        player1Score += countNInARow(i, P1) * std::pow(10, i - 2);
        player2Score += countNInARow(i, P2) * std::pow(10, i - 2);
    }

    return player1Score - player2Score;
}

bool Board::checkForDraw() {
    for (int row = 0; row < numOfRows; row++) {
        for (int col = 0; col < numOfColumns; col++) {
            if (gameBoard[row][col] == EMPTY) {
                return false;
            }
        }
    }

    return true;
}

std::string Board::getGameBoardAsString() {
    std::string output;
    output += "|";
    for (int j = 1; j <= numOfColumns; j++) {
        output += (" " + std::to_string(j) + " |");
    }
    output += "\n";
    
    output += " ---------------------------\n";
    
    for (int i = 0; i < numOfRows; i++) {
        for (int j = 0; j < numOfColumns; j++) {
            char symbol = '-';
            if (gameBoard[i][j] == P1) {
                symbol = 'X';
            } else if (gameBoard[i][j] == P2) {
                symbol = 'O';
            }
            output += "| " + std::string(1, symbol) + " ";
            if (j == numOfColumns - 1) {
                output += "|\n";
            }
        }
    }
    
        output += " ---------------------------\n";
        output += "*****************************\n";
    
        
    return output;
}