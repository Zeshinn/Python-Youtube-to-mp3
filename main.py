import yt_dlp
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import threading
ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'ffmpeg_location': '.\\ffmpeg.exe'
    }


class YouTubeMP3Converter(QWidget):
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.t1 = threading.Thread()

    def init_ui(self):
        self.setWindowTitle("YouTube MP3 Converter")
        self.setFixedSize(400, 250)
        self.setStyleSheet("background-color: #212121; color: white;")

        main_layout = QVBoxLayout()

        title_label = QLabel("YouTube MP3 Converter")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #FF0000; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        input_label = QLabel("Enter YouTube Link:")
        input_label.setFont(QFont("Arial", 12))
        input_label.setStyleSheet("margin-bottom: 10px;")
        main_layout.addWidget(input_label)

        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Paste YouTube link here")
        self.link_input.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 5px;
                color: white;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 1px solid #FF0000;
            }
        """)
        main_layout.addWidget(self.link_input)

        download_button = QPushButton("Download MP3")
        download_button.setFont(QFont("Arial", 12))
        download_button.setCursor(Qt.PointingHandCursor)
        download_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        main_layout.addWidget(download_button)
        download_button.clicked.connect(self.on_download_clicked)
        
        trademark_label = QLabel("Powered by Denis Ivanov™")
        trademark_label.setFont(QFont("Arial", 10, True))
        trademark_label.setAlignment(Qt.AlignCenter)
        trademark_label.setStyleSheet("color: #888888; margin-top: 20px;")
        main_layout.addWidget(trademark_label)

        self.setLayout(main_layout)

    
    def download_mp3(self):
        if(self.link_input.text() == ""):
            return
        URLS = [self.link_input.text()]
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                error_code = ydl.download(URLS)
                self.link_input.setText("")
                if error_code == 0:
                    self.link_input.setPlaceholderText("Successful!")
                else:
                    self.link_input.setPlaceholderText("Error!")
            except Exception:
                self.link_input.setText("")
                self.link_input.setPlaceholderText("Error!")
    
    def on_download_clicked(self):
        if self.t1.is_alive():
            self.link_input.setText("")
            self.link_input.setPlaceholderText("Already Converting! Please Wait!")
        else:
            self.t1 = threading.Thread(target=self.download_mp3)
            self.t1.start()    
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeMP3Converter()
    window.show()
    sys.exit(app.exec_())