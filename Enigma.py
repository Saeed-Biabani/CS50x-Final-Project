from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QFileDialog, QLabel
from PyQt5.uic import loadUi
import sys
from sqlite3 import *
import pickle
import datetime

class Enigma(QMainWindow):
    def __init__(self):
        super(Enigma , self).__init__()
        loadUi("enigma.ui" , self)
        
        self.rotor_1 = ''
        self.rotor_beta_1 = ''
        
        self.rotor_2 = ''
        self.rotor_beta_2 = ''
        
        self.rotor_3 = ''
        self.rotor_beta_3 = ''
        
        self.result = self.findChild(QTextEdit , 'result')
        self.txt = self.findChild(QLineEdit , 'input')
        self.bcs = self.findChild(QPushButton, 'bcs')
        self.txt = self.findChild(QTextEdit , 'txt')
        self.reset = self.findChild(QPushButton , 'reset')
        self.browse = self.findChild(QPushButton , 'browse')
        self.setting = self.findChild(QPushButton , 'setting')
        self.username = self.findChild(QLineEdit, 'username')
        self.password = self.findChild(QLineEdit, 'password')
        self.show_user_info = self.findChild(QLineEdit, 'show_user_info')
        self.save_db = self.findChild(QPushButton, 'save_db')
        self.login = self.findChild(QPushButton , 'login')
        self.r1 = self.findChild(QLabel , 'r1')
        self.r2 = self.findChild(QLabel , 'r2')
        self.r3 = self.findChild(QLabel , 'r3')
        
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.num = '1234567890'
        
        self.cipher = ''
        self.plain = ''
        self.setting_path = ''
        
        self.db = connect("Cryptography.db")
        self.person_id = ''
        self.rotor_id = 0
        
        self.rotate_counter = 0
        self.unrotate_counter = 0
        
        self._now = datetime.datetime.now()
        
        self.input.setEnabled(False)
        self.reset.setEnabled(False)
        self.browse.setEnabled(False)
        self.bcs.setEnabled(False)
        self.setting.setEnabled(False)
        self.save_db.setEnabled(False)
        
        self.show_user_info.hide()
        
        self.input.textChanged['QString'].connect(self.Get_input)
        self.input.textChanged['QString'].connect(self.input.clear)
        self.input.returnPressed.connect(self.Next_Line)
        self.password.returnPressed.connect(self._login)
        self.bcs.clicked.connect(self.Dell)
        self.reset.clicked.connect(self.reset_app)
        self.browse.clicked.connect(self.browse_file)
        self.setting.clicked.connect(self.Setting)
        self.login.clicked.connect(self._login)
        self.save_db.clicked.connect(self.save_on_db)
        self.bcs.clicked.connect(self.input.setFocus)
        
    def _login(self):
        _user = self.username.text()
        _pass = self.password.text()
        
        crs = self.db.cursor()
        
        res = crs.execute(f"SELECT pass FROM user_pass where user = '{_user}'")
        
        for item in res:
            if item[0] == _pass:
                self.setting.setEnabled(True)
                self.username.close()
                self.password.close()
                self.login.close()
                
                ask = crs.execute(f"SELECT person_id FROM user_pass where user = '{_user}'")
                for _id in ask:
                    self.person_id = _id[0]
                
                self.show_info(self.person_id)
                crs.execute(f"INSERT INTO login VALUES ({self.person_id}, '{self._now.date()}', '{self._now.time()}')")
                self.db.commit()
    
    def show_info(self, _id):
        crs = self.db.cursor()
        
        res = crs.execute(f"SELECT name FROM info where id = '{_id}'")
        
        for item in res:
            name = item[0]
            
        self.show_user_info.show()
        self.show_user_info.setText(f"{name} : {self.person_id}")
        
    def save_on_db(self):
        crs = self.db.cursor()
        crs.execute(f"INSERT INTO msg VALUES ({self.person_id}, {self.rotor_id}, '{self._now.date()}', '{self._now.time()}', '{self.cipher}')")
        self.db.commit()
        
    
    def browse_file(self):
        fname = QFileDialog.getOpenFileName(self, "Browse")
        if fname[0] != '':
            with open(fname[0], "r") as input_file:
                reader = input_file.read()
                for char in reader:
                    self.Get_Char(char)
    
    
    def Get_input(self):
        char = self.input.text()
        self.Get_Char(char)
        
        
    def reset_app(self):
        self.cipher = ''
        self.plain = ''
        self.fix_setting(self.setting_path)
        self.Write()
        self._now = datetime.datetime.now()
    
    
    def Setting(self):
        fname = QFileDialog.getOpenFileName(self, "Browse")
        if fname[0] != '':
            self.setting_path = fname[0]
            self.fix_setting(fname[0])
            self.save_setting()
            
            
    def save_setting(self):
        crs = self.db.cursor()
        res = crs.execute("SELECT rotor_id FROM setting ORDER BY rotor_id DESC LIMIT 1")
        for item in res:
            self.rotor_id = item[0]+1
        
        crs.execute(f"INSERT INTO setting VALUES ({self.rotor_id}, '{self.rotor_1}', '{self.rotor_2}', '{self.rotor_3}', '{self.rotor_beta_1}', '{self.rotor_beta_2}', '{self.rotor_beta_3}')")
        self.db.commit()
         
    
    def fix_setting(self, fname):
        
        self.rotate_counter = 0
        self.unrotate_counter = 0
        
        self.input.setEnabled(True)
        self.reset.setEnabled(True)
        self.browse.setEnabled(True)
        self.bcs.setEnabled(True)
        self.save_db.setEnabled(True)
        
        with open(fname, 'rb') as setting:
            self.rotor_1, self.rotor_beta_1, self.rotor_2, self.rotor_beta_2, self.rotor_3, self.rotor_beta_3 = pickle.load(setting)
        self.make_label()
          
    
    def Get_Char(self, char):
        
        if char != '' and char in self.alphabet:
            # self.rotate_counter += 1
            self.plain += char
            self.Encode_Alpha((char, 'l'))
            
        elif char != '' and char in self.alphabet_upper:
            # self.rotate_counter += 1
            self.plain += char
            self.Encode_Alpha((char, 'u'))
        
        elif char != '' and char in self.num:
            # self.rotate_counter += 1
            self.plain += char
            self.Encode_Beta(char)
            
        elif char == ' ' or char not in self.alphabet:
            self.plain += char
            self.Make_Text(char)
        
        
    def Reflector(self, char):
        if char in self.alphabet:
            return self.alphabet[len(self.alphabet)-self.alphabet.index(char)-1] 
         
        elif char in self.num:
            return self.num[len(self.num)-self.num.index(char)-1] 
    
    
    def Encode_Beta(self, char):
        index = self.num.index(char)
        c1 = self.rotor_beta_1[index]
        
        index = self.num.index(c1)
        c2 = self.rotor_beta_2[index]
        
        index = self.num.index(c2)
        c3 = self.rotor_beta_3[index]
        
        r = self.Reflector(c3)
        
        index = self.rotor_beta_3.index(r)
        c3 = self.num[index]
        
        index = self.rotor_beta_2.index(c3)
        c2 = self.num[index]
        
        index = self.rotor_beta_1.index(c2)
        char= self.num[index]
        
        self.Make_Text(char)
        # self.Rotate()
    
    
    def Encode_Alpha(self, char):
        char_lower = char[0].lower()
        
        index = self.alphabet.index(char_lower)
        c1 = self.rotor_1[index]
        
        index = self.alphabet.index(c1)
        c2 = self.rotor_2[index]
        
        index = self.alphabet.index(c2)
        c3 = self.rotor_3[index]
        
        r = self.Reflector(c3)
        
        index = self.rotor_3.index(r)
        c3 = self.alphabet[index]
        
        index = self.rotor_2.index(c3)
        c2 = self.alphabet[index]
        
        index = self.rotor_1.index(c2)
        c1= self.alphabet[index]
        
        if char[1] == 'u':
            c1 = c1.upper()
        
        self.Make_Text(c1)
        self.rotate_counter += 1
        self.Rotate()

        
    def Rotate(self):
        self.rotor_1 = self.rotor_1[1:] + self.rotor_1[0]
        
        if self.rotate_counter % 26 == 0:
            self.rotor_2 = self.rotor_2[1:] + self.rotor_2[0]
            if self.rotate_counter  % (26*26) == 0:
                self.rotor_3 = self.rotor_3[1:] + self.rotor_3[0]


    def Make_Text(self, char):
        self.cipher += char
        self.Write()

        
    def Next_Line(self):
        self.plain += '\n'
        self.Make_Text('\n')

        
    def Dell(self):
        if self.cipher != '':
            if self.cipher[-1] != ' ':
                self.unrotate_counter += 1
                self.Unrotate()
            self.cipher = self.cipher[:-1]
            self.plain = self.plain[:-1]
            self.Write()
    
    
    def Unrotate(self):
        self.rotor_1 = self.rotor_1[-1] + self.rotor_1[:-1]
        
        if self.unrotate_counter % 26 == 0:
            self.rotor_2 = self.rotor_2[-1] + self.rotor_2[:-1]
            if self.unrotate_counter  % (26*26) == 0:
                self.rotor_3 = self.rotor_3[-1] + self.rotor_3[:-1]
    
    
    def make_label(self):
        self.r1.setText(self.rotor_1[0])
        self.r2.setText(self.rotor_2[0])
        self.r3.setText(self.rotor_3[0])            

    
    def Write(self):
        self.make_label()
        self.result.setText(self.cipher)
        self.txt.setText(self.plain)
        self._File()


    def _File(self):
        with open('Message.txt', 'w') as file:
            file.write(self.cipher)


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Enigma()
    window.show()
    sys.exit(app.exec_())