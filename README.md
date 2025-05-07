# Verificare Regex pe bază de NFA

Acest proiect citește expresii regulate dintr-un fișier JSON, le transformă într-un automat finit nedeterminist (NFA) și verifică dacă șiruri de caractere sunt acceptate de acesta.

## 📂 Structura proiectului

```
regex_verifier/
├── main.py               # Scriptul principal care procesează regexurile și testează șirurile
├── LNFAaccept.py         # Modul extern care conține funcția Verify pentru verificarea cuvintelor
├── data.json             # Fișierul cu expresii regulate și șiruri de testat
└── README.md             # Documentația proiectului
```

## ▶️ Cum se rulează codul

1. Asigură-te că ai Python 3 instalat.
2. Plasează expresiile regulate și șirurile de testat în fișierul `data.json`, în formatul:

```json
[
  {
    "name": "Test1",
    "regex": "(a|b)*abb",
    "test_strings": [
      {"input": "abb", "expected": true},
      {"input": "ab", "expected": false}
    ]
  }
]
```

3. Rulează scriptul din terminal cu:

```bash
python main.py
```

Rezultatul va afișa pentru fiecare expresie dacă toate testele au trecut corect.

## 🛠️ Decizii de implementare

- **Conversie la forma poloneză inversă (RPN)**: Expresiile sunt convertite din notație infixată în postfixată pentru a putea construi mai ușor NFA-ul.
- **Adăugare automată a operatorului de concatenare (`.`)**: Concatenarea este introdusă explicit între caractere unde este necesar.
- **Construire NFA pentru fiecare operator**:
  - `|` (alternativă),
  - `.` (concatenare),
  - `*` (zero sau mai multe repetări),
  - `+` (una sau mai multe repetări),
  - `?` (zero sau una).
- **Verificare prin funcția `Verify`**: Importată din `LNFAaccept.py`, această funcție determină dacă un cuvânt este acceptat de NFA-ul generat.

---

📌 Proiectul poate fi extins pentru a suporta și alte funcționalități, cum ar fi expresii mai complexe sau conversia către DFA.
