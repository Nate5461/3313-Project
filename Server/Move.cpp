#include "Move.h"

Move::Move() : row(0), column(0), value(0) {}

Move::Move(int row, int col) : row(row), column(col), value(0) {}

Move::Move(int value) : row(0), column(0), value(value) {}

Move::Move(int row, int col, int value) : row(row), column(col), value(value) {}

int Move::getRow() const {
    return row;
}

void Move::setRow(int row) {
    this->row = row;
}

int Move::getColumn() const {
    return column;
}

void Move::setColumn(int column) {
    this->column = column;
}

int Move::getValue() const {
    return value;
}

void Move::setValue(int value) {
    this->value = value;
}