import sys
import random
import math
import os
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QTextEdit, QTabWidget

class RSAKeyGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('RSA Key Generator')
        self.resize(600, 400)
        self.layout = QVBoxLayout()

        # Создаем вкладки
        self.tabs = QTabWidget()
        self.generate_tab = QWidget()
        self.encrypt_tab = QWidget()
        self.decrypt_tab = QWidget()
        self.crack_tab = QWidget()
        self.brute_force_tab = QWidget()
        self.tabs.addTab(self.generate_tab, "Generate Keys")
        self.tabs.addTab(self.encrypt_tab, "Encrypt Message")
        self.tabs.addTab(self.decrypt_tab, "Decrypt Message")
        self.tabs.addTab(self.crack_tab, "Crack Cipher")
        self.tabs.addTab(self.brute_force_tab, "Brute Force Attack")

        # Настройка вкладки для генерации ключей
        self.init_generate_tab()

        # Настройка вкладки для шифрования сообщения
        self.init_encrypt_tab()

        # Настройка вкладки для дешифровки сообщения
        self.init_decrypt_tab()

        # Настройка вкладки для взлома шифра
        self.init_crack_tab()

        # Настройка вкладки для метода полного перебора
        self.init_brute_force_tab()

        # Добавляем вкладки в главное окно
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def init_generate_tab(self):
        self.generate_tab.layout = QVBoxLayout()

        self.key_length_label = QLabel('Key Length (in bits):')
        self.key_length_spinbox = QSpinBox()
        self.key_length_spinbox.setMinimum(8)
        self.key_length_spinbox.setMaximum(1024)
        self.key_length_spinbox.setValue(8)

        self.generate_button = QPushButton('Generate Keys')
        self.generate_button.clicked.connect(self.generate_keys)

        self.result_label = QLabel('')

        self.generate_tab.layout.addWidget(self.key_length_label)
        self.generate_tab.layout.addWidget(self.key_length_spinbox)
        self.generate_tab.layout.addWidget(self.generate_button)
        self.generate_tab.layout.addWidget(self.result_label)

        self.generate_tab.setLayout(self.generate_tab.layout)

    def init_encrypt_tab(self):
        self.encrypt_tab.layout = QVBoxLayout()

        self.public_key_label = QLabel('Public Key (n e):')
        self.public_key_edit = QTextEdit()
        
        self.load_public_key_button = QPushButton('Load Public Key from File')
        self.load_public_key_button.clicked.connect(self.load_public_key_file)
        self.encrypt_tab.layout.addWidget(self.load_public_key_button)

        self.message_label = QLabel('Message:')
        self.message_edit = QTextEdit()

        self.encrypt_button = QPushButton('Encrypt')
        self.encrypt_button.clicked.connect(self.encrypt_message)

        self.encrypted_message_label = QLabel('Encrypted Message:')
        self.encrypted_message_edit = QTextEdit()
        self.encrypted_message_edit.setReadOnly(True)

        self.encrypt_tab.layout.addWidget(self.public_key_label)
        self.encrypt_tab.layout.addWidget(self.public_key_edit)
        self.encrypt_tab.layout.addWidget(self.message_label)
        self.encrypt_tab.layout.addWidget(self.message_edit)
        self.encrypt_tab.layout.addWidget(self.encrypt_button)
        self.encrypt_tab.layout.addWidget(self.encrypted_message_label)
        self.encrypt_tab.layout.addWidget(self.encrypted_message_edit)

        self.encrypt_tab.setLayout(self.encrypt_tab.layout)

    def init_decrypt_tab(self):
        self.decrypt_tab.layout = QVBoxLayout()

        self.private_key_label = QLabel('Private Key (n d):')
        self.private_key_edit = QTextEdit()

        self.load_private_key_button = QPushButton('Load Private Key from File')
        self.load_private_key_button.clicked.connect(self.load_private_key_file)
        self.decrypt_tab.layout.addWidget(self.load_private_key_button)

        self.encrypted_message_label_2 = QLabel('Encrypted Message (hex):')
        self.encrypted_message_edit_2 = QTextEdit()

        self.load_encrypted_message_button = QPushButton('Load Encrypted Message from File')
        self.load_encrypted_message_button.clicked.connect(self.load_encrypted_message_file)
        self.decrypt_tab.layout.addWidget(self.load_encrypted_message_button)

        self.decrypt_button = QPushButton('Decrypt')
        self.decrypt_button.clicked.connect(self.decrypt_message)

        self.decrypted_message_label = QLabel('Decrypted Message:')
        self.decrypted_message_edit = QTextEdit()
        self.decrypted_message_edit.setReadOnly(True)

        self.decrypt_tab.layout.addWidget(self.private_key_label)
        self.decrypt_tab.layout.addWidget(self.private_key_edit)
        self.decrypt_tab.layout.addWidget(self.encrypted_message_label_2)
        self.decrypt_tab.layout.addWidget(self.encrypted_message_edit_2)
        self.decrypt_tab.layout.addWidget(self.decrypt_button)
        self.decrypt_tab.layout.addWidget(self.decrypted_message_label)
        self.decrypt_tab.layout.addWidget(self.decrypted_message_edit)

        self.decrypt_tab.setLayout(self.decrypt_tab.layout)

    def init_crack_tab(self):
        self.crack_tab.layout = QVBoxLayout()

        self.public_key_label_2 = QLabel('Public Key (n e):')
        self.public_key_edit_2 = QTextEdit()

        self.load_public_key_button_2 = QPushButton('Load Public Key')
        self.load_public_key_button_2.clicked.connect(self.load_public_key_file_2)

        self.crack_button = QPushButton('Crack Cipher')
        self.crack_button.clicked.connect(self.crack_cipher)

        self.cracked_key_label = QLabel('Cracked Private Key (n d):')
        self.cracked_key_edit = QTextEdit()
        self.cracked_key_edit.setReadOnly(True)

        self.crack_tab.layout.addWidget(self.public_key_label_2)
        self.crack_tab.layout.addWidget(self.public_key_edit_2)
        self.crack_tab.layout.addWidget(self.load_public_key_button_2)
        self.crack_tab.layout.addWidget(self.crack_button)
        self.crack_tab.layout.addWidget(self.cracked_key_label)
        self.crack_tab.layout.addWidget(self.cracked_key_edit)

        self.crack_tab.setLayout(self.crack_tab.layout)

    def init_brute_force_tab(self):
        self.brute_force_tab.layout = QVBoxLayout()

        self.public_key_label_3 = QLabel('Public Key (n e):')
        self.public_key_edit_3 = QTextEdit()

        self.encrypted_message_label_3 = QLabel('Encrypted Message (hex):')
        self.encrypted_message_edit_3 = QTextEdit()

        self.load_public_key_button_3 = QPushButton('Load Public Key')
        self.load_public_key_button_3.clicked.connect(self.load_public_key_file_3)

        self.load_encrypted_message_button_3 = QPushButton('Load Encrypted Message')
        self.load_encrypted_message_button_3.clicked.connect(self.load_encrypted_message_file_3)

        self.brute_force_button = QPushButton('Brute Force Attack')
        self.brute_force_button.clicked.connect(self.brute_force_attack)

        self.decrypted_message_label_2 = QLabel('Decrypted Message:')
        self.decrypted_message_edit_2 = QTextEdit()
        self.decrypted_message_edit_2.setReadOnly(True)

        self.brute_force_tab.layout.addWidget(self.public_key_label_3)
        self.brute_force_tab.layout.addWidget(self.public_key_edit_3)
        self.brute_force_tab.layout.addWidget(self.load_public_key_button_3)
        self.brute_force_tab.layout.addWidget(self.encrypted_message_label_3)
        self.brute_force_tab.layout.addWidget(self.encrypted_message_edit_3)
        self.brute_force_tab.layout.addWidget(self.load_encrypted_message_button_3)
        self.brute_force_tab.layout.addWidget(self.brute_force_button)
        self.brute_force_tab.layout.addWidget(self.decrypted_message_label_2)
        self.brute_force_tab.layout.addWidget(self.decrypted_message_edit_2)

        self.brute_force_tab.setLayout(self.brute_force_tab.layout)




    '''
    Функция генерации ключей
    '''
    def generate_keys(self):
        # Получаем выбранную пользователем длину ключа
        key_length = self.key_length_spinbox.value()

        # Генерируем два случайных простых числа p и q
        p = self.generate_prime(key_length)
        q = self.generate_prime(key_length)
        
        # Если случайно сгенерированные p и q совпадают, генерируем q заново
        while p == q:
            q = self.generate_prime(key_length)

        # Вычисляем значение модуля n
        n = p * q
        
        # Вычисляем значение функции Эйлера от n
        phi_n = (p - 1) * (q - 1)
        
        # Выбираем случайный открытый экспонент e, такой что 1 < e < phi(n) и gcd(e, phi(n)) == 1
        e = self.choose_public_exponent(phi_n)
        
        # Вычисляем секретный экспонент d с помощью алгоритма нахождения модулярного обратного
        d = self.modular_inverse(e, phi_n)

        # Формируем открытый и закрытый ключи
        public_key = (n, e)
        private_key = (n, d)

        # Переводим ключи в шестнадцатеричный формат
        public_key_hex = "{0:x} {1:x}".format(public_key[0], public_key[1])
        private_key_hex = "{0:x} {1:x}".format(private_key[0], private_key[1])
        n_hex = hex(n)[2:]  # Убираем префикс '0x'

        # Записываем ключи в файлы
        current_directory = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_directory, "public_key.txt"), "w") as file:
            file.write(public_key_hex)
        with open(os.path.join(current_directory, "private_key.txt"), "w") as file:
            file.write(private_key_hex)
        with open(os.path.join(current_directory, "n.txt"), "w") as file:
            file.write(n_hex)

        # Выводим открытый и закрытый ключи на экран
        self.result_label.setText(f"Public Key: {public_key_hex}\nPrivate Key: {private_key_hex}")  # Обновляем метку с результатом работы функции


    '''
    Функция шифрования сообщений
    '''
    def encrypt_message(self):
        # Получаем открытый ключ и сообщение из соответствующих текстовых полей
        public_key_str = self.public_key_edit.toPlainText()
        message = self.message_edit.toPlainText()

        # Проверяем, что поля не пустые
        if not public_key_str or not message:
            return

        # Разбиваем строку открытого ключа на две части (n и e)
        public_key_str = public_key_str.split()
        if len(public_key_str) != 2:
            return

        try:
            # Преобразуем шестнадцатеричные строки в целые числа
            n = int(public_key_str[0], 16)
            e = int(public_key_str[1], 16)
        except ValueError:
            return

        # Шифруем сообщение с помощью открытого ключа
        encrypted_message = self.encrypt(message, (n, e))
        
        # Записываем зашифрованное сообщение в файл
        current_directory = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_directory, "encrypted_message.txt"), "w") as file:
            file.write(encrypted_message)
        
        # Выводим зашифрованное сообщение в текстовое поле
        self.encrypted_message_edit.setPlainText(encrypted_message)


    '''
    Функция дешифровки сообщений
    '''
    def decrypt_message(self):
        # Получаем закрытый ключ и зашифрованное сообщение из соответствующих текстовых полей
        private_key_str = self.private_key_edit.toPlainText()
        encrypted_message_hex = self.encrypted_message_edit_2.toPlainText()

        # Проверяем, что поля не пустые
        if not private_key_str or not encrypted_message_hex:
            return

        # Разбиваем строку закрытого ключа на две части (n и d)
        private_key_str = private_key_str.split()
        if len(private_key_str) != 2:
            return

        try:
            # Преобразуем шестнадцатеричные строки в целые числа
            n = int(private_key_str[0], 16)
            d = int(private_key_str[1], 16)
        except ValueError:
            return

        # Расшифровываем сообщение с помощью закрытого ключа
        decrypted_message = self.decrypt(encrypted_message_hex, (n, d))

        # Выводим расшифрованное сообщение в текстовое поле
        self.decrypted_message_edit.setPlainText(decrypted_message)


    '''
    Функция взлома методом факторизации n
    
    Метод взлома шифра RSA, реализованный в данном коде, 
    основан на факторизации числа n, которое является 
    произведением двух больших простых чисел p и q. 
    Если удалось найти простые множители p и q, 
    то возможно вычислить значение функции Эйлера 
    от n (phi(n)) и, далее, вычислить секретный экспонент d.
    '''
    def crack_cipher(self):
        # Получаем открытый ключ из соответствующего текстового поля
        public_key_str = self.public_key_edit_2.toPlainText()

        # Проверяем, что поле не пустое
        if not public_key_str:
            return

        # Разбиваем строку открытого ключа на две части (n и e)
        public_key_str = public_key_str.split()
        if len(public_key_str) != 2:
            return

        try:
            # Преобразуем шестнадцатеричные строки в целые числа
            n = int(public_key_str[0], 16)
            e = int(public_key_str[1], 16)
        except ValueError:
            return

        # Факторизуем n на простые множители p и q
        p, q = self.factorize_n(n)
        # Если не удалось найти простые множители, выходим из функции
        if p is None or q is None:
            return

        # Вычисляем значение функции Эйлера от n
        phi_n = (p - 1) * (q - 1)
        
        # Вычисляем секретный экспонент d с помощью алгоритма нахождения модулярного обратного
        d = self.modular_inverse(e, phi_n)

        # Переводим закрытый ключ в шестнадцатеричный формат
        cracked_key_hex = "{0:x} {1:x}".format(n, d)

        # Выводим взломанный закрытый ключ на экран
        self.cracked_key_edit.setPlainText(cracked_key_hex)


    '''
    Функция взлома шифра методом грубой силы(перебора)
    
    Метод brute_force_attack представляет собой 
    попытку взлома шифра методом "грубой силы" (brute force). 
    Он основан на попытке перебора возможных вариантов закрытого ключа 
    (private key) для данного открытого ключа (public key), 
    чтобы расшифровать зашифрованное сообщение.
    '''
    def brute_force_attack(self):
        # Получаем открытый ключ и зашифрованное сообщение из соответствующих текстовых полей
        public_key_str = self.public_key_edit_3.toPlainText()
        encrypted_message_hex = self.encrypted_message_edit_3.toPlainText()

        # Проверяем, что поля не пустые
        if not public_key_str or not encrypted_message_hex:
            return

        # Разбиваем строку открытого ключа на две части (n и e)
        public_key_str = public_key_str.split()
        if len(public_key_str) != 2:
            return

        try:
            # Преобразуем шестнадцатеричные строки в целые числа
            n = int(public_key_str[0], 16)
            e = int(public_key_str[1], 16)
        except ValueError:
            return

        # Вычисляем значение функции Эйлера от n
        phi_n = self.compute_phi_n(n)
        
        # Находим все возможные закрытые ключи, соответствующие открытому ключу
        possible_private_keys = self.find_possible_private_keys(phi_n, e)
        
        # Пытаемся расшифровать сообщение для каждого найденного закрытого ключа
        for d in possible_private_keys:
            decrypted_message = self.decrypt(encrypted_message_hex, (n, d))
            # Если удалось расшифровать сообщение, выводим его и завершаем функцию
            if decrypted_message is not None:
                self.decrypted_message_edit_2.setPlainText(decrypted_message)
                return


    def generate_prime(self, num_bits=16):
        # Генерируем случайное число заданной длины в битах
        while True:
            prime_candidate = random.getrandbits(num_bits)
            # Проверяем, является ли сгенерированное число простым
            if self.is_prime(prime_candidate):
                return prime_candidate  # Если число простое, возвращаем его


    def gcd(self, a, b):
        # Находим наибольший общий делитель двух чисел a и b
        while b:
            a, b = b, a % b  # Заменяем a на b, а b на остаток от деления a на b
        return a  # Возвращаем последнее ненулевое значение a, которое будет наибольшим общим делителем


    def choose_public_exponent(self, phi_n):
        # Выбираем случайное целое число в интервале (2, phi_n - 1) включительно
        e = random.randint(2, phi_n - 1)
        # Проверяем, что выбранное число взаимно просто с phi_n
        while self.gcd(e, phi_n) != 1:
            # Если число не взаимно простое с phi_n, выбираем новое случайное число
            e = random.randint(2, phi_n - 1)
        return e  # Возвращаем число e, которое является открытым экспонентом


    def extended_gcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)


    def modular_inverse(self, a, m):
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            raise Exception('Modular inverse does not exist')
        else:
            return x % m


    def encrypt(self, message, public_key):
        # Шифруем сообщение с использованием открытого ключа
        n, e = public_key
        # Преобразуем каждый символ сообщения в шестнадцатеричное представление его шифрованного эквивалента
        encrypted_message = [hex(pow(ord(char), e, n))[2:] for char in message]
        # Объединяем шифрованные символы в одну строку, разделяя пробелами
        return ' '.join(encrypted_message)

    def decrypt(self, encrypted_message_hex, private_key):
        # Расшифровываем зашифрованное сообщение с использованием закрытого ключа
        n, d = private_key
        try:
            # Преобразуем каждый шестнадцатеричный символ зашифрованного сообщения в целое число
            encrypted_message = [int(hex_char, 16) for hex_char in encrypted_message_hex.split()]
            # Восстанавливаем исходные символы, применяя операцию возведения в степень по модулю n и d
            decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
            return decrypted_message  # Возвращаем расшифрованное сообщение
        except:
            return None  # В случае ошибки возвращаем None


    def fast_exponentiation(self, base, exponent, modulus):
        # Рекурсивная функция быстрого возведения в степень методом Лагранжа
        if exponent == 0:
            return 1
        elif exponent % 2 == 0:
            result = self.fast_exponentiation(base, exponent // 2, modulus)
            return (result * result) % modulus
        else:
            result = self.fast_exponentiation(base, (exponent - 1) // 2, modulus)
            return (base * result * result) % modulus


    def factorize_n(self, n):
        # Метод Ферма для факторизации n
        p = None
        q = None

        # Вычисляем квадратный корень из n
        a = math.isqrt(n)
        # Вычисляем a^2 - n
        b2 = a * a - n
        # Пока b2 меньше 0 или не является полным квадратом, увеличиваем a и пересчитываем b2
        while b2 < 0 or not math.isqrt(b2) ** 2 == b2:
            a += 1
            b2 = a * a - n

        # Вычисляем простые множители p и q
        p = a + math.isqrt(b2)
        q = a - math.isqrt(b2)

        return p, q  # Возвращаем найденные простые множители p и q


    def is_prime(self, n, k=5):
        # Проверяем, является ли число n простым с помощью теста Миллера-Рабина
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False

        # Вычисляем значения s и d
        s = 0
        d = n - 1
        while d % 2 == 0:
            d //= 2
            s += 1

        # Проводим k итераций теста Миллера-Рабина
        for _ in range(k):
            a = random.randint(2, n - 1)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True


    def compute_phi_n(self, n):
        # Вычисляем значение функции Эйлера от n
        p, q = self.factorize_n(n)
        return (p - 1) * (q - 1)  # Возвращаем значение функции Эйлера


    def find_possible_private_keys(self, phi_n, e):
        # Находим все возможные значения закрытого ключа d, соответствующие открытому ключу
        possible_private_keys = []
        for d in range(2, phi_n):
            if (d * e) % phi_n == 1:  # Проверяем условие d * e ≡ 1 (mod phi_n)
                possible_private_keys.append(d)
        return possible_private_keys  # Возвращаем список возможных значений закрытого ключа


    def load_public_key_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load Public Key File', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'r') as file:
                public_key = file.read().strip()
                self.public_key_edit.setPlainText(public_key)

    def load_private_key_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load Private Key File', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'r') as file:
                private_key = file.read().strip()
                self.private_key_edit.setPlainText(private_key)

    def load_encrypted_message_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load Encrypted Message File', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'r') as file:
                encrypted_message = file.read().strip()
                self.encrypted_message_edit_2.setPlainText(encrypted_message)

    def load_public_key_file_2(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load Public Key File', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'r') as file:
                public_key = file.read().strip()
                self.public_key_edit_2.setPlainText(public_key)

    def load_public_key_file_3(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load Public Key File', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'r') as file:
                public_key = file.read().strip()
                self.public_key_edit_3.setPlainText(public_key)

    def load_encrypted_message_file_3(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load Encrypted Message File', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'r') as file:
                encrypted_message = file.read().strip()
                self.encrypted_message_edit_3.setPlainText(encrypted_message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RSAKeyGenerator()
    window.show()
    sys.exit(app.exec_())