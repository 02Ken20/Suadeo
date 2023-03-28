import sys

from PyQt5 import QtWidgets

from BookRecommendationSystem import recommendBook, fromBookTableToText
from FilmRecommendationSystem import recommendFilm, fromFilmTableToText
from MusicRecommendationSystem import recommendMusic, fromMusicTableToText
from suadeo2 import Ui_MainWindow


class SuadeoUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(SuadeoUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Suadeo")

        self.refreshPage()
        self.ui.searchBar.setPlaceholderText("Search")
        # self.ui.searchButton.clicked.connect(self.searchFilms)
        self.ui.filmsButton.clicked.connect(self.searchFilmsWindow)
        self.ui.booksButton.clicked.connect(self.searchBooksWindow)
        self.ui.musicButton.clicked.connect(self.searchMusicWindow)


    def searchFilmsWindow(self):
        self.refreshPage()
        self.ui.filmsButton.setStyleSheet(
            "QPushButton{ color: black; background-color: rgb(149, 255, 223); border: 1px solid rgb(78, 84, 140); border-radius: 15px; width: 130px;height: 50px; }")
        self.ui.booksButton.setStyleSheet("QPushButton{ color: black; background-color: rgb(78, 84, 140); border: 1px solid rgb(78, 84, 140); border-radius: 15px; width: 130px;height: 50px; }")
        self.ui.musicButton.setStyleSheet("QPushButton{ color: black; background-color: rgb(78, 84, 140); border: 1px solid rgb(78, 84, 140); border-radius: 15px; width: 130px;height: 50px; }")
        self.ui.searchButton.clicked.connect(self.searchFilms)

    def searchBooksWindow(self):
        self.refreshPage()
        self.ui.filmsButton.setStyleSheet(
            "QPushButton{ color: black; background-color: rgb(78, 84, 140); border: 1px solid rgb(78, 84, 140); border-radius: 15px; width: 130px;height: 50px; }")
        self.ui.booksButton.setStyleSheet(
            "QPushButton{ color: black; background-color: rgb(149, 255, 223); border: 1px solid rgb(78, 84, 140); border-radius: 15px; width: 130px;height: 50px; }")
        self.ui.musicButton.setStyleSheet(
            "QPushButton{ color: black; background-color: rgb(78, 84, 140); border: 1px solid rgb(78, 84, 140); border-radius: 15px; width: 130px;height: 50px; }")
        self.ui.searchButton.clicked.connect(self.searchBooks)

    def searchMusicWindow(self):
        self.refreshPage()
        self.ui.filmsButton.setStyleSheet(
            "QPushButton{ color: black; background-color: rgb(78, 84, 140); border: 1px solid rgb(78, 84, 140); border-radius: 15px; width: 130px;height: 50px; }")
        self.ui.booksButton.setStyleSheet(
            "QPushButton{ color: black; background-color: rgb(78, 84, 140); border: 1px solid rgb(78, 84, 140); border-radius: 15px; width: 130px;height: 50px; }")
        self.ui.musicButton.setStyleSheet(
            "QPushButton{ color: black; background-color: rgb(149, 255, 223); border: 1px solid rgb(78, 84, 140); border-radius: 15px; width: 130px;height: 50px; }")
        self.ui.searchButton.clicked.connect(self.searchMusic)

    def searchFilms(self):
        input_film = self.ui.searchBar.text()
        recommendation = recommendFilm(input_film)
        self.ui.result1.setText(fromFilmTableToText(recommendation, 0))
        self.ui.result2.setText(fromFilmTableToText(recommendation, 1))
        self.ui.result3.setText(fromFilmTableToText(recommendation, 2))
        self.ui.result4.setText(fromFilmTableToText(recommendation, 3))
        self.ui.result5.setText(fromFilmTableToText(recommendation, 4))
        self.ui.result6.setText(fromFilmTableToText(recommendation, 5))

    def searchBooks(self):
        input_book = self.ui.searchBar.text()
        recommendation = recommendBook(input_book)
        self.ui.result1.setText(fromBookTableToText(recommendation, 0))
        self.ui.result2.setText(fromBookTableToText(recommendation, 1))
        self.ui.result3.setText(fromBookTableToText(recommendation, 2))
        self.ui.result4.setText(fromBookTableToText(recommendation, 3))
        self.ui.result5.setText(fromBookTableToText(recommendation, 4))
        self.ui.result6.setText(fromBookTableToText(recommendation, 5))

    def searchMusic(self):
        input_music = self.ui.searchBar.text()
        recommendation = recommendMusic(input_music)
        self.ui.result1.setText(fromMusicTableToText(recommendation, 0))
        self.ui.result2.setText(fromMusicTableToText(recommendation, 1))
        self.ui.result3.setText(fromMusicTableToText(recommendation, 2))
        self.ui.result4.setText(fromMusicTableToText(recommendation, 3))
        self.ui.result5.setText(fromMusicTableToText(recommendation, 4))
        self.ui.result6.setText(fromMusicTableToText(recommendation, 5))


    def refreshPage(self):
        self.ui.searchBar.setPlaceholderText("Search")
        self.ui.searchBar.setText("")
        self.ui.result1.setText("")
        self.ui.result2.setText("")
        self.ui.result3.setText("")
        self.ui.result4.setText("")
        self.ui.result5.setText("")
        self.ui.result6.setText("")

app = QtWidgets.QApplication([])
application = SuadeoUI()
application.show()

sys.exit(app.exec())