class StartWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proces Testowania")
        self.setGeometry(300, 300, 400, 700)

        layout = QVBoxLayout()

        label = QLabel("Start testowanie podzespołu")
        layout.addWidget(label)

        # Pole do wyświetlania logów (wysyłane i odbierane komendy)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # Przyciski do wysyłania komend
        self.btn_start1 = QPushButton("Wyślij 'start1'")
        self.btn_start1.clicked.connect(lambda: self.send_command("start1"))
        layout.addWidget(self.btn_start1)

        self.btn_stop1 = QPushButton("Wyślij 'stop1'")
        self.btn_stop1.clicked.connect(lambda: self.send_command("stop1"))
        layout.addWidget(self.btn_stop1)

        self.btn_start2 = QPushButton("Wyślij 'start2'")
        self.btn_start2.clicked.connect(lambda: self.send_command("start2"))
        layout.addWidget(self.btn_start2)

        self.btn_stop2 = QPushButton("Wyślij 'stop2'")
        self.btn_stop2.clicked.connect(lambda: self.send_command("stop2"))
        layout.addWidget(self.btn_stop2)

        self.setLayout(layout)

        # Serial
        self.ser = None
        self.open_serial()

        # Timer do odbioru danych
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(100)  # co 100 ms sprawdzaj port

        global last_selected_item, selected_list

        # --- na końcu __init__ ---
        self.log_text.append("Inicjalizacja zakończona.")
        self.log_text.append(f"Zmienna A = {last_selected_item}")
        self.log_text.append(f"Zmienna B = {selected_list}")

        if last_selected_item == "" :
            self.log_text.append("Nie wybrano podzespolu do testowania")
        else:
            dane = extract_reactive_value(last_selected_item)
            dane_typ = dane['type']
            dane_wartosc = float(dane['value'])
            dane_jednostka = dane['unit']

            print(dane_typ)  # → 'C'
            self.log_text.append(f"Typ = {dane_typ}")
            print(dane_wartosc)  # → 15.0
            self.log_text.append(f"Wartosc = {dane_wartosc}")
            print(dane_jednostka)  # → 'uF
            self.log_text.append(f"Jednostka = {dane_wartosc}")

            def wait_for_response(timeout_ms=1000):

                import time
                start_time = time.time()
                timeout_s = timeout_ms / 1000.0

                while (time.time() - start_time) < timeout_s:
                    pass

            def start_measurement1f(self):
                self.send_command("start1rez")
                self.log_text.append("wysłano start1rez")
                # Po 2 s wywoła stop_measurement
                QTimer.singleShot(2000, self.stop_measurement)

            def stop_measurement1f(self):
                self.send_command("stop1rez")
                self.log_text.append("wysłano stop1rez")

            def prad_z_marginesem(prad_A, procent=20):
                """
                Oblicza zakres prądu ± podany procent.

                Parametry:
                - prad_A (float): wartość prądu w amperach
                - procent (float): procent odchylenia (domyślnie 20)

                Zwraca:
                - tuple: (prad_min, prad_max)
                """
                delta = prad_A * procent / 100.0
                return prad_A - delta, prad_A + delta

            global global_u1, global_u_avg, global_i1
            if selected_list == "1":
                self.log_text.append("Liczymy wartosc pradu z rezystorem\n"
                                     "dla kondensatora 1 fazowego")
                self.log_text.append("Uruchamiamy pomiar z rezystorem")

                self.log_text.append("")
                self.log_text.append("wysyłamy -> -> -> ")
                self.send_command("start1rez")
                self.log_text.append("")
                #wait_for_response(timeout_ms=2000)
                self.log_text.append("")
                napiecie = float(global_u1)
                self.log_text.append(f"napiecie = {napiecie}")
                self.log_text.append("wysyłamy -> -> -> ")
                self.send_command("stop1rez")

                # Wywolanie funkcji i przechwycenie wynikow
                prad, napiecie_rezystor, napiecie_kondensator, moc_rezystor = oblicz_parametry_RC(dane_wartosc,napiecie,7.33, 50)
                self.log_text.append(f"prad wyliczony = {prad}")
                I_min, I_max = prad_z_marginesem(prad)
                self.log_text.append(f"Prąd: {prad} A, zakres ±20%: {I_min:.2f} A – {I_max:.2f} A")
                print(f"Prąd: {prad} A, zakres ±20%: {I_min:.2f} A – {I_max:.2f} A")
                if global_i1 >= I_min and global_i1 <= I_max:
                    self.log_text.append("")
                    self.log_text.append("Wartosc pradu z rezystorem miesci sie w widełkach")

                else:
                    self.log_text.append("Wartosc pradu z rezystorem nie miesci sie w widełkach")
                    self.log_text.append(f"Prad zmiwerzony : {global_i1}")




            elif selected_list == "2":
                self.log_text.append("Liczymy wartosc pradu z rezystorem\n"
                                     "dla kondensatora 3 fazowego")
                self.log_text.append("Uruchamiamy pomiar z rezystorem")

                self.send_command("start2rez")
                QTimer.singleShot(1000, lambda: self.log_text.append("Kolejna akcja po 1 s"))
                napiecie = global_u_avg
                self.log_text.append(f"Napięcie wynosi : {napiecie}")
                self.send_command("stop2rez")
            elif selected_list == "3":
                self.log_text.append("Liczymy wartosc pradu z rezystorem\n"
                                     "dla dlawika 1 fazowego")
                self.log_text.append("Uruchamiamy pomiar z rezystorem")

                self.send_command("start1rez")
                QTimer.singleShot(1000, lambda: self.log_text.append("Kolejna akcja po 1 s"))
                napiecie = global_u1
                self.log_text.append(f"Napięcie wynosi : {napiecie}")
                self.send_command("stop1rez")
            elif selected_list == "4":
                self.log_text.append("Liczymy wartosc pradu z rezystorem\n"
                                     "dla dlawika 3 fazowego")
                self.log_text.append("Uruchamiamy pomiar z rezystorem")

                self.send_command("start2rez")
                QTimer.singleShot(1000, lambda: self.log_text.append("Kolejna akcja po 1 s"))
                napiecie = global_u_avg
                self.log_text.append(f"Napięcie wynosi : {napiecie}")
                self.send_command("stop2rez")
            else:
                self.log_text.append("Brak zawartosci zmiennej - Selected_list")


    def open_serial(self):
        global COM
        try:
            self.ser = serial.Serial(COM, 9600, timeout=0.1)
            self.log_text.append(f"Połączono z portem {COM}")
        except Exception as e:
            self.log_text.append(f"Nie udało się otworzyć portu {COM}: {e}")

    def send_command(self, cmd):
        if self.ser and self.ser.is_open:
            self.ser.write((cmd + "\n").encode())  # wysyłanie z końcem linii
            self.log_text.append(f"Wysłano komendę: {cmd}")
        else:
            self.log_text.append("Port nieotwarty!")

    def read_serial(self):
        if self.ser and self.ser.in_waiting:
            try:
                data = self.ser.readline().decode().strip()
                if data:
                    self.log_text.append(f"Odebrano: {data}")
            except Exception as e:
                self.log_text.append(f"Błąd odczytu: {e}")

    def closeEvent(self, event):
        """Zamyka port szeregowy przy zamknięciu okna"""
        if hasattr(self, 'timer'):
            self.timer.stop()  # zatrzymujemy timer, żeby nie wywoływał read_serial
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.log_text.append(f"Port {COM} został zamknięty.")
            print("Zamknieto okno 'Start', zamknieto port COM")
        event.accept()
