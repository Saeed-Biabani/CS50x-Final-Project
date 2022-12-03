# Enigma Machine
## CS50
> This was my final project for conclude the CS50 Introduction to Computer Sciense course.

> [Python](https://www.python.org/), [PyQt5](https://doc.qt.io/qtforpython/), [SQLite3](https://www.sqlite.org/index.html), [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface), [CS50](https://cs50.harvard.edu/x/2020/)
## URL
> [Video](https://youtu.be/H7qL61GzwY8)
## Explaining the project and the database

My Project is a GUI app that allows the user to encrypt the desired message, so that no one knows it's content.

and recive the encrypted text in a .txt file and send it to the recipient.

It can also save the message & decodeing settings in the DataBase so as not to lose them.

- All information about users, login, message and selected setting for each people are stored in Cryptography.db.

```sql
CREATE TABLE info (id INT PRIMARY KEY NOT NULL, name TEXT, phone TEXT, email TEXT);
CREATE TABLE user_pass (person_id INT PRIMARY KEY NOT NULL, user TEXT, pass TEXT);
CREATE TABLE msg (person_id INT NOT NULL, rotor_id INT NOT NULL, date TEXT, time TEXT, msg TEXT);
CREATE TABLE login (person_id INT NOT NULL, date TEXT, time TEXT);
CREATE TABLE setting (rotor_id INT PRIMARY KEY NOT NULL, alpha_1 TEXT, alpha_2 TEXT, alpha_3 TEXT, beta_1 TEXT, beta_2 TEXT, beta_3 TEXT);

```
> SQL Schematic

### Encryption

```python
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
```
> This part has the task of saving user logins to the program in the database.

```python

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

```
> This section is for encodeing alphabets.

```python

def Reflector(self, char):
        if char in self.alphabet:
            return self.alphabet[len(self.alphabet)-self.alphabet.index(char)-1] 
         
        elif char in self.num:
            return self.num[len(self.num)-self.num.index(char)-1] 

```
> The task of this part is to reflect the characters that are sent to it.
### Description

- Execute ```$ python3 Setting.py```
> It will give you a file that named Rotors.setting
- Execute ```$ python3 Enugma.py```
- Login whit your Username & Password
- From ```Manual Setting``` select ```Rotors.setting```
> This is a binary file that configures the machine
- Now you can write your message in input box
> From ```Input File``` You can also use .txt file as input

### About CS50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

Thank you for all CS50.

- Where I get CS50 course?
https://cs50.harvard.edu/x/2020/
