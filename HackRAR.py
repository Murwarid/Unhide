import itertools
import os
import subprocess
import sys
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QIcon, QClipboard, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QApplication, \
    QMessageBox, QTextEdit, QRadioButton, QFileDialog, QGroupBox, QSpacerItem, QSizePolicy, QCheckBox, QProgressBar, \
    QDialog
import aspose.zip as az
import time

filepath = "None"
selectedRadio = "1"
clickFlag = True
currentDir = os.getcwd()
currentDir = currentDir.replace("\\", "/", currentDir.count("\\", 0,len(currentDir)))

minlenght = 1
maxlenght = 5
charactersLower = "abcdefghijklmnopqrstuvwxyz"
charactersUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = " !@#$%^&*()_+-=[]{}|;:',.<>?/~`    "
prefix = ""
suffix = ""

allChars = numbers + charactersLower + charactersUpper + symbols

passwordDic = currentDir + "/passFiles/rockyou.txt"

def settings():
    global minlenght
    global maxlenght
    global charactersLower
    global charactersUpper
    global numbers
    global symbols
    global allChars
    global prefix
    global suffix

    if not int(passMaxLineEdit.text()) > int(passMinLineEdit.text()):
        messageBox("Error", "Set the length properly\nMax length must be greater than min length.", QMessageBox.Warning)
        passMinLineEdit.setText("1")
        passMaxLineEdit.setText("5")
    else:
        minlenght = int(passMinLineEdit.text())
        maxlenght = int(passMaxLineEdit.text())
        charactersLower = str(lowercaseLineEdit.text())
        if not lowercaseCheckbox.isChecked():
            charactersLower = ""
        charactersUpper = str(uppercaseLineEdit.text())
        if not uppercaseCheckbox.isChecked():
            charactersUpper = ""
        numbers = str(numbersLineEdit.text())
        if not numbersCheckbox.isChecked():
            numbers = ""
        symbols = str(symbolsLineEdit.text())
        if not symbolsCheckbox.isChecked():
            symbols = ""
        prefix = str(prefixLineEdit.text())
        if not prefixCheckbox.isChecked():
            prefix = ""
        suffix = str(suffixLineEdit.text())
        if not suffixCheckbox.isChecked():
            suffix = ""
        allChars = charactersLower + charactersUpper + numbers + symbols
        settingWindow.hide()


def messageBox(title, text, icon):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setIcon(icon)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


class ClickableTextEdit(QTextEdit):
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton) or (event.button() == Qt.RightButton) or (event.button() == Qt.TabFocus):
            if clickFlag:
                if filepath == "None":
                    file_field.setText("")
        super().mousePressEvent(event)


def add():
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("RAR/ZIP Files (*.rar *.zip)")

    if file_dialog.exec_():
        file_paths = file_dialog.selectedFiles()
        if file_paths:
            global filepath
            filepath = file_paths[0]
            file_field.setText(filepath)

        else:
            messageBox("File Error", "There isn't any file selected!", QMessageBox.Critical)


def getPassword(pswd):
    global password
    password = pswd


def copy():
    global password
    clipboard = QApplication.clipboard()
    clipboard.clear()
    clipboard.setText(password, mode=QClipboard.Clipboard)
    QMessageBox.information(hachRarWindow, " ", "Copied to Clipboard!")


def selectRadio1():
    settings_button.setEnabled(False)
    settings_button0.setEnabled(True)
    radio1.setChecked(True)
    radio2.setChecked(False)
    radio3.setChecked(False)
    global selectedRadio
    selectedRadio = "1"


def selectRadio2():
    settings_button.setEnabled(True)
    settings_button0.setEnabled(False)
    radio1.setChecked(False)
    radio2.setChecked(True)
    radio3.setChecked(False)
    global selectedRadio
    selectedRadio = "2"


def selectRadio3():
    settings_button.setEnabled(False)
    settings_button0.setEnabled(False)
    radio1.setChecked(False)
    radio2.setChecked(False)
    radio3.setChecked(True)
    global selectedRadio
    selectedRadio = "3"

    global minlenght
    global maxlenght
    global charactersLower
    global charactersUpper
    global numbers
    global symbols
    global allChars
    global prefix
    global suffix

    minlenght = 1
    maxlenght = 30
    charactersLower = "abcdefghijklmnopqrstuvwxyz"
    charactersUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789۰۱۲۳۴۵۶۷۸۹"
    symbols = " !@#$%^&*()_+-=[]{}|;:',.<>?/~`    "

    allChars = charactersLower + charactersUpper + numbers + symbols


