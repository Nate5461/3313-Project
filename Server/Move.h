#pragma once

class Move {
private:
    int row;
    int column;
    int value;

public:
    Move();
    Move(int row, int col);
    Move(int value);
    Move(int row, int col, int value);

    // Getters and setters
    int getRow() const;
    void setRow(int row);
    int getColumn() const;
    void setColumn(int column);
    int getValue() const;
    void setValue(int value);
};