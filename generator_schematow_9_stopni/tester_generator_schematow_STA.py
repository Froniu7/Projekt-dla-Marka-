from funkcje import read_rows, generowanie_schematow_elementy1fazowe


Image_path = "pliki_graficzne/"
nazwa_plik_graficznego_do_wygenerowania = "merged_horizontal2"

#tworze 3 listy, każda zawiera jeden z wierszy pliku CSV
faza1, faza2, faza3 = read_rows("test.csv")

#generowanie schematu
generowanie_schematow_elementy1fazowe(faza1,faza2,faza3, Image_path, nazwa_plik_graficznego_do_wygenerowania)


