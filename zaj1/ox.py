class OX:
    ALL_SPACES = list('123456789')  # Klucze słownika planszy KIK.
    X, O, BLANK = 'X', 'O', ' '  # Stałe reprezentujące wartości tekstowe.

    def __init__(self):
        self.gameBoard = self.getBlankBoard()

    def getBlankBoard(self):
        """Tworzy nową, pustą planszę gry w kółko i krzyżyk."""
        board = {}  # Plansza jest reprezentowana przez słownik Pythona.
        for space in self.ALL_SPACES:
            board[space] = self.BLANK  # Wszystkie pola na początku są puste.
        return board

    def __str__(self):
        """Zwraca tekstową reprezentację planszy."""
        return f'''
                    {self.gameBoard['1']}|{self.gameBoard['2']}|{self.gameBoard['3']} 1 2 3 
                    -+-+- 
                    {self.gameBoard['4']}|{self.gameBoard['5']}|{self.gameBoard['6']} 4 5 6 
                    -+-+- 
                    {self.gameBoard['7']}|{self.gameBoard['8']}|{self.gameBoard['9']} 7 8 9'''

    def isValidSpace(self, space):
        """Zwraca True, jeśli pole na planszy ma prawidłowy numer i pole jest puste."""
        if space is None:
            return False
        return space in self.ALL_SPACES or self.gameBoard[space] == self.BLANK

    def isWinner(self, player):
        """Zwraca True, jeśli gracz jest zwycięzcą tej planszy KIK."""
        b, p = self.gameBoard, player  # Krótsze nazwy jako "składniowy cukier".
        # Sprawdzenie, czy trzy takie same znaki występują w wierszach, kolumnach i po przekątnych.
        return ((b['1'] == b['2'] == b['3'] == p) or  # poziomo na górze
                (b['4'] == b['5'] == b['6'] == p) or  # poziomo w środku
                (b['7'] == b['8'] == b['9'] == p) or  # poziomo u dołu
                (b['1'] == b['4'] == b['7'] == p) or  # pionowo z lewej
                (b['2'] == b['5'] == b['8'] == p) or  # pionowo w środku
                (b['3'] == b['6'] == b['9'] == p) or  # pionowo z prawej
                (b['3'] == b['5'] == b['7'] == p) or  # przekątna 1
                (b['1'] == b['5'] == b['9'] == p))  # przekątna 2

    def isBoardFull(self):
        """Zwraca True, jeśli wszystkie pola na planszy są zajęte."""
        for space in self.ALL_SPACES:
            if self.gameBoard[space] == self.BLANK:
                return False  # Jeśli nawet jedno pole jest puste, zwracaj False.
        return True  # Nie ma wolnych pól, zatem zwróć True.

    def updateBoard(self, space, mark):
        """Ustawia pole na planszy na podany znak."""
        self.gameBoard[space] = mark

    def playGame(self):
        """Rozgrywka w kółko i krzyżyk."""
        print('Witaj w grze kółko i krzyżyk!')
        gameBoard = self.getBlankBoard()  # Utwórz słownik planszy KIK.
        currentPlayer, nextPlayer = self.X, self.O  # X wykonuje ruch jako pierwszy, O jako następny.
        while True:
            print(self)  # Wyświetl planszę na ekranie.

            # Zadawaj graczowi pytanie, aż wprowadzi prawidłową liczbę od 1 do 9:
            move = None
            while not self.isValidSpace(move):
                print(f'Jaki jest ruch gracza {currentPlayer}? (1-9)')
                move = input()
            self.updateBoard(move, currentPlayer)  # Wykonanie ruchu.
            # Sprawdzenie, czy gra jest zakończona:
            if self.isWinner(currentPlayer):  # Sprawdzenie, kto wygrał.
                print(self)
                print(currentPlayer + ' wygrał grę!')
                break
            elif self.isBoardFull():  # Sprawdzenie remisu.
                print(self)
                print('Gra zakończyła się remisem!')
                break
            currentPlayer, nextPlayer = nextPlayer, currentPlayer  # Zmiana gracza.
        print('Dziękuję za grę!')

if __name__ == '__main__':
    ox = OX()
    ox.playGame()