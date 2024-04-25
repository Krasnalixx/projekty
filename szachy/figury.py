from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QLabel


class ChessPiece:
    def __init__(self, color, position):
        self.color = color  # 'B' dla białych, 'C' dla czarnych
        self.position = position  # Pozycja w formacie (x, y)
    def getLegalMoves(self, board):
        # To jest metoda szablonowa, powinna być nadpisana w klasach dziedziczących
        pass


class Knight(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def getLegalMoves(self, board):
        moves = []
        directions = [
            (2, 1), (1, 2), (-1, -2), (-2, -1),
            (-2, 1), (-1, 2), (1, -2), (2, -1)
        ]
        for dx, dy in directions:
            x, y = self.position[0] + dx, self.position[1] + dy
            if (0 <= x < 8) and (0 <= y < 8):
                if not board.isOccupied(x, y) or board.isOccupiedByColor(x, y, self.getOppositeColor()):
                    moves.append((x, y))
        return moves

    def getOppositeColor(self):
        return 'B' if self.color == 'C' else 'C'


class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.firstMove = True

    def getLegalMoves(self, board):
        moves = []
        direction = -1 if self.color == 'B' else 1  # Białe pionki poruszają się w górę planszy, czarne w dół
        start_row = 6 if self.color == 'B' else 1  # Startowy rząd dla białych i czarnych pionków

        # Ruch o jedno pole do przodu
        x, y = self.position[0], self.position[1] + direction
        if (0 <= x < 8) and (0 <= y < 8) and not board.isOccupied(x, y):
            moves.append((x, y))

            # Ruch o dwa pola do przodu (tylko gdy pionek stoi na pozycji startowej)
            if self.firstMove and self.position[1] == start_row:
                x, y = self.position[0], self.position[1] + 2 * direction
                if (0 <= x < 8) and (0 <= y < 8) and not board.isOccupied(x, y):
                    moves.append((x, y))

        if board.isOccupiedByColor(self.position[0] + direction, self.position[1] + direction, self.getOppositeColor()):
            moves.append((self.position[0] + direction, self.position[1] + direction))
        if board.isOccupiedByColor(self.position[0] - direction, self.position[1] + direction, self.getOppositeColor()):
            moves.append((self.position[0] - direction, self.position[1] + direction))

        return moves

    def getOppositeColor(self):
        return 'B' if self.color == 'C' else 'C'


class Rook(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.hasMoved = False

    def getLegalMoves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            x, y = self.position
            while True:
                x += dx
                y += dy
                if 0 <= x < 8 and 0 <= y < 8:
                    if board.isOccupied(x, y):
                        if board.isOccupiedByColor(x, y, self.getOppositeColor()):
                            moves.append((x, y))
                        break
                    else:
                        moves.append((x, y))
                else:
                    break

        return moves

    def move(self, newPos):
        self.position = newPos
        self.hasMoved = True  # Ustaw atrybut hasMoved na True po wykonaniu ruchu

    def getOppositeColor(self):
        return 'B' if self.color == 'C' else 'C'


class Queen(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def getLegalMoves(self, board):
        moves = []
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            x, y = self.position

            while True:
                x += dx
                y += dy

                if 0 <= x < 8 and 0 <= y < 8:
                    if board.isOccupied(x, y):
                        if board.isOccupiedByColor(x, y, self.getOppositeColor()):
                            moves.append((x, y))
                        break
                    else:
                        moves.append((x, y))
                else:
                    break

        return moves

    def getOppositeColor(self):
        return 'B' if self.color == 'C' else 'C'


class Bishop(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def getLegalMoves(self, board):
        moves = []
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        for dx, dy in directions:
            x, y = self.position

            while True:
                x += dx
                y += dy

                if 0 <= x < 8 and 0 <= y < 8:
                    if board.isOccupied(x, y):
                        if board.isOccupiedByColor(x, y, self.getOppositeColor()):
                            moves.append((x, y))
                        break
                    else:
                        moves.append((x, y))
                else:
                    break

        return moves

    def getOppositeColor(self):
        return 'B' if self.color == 'C' else 'C'


class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.hasMoved = False

    def getLegalMoves(self, board):
        moves = []
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            x, y = self.position[0] + dx, self.position[1] + dy
            if 0 <= x < 8 and 0 <= y < 8:
                if not board.isOccupied(x, y) or board.isOccupiedByColor(x, y, self.getOppositeColor()):
                    moves.append((x, y))

        # Sprawdź możliwość roszady
        if not self.hasMoved:
            rook = board.occupiedFields.get((7, self.position[1]))
            if rook and not rook.pieceObject.hasMoved:
                # Sprawdź, czy pola między królem a wieżą są puste
                if not any([board.isOccupied(x, self.position[1]) for x in range(self.position[0] + 1, 7)]):
                    moves.append((6, self.position[1]))

            # Sprawdź możliwość długiej roszady
        if not self.hasMoved:
            rook = board.occupiedFields.get((0, self.position[1]))
            if rook and not rook.pieceObject.hasMoved:
                # Sprawdź, czy pola między królem a wieżą są puste
                if not any([board.isOccupied(x, self.position[1]) for x in range(1, self.position[0])]):
                    moves.append((2, self.position[1]))
        return moves

    def move(self, newPos):
        self.position = newPos
        self.hasMoved = True

    def getOppositeColor(self):
        return 'B' if self.color == 'C' else 'C'


# ... reszta twojego kodu dla klas ...

class GameOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wybierz wariant gry")
        self.layout = QVBoxLayout(self)

        # Wybór czasu gry
        self.combo = QComboBox(self)
        self.combo.addItem("Bullet - 1 minuta", userData={"minutes": 1, "increment": 0})
        self.combo.addItem("Blitz - 5 minut", userData={"minutes": 5, "increment": 0})
        self.combo.addItem("Rapid - 10 minut", userData={"minutes": 10, "increment": 0})
        self.combo.addItem("Increment - 3 minuty + 3 sekundy", userData={"minutes": 3, "increment": 3})
        self.layout.addWidget(self.combo)

        self.startButton = QPushButton("Start", self)
        self.startButton.clicked.connect(self.accept)
        self.layout.addWidget(self.startButton)
    def selectedOption(self):
        # Zwraca opcje gry oraz adres IP i port jako słownik
        return {
            "gameOption": self.combo.currentData(),
        }


class PromotionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Promocja Piona")
        self.selectedPiece = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.instructionLabel = QLabel("Wpisz nazwę figury (królowa, wieża, goniec, skoczek):")
        layout.addWidget(self.instructionLabel)

        self.pieceInput = QLineEdit(self)
        layout.addWidget(self.pieceInput)

        self.confirmButton = QPushButton("Potwierdź")
        self.confirmButton.clicked.connect(self.confirmSelection)
        layout.addWidget(self.confirmButton)

    def confirmSelection(self):
        pieceName = self.pieceInput.text().lower()
        if pieceName in ["królowa", "wieża", "goniec", "skoczek"]:
            self.selectedPiece = pieceName
            self.accept()
        else:
            self.instructionLabel.setText("Nieprawidłowa nazwa figury! Wpisz ponownie:")


class Move2:
    def __init__(self, turn_number, start_pos, end_pos, piece_type, enpassant, captured_piece, castling, promotion):
        self.turn_number = turn_number
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.piece_type = piece_type
        self.enPassant = enpassant
        self.captured_piece = captured_piece
        self.castling = castling
        self.promotion = promotion
