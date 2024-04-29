import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QHBoxLayout, QWidget, QColorDialog, QTextEdit
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QBrush, QColor, QPixmap
from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer, QTime
import resources_rc
from figures import Rook, Bishop, Knight, Pawn, Queen, King, GameOptionsDialog, PromotionDialog, Move2

def globalExceptionHandler(exc_type, exc_value, exc_traceback):
    # Logowanie lub drukowanie informacji o wyjątku
    print(exc_type, exc_value)
    # Dodatkowo, ślad stosu:
    import traceback
    traceback.print_tb(exc_traceback)

class DraggablePiece(QGraphicsPixmapItem):
    def __init__(self, pixmap, filename, position, chessBoard):
        super(DraggablePiece, self).__init__(pixmap)
        self.chessBoard = chessBoard
        self.filename = filename
        self.pieceType, self.color = filename.replace('.png', '').split('/')[-1][:-1], filename[-5]
        self.setFlag(QGraphicsPixmapItem.ItemIsMovable)
        self.setFlag(QGraphicsPixmapItem.ItemSendsGeometryChanges)
        self.originalPixmap = pixmap
        self.occupiedFields = None
        self.position = position
        self.pieceObject = self.createPieceObject(self.pieceType, self.color, position)
        self.legalMoves = None
        self.enPassant = None
        self.Promotion = False
    def createPieceObject(self, pieceType, color, position):
        if pieceType == "skoczek":
            return Knight(color, position)
        elif pieceType == "pionek":
            return Pawn(color, position)
        elif pieceType == "wieża":
            return Rook(color, position)
        elif pieceType == "goniec":
            return Bishop(color, position)
        elif pieceType == "królowa":
            return Queen(color, position)
        elif pieceType == "król":
            return King(color, position)
        else:
            return None
    def positionToNotation(self, x, y):
        column = chr(ord('a') + x)
        row = str(8 - y)
        return column + row

    def changeAppearance(self, newPixmap, newFilename):
        squareSize = 100  # Użyj tej samej wielkości kwadratu, co przy inicjalizacji
        scaledPixmap = newPixmap.scaledToHeight(squareSize, Qt.SmoothTransformation)
        self.setPixmap(scaledPixmap)
        self.filename = newFilename
        self.pieceType, self.color = newFilename.replace('.png', '').split('/')[-1][:-1], newFilename[-5]
        xOffset = (squareSize - scaledPixmap.width()) / 2
        self.originalPixmap = scaledPixmap
        currentPos = self.pos()
        xGrid = round(currentPos.x() / squareSize)
        yGrid = round(currentPos.y() / squareSize)
        self.setPos(xGrid * squareSize + xOffset, yGrid * squareSize)

    def mousePressEvent(self, event):
        if not self.chessBoard.history:
            shrinkedPixmap = self.originalPixmap.scaled(self.originalPixmap.size() * 0.8, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(shrinkedPixmap)
        self.originalPosition = self.pos()
        super(DraggablePiece, self).mousePressEvent(event)
        self.legalMoves = self.pieceObject.getLegalMoves(self.scene().views()[0].window()) if self.pieceObject else []
        currentPos = self.pos()  # Pobiera aktualną pozycję pionka
        squareSize = 100  # Zakładając, że wielkość kwadratu to 100
        currentXIndex = int(currentPos.x() / squareSize)  # Przeliczanie na indeksy szachownicy
        currentYIndex = int(currentPos.y() / squareSize)
        if isinstance(self.pieceObject, Pawn):  # Sprawdzenie, czy przesuwany jest pionek
            lastMove = self.chessBoard.move_history[-1] if self.chessBoard.move_history else None
            if lastMove:
                lastStartPos=lastMove.start_pos
                lastEndPos=lastMove.start_pos
                lastPieceType=lastMove.piece_type

                if lastPieceType == "Pawn" and abs(lastStartPos[1]-lastEndPos[1])==2:  # Sprawdzenie, czy ostatni ruch był wykonany przez pion przeciwnika
                    if abs(lastEndPos[0] - currentXIndex) == 1 and currentYIndex==lastEndPos[1]:  # Sprawdzenie, czy pion przeciwnika jest obok

                        if chessBoard.currentTurn == 'C':
                            self.legalMoves.append((lastEndPos[0], lastEndPos[1] + 1))
                        else:
                            self.legalMoves.append((lastEndPos[0], lastEndPos[1] - 1))
                        self.enPassant = lastEndPos
        if isinstance(self.pieceObject, King) and not self.pieceObject.hasMoved:
            opponentColor = 'C' if chessBoard.currentTurn == 'B' else 'B'
            allOpponentMoves = chessBoard.getAllLegalMoves(opponentColor)
            threatenedPositions = [(i, 0) for i in range(1, 5)]
            isThreatened = any(pos in allOpponentMoves for pos in threatenedPositions)

            if chessBoard.hasRookMoved((0, 0)) or isThreatened:
                positionToRemove = (2, 0)  # Ta pozycja może być różna w zależności od twojej logiki roszady
                if positionToRemove in self.legalMoves:
                    self.legalMoves.remove(positionToRemove)
            threatenedPositions2 = [(i,7) for i in range(1, 5)]
            isThreatened2 = any(pos in allOpponentMoves for pos in threatenedPositions2)
            if chessBoard.hasRookMoved((0, 7)) or isThreatened2:
                positionToRemove2 = (2, 7)  # Ta pozycja może być różna w zależności od twojej logiki roszady
                if positionToRemove2 in self.legalMoves:
                    self.legalMoves.remove(positionToRemove2)
        if isinstance(self.pieceObject, King) and not self.pieceObject.hasMoved:
            opponentColor = 'C' if chessBoard.currentTurn == 'B' else 'B'
            allOpponentMoves = chessBoard.getAllLegalMoves(opponentColor)
            threatenedPositions = [(i,0) for i in range(4, 7)]
            isThreatened = any(pos in allOpponentMoves for pos in threatenedPositions)

            if chessBoard.hasRookMoved((7, 0)) or isThreatened:
                positionToRemove = (6, 0)  # Ta pozycja może być różna w zależności od twojej logiki roszady
                if positionToRemove in self.legalMoves:
                    self.legalMoves.remove(positionToRemove)
            threatenedPositions2 = [(i,7) for i in range(4, 7)]
            isThreatened2 = any(pos in allOpponentMoves for pos in threatenedPositions2)

            if chessBoard.hasRookMoved((7, 7)) or isThreatened2:
                positionToRemove2 = (6, 7)  # Ta pozycja może być różna w zależności od twojej logiki roszady
                if positionToRemove2 in self.legalMoves:
                    self.legalMoves.remove(positionToRemove2)

        self.legalMoves = [move for move in self.legalMoves if chessBoard.simulateMove((currentXIndex, currentYIndex), move)]

        if not self.chessBoard.history:
            self.scene().views()[0].window().highlightLegalMoves(self.legalMoves)
        super(DraggablePiece, self).mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)
            self.scene().views()[0].window().resetSquareHighlights()
            squareSize = 100
            newPos2 = self.snapToGrid(self.pos(), squareSize)
            if newPos2 is not None and not self.chessBoard.history:
                newPos = QPointF(newPos2.x() - 7, newPos2.y() - 10)
                self.setPixmap(self.originalPixmap)  # Przywróć oryginalny rozmiar figury
                chessBoard = self.scene().views()[0].window()

                if self.color == chessBoard.currentTurn:
                    if newPos is not None:
                        xIndex, yIndex = int(newPos.x() / squareSize), int(newPos.y() / squareSize)
                        oldXIndex, oldYIndex = int(self.originalPosition.x() / squareSize), int(self.originalPosition.y() / squareSize)
                        startNotation = self.positionToNotation(oldXIndex, oldYIndex)
                        endNotation = self.positionToNotation(xIndex, yIndex)
                        if (xIndex, yIndex) in self.legalMoves:
                            start_position = (oldXIndex, oldYIndex)
                            end_position = (xIndex, yIndex)
                            captured_piece = None
                            if (xIndex, yIndex) in self.occupiedFields:
                                captured_piece = type(self.occupiedFields[(xIndex, yIndex)].pieceObject).__name__
                                targetPiece = self.occupiedFields[(xIndex, yIndex)]
                                if targetPiece.color != self.color:  # Zbij figurę przeciwnika
                                    self.scene().removeItem(targetPiece)  # Usuń zbijaną figurę z planszy
                                    del self.occupiedFields[(xIndex, yIndex)]  # Usuń zbijaną figurę z zajętych pól
                            elif self.enPassant and (xIndex, yIndex-1) == self.enPassant and chessBoard.currentTurn=='C':
                                targetPiece2 = self.occupiedFields[self.enPassant]
                                self.scene().removeItem(targetPiece2)
                                del self.occupiedFields[self.enPassant]
                            elif self.enPassant and (xIndex, yIndex+1) == self.enPassant and chessBoard.currentTurn=='B':
                                targetPiece2 = self.occupiedFields[self.enPassant]
                                self.scene().removeItem(targetPiece2)
                                del self.occupiedFields[self.enPassant]

                            if self.pieceType=="wieża":
                                for element in chessBoard.Rook_moved:
                                    if oldXIndex==element[0] and oldYIndex==element[1]:
                                        element[2]=True
                            rookHasMoved = chessBoard.hasRookMoved((oldXIndex,oldXIndex))
                            castling = None
                            if isinstance(self.pieceObject, King) and not self.pieceObject.hasMoved and not rookHasMoved:
                                # Sprawdzanie ruchu o dwa pola w prawo
                                if xIndex == oldXIndex + 2:
                                    rook = self.occupiedFields.get((7, yIndex))
                                    if rook and isinstance(rook.pieceObject, Rook) and not rook.pieceObject.hasMoved:
                                        self.makeCastlingMove((7, yIndex), (xIndex - 1, yIndex), rook)
                                        castling = 'short'
                                # Sprawdzanie ruchu o dwa pola w lewo
                                elif xIndex == oldXIndex - 2:
                                    # Wykonaj roszadę z wieżą po lewej stronie
                                    rook = self.occupiedFields.get((0, yIndex))
                                    if rook and isinstance(rook.pieceObject, Rook) and not rook.pieceObject.hasMoved:
                                        self.makeCastlingMove((0, yIndex), (xIndex + 1, yIndex), rook)
                                        castling = 'long'

                            self.occupiedFields.pop((oldXIndex, oldYIndex), None)
                            self.occupiedFields[(xIndex, yIndex)] = self
                            self.setPos(newPos.x(), newPos.y())
                            if isinstance(self.pieceObject, Rook) or isinstance(self.pieceObject, King):
                                self.pieceObject.hasMoved = True
                            imageName = None
                            if isinstance(self.pieceObject, Pawn):
                                if (self.color == 'B' and yIndex == 0) or (self.color == 'C' and yIndex == 7):
                                    self.scene().removeItem(self)
                                    dialog = PromotionDialog()
                                    if dialog.exec_() == QDialog.Accepted:
                                        selectedPiece = dialog.selectedPiece
                                        # Przekształć wybraną nazwę figury na odpowiednią nazwę pliku
                                        pieceNameToFile = {
                                            'królowa': 'królowa',
                                            'wieża': 'wieża',
                                            'goniec': 'goniec',
                                            'skoczek': 'skoczek'
                                        }
                                        imageName = pieceNameToFile[selectedPiece] + self.color + '.png'
                                        promotedPiece = chessBoard.addPiece(imageName, xIndex, yIndex, addToOccupied=True)
                                        self.occupiedFields[(xIndex, yIndex)] = promotedPiece
                                        self.Promotion = True

                            if self.pieceObject:
                                self.pieceObject.position = (xIndex, yIndex)
                            moveNotation = f"{startNotation}{endNotation}"
                            chessBoard.addMoveToLog(moveNotation)
                            chessBoard.currentTurn = 'C' if chessBoard.currentTurn == 'B' else 'B'
                            self.chessBoard.moveCount += 1
                            if not self.Promotion:
                                self.Promotion = False
                            enpassant = self.enPassant
                            move = Move2(self.chessBoard.moveCount, startNotation, endNotation, self.pieceType, enpassant, captured_piece, castling, imageName)
                            self.chessBoard.move_history.append(move)
                            chessBoard.currentMoveIndex = len(chessBoard.move_history)
                            chessBoard.switchTimer()
                            if not chessBoard.checkForLegalMoves(chessBoard.currentTurn):
                                if self.checkForCheck(chessBoard.currentTurn):
                                    print("Mat")
                                    chessBoard.showMateMessege()
                                else:
                                    print("Pat")



                        else:
                            self.setPos(self.originalPosition)  # Cofnij, jeśli ruch jest nielegalny
                            self.enPassant = None
                    else:
                        self.setPos(self.originalPosition)  # Cofnij, jeśli ruch jest nieprawidłowy
                        self.enPassant = None
                else:
                    self.setPos(self.originalPosition)  # Cofnij, jeśli ruch wykonano niewłaściwą figurą
                    self.enPassant = None

                super(DraggablePiece, self).mouseReleaseEvent(event)
            else:
                self.setPos(self.originalPosition)

    def makeCastlingMove(self, rookStartPos, rookEndPos, rook):

        self.occupiedFields.pop(rookStartPos)
        self.occupiedFields[rookEndPos] = rook
        rook.setPos(rookEndPos[0] * 100 + (100 - rook.pixmap().width()) / 2,
                    rookEndPos[1] * 100 + (100 - rook.pixmap().height()) / 2)

        # Dodaj tę linię, aby zaktualizować pozycję logiki wieży
        rook.pieceObject.position = rookEndPos

        # Możesz także zaktualizować atrybut hasMoved wieży, aby wskazać, że wieża została już przesunięta
        rook.pieceObject.hasMoved = True

    def checkForCheck(self, kingColor):

        kingPos = None
        attacksOnKing = False  # Licznik ataków na króla

        # Znajdź pozycję króla
        for (x, y), piece in self.occupiedFields.items():
            if isinstance(piece.pieceObject, King) and piece.color == kingColor:
                kingPos = (x, y)
                break

        if kingPos is None:
            return False  # Król tego koloru nie został znaleziony, co nie powinno się zdarzyć

        # Sprawdź wszystkie figury przeciwnika, czy mogą atakować króla
        for (x, y), piece in self.occupiedFields.items():
            if piece.color != kingColor:  # Sprawdzaj tylko figury przeciwnika
                moves=piece.pieceObject.getLegalMoves(chessBoard) if piece.pieceObject else []
                for move in moves:
                    if kingPos==move:
                        attacksOnKing = True
                        break
        return attacksOnKing


    def snapToGrid(self, pos, squareSize):
        boardSize = 8  # Rozmiar planszy 8x8
        maxPosition = squareSize * (boardSize - 1)  # Maksymalna pozycja w pikselach

        # Obliczenie indeksów najbliższego kwadratu
        xIndex = round(pos.x() / squareSize)
        yIndex = round(pos.y() / squareSize)

        # Sprawdzenie, czy pozycja znajduje się w granicach planszy
        if 0 <= xIndex < boardSize and 0 <= yIndex < boardSize:
            # Obliczenie nowej pozycji, tak aby figura znalazła się na środku kwadratu
            newX = xIndex * squareSize + (squareSize - self.pixmap().width()) / 2
            newY = yIndex * squareSize + (squareSize - self.pixmap().height()) / 2
            return QPointF(newX, newY)
        else:
            return None