def file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.zip':
        return 'ZIP'
    elif file_extension.lower() == '.rar':
        return 'RAR'
    else:
        return 'Unknown'


def update_progress_bar():
    currentVal = progress_bar.value()
    if currentVal == 0:
        progress_bar.setValue(50)
    elif currentVal == 50:
        progress_bar.setValue(100)
    elif currentVal == 100:
        progress_bar.setValue(0)


def updatePassLabel(count, start_time, end_time):
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    passCountLabel.setText(f"Total Checked Passwords: {str(count)}   Total Time Spent: {minutes}m:{seconds}s")


def crack_password(rar_file, password_list):
    # Set up the startupinfo to hide the window
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    start_time = time.perf_counter()
    passCount = 0
    progress_bar.setValue(0)
    count = True
    extract_dir = currentDir + "/HackRARFiles"

    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    extracted_files = os.listdir(extract_dir)
    for filename in extracted_files:
        filepath = os.path.join(extract_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    fileType = file_type(rar_file)

    if count:
        if (fileType.upper() == "RAR"):
            update_progress_bar()
            try:
                count = False
                # subprocess.run(['unrar', 'x', '-p{}'.format('TheFileIsUnprotected'), rar_file, extract_dir], check=True)
                subprocess.run(['unrar', 'x', '-p{}'.format('TheFileIsUnprotected'), rar_file, extract_dir], check=True,
                               startupinfo=startupinfo)
                progress_bar.setValue(100)
                end_time = time.perf_counter()
                updatePassLabel(1, start_time, end_time)
                return True, ""
            except:
                pass
        elif (fileType.upper() == "ZIP"):
            update_progress_bar()
            try:
                count = False
                with az.Archive(rar_file) as archive:
                    archive.extract_to_directory(extract_dir)
                progress_bar.setValue(100)
                end_time = time.perf_counter()
                updatePassLabel(1, start_time, end_time)
                return True, ""
            except:
                pass
    if (password_list != "None"):
        with open(password_list, 'r') as file:
            if (fileType.upper() == "RAR"):
                for line in file:
                    update_progress_bar()
                    passCount += 1
                    end_time = time.perf_counter()
                    updatePassLabel(passCount,start_time,end_time)
                    for word in line.split():
                        try:
                            # subprocess.run(['unrar', 'x', '-p{}'.format(word), rar_file, extract_dir], check=True)
                            subprocess.run(['unrar', 'x', '-p{}'.format(word), rar_file, extract_dir],
                                           check=True,
                                           startupinfo=startupinfo)
                            getPassword(word)
                            progress_bar.setValue(100)
                            end_time = time.perf_counter()
                            updatePassLabel(passCount + 1, start_time, end_time)
                            return True, word
                        except:
                            continue
            elif (fileType.upper() == "ZIP"):
                for line in file:
                    update_progress_bar()
                    passCount += 1
                    end_time = time.perf_counter()
                    updatePassLabel(passCount,start_time,end_time)
                    for word in line.split():
                        try:
                            options = az.ArchiveLoadOptions()
                            options.decryption_password = word

                            with az.Archive(rar_file, options) as archive:
                                archive.extract_to_directory(extract_dir)
                            getPassword(word)
                            progress_bar.setValue(100)
                            end_time = time.perf_counter()
                            updatePassLabel(passCount + 1, start_time, end_time)
                            return True, word
                        except:
                            continue
    elif (password_list == "None"):
        if (fileType.upper() == "RAR"):
            for length in range(minlenght, maxlenght + 1):
                combinations = itertools.product(allChars, repeat=length)
                for combination in combinations:
                    aWord = "".join(combination)
                    aWord = prefix + aWord + suffix
                    update_progress_bar()
                    passCount += 1
                    end_time = time.perf_counter()
                    updatePassLabel(passCount,start_time,end_time)
                    try:
                        # subprocess.run(['unrar', 'x', '-p{}'.format(aWord), rar_file, extract_dir], check=True)
                        subprocess.run(['unrar', 'x', '-p{}'.format(aWord), rar_file, extract_dir],
                                       check=True,
                                       startupinfo=startupinfo)
                        getPassword(aWord)
                        progress_bar.setValue(100)
                        end_time = time.perf_counter()
                        updatePassLabel(passCount + 1, start_time, end_time)
                        return True, aWord
                    except:
                        continue
        elif (fileType.upper() == "ZIP"):
            for length in range(minlenght, maxlenght + 1):
                combinations = itertools.product(allChars, repeat=length)
                for combination in combinations:
                    aWord = "".join(combination)
                    aWord = prefix + aWord + suffix
                    update_progress_bar()
                    passCount += 1
                    end_time = time.perf_counter()
                    updatePassLabel(passCount,start_time,end_time)
                    try:
                        options = az.ArchiveLoadOptions()
                        options.decryption_password = aWord

                        with az.Archive(rar_file, options) as archive:
                            archive.extract_to_directory(extract_dir)
                        getPassword(aWord)
                        progress_bar.setValue(100)
                        end_time = time.perf_counter()
                        updatePassLabel(passCount + 1, start_time, end_time)
                        return True, aWord
                    except:
                        continue

    return False, "None"


def start():
    fileaddress = file_field.toPlainText()
    if fileaddress == 'Write address or press "Add" button for inserting encrypted zip file.':
        messageBox("File Error", "There isn't any file selected!\nPlease select a file.", QMessageBox.Critical)
        add()

    elif not os.path.exists(fileaddress):
        global filepath
        filepath = " "
        messageBox("File Error", "The file is not exist or the inserted address is incorrect.", QMessageBox.Critical)

    else:
        if (selectedRadio == "1"):
            status = crack_password(fileaddress, passwordDic)
            Password = status[1]
            status = status[0]

            if status:
                passwordLabel.setEnabled(True)
                passwordLabel.setText('<b>Your password is:' + str(Password) + '</b>')
                copybutton.setEnabled(True)
                messageBox("Information", "Your password successfully found!", QMessageBox.Information)

            else:
                messageBox("Not Found", "Your password not found.\n"
                                        "Try a fixed dictionary attack or all possibility attack.",
                           QMessageBox.Information)
        elif (selectedRadio == "2"):
            status = crack_password(fileaddress, "None")
            Password = status[1]
            status = status[0]
            if status:
                passwordLabel.setEnabled(True)
                passwordLabel.setText('<b>Your password is:' + str(Password) + '</b>')
                copybutton.setEnabled(True)
                messageBox("Information", "Your password successfully found!", QMessageBox.Information)

            else:
                messageBox("Not Found", "Your password not found.\n"
                                        "Try all possibility attack and be patient that will take more time.",
                           QMessageBox.Information)

        elif (selectedRadio == "3"):
            status = crack_password(fileaddress, "None")
            Password = status[1]
            status = status[0]
            if status:
                passwordLabel.setEnabled(True)
                passwordLabel.setText('<b>Your password is:' + str(Password) + '</b>')
                copybutton.setEnabled(True)
                messageBox("Information", "Your password successfully found!", QMessageBox.Information)

            else:
                messageBox("Not Found", "Your password not found.\n"
                                        "I am sorry your password did not found it must be "
                                        "very hard complex password that did not found.",
                           QMessageBox.Information)


def close():
    sys.exit(1)


# --------------------------Setting0Window Functions--------------------------------

fileAdded = False

def manualAdd():
    global fileAdded
    global passwordDic
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("TXT Files (*.txt)")

    if file_dialog.exec_():
        file_paths = file_dialog.selectedFiles()
        if file_paths:
            global filepath
            filepath = file_paths[0]
            manualInsertLineEdit.setText(filepath)
            passwordDic = filepath
            fileAdded = True

        else:
            messageBox("File Error", "There isn't any file selected!", QMessageBox.Critical)


accumulated_data = [ currentDir + "/passFiles/rockyou.txt"]
whichRadio = "files"


def handleRadios():
    global accumulated_data
    global whichRadio
    data = None

    if rockyouRadio.isChecked():
        data = currentDir + "/passFiles/rockyou.txt"
    elif mostCommonRadio.isChecked():
        data = currentDir + "/passFiles/10k-most-common.txt"
    elif someCommonRadio.isChecked():
        data = currentDir + "/passFiles/SomeCommon.txt"
    elif mostUsedNCSCRadio.isChecked():
        data = currentDir + "/passFiles/100k-most-usedNCSC.txt"
    elif top100KRadio.isChecked():
        data = currentDir + "/passFiles/Top-100K.txt"
    elif top1MRadio.isChecked():
        data = currentDir + "/passFiles/Top-1M.txt"

    if data:
        accumulated_data.append(data)

    if selectFileRadio.isChecked():
        filesGroup.setEnabled(True)
        manualInsertLineEdit.setEnabled(False)
        manualInsertButton.setEnabled(False)
        manualInsertRadio.setChecked(False)
        whichRadio = "files"

    elif manualInsertRadio.isChecked():
        filesGroup.setEnabled(False)
        manualInsertLineEdit.setEnabled(True)
        manualInsertButton.setEnabled(True)
        selectFileRadio.setChecked(False)
        whichRadio = "manual"


def ok():
    global whichRadio
    global fileAdded
    global passwordDic
    global accumulated_data

    if whichRadio == "files":
        passwordDic = accumulated_data[len(accumulated_data) - 1]
        setting0Window.hide()
        print("files: ", passwordDic)
    elif whichRadio == "manual" and fileAdded:
        if os.path.exists(str(manualInsertLineEdit.text())):
            passwordDic = str(manualInsertLineEdit.text())
            setting0Window.hide()
            print("manual: ", passwordDic)
        else:
            messageBox("File Path Error", "The file path is not valid.\n"
                                          "Please insert a valid file address or press Add button to add a file.",
                       QMessageBox.Warning)

# ----------------------Setting0Window Function Finished-----------------------------

# ----------------------------Settings Window Functions----------------------------------------

def testRepitation(text):
    newText = list(text.lower())
    charRepitation = []
    indexOfRepited = []
    for i in range(len(newText)):
        if newText.count(newText[i]) >= 2:
            indexOfRepited.append(i)

    for j in indexOfRepited:
        if not newText[j] in charRepitation:
            charRepitation.append(newText[j])
        else:
            del newText[j]
    return "".join(newText)


def lowercaseText(text):
    text = testRepitation(text)
    lowercaseLineEdit.setText(text.lower())


def uppercaseText(text):
    text = testRepitation(text)
    uppercaseLineEdit.setText(text.upper())


def lowercaseCheck():
    if lowercaseCheckbox.isChecked():
        lowercaseLineEdit.setEnabled(True)
        print("The lowerchecked")
    else:
        print("The lower not checked")
        lowercaseLineEdit.setEnabled(False)


def uppercaseCheck():
    if uppercaseCheckbox.isChecked():
        uppercaseLineEdit.setEnabled(True)
    else:
        uppercaseLineEdit.setEnabled(False)


def numbers(num):
    num = testRepitation(num)
    numbersLineEdit.setText(num)


def numbersCheck():
    if numbersCheckbox.isChecked():
        numbersLineEdit.setEnabled(True)
    else:
        numbersLineEdit.setEnabled(False)


def symbols(sym):
    sym = testRepitation(sym)
    symbolsLineEdit.setText(sym)


def symbolsCheck():
    if symbolsCheckbox.isChecked():
        symbolsLineEdit.setEnabled(True)
    else:
        symbolsLineEdit.setEnabled(False)


def prefixCheck():
    if prefixCheckbox.isChecked():
        prefixLineEdit.setEnabled(True)
    else:
        prefixLineEdit.setEnabled(False)


def suffixCheck():
    if suffixCheckbox.isChecked():
        suffixLineEdit.setEnabled(True)
    else:
        suffixLineEdit.setEnabled(False)

# ----------------------------Settings Window Functions Finished-----------------------------------------

# ---------------------------------------------------Main Started----------------------------------------------
if __name__ == '__main__':
    hachRarApp = QApplication(sys.argv)
    hachRarWindow = QWidget()

    desktop = hachRarApp.desktop()
    screen = desktop.screenGeometry()
    screen_height = screen.height()
    screen_width = screen.width()

    hachRarWindow.setWindowIcon(QIcon(currentDir + "/icons/HackRaricon.ico"))
    hachRarWindow.setWindowTitle("WinRAR Password Cracker")
    hachRarWindow.setGeometry(int(screen_width / 2 - 550), int(screen_height / 2 - 220), 1100, 600)

    mainlayout = QVBoxLayout()

    pixmap = QPixmap(currentDir + "/icons/HackRarIcon3.ico")
    imagelabel = QLabel()
    imagelabel.setPixmap(pixmap)
    imagelabel.setStyleSheet("background-color: #f0f0f0;")
    mainlayout.addWidget(imagelabel)

    vbox = QVBoxLayout()

    progress_bar = QProgressBar()
    progress_bar.setFixedWidth(550)
    progress_bar.setMaximum(100)
    vbox.addWidget(progress_bar)

    hbox = QHBoxLayout()

    file_field = ClickableTextEdit(hachRarWindow)
    file_field.setContentsMargins(0, 0, 80, 40)
    file_field.setFixedSize(500, 35)
    file_field.setText('Write address or press "Add" button for inserting encrypted zip file.')

    hbox.addWidget(file_field)

    add_button = QPushButton("Add", hachRarWindow)
    add_button.clicked.connect(add)
    add_button.setFixedWidth(120)
    hbox.addWidget(add_button)
    add_button.setCursor(Qt.PointingHandCursor)

    vbox.addLayout(hbox)

    h1box = QHBoxLayout()

    radio1 = QRadioButton("Use known keywords (take little time).")
    h1box.addWidget(radio1)
    radio1.setCursor(Qt.PointingHandCursor)
    radio1.setFixedSize(416, 40)
    radio1.setChecked(True)
    radio1.clicked.connect(selectRadio1)



    # ------------------------Settings0Window Started -----------------------------


    setting0Window = QDialog(hachRarWindow)

    setting0Window.setWindowIcon(QIcon(currentDir + "/icons/Settings.ico"))
    setting0Window.setWindowTitle("Known Keyword Attack Settings")
    setting0Window.setGeometry(int(screen_width / 2 - 540), int(screen_height / 2 - 210), 1090, 600)

    setting0layout = QVBoxLayout()

    label0Layout = QVBoxLayout()
    setting0Label = QLabel("<b>Select From Following Keywords Files or Manually Insert One:</b>")
    label0Layout.addWidget(setting0Label)
    empty0Label = QLabel("")
    label0Layout.addWidget(empty0Label)
    label0Layout.setAlignment(Qt.AlignCenter)
    setting0layout.addLayout(label0Layout)

    selectFileRadio = QRadioButton("Select a Dictionary")
    selectFileRadio.setChecked(True)
    selectFileRadio.clicked.connect(handleRadios)
    setting0layout.addWidget(selectFileRadio)

    filesGroup = QGroupBox("Files")
    group0Hbox = QHBoxLayout()
    filesGroup.setLayout(group0Hbox)

    groupVbox0 = QVBoxLayout()

    rockyouRadio = QRadioButton("RockYou")
    rockyouRadio.setChecked(True)
    rockyouRadio.clicked.connect(handleRadios)
    groupVbox0.addWidget(rockyouRadio)

    mostCommonRadio = QRadioButton("10k-most-common")
    mostCommonRadio.clicked.connect(handleRadios)
    groupVbox0.addWidget(mostCommonRadio)

    group0Hbox.addLayout(groupVbox0)

    groupVbox1 = QVBoxLayout()

    someCommonRadio = QRadioButton("SomeCommon")
    someCommonRadio.clicked.connect(handleRadios)
    groupVbox1.addWidget(someCommonRadio)

    mostUsedNCSCRadio = QRadioButton("100k-most-usedNCSC")
    mostUsedNCSCRadio.clicked.connect(handleRadios)
    groupVbox1.addWidget(mostUsedNCSCRadio)

    group0Hbox.addLayout(groupVbox1)

    groupVbox2 = QVBoxLayout()

    top100KRadio = QRadioButton("Top-100K")
    top100KRadio.clicked.connect(handleRadios)
    groupVbox2.addWidget(top100KRadio)

    top1MRadio = QRadioButton("Top-1M")
    top1MRadio.clicked.connect(handleRadios)
    groupVbox2.addWidget(top1MRadio)

    group0Hbox.addLayout(groupVbox2)

    setting0layout.addLayout(group0Hbox)

    setting0layout.addWidget(filesGroup)

    manualInsertRadio = QRadioButton("Manual Insert Password Dictionary")
    manualInsertRadio.clicked.connect(handleRadios)
    setting0layout.addWidget(manualInsertRadio)

    manualHbox = QHBoxLayout()
    manualInsertLineEdit = QLineEdit("")
    manualInsertLineEdit.setEnabled(False)
    manualHbox.addWidget(manualInsertLineEdit)

    manualInsertButton = QPushButton("Add")
    manualInsertButton.setEnabled(False)
    manualInsertButton.clicked.connect(manualAdd)
    manualHbox.addWidget(manualInsertButton)

    setting0layout.addLayout(manualHbox)

    okButton = QPushButton("Ok")
    okButton.setFixedWidth(200)
    okButton.clicked.connect(ok)
    setting0layout.addWidget(okButton)

    setting0layout.setAlignment(Qt.AlignCenter)
    setting0Window.setLayout(setting0layout)

    # ---------------------Settings0Window Finished----------------------------------------


    settings_button0 = QPushButton("")
    settings_button0.setFixedSize(30, 30)
    settings_button0.setCursor(Qt.PointingHandCursor)
    icon = QIcon(currentDir + "/icons/Settings.ico")
    settings_button0.setIcon(icon)
    settings_button0.clicked.connect(setting0Window.exec_)
    settings_button0.setEnabled(True)
    h1box.addWidget(settings_button0)

    vbox.addLayout(h1box)

    h2box = QHBoxLayout()
    radio2 = QRadioButton("Use Fixed Dictionary Attack (depends on your settings).")
    radio2.setCursor(Qt.PointingHandCursor)
    radio2.setFixedSize(416, 40)
    radio2.clicked.connect(selectRadio2)
    h2box.addWidget(radio2)


    # ----------------------------Settings Window-----------------------------------------

    settingWindow = QDialog(hachRarWindow)

    settingWindow.setWindowIcon(QIcon(currentDir + "/icons/Settings.ico"))
    settingWindow.setWindowTitle("Fixed Dictionary Attack Settings")
    settingWindow.setGeometry(int(screen_width / 2 - 540), int(screen_height / 2 - 210), 1090, 600)

    settinglayout = QVBoxLayout()

    labelLayout = QVBoxLayout()
    settingLabel = QLabel("<b>How Much You Know About Your Forgotten Password</b>")
    labelLayout.addWidget(settingLabel)
    emptyLabel = QLabel("")
    labelLayout.addWidget(emptyLabel)
    labelLayout.setAlignment(Qt.AlignCenter)
    settinglayout.addLayout(labelLayout)

    passLengthGroup = QGroupBox("Password Length")
    firstLayout = QHBoxLayout()
    passLengthGroup.setLayout(firstLayout)

    firstLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    passMinLabel = QLabel("Minimum Password Length:")
    firstLayout.addWidget(passMinLabel)

    passMinLineEdit = QLineEdit("1")
    passMinLineEdit.setFixedWidth(30)
    passMinValidator = QRegExpValidator(QRegExp("[0-9]+"))
    passMinLineEdit.setValidator(passMinValidator)
    firstLayout.addWidget(passMinLineEdit)

    passEmptyLabel = QLabel("")
    firstLayout.addWidget(passEmptyLabel)

    passMaxLabel = QLabel("Maximum Password Length:")
    firstLayout.addWidget(passMaxLabel)

    passMaxLineEdit = QLineEdit("5")
    passMaxLineEdit.setFixedWidth(30)
    passMaxValidator = QRegExpValidator(QRegExp("[0-9]+"))
    passMaxLineEdit.setValidator(passMaxValidator)
    firstLayout.addWidget(passMaxLineEdit)

    firstLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    settinglayout.addLayout(firstLayout)

    settinglayout.addWidget(passLengthGroup)

    charSetGroup = QGroupBox("Characters Setting")

    secondLayout = QHBoxLayout()
    charSetGroup.setLayout(secondLayout)

    secondLayout1 = QVBoxLayout()

    charsetHbox1 = QHBoxLayout()
    charsetHbox1.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    lowercaseCheckbox = QCheckBox("Lowercase letters")
    lowercaseCheckbox.setChecked(True)
    lowercaseCheckbox.clicked.connect(lowercaseCheck)
    charsetHbox1.addWidget(lowercaseCheckbox)

    lowercaseLineEdit = QLineEdit("abcdefghijklmnopqrstuvwxyz")
    lowercaseLineEdit.setFixedWidth(265)
    lowercaseLineEdit.textChanged.connect(lowercaseText)
    lowercaseValidator = QRegExpValidator(QRegExp("[a-zA-Z]+"))
    lowercaseLineEdit.setValidator(lowercaseValidator)
    charsetHbox1.addWidget(lowercaseLineEdit)

    charsetHbox1.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    secondLayout1.addLayout(charsetHbox1)

    charsetHbox2 = QHBoxLayout()
    charsetHbox2.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    uppercaseCheckbox = QCheckBox("Uppercase letters")
    uppercaseCheckbox.setChecked(True)
    uppercaseCheckbox.clicked.connect(uppercaseCheck)
    charsetHbox2.addWidget(uppercaseCheckbox)

    uppercaseLineEdit = QLineEdit("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    uppercaseLineEdit.setFixedWidth(265)
    uppercaseLineEdit.textChanged.connect(uppercaseText)
    uppercaseValidator = QRegExpValidator(QRegExp("[a-zA-Z]+"))
    uppercaseLineEdit.setValidator(uppercaseValidator)
    charsetHbox2.addWidget(uppercaseLineEdit)

    charsetHbox2.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    secondLayout1.addLayout(charsetHbox2)
    secondLayout.addLayout(secondLayout1)

    secondLayout2 = QVBoxLayout()
    charSetGroup.setLayout(secondLayout2)

    charsetHbox1 = QHBoxLayout()
    charsetHbox1.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    numbersCheckbox = QCheckBox("Numbers")
    numbersCheckbox.setChecked(True)
    numbersCheckbox.clicked.connect(numbersCheck)
    charsetHbox1.addWidget(numbersCheckbox)

    numbersLineEdit = QLineEdit("۰۱۲۳۴۵۶۷۸۹0123456789")
    numbersLineEdit.setFixedWidth(280)
    numbersValidator = QRegExpValidator(QRegExp("[0-9۰-۹]+"))
    numbersLineEdit.setValidator(numbersValidator)
    numbersLineEdit.textChanged.connect(numbers)
    charsetHbox1.addWidget(numbersLineEdit)

    charsetHbox1.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    secondLayout2.addLayout(charsetHbox1)

    charsetHbox2 = QHBoxLayout()
    charsetHbox2.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    symbolsCheckbox = QCheckBox("Symbols")
    symbolsCheckbox.setChecked(True)
    symbolsCheckbox.clicked.connect(symbolsCheck)
    charsetHbox2.addWidget(symbolsCheckbox)

    symbolsLineEdit = QLineEdit("~!@#$%^&*()_+{}:\"|<>?`-=[];'\\,./")
    symbolsLineEdit.setFixedWidth(280)
    symbolsValidator = QRegExpValidator(QRegExp("[^0-9a-zA-Zا-ی۰-۹]+"))
    symbolsLineEdit.setValidator(symbolsValidator)
    symbolsLineEdit.textChanged.connect(symbols)
    charsetHbox2.addWidget(symbolsLineEdit)

    charsetHbox2.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    secondLayout2.addLayout(charsetHbox2)

    secondLayout.addLayout(secondLayout2)

    settinglayout.addWidget(charSetGroup)

    affixGroup = QGroupBox("Affix Settings")
    thirdLayout = QHBoxLayout()
    affixGroup.setLayout(thirdLayout)

    prefixHbox = QHBoxLayout()
    prefixHbox.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    prefixCheckbox = QCheckBox("Specify your password prefix:")
    prefixCheckbox.clicked.connect(prefixCheck)
    prefixHbox.addWidget(prefixCheckbox)

    prefixLineEdit = QLineEdit()
    prefixLineEdit.setFixedWidth(150)
    prefixLineEdit.setEnabled(False)
    prefixHbox.addWidget(prefixLineEdit)

    prefixHbox.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    thirdLayout.addLayout(prefixHbox)

    suffixHbox = QHBoxLayout()
    suffixHbox.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    suffixCheckbox = QCheckBox("Specify your password suffix:")
    suffixCheckbox.clicked.connect(suffixCheck)
    suffixHbox.addWidget(suffixCheckbox)

    suffixLineEdit = QLineEdit()
    suffixLineEdit.setFixedWidth(150)
    suffixLineEdit.setEnabled(False)
    suffixHbox.addWidget(suffixLineEdit)

    suffixHbox.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    thirdLayout.addLayout(suffixHbox)

    settinglayout.addWidget(affixGroup)

    setButtonLayout = QVBoxLayout()
    buttonEmptyLabel = QLabel("")
    setButtonLayout.addWidget(buttonEmptyLabel)
    setSettingButton = QPushButton("Set")
    setSettingButton.setFixedSize(150, 45)
    setButtonLayout.addWidget(setSettingButton)
    setSettingButton.clicked.connect(settings)
    setButtonLayout.setAlignment(Qt.AlignCenter)
    settinglayout.addLayout(setButtonLayout)

    settinglayout.setAlignment(Qt.AlignCenter)
    settingWindow.setLayout(settinglayout)
    # -----------------------------------SettingsWindow Finished---------------------------


    settings_button = QPushButton("")
    settings_button.setFixedSize(30, 30)
    settings_button.setCursor(Qt.PointingHandCursor)
    icon = QIcon(currentDir + "/icons/Settings.ico")
    settings_button.setIcon(icon)
    settings_button.clicked.connect(settingWindow.exec_)
    settings_button.setEnabled(False)
    h2box.addWidget(settings_button)

    vbox.addLayout(h2box)

    h3box = QHBoxLayout()

    radio3 = QRadioButton("Use all possibilities.")
    radio3.setFixedSize(513, 40)
    radio3.setCursor(Qt.PointingHandCursor)
    radio3.clicked.connect(selectRadio3)
    h3box.addWidget(radio3)

    vbox.addLayout(h3box)

    h4box = QHBoxLayout()
    startButton = QPushButton("Start")
    startButton.clicked.connect(start)
    startButton.setFixedWidth(120)
    startButton.setCursor(Qt.PointingHandCursor)
    h4box.addWidget(startButton)

    cancelButton = QPushButton("Close")
    cancelButton.clicked.connect(close)
    cancelButton.setFixedWidth(120)
    cancelButton.setCursor(Qt.PointingHandCursor)
    h4box.addWidget(cancelButton)
    vbox.addLayout(h4box)

    vbox.setAlignment(Qt.AlignCenter)
    mainlayout.addLayout(vbox)

    labelsBox = QVBoxLayout()

    h5box = QHBoxLayout()

    passwordLabel = QLabel('<b>Your password is: XXXXXXXXXX</b>')
    passwordLabel.setEnabled(False)

    h5box.addWidget(passwordLabel)

    copybutton = QPushButton("Copy")
    copybutton.clicked.connect(copy)
    copybutton.setEnabled(False)
    copybutton.setFixedWidth(120)
    h5box.addWidget(copybutton)
    h5box.setAlignment(Qt.AlignCenter)

    labelsBox.setAlignment(Qt.AlignCenter)
    labelsBox.addLayout(h5box)

    passCountLabel = QLabel("Total Checked Passwords: 000000   Total Time Spent: 00m:00s            .")
    passCountLabel.setMaximumSize(900,50)
    passCountLabel.setMinimumSize(600, 50)
    labelsBox.addWidget(passCountLabel)

    mainlayout.addLayout(labelsBox)

    label_width = screen_width * 0.065

    createBox = QHBoxLayout()
    createBox.addStretch(1)

    creatorLabel = QLabel("Created By Asrar")
    creatorLabel.setStyleSheet("color: gray;")
    creatorLabel.setMaximumSize(int(label_width), 11777515)
    createBox.addWidget(creatorLabel)

    mainlayout.addLayout(createBox)
    mainlayout.setAlignment(Qt.AlignTop)
    hachRarWindow.setLayout(mainlayout)
    hachRarWindow.show()
    hachRarApp.exec_()
