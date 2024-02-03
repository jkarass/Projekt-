Jest to projekt na zaliczenie "Bezpieczne trzymanie plików" 

Cały projekt dzieli sie na dwa programy.

Pierwszym jest serwer, jest on oczywiście lokalny i z przyczyn technicznych nie jest on plikiem wykonywalnym.
Przez co wymaga posiadania wszystkich bibliotek przez użytkownika (ufam iż to nie problem) 

Drugi to skromny program z interfejsem graficznym, tak co by człowiek nie musiał się męczyć z wrzucaniem plików na serwer
za pomocą komend. Ten jest już plikiem wykonywalnym, nie jest on idealny, nie mniej działa. Chociaż dość łatwo go zbugować.

Sam folder z projektem posiada jeszcze dwa podfoldery:

uploaded_files: Tam są trzymane zaszyfrowane pliki, pliki są zaszyfrowane 256 bitowym symetrycznym kluczem AES. 

pliki py: Tutaj jest kod obu "programów" w roszerzeniu .py 

Są też dwa pliki txt, za pomocą których można przetestować działanie programu. 
 