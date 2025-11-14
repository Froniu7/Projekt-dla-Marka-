import functions


if __name__ == "__main__":

   #pobieramy przekazane argumenty
   moc_zamowiona, moc_max, przekladnia_uzwojenie_pierwotne, przekladnia_uzwojenie_wtorne, VA, przewod, dlugosc_przewodu, asymetria, strona = functions.get_arguments()

   #zapisujemy dane do pliku wyniki.json
   functions.zapisz_pole_json("wyniki.json", "moc_zamowiona", moc_zamowiona)
   functions.zapisz_pole_json("wyniki.json", "moc_max", moc_max)
   functions.zapisz_pole_json("wyniki.json", "uzwojenie_pierwotne", przekladnia_uzwojenie_pierwotne)
   functions.zapisz_pole_json("wyniki.json", "uzwojenie_wtorne", przekladnia_uzwojenie_wtorne)
   functions.zapisz_pole_json("wyniki.json", "VA", VA)
   functions.zapisz_pole_json("wyniki.json", "przekroj_przewod", przewod)
   functions.zapisz_pole_json("wyniki.json", "dlugosc_przewod", dlugosc_przewodu)
   functions.zapisz_pole_json("wyniki.json", "asymetria", asymetria)
   functions.zapisz_pole_json("wyniki.json", "strona", strona)


   #liczymy prad przy obciarzeniu - podanym na fakturze - sytuacja idealna max obciarzenie
   prad_dla_mocy_zamowionej = functions.prad(moc_zamowiona, asymetria)
   functions.zapisz_pole_json("wyniki.json", "prad_przy_moc_zamowiona", prad_dla_mocy_zamowionej)

   #liczymy prad dla sytuacji wystepujacej w sieci
   prad_dla_mocy_rzeczywistej = functions.prad(moc_max, asymetria)
   functions.zapisz_pole_json("wyniki.json", "prad_przy_moc_wystepujaca", prad_dla_mocy_rzeczywistej)

   #liczymy przekladnie dla wybranego przekladnika -
   przekladnia = functions.wyliczenie_przekladni(przekladnia_uzwojenie_pierwotne, przekladnia_uzwojenie_wtorne)
   functions.zapisz_pole_json("wyniki.json", "przekladnia", przekladnia)

   #liczymy straty na przewodzie kablowym sterowniczym , przy pradzie dla mocy zamowionej
   Pstrat_moc_zamowiona = functions.obliczenie_mocy_wydzielonej(przekladnia, dlugosc_przewodu, przewod, prad_dla_mocy_zamowionej)
   functions.zapisz_pole_json("wyniki.json", "moc_strat_przy_moc_zamowiona", Pstrat_moc_zamowiona)

   #sprawdzamy czy warunek jest spelniony
   warunek_dla_mocy_zamowionej = functions.sprawdzenie_warunku(Pstrat_moc_zamowiona, VA)
   functions.zapisz_pole_json("wyniki.json", "warunek_dla_moc_zamowiona", warunek_dla_mocy_zamowionej)

   # liczymy straty na przewodzie kablowym sterowniczym , przy pradzie dla mocy wystepujacej w sieci
   Pstrat_moc_wystepujaca = functions.obliczenie_mocy_wydzielonej(przekladnia, dlugosc_przewodu, przewod, prad_dla_mocy_rzeczywistej)
   functions.zapisz_pole_json("wyniki.json", "moc_strat_przy_moc_wystepujaca", Pstrat_moc_wystepujaca)

   # sprawdzamy czy warunek jest spelniony
   warunek_dla_mocy_wystepujacej = functions.sprawdzenie_warunku(Pstrat_moc_wystepujaca, VA)
   functions.zapisz_pole_json("wyniki.json", "warunek_dla_moc_wystepujaca", warunek_dla_mocy_wystepujacej)

   aktualna_data = functions.aktualna_data()
   functions.zapisz_pole_json("wyniki.json", "data_modyfikacji", aktualna_data)