class ChessBoard(QWidget):
    def __init__(self, gameOption=None):
        super(ChessBoard, self).__init__()
        self.originalSquareColors = {}
        self.occupiedFields = {}
        self.currentSet = 'bierki1'
        self.currentInput = ""
        self.currentTurn = 'B'
        self.moveCount=1
        self.Rook_moved = [[0,0,False], [0,7,False], [7,0,False], [7,7,False]]
        self.move_history = []
        self.currentMoveIndex = self.moveCount
        self.history = False
        self.increment = gameOption.get("increment", 0) if gameOption else 0

        # Ustawienia sceny i widoku
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(800, 800)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Tworzenie przycisku do zmiany zestawu figur
        self.changeSetButton = QPushButton("Change the set of figures")
        self.changeSetButton.clicked.connect(self.changePieceSet)

        # Tworzenie przycisków do zmiany kolorów szachownicy
        self.changeColor1Button = QPushButton("Change color 1")
        self.changeColor2Button = QPushButton("Change color 2")
        self.movesLabel = QTextEdit("Moves: ")
        # Połącz przyciski ze slotami reakcji
        self.changeColor1Button.clicked.connect(self.changeColor1)
        self.changeColor2Button.clicked.connect(self.changeColor2)

        # Dodanie QLabel do wyświetlania ruchów

        # Tworzenie pionowego layoutu dla przycisków i etykiet
        self.buttonsLayout = QVBoxLayout()

        self.initChessClock(gameOption)

        self.prevMoveButton = QPushButton("Previous move")
        self.nextMoveButton = QPushButton("Next move")

        # Dodaj przyciski do layoutu
        self.buttonsLayout.addWidget(self.prevMoveButton)
        self.buttonsLayout.addWidget(self.nextMoveButton)

        # Połącz przyciski z funkcjami obsługującymi kliknięcia
        self.prevMoveButton.clicked.connect(self.prevMove)
        self.nextMoveButton.clicked.connect(self.nextMove)

        # Dodaj przyciski do QVBoxLayout
        self.buttonsLayout.addWidget(self.changeSetButton)
        self.buttonsLayout.addWidget(self.changeColor1Button)
        self.buttonsLayout.addWidget(self.changeColor2Button)

        self.buttonsLayout.addWidget(self.movesLabel)
        # Dodaj etykietę ruchów do QVBoxLayout

        # Utwórz główny QHBoxLayout
        self.mainLayout = QHBoxLayout()

        # Dodaj widok szachownicy do głównego layoutu
        self.mainLayout.addWidget(self.view)

        # Dodaj QVBoxLayout z przyciskami i etykietą ruchów do głównego layoutu
        self.mainLayout.addLayout(self.buttonsLayout)

        # Ustaw główny layout dla tego widgetu
        self.setLayout(self.mainLayout)

        self.drawBoard()
        self.addPieces()
        self.show()

    def initChessClock(self, gameOption):
        minutes = gameOption["minutes"]
        increment = gameOption["increment"]

        self.timerWhite = QTimer(self)
        self.timerBlack = QTimer(self)
        self.timeWhite = QTime(0, minutes, 0)  # 5 minut dla białych
        self.timeBlack = QTime(0, minutes, 0)  # 5 minut dla czarnych

        self.timerWhite.timeout.connect(self.updateTimerWhite)
        self.timerBlack.timeout.connect(self.updateTimerBlack)

        self.displayWhite = QLabel(self.timeWhite.toString("mm:ss"))
        self.displayBlack = QLabel(self.timeBlack.toString("mm:ss"))

        # Możesz dostosować layout, aby umieścić zegary tam, gdzie chcesz
        self.buttonsLayout.addWidget(self.displayWhite)
        self.buttonsLayout.addWidget(self.displayBlack)

        # Startuj timer dla białych, gdyż zaczynają grę
        self.timerWhite.start(1000)

    def updateTimerWhite(self):
        self.timeWhite.addMSecs(300)
        self.timeWhite = self.timeWhite.addSecs(-1)
        self.displayWhite.setText(self.timeWhite.toString("mm:ss"))
        if self.timeWhite.toString("mm:ss") == "00:00":
            self.timerWhite.stop()
            # Obsługa końca gry, gdy czas białych się skończy

    def updateTimerBlack(self):
        self.timeBlack = self.timeBlack.addSecs(-1)
        self.displayBlack.setText(self.timeBlack.toString("mm:ss"))
        if self.timeBlack.toString("mm:ss") == "00:00":
            self.timerBlack.stop()
            # Obsługa końca gry, gdy czas czarnych się skończy

    def switchTimer(self):
        if self.timeWhite == QTime(0, 0):
            self.timerWhite.stop()
            self.showTimeOutMessage("Biały")
        elif self.timeBlack == QTime(0, 0):
            self.timerBlack.stop()
            self.showTimeOutMessage("Czarny")

        if self.currentTurn == 'C':
            self.timerWhite.stop()
            # Przełącz na czarne i dodaj inkrementację do zegara białych
            if self.timeWhite.second() + self.increment < 60:
                self.timeWhite = self.timeWhite.addSecs(self.increment)
            else:
                additionalMinutes = (self.timeWhite.second() + self.increment) // 60
                additionalSeconds = (self.timeWhite.second() + self.increment) % 60
                self.timeWhite = self.timeWhite.addSecs(-self.timeWhite.second()).addSecs(additionalSeconds).addSecs(
                    60 * additionalMinutes)
            self.displayWhite.setText(self.timeWhite.toString("mm:ss"))
            self.timerBlack.start(1000)
        else:
            self.timerBlack.stop()
            # Przełącz na białe i dodaj inkrementację do zegara czarnych
            if self.timeBlack.second() + self.increment < 60:
                self.timeBlack = self.timeBlack.addSecs(self.increment)
            else:
                additionalMinutes = (self.timeBlack.second() + self.increment) // 60
                additionalSeconds = (self.timeBlack.second() + self.increment) % 60
                self.timeBlack = self.timeBlack.addSecs(-self.timeBlack.second()).addSecs(additionalSeconds).addSecs(
                    60 * additionalMinutes)
            self.displayBlack.setText(self.timeBlack.toString("mm:ss"))
            self.timerWhite.start(1000)
    def showTimeOutMessage(self, player):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Time's up!")
        msg.setInformativeText(f"Time has run out for player {player}.")
        msg.setWindowTitle("Time Out")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()

    def showMateMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Checkmate!")
        player = "White" if self.currentTurn == "C" else "Black"
        msg.setInformativeText(f"Player {player} wins.")
        msg.setWindowTitle("Game Over")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()


    def updateMove(self, startNotation, endNotation):
        super().updateMove(startNotation, endNotation)  # Wywołaj oryginalną metodę z klasy bazowej
        self.switchTimer()
    def prevMove(self):
        # Zmniejsz indeks aktualnego ruchu i odśwież stan gry
        if self.currentMoveIndex > 0:
            self.currentMoveIndex -= 1
            self.history = True
            currentMove = self.move_history[self.currentMoveIndex]
            moveText = f"Tura: {currentMove.turn_number - 1}, Ruch: {currentMove.start_pos} -> {currentMove.end_pos}"
            print(moveText)  # Możesz wyświetlić to w QLabel lub QTextEdit zamiast konsoli
            if currentMove.promotion:
                endX, endY = self.translatePosition(currentMove.end_pos)
                if (endX, endY) in self.occupiedFields:
                    promoted_piece_item = self.occupiedFields[(endX, endY)]
                    self.scene.removeItem(promoted_piece_item)
                    color = 'C.png' if currentMove.turn_number % 2 else 'B.png'
                    pion=f"pionek"+color
                    self.addPiece(pion, endX, endY)

            move = currentMove.end_pos + currentMove.start_pos
            self.makeMove(move)
            if currentMove.captured_piece:
                endX, endY = self.translatePosition(currentMove.end_pos)
                color = 'B.png' if currentMove.turn_number % 2 else 'C.png'
                piece_translation = {
                    'Pawn': 'pionek'+color,
                    'Bishop': 'goniec'+color,
                    'Knight': 'skoczek'+color,
                    'Rook': 'wieża'+color,
                    'Queen': 'królowa'+color
                }
                captured_piece_polish = piece_translation.get(currentMove.captured_piece, "Nieznana figura")
                added_piece = self.addPiece(captured_piece_polish,endX, endY)
                self.occupiedFields[(endX, endY)] = added_piece
            if currentMove.enPassant:
                color = 'B.png' if currentMove.turn_number % 2 else 'C.png'
                added_piece = self.addPiece('pionek'+color, currentMove.enPassant[0], currentMove.enPassant[1])
                self.occupiedFields[currentMove.enPassant] = added_piece
            if currentMove.castling:
                if currentMove.castling=='long':
                    start = 'd'+currentMove.start_pos[1]
                    stop = 'a'+currentMove.start_pos[1]
                    move2=start+stop
                    self.makeMove(move2)
                elif currentMove.castling=='short':
                    start = 'f'+currentMove.start_pos[1]
                    stop = 'h'+currentMove.start_pos[1]
                    move2=start+stop
                    self.makeMove(move2)
            self.history = True


    def nextMove(self):
        # Zwiększ indeks aktualnego ruchu i odśwież stan gry
        if self.currentMoveIndex < len(self.move_history):
            self.history = True
            self.currentMoveIndex += 1
            currentMove = self.move_history[self.currentMoveIndex-1]
            moveText = f"Tura: {currentMove.turn_number-1}, Ruch: {currentMove.start_pos} -> {currentMove.end_pos}"
            print(moveText)  # Możesz wyświetlić to w QLabel lub QTextEdit zamiast konsoli
            if currentMove.captured_piece:
                endX, endY = self.translatePosition(currentMove.end_pos)
                if (endX, endY) in self.occupiedFields:
                    captured_piece_item = self.occupiedFields[(endX, endY)]
                    self.scene.removeItem(captured_piece_item)
                    del self.occupiedFields[(endX, endY)]
            move=currentMove.start_pos+currentMove.end_pos
            if currentMove.enPassant:
                if currentMove.enPassant in self.occupiedFields:
                    captured_piece_item = self.occupiedFields[currentMove.enPassant]
                    self.scene.removeItem(captured_piece_item)
                    del self.occupiedFields[currentMove.enPassant]
            if currentMove.castling:
                if currentMove.castling=='long':
                    start = 'a'+currentMove.start_pos[1]
                    stop = 'd'+currentMove.start_pos[1]
                    move2=start+stop
                    self.makeMove(move2)
                elif currentMove.castling=='short':
                    start = 'h'+currentMove.start_pos[1]
                    stop = 'f'+currentMove.start_pos[1]
                    move2=start+stop
                    self.makeMove(move2)
            if currentMove.promotion:
                startX, startY = self.translatePosition(currentMove.start_pos)
                if (startX, startY) in self.occupiedFields:
                    print("promo")
                    print(currentMove.promotion)
                    promoted_piece_item = self.occupiedFields[(startX, startY)]
                    self.scene.removeItem(promoted_piece_item)
                    self.addPiece(currentMove.promotion, startX, startY)

            self.makeMove(move)
            self.history = True

    def makeMove(self, move):
        try:

            # Interpretuj ruch, na przykład "e2e4"
            if len(move) == 4 and move[2] in 'abcdefgh' and move[3].isdigit() and 1 <= int(move[3]) <= 8:

                start = move[:2]  # "e2"
                end = move[2:]  # "e4"
                # Przetłumacz pozycje na współrzędne szachownicy i wykonaj ruch
                startX, startY = self.translatePosition(start)
                endX, endY = self.translatePosition(end)

                # Sprawdź, czy pole startowe jest zajęte przez figurę
                if (startX, startY) in self.occupiedFields:
                    chessBoard.currentTurn = 'C' if chessBoard.currentTurn == 'B' else 'B'
                    movingPiece = self.occupiedFields[(startX, startY)]

                    # Sprawdź, czy docelowe pole jest wolne
                    if (endX, endY) not in self.occupiedFields:
                        # Usuń figurę z aktualnej pozycji
                        self.occupiedFields.pop((startX, startY))
                        # Dodaj figurę do nowej pozycji
                        self.occupiedFields[(endX, endY)] = movingPiece

                        newPos = QPointF(endX * 100 + (100 - movingPiece.pixmap().width()) / 2,
                                         endY * 100 + (100 - movingPiece.pixmap().height()) / 2)
                        movingPiece.setPos(newPos)
                        if not self.history:
                            self.currentMoveIndex+=1
                            self.movesLabel.append(f"{self.currentMoveIndex}: {start}{end}")
        except Exception as e:
            print(f"Wystąpił błąd makeMove: {e}")

    def checkForLegalMoves(self, playerColor):
        # Tworzenie tymczasowej kopii wartości słownika, aby uniknąć błędu zmiany słownika podczas iteracji
        pieces = list(self.occupiedFields.values())
        for piece in pieces:
            if piece.color == playerColor:
                originalPosition = piece.position
                legalMoves = piece.pieceObject.getLegalMoves( piece.scene().views()[0].window()) if piece.pieceObject else []
                for move in legalMoves:
                    if self.simulateMove(originalPosition, move):
                        return True  # Znaleziono legalny ruch, gracz nie jest w szachu/matowej sytuacji
        return False

    def simulateMove(self, start_position, end_position):
        # Tymczasowo przesuń figurę
        piece = self.occupiedFields.pop(start_position, None)
        if piece is None:
            return False  # Nie ma figury do przesunięcia

        captured_piece = self.occupiedFields.get(end_position)
        self.occupiedFields[end_position] = piece

        # Sprawdź, czy po ruchu król jest w szachu
        is_check = piece.checkForCheck(piece.color)

        # Cofnij ruch
        self.occupiedFields[start_position] = piece
        if captured_piece is not None:
            self.occupiedFields[end_position] = captured_piece
        else:
            self.occupiedFields.pop(end_position, None)

        return not is_check
    def getAllLegalMoves(self, color):
        allLegalMoves = set()  # Używamy zbioru, aby uniknąć duplikatów

        for piece in self.occupiedFields.values():
            if piece.color == color:  # Sprawdź, czy kolor figury zgadza się z zadanym kolorem
                # Dynamicznie generuj legalne ruchy dla figury
                legalMoves = piece.pieceObject.getLegalMoves(self) if piece.pieceObject else []
                # Dodaj każdy legalny ruch do zbioru
                allLegalMoves.update(legalMoves)

        return allLegalMoves

    def hasRookMoved(self, position):
        for rook_position in self.Rook_moved:
            if rook_position[0] == position[0] and rook_position[1] == position[1]:
                return rook_position[2]
        return False
    def highlightLegalMoves(self, moves):
        for move in moves:
            x, y = move
            self.highlightSquare(x, y, QColor("yellow"))  # Przykład zaznaczenia żółtym kolorem

    def resetSquareHighlights(self):
        for (x, y), color in self.originalSquareColors.items():
            square = self.rectItems[y][x]
            square.setBrush(QBrush(color))
        self.originalSquareColors.clear()
    def highlightSquare(self, x, y, color):
        square = self.rectItems[y][x]
        # Zapisz oryginalny kolor, jeśli jeszcze nie został zapisany
        if (x, y) not in self.originalSquareColors:
            self.originalSquareColors[(x, y)] = square.brush().color()
        # Zaznacz kwadrat
        square.setBrush(QBrush(color))
    def isOccupied(self, x, y):
        return (x, y) in self.occupiedFields
    def isOccupiedByColor(self, x, y, color):
        piece = self.occupiedFields.get((x, y))
        if piece and piece.color == color:
            return True
        return False

    def addMoveToLog(self, move):
        # Dodaj ruch do QTextEdit
        number = f"{chessBoard.moveCount}: "
        self.movesLabel.append(number + move)

    def positionToNotation(self, x, y):
        column = chr(ord('a') + x)
        row = str(8 - y)
        return column + row

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Kiedy wciśnięty zostanie Enter, spróbuj wykonać ruch
            self.makeMove(self.currentInput)
            self.currentInput = ""  # Resetuj wprowadzone dane
        else:
            # Dodaj wciśnięty klawisz do aktualnie wprowadzanych danych
            self.currentInput += event.text()

    def translatePosition(self, position):
        try:
            # Pozycje szachowe zaczynają się od "a1" dla lewego dolnego rogu
            column = position[0]  # "a" do "h"
            row = position[1]  # "1" do "8"
            # Zamiana na współrzędne szachownicy; 'a' ma wartość ASCII 97
            x = ord(column) - ord('a')
            y = 8 - int(row)  # Szachownica w PyQt zaczyna się od góry
            return x, y
        except Exception as e:
            print(f"Wystąpił błąd translatePosition: {e}")
    def changeColor1(self):
        color = QColorDialog.getColor()
        if color.isValid() and color!=self.color2:
            self.color1 = color
            self.drawBoard()

    def changeColor2(self):
        color = QColorDialog.getColor()
        if color.isValid() and color!=self.color1:
            self.color2 = color
            self.drawBoard()

    def changePieceSet(self):
        # zmiana zestawu figur
        if self.currentSet == 'bierki1':
            newSet = 'bierki2'
        else:
            newSet = 'bierki1'

        # aktualizacja obrazków dla wszystkich bierek
        for item in self.scene.items():
            if isinstance(item, DraggablePiece):
                # stworzenie nowej ścieżki do obrazka
                newImagePath = f":/{newSet}/{item.pieceType}{item.color}.png"
                newPixmap = QPixmap(newImagePath)
                if not newPixmap.isNull():
                    # aktualizacja wyglądu bierki
                    item.changeAppearance(newPixmap, newImagePath)
                    # ważne: aktualizacja oryginalnej pixmapy
                    item.originalPixmap = newPixmap.scaledToHeight(100, Qt.SmoothTransformation)
                else:
                    print(f"Nie udało się załadować obrazka: {newImagePath}")

        # zapisanie nowego zestawu figur jako obecnego
        self.currentSet = newSet

    def drawBoard(self):
        boardSize = 8
        squareSize = 100
        self.color1 = self.color1 if hasattr(self, 'color1') else QColor('white')
        self.color2 = self.color2 if hasattr(self, 'color2') else QColor('gray')

        # Zakładając, że rectItems jest listą kwadratów szachownicy
        if not hasattr(self, 'rectItems'):
            self.rectItems = [[None for _ in range(boardSize)] for _ in range(boardSize)]
            for row in range(boardSize):
                for col in range(boardSize):
                    color = self.color1 if (row + col) % 2 == 0 else self.color2
                    square = QRectF(col * squareSize, row * squareSize, squareSize, squareSize)
                    rectItem = self.scene.addRect(square, brush=QBrush(color))
                    self.rectItems[row][col] = rectItem
        else:
            for row in range(boardSize):
                for col in range(boardSize):
                    color = self.color1 if (row + col) % 2 == 0 else self.color2
                    self.rectItems[row][col].setBrush(QBrush(color))

    def addPieces(self):
        # Początkowa konfiguracja dla czarnych i białych figur
        initial_setup = [
            ('wieżaC', 0, 0), ('skoczekC', 1, 0), ('goniecC', 2, 0), ('królC', 4, 0),
            ('królowaC', 3, 0), ('goniecC', 5, 0), ('skoczekC', 6, 0), ('wieżaC', 7, 0),
            ('pionekC', 0, 1), ('pionekC', 1, 1), ('pionekC', 2, 1), ('pionekC', 3, 1),
            ('pionekC', 4, 1), ('pionekC', 5, 1), ('pionekC', 6, 1), ('pionekC', 7, 1),
            ('wieżaB', 0, 7), ('skoczekB', 1, 7), ('goniecB', 2, 7), ('królB', 4, 7),
            ('królowaB', 3, 7), ('goniecB', 5, 7), ('skoczekB', 6, 7), ('wieżaB', 7, 7),
            ('pionekB', 0, 6), ('pionekB', 1, 6), ('pionekB', 2, 6), ('pionekB', 3, 6),
            ('pionekB', 4, 6), ('pionekB', 5, 6), ('pionekB', 6, 6), ('pionekB', 7, 6)
        ]

        # Iteracja przez początkową konfigurację i dodawanie każdej figury
        for piece_type, x, y in initial_setup:
            imageName = f"{piece_type}.png"
            self.addPiece(imageName, x, y)

    def addPiece(self, imageName, x, y, addToOccupied=True):
        squareSize = 100
        resource_path = f":/{self.currentSet}/{imageName}"
        pixmap = QPixmap(resource_path).scaledToHeight(squareSize, Qt.SmoothTransformation)
        if pixmap.isNull():
            print(f"Nie udało się załadować obrazka z {resource_path}")
            return

        color = 'B' if 'B' in imageName else 'C'
        piece = DraggablePiece(pixmap, resource_path, (x, y), self)
        xOffset = (squareSize - pixmap.width()) / 2
        piece.setPos(x * squareSize + xOffset, y * squareSize)
        self.scene.addItem(piece)
        if addToOccupied:
            self.occupiedFields[(x, y)] = piece
        piece.occupiedFields = self.occupiedFields
        return piece



if __name__ == '__main__':
    sys.excepthook = globalExceptionHandler
    app = QApplication(sys.argv)
    dialog = GameOptionsDialog()
    if dialog.exec_() == QDialog.Accepted:
        options = dialog.selectedOption()
        gameOption = options["gameOption"]
        chessBoard = ChessBoard(gameOption)
        chessBoard.show()
        sys.exit(app.exec_())

