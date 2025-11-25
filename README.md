# Kockapakolás - Cube Packing Optimization Project

## Tartalomjegyzék

1. [Bevezetés](#bevezetés)
2. [Projekt áttekintése](#projekt-áttekintése)
3. [Telepítés és Beállítás](#telepítés-és-beállítás)
4. [Architektúra](#architektúra)
5. [Modulok Részletes Dokumentációja](#modulok-részletes-dokumentációja)
6. [Használat](#használat)
7. [API Referencia](#api-referencia)
8. [Algoritmusok](#algoritmusok)
9. [Konfigurációs Paraméterek](#konfigurációs-paraméterek)
10. [Fejlesztői Útmutató](#fejlesztői-útmutató)

---

## Bevezetés

A **Kockapakolás** projekt egy speciális 3D geometriai optimalizálási probléma megoldására épített szoftver. A projekt célja az, hogy megtalálja az optimális elrendezést az `n` darab, különböző méretű kocka (1-től n-ig terjedő méretű) számára egy nagyobb, `n×n×n` méretű térben.

Ez egy összetett kombinatorikus optimalizálási problémá, amelynek megoldása gyakorlati alkalmazásokat érdekelhet az anyagfeltöltésben, szállítmány-optimalizálásban és térkihasználás-maximalizálásban.

### A Probléma Definíciója

Adott:
- Egy `n×n×n` méretű tér (az alapkocka)
- `n` darab kocka, méretei: `1, 2, 3, ..., n`

Cél:
- Helyezzük el az összes kockát az alaptérben úgy, hogy:
  - Egyetlen kocka sem lóg ki a tér határain
  - A kockák nem átfedésben vannak
  - Maximalizáljuk a felhasznált teret (vagy más alkalmazástól függő célfüggvényt)

---

## Projekt Áttekintése

### Célok

1. **Genetikai algoritmus implementáció**: A megoldások számára az evolúciós megközelítés
2. **Konstruktív módszer**: Heurisztikus elhelyezési stratégiák
3. **Web-alapú felület**: Felhasználóbarát GUI a kísérletekhez
4. **REST API**: Programmatikus hozzáférés az algoritmusokhoz
5. **Eredmények kezelése**: Adatbázis-szerű eredménytárolás és lekérdezés

### Fő Jellemzők

- ✅ GUI alkalmazás (Tkinter)
- ✅ Többszálú feldolgozás (threading)
- ✅ Process-menedzsment (párhuzamos futtatás)
- ✅ Web-alapú adminisztráció (Flask)
- ✅ REST API (FastAPI)
- ✅ 3D vizualizáció (Matplotlib)
- ✅ Széleskörű paraméterezés
- ✅ Eredmények exportálása (JSON, PNG)

---

## Telepítés és Beállítás

### Előfeltételek

Python 3.8+ szükséges

### Függőségek

```bash
pip install flask
pip install fastapi
pip install uvicorn
pip install numpy
pip install matplotlib
pip install pydantic
```

### Telepítési Lépések

1. **Projekt klónozása/másolása**
   ```bash
   cd projektlabor
   ```

2. **Virtuális környezet létrehozása (ajánlott)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # vagy
   venv\Scripts\activate  # Windows
   ```

3. **Függőségek telepítése**
   ```bash
   pip install -r requirements.txt
   ```

4. **Az `results/` és `output_logs/` könyvtárak létrehozása** (ha nem léteznek)
   ```bash
   mkdir results
   mkdir output_logs
   ```

### Futtatás

#### GUI alkalmazás
```bash
python main.py
```

#### Flask web-alkalmazás
```bash
python web_app.py
# Nyissa meg a böngészőt: http://localhost:5000
```

#### FastAPI szerver
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

#### Egyszerű tesztalkalmazás
```bash
python generate_basics.py
```

---

## Architektúra

### Rendszer Komponensek

```
┌─────────────────────────────────────────────┐
│           Felhasználói Interfészek          │
├─────────────────────────────────────────────┤
│ mainGUI.py (Tkinter)   │  web_app.py (Flask)│
└────────────┬───────────┬────────────────────┘
             │           │
┌────────────▼───────────▼────────────────────┐
│      Alkalmazás Logika                      │
├─────────────────────────────────────────────┤
│ ServerApplication | server.py (FastAPI)    │
└────────────┬─────────────┬──────────────────┘
             │             │
┌────────────▼──────────────▼─────────────────┐
│      Algoritmusok & Megoldók                │
├─────────────────────────────────────────────┤
│ Genetic  │  Constructive  │  CubeSolver    │
└────────────┬───────────────┬────────────────┘
             │               │
┌────────────▼───────────────▼─────────────────┐
│         Adatmodellek                        │
├─────────────────────────────────────────────┤
│ Space (tér)  │  Cube (kocka)  │ Process    │
└─────────────────────────────────────────────┘
```

### Rétegek

1. **Prezentációs Réteg**: GUI és web felületek
2. **Üzleti Logika Réteg**: Algoritmusok, ServerApplication
3. **Adatréteg**: Space, Cube, Process modellek
4. **Támogatási Réteg**: Konfigurációs paraméterek, segédfüggvények

---

## Modulok Részletes Dokumentációja

### 1. **Cube.py** - Kocka Adatmodellje

Az egyes kockákat reprezentáló osztály.

#### Fő Metódusok

```python
class Cube:
    def __init__(self, size, x=0, y=0, z=0):
        """
        Létrehoz egy kockát adott mérettel és pozícióval

        Args:
            size (float): A kocka mérete
            x, y, z (float): Pozíció koordináták (alapértelmezetten az origó)
        """

    def set_position(self, x, y, z):
        """Beállítja a kocka pozícióját"""

    def set_random_position(self, lower, upper, step):
        """
        Véletlen pozícióval helyezi el a kockát [lower, upper) intervallumban

        Args:
            lower, upper (int): Intervallum határai
            step (int): Lépésköz
        """

    def get_center(self, rounding=None):
        """
        Visszaadja a kocka középpontját

        Returns:
            tuple: (x, y, z) koordináták
        """

    def set_faces(self):
        """Kiszámítja és beállítja a kocka felületeit 3D koordinátákban"""
```

#### Belső Adatok

- `vertices`: A kocka 8 csúcsa (3D pontok)
- `faces`: A kocka 6 lapja (4 csúcs listái)
- `size`, `x`, `y`, `z`: Méret és pozíció

### 2. **Space.py** - 3D Tér Reprezentáció

A teljes teret és a kockákat kezelő osztály.

#### Fő Metódusok

```python
class Space:
    def __init__(self, n, accuracy=0, reach=None, do_setup=True):
        """
        Létrehoz egy n×n×n méretű teret n darab kockával (méretei: 1-n)

        Args:
            n (int): Tér mérete és kockák száma
            accuracy (int): Tizedeshelyek száma
            reach (float): Kritikus pontok távolsága
            do_setup (bool): Inicializáljon-e beállítást
        """

    def setup(self, reach=1):
        """
        Előzetes beállítás: első 13 kocka kritikus pontokra
        (AI által optimalizált sorrend)
        """

    def setup_with_optimal_reach(self):
        """
        Megtalálja az optimális 'reach' értéket
        (a minimális távolság a kritikus pontok között)
        """

    def randomize(self):
        """Randomizálja az összes kocka pozícióját"""

    def plot_space(self, path="default.png", title=None):
        """
        3D vizualizáció matplotlib segítségével

        Args:
            path (str): Kép mentési útvonala
            title (str): Kép címe
        """

    def is_part_of_a_cube(self, point):
        """Ellenőrzi, hogy a pont egy kocka része-e"""

    def is_cube_within_base_cube(self, cube):
        """Ellenőrzi, hogy a kocka kilóg-e az alapkockán"""

    def monte_carlo_filled_ratio(self, value, mode="strict", sample_size=5000):
        """
        Monte Carlo módszerrel becsüli a betöltöttségi hányadost

        Args:
            value (float): Ellenőrzés korlátja
            mode (str): "strict" vagy egyéb
            sample_size (int): Minták száma
        """

    def check_grid_coverage(self, value):
        """Ellenőrzi, hogy az összes rácspont fedett-e"""

    def next_size_filled_ratio(self, current, next_value):
        """Kitöltöttségi hányadost számít az adott intervallumban"""

    def to_json(self):
        """JSON formátumba konvertálja az elrendezést"""

    def print_space(self, path, title=None):
        """JSON-t ment fájlba"""
```

#### Belső Adatok

- `cubes`: Az összes kocka listája (n darab)
- `n`, `accuracy`, `reach`: Paraméterek
- `fitness`: Aktuális fitnesz érték

#### Kritikus Pontok

Az első 13 kocka speciális pozícióira helyezkedik el:
- Buffer pont
- 8 sarokpont: (0,0,0), (0,1,0), (1,0,0), stb.
- 4 él-felezőpont

### 3. **Cube Solver.py** - Absztrakt Megoldó

Az összes megoldó alaposztálya.

```python
class CubeSolver:
    def to_json(self):
        """Paramétereket JSON-ként adja vissza"""

    def get_params_string(self):
        """Paramétereket szöveges stringként adja vissza"""

    def pause(self):
        """Megállítja a futást"""

    def resume(self):
        """Folytatja a futást"""

    def stop(self):
        """Leállítja a futást véglegesen"""

    def run(self):
        """Indítja a megoldást (generátor)"""

    def export_results(self, indices=None):
        """Exportálja az eredményeket JSON és PNG formátban"""
```

### 4. **Genetic.py** - Genetikai Algoritmus

Az evolúciós megoldó implementáció.

#### Genetikai Operátorok

```python
def crossover(self, individual1, individual2):
    """
    Keresztezés: az első individual1 első részét, individual2 utolsó részét veszi

    Vágási pont: random 2 és n-1 között
    """

def mutation(self, individual):
    """
    Mutáció: minden kocka (az első kivételével) mutáció_rátás valószínűséggel

    - x, y, z koordináták megváltoznak ±0.5 vagy ±1 értékkel
    - Meg van korlátozva az [0, n] intervallumra
    - Kerekítés az accuracy szerint
    """

def fitness(self, individual, mode=1):
    """
    Fitnesz függvény

    Args:
        mode (int):
            1 - Monte Carlo becslés (gyorsabb, pontatlanabb)
            2 - Full grid coverage (számításigényes, pontosabb)

    Büntetések:
    - -1 ha kocka lóg ki az alapkockán
    - -1 ha nem fedett minden 0-s koordináta
    """

def selection(self, k=5):
    """Турниршаж: k véletlenszerű egyedből a legjobban jót választja"""
```

#### Paraméterek

```python
def __init__(self, n, population_size=50, generations=None,
             mutation_rate=0.1, accuracy=0, reach=None, fitness_mode=1):
    """
    Args:
        n (int): Kockák száma és tér mérete
        population_size (int): Populáció nagysága
        generations (int): Generációk száma (None = végtelenség)
        mutation_rate (float): Mutáció valószínűsége [0, 1]
        accuracy (int): Tizedesjegyek száma (0 = egész számok)
        reach (float): Kritikus pontok távolsága (None = optimális keresése)
        fitness_mode (int): 1 vagy 2
    """
```

#### Futás

```python
for msg in genetic.run():
    print(msg)  # "Generation X: The score of the best individual: Y"
```

#### Eredmények Exportálása

Az algoritmus befejezéskor automatikusan exportálja az eredményeket:
- JSON fájlok: `results/<paraméterek>/spaces/`
- PNG képek (opcionális): `results/<paraméterek>/plots/`

### 5. **Constructive.py** - Konstruktív Algoritmus

Heurisztikus kockaelhelyezési stratégiák.

#### Stratégiák

```python
def corner_first_strategy(self, space):
    """
    Sarok-elsõ stratégia:
    - Az első 13 kocka már fel van helyezve (setup)
    - A többi kocka a legjobb pozícióra kerül

    Lépések:
    1. Megkeresi az összes "lyukat" (üres helyet)
    2. Értékeli a lehetséges pozíciókat
    3. Kiválasztja a legjobbat (max pontszám)
    """

def layer_by_layer_strategy(self, space):
    """
    Réteg-rétegre stratégia (JELENLEG NEM MŰKÖDIK)
    - Nem ajánlott
    """

def hybrid_strategy(self, space):
    """
    Hibrid stratégia (ha implementálva lenne)
    """
```

#### Pozícióértékelés

```python
def score_position(self, space, cube, x, y, z):
    """
    Pontszámítás:
    - Büntetés (-1000) ha kilóg az alapkockán
    - Plusz pont az üres részekért
    - Plusz pont a távolságért az origótól (0.01 × távolság)
    """
```

### 6. **Process.py** - Folyamat Kezelés

Egyedi solver folyamat futtatása külön szálban.

```python
class Process:
    def __init__(self, solver: CubeSolver, priority=0):
        """
        Args:
            solver: Genetic vagy Constructive solver
            priority: Folyamat prioritása (magasabb = előbb szerar)
        """

    def pause(self):
        """Szüneteltet"""

    def resume(self):
        """Folytatja"""

    def terminate(self):
        """Leállítja és meghívja az on_terminate callback-et"""

    def to_json(self):
        """Solver paramétereit adja vissza"""
```

#### Logging

A Process minden üzenetet logol az `output_logs/<Process_...>.txt` fájlba.

### 7. **ServerApplication.py** - Szerver Logika

Többfolyamat-kezelés, eredménytárolás.

```python
class ServerApplication:
    def add_process(self, process, start_immediately=False):
        """
        Hozzáadja a folyamatot

        Args:
            start_immediately: Azonnal indítsa-e vagy várakozzon
        """

    def get_processes(self, format=None):
        """
        Folyamatok listázása

        Args:
            format: "json" = JSON formátum, None = objektumok
        """

    def change_active_process(self, index):
        """Az aktív folyamat váltása"""

    def terminate_process(self, index):
        """Folyamat leállítása"""

    def highest_priority_process_index(self):
        """A legmagasabb prioritású folyamat indexe"""

    def get_best_space(self, n):
        """Legjobb elrendezés lekérdezése n-hez"""

    def load_results(self):
        """Korábbi eredmények betöltése az `results/` mappából"""
```

#### Aktív Folyamat Logika

- Egyszerre csak egy folyamat fut (aktív)
- Új folyamat indítása szüneteltet az aktuális folyamatot
- Lezárult folyamat után a legmagasabb prioritású folyamat indul

### 8. **web_app.py** - Flask Web Alkalmazás

Webalapú felhasználói felület és API.

#### Útvonalak

**Publikus (bejelentkezés nélkül elérhető):**

```
GET  /                    - Kezdőlap
GET  /browse              - Korábban lefuttatott megoldások listázása
GET  /api/results         - Összes eredmény (JSON)
GET  /api/results/<n>     - Adott n-hez tartozó eredmények
GET  /api/results/best/<n>  - Legjobb megoldás n-hez
GET  /api/stats           - Általános statisztikák
GET  /login               - Bejelentkezési form
POST /login               - Bejelentkezés feldolgozása
GET  /logout              - Kijelentkezés
```

**Bejelentkezés szükséges:**

```
GET  /processes           - Aktív folyamatok listája (HTML)
GET  /new-process         - Új folyamat létrehozása (HTML)
GET  /api/processes       - Aktív folyamatok (JSON)
POST /api/processes/add   - Új folyamat hozzáadása
POST /api/processes/<i>/terminate  - Folyamat leállítása
POST /api/processes/<i>/activate   - Folyamat aktiválása
```

#### Bejelentkezés

```
Alapértelmezett felhasználónév: admin
Alapértelmezett jelszó: admin
```

⚠️ **Biztonsági figyelmeztetés**: Éles módban módosítsa az `app.secret_key`-t és a jelszót!

### 9. **server.py** - FastAPI REST Szerver

Alternatív REST API (FastAPI)

#### Végpontok

```
GET  /                    - Üzenet
GET  /results/<n>         - Eredmények n-hez
POST /add_genetic_process - Genetikai folyamat hozzáadása
POST /terminate_process/<i> - Folyamat leállítása
POST /change_active_process/<i> - Aktív folyamat váltása
GET  /processes           - Aktív folyamatok
```

### 10. **mainGUI.py** - Tkinter GUI

Egyszerű asztali alkalmazás a genetikai algoritmushoz.

#### Felület

```
N:                 [20]           [Kimeneti szöveg]
Population size:   [50]
Generations:       [100]
Mutation rate:     [0.1]
Accuracy:          [0]

[START]  [STOP]
```

#### Paraméterek

- **N**: Kockák száma (8-tól)
- **Population size**: Populáció nagysága (50-től)
- **Generations**: Generációk száma (0 = végtelenség)
- **Mutation rate**: Mutáció valószínűsége (0.0-1.0)
- **Accuracy**: Tizedesjegyek száma

#### Futtatás

```bash
python main.py
```

---

## Használat

### 1. GUI-val (Tkinter)

```bash
python main.py
```

1. Adja meg a paramétereket
2. Kattintson a "Start" gombra
3. Figyelje a kimeneti ablakot az előrehaladásért
4. Kattintson a "Stop" gombra leállításhoz

**Kimeneti üzenet formája:**
```
Generation 1: The score of the best individual: 18.5
Generation 2: The score of the best individual: 19.2
...
Exporting results...
Done!
```

### 2. Web-alkalmazással (Flask)

```bash
python web_app.py
```

Nyissa meg: `http://localhost:5000`

1. **Csatornázás felületre**: Bejelentkezés `admin`/`admin` felhasználóval
2. **"Új Folyamat" létre**: Paramétereket megadva
3. **Folyamatok Figyelése**: Aktív folyamatok állapota
4. **Eredmények Böngészése**: Korábban futtatott megoldások

### 3. FastAPI-val (Szerver)

```bash
uvicorn server:app --reload
```

Nyissa meg: `http://localhost:8000/docs` (Swagger UI)

#### Példa: Genetikai folyamat hozzáadása

```bash
curl -X POST "http://localhost:8000/add_genetic_process" \
  -H "Content-Type: application/json" \
  -d '{
    "n": 11,
    "population_size": 50,
    "generations": 100,
    "mutation_rate": 0.1,
    "accuracy": 0,
    "reach": null,
    "fitness_mode": 2
  }'
```

### 4. Programmatikusan (Python)

```python
from genetic import Genetic

# Genetikai algoritmus futtatása
genetic = Genetic(
    n=11,
    population_size=50,
    generations=100,
    mutation_rate=0.1,
    accuracy=0,
    reach=None,
    fitness_mode=2
)

for msg in genetic.run():
    print(msg)

# Eredmények importálása
results = genetic.results
for result in results:
    print(f"N={result['n']}, Fitness={result['result']}")
```

---

## API Referencia

### Flask Web API

#### GET `/api/results`

Összes eredményt adja vissza n szerint csoportosítva.

**Válasz:**
```json
{
  "10": [
    {
      "n": 10,
      "result": 19.5,
      "cubes": [...],
      "solver_type": "genetic"
    },
    ...
  ],
  "11": [...]
}
```

#### GET `/api/results/<n>`

Összes eredményt adja vissza egy adott n-hez.

**Válasz:**
```json
[
  {
    "n": 11,
    "result": 19.8,
    "cubes": [...]
  },
  ...
]
```

#### GET `/api/results/best/<n>`

A legjobb megoldást adja vissza n-hez.

**Válasz:**
```json
{
  "n": 11,
  "result": 19.8,
  "cubes": [
    {
      "size": 11,
      "x": 0,
      "y": 0,
      "z": 0
    },
    ...
  ]
}
```

#### GET `/api/stats`

Általános statisztikákat ad vissza.

**Válasz:**
```json
{
  "total_results": 45,
  "active_processes": 2,
  "n_values": [10, 11, 12],
  "best_by_n": {
    "10": 19.5,
    "11": 19.8,
    "12": 20.1
  }
}
```

#### GET `/api/processes` (bejelentkezés szükséges)

Az összes aktív folyamatot listázza.

**Válasz:**
```json
{
  "processes": [
    {
      "n": 11,
      "population_size": 50,
      "generations": 100,
      "mutation_rate": 0.1,
      "accuracy": 0,
      "fitness_mode": 2
    }
  ],
  "active_index": 0
}
```

#### POST `/api/processes/add` (bejelentkezés szükséges)

Új folyamatot ad hozzá.

**Test:**
```json
{
  "type": "genetic",
  "n": 11,
  "population_size": 50,
  "generations": 100,
  "mutation_rate": 0.1,
  "accuracy": 0,
  "reach": null,
  "fitness_mode": 2,
  "priority": 0,
  "start_immediately": true
}
```

vagy konstruktív:

```json
{
  "type": "constructive",
  "n": 11,
  "accuracy": 0,
  "reach": null,
  "strategy": "corner_first",
  "iterations": 5,
  "priority": 1,
  "start_immediately": false
}
```

#### POST `/api/processes/<index>/terminate` (bejelentkezés szükséges)

Leállítja az adott folyamatot.

#### POST `/api/processes/<index>/activate` (bejelentkezés szükséges)

Az adott folyamatot teszi aktívvá.

---

## Algoritmusok

### Genetikai Algoritmus Mély Elemzése

#### Inicializálás

1. **Első kocka fixálása**: Az `n` méretű kocka az origóban (0,0,0)
2. **Kritikus pontok**: Az első 13 kocka az AI-által optimalizált kritikus pontokra kerül
3. **Véletlenszerű elhelyezés**: A maradék kockák randomizálva

#### Generáció Folyamata

```
Generáció k:
  1. Fitnesz számítása (összes egyedre)
  2. Legjobb egyed szelektálása
  3. Új populáció létrehozása:
     - Legjobb egyed: 1 példány
     - Keresztezés (selection → crossover) × (population_size - 1)
     - Mutáció (minden gyermekre)
  4. Populáció csere
```

#### Paraméterk Hatása

| Paraméter | Hatás | Ajánlott érték |
|-----------|-------|----------------|
| `population_size` | Nagyobb = több diverzitás, lassabb | 50-100 |
| `mutation_rate` | Nagyobb = több véletlenszerűség | 0.05-0.3 |
| `generations` | Több = jobb megoldások | 100-1000 |
| `accuracy` | Nagyobb = finomabb rács | 0-3 |

#### Fitnesz Függvény

**Mode 1 (Monte Carlo):**
- Gyorsabb, pontatlanabb
- Véletlenszerű mintavételezéssel becsüli a betöltöttséget
- Célérték: 2n-1

**Mode 2 (Full Grid Coverage):**
- Lassabb, pontosabb
- Rácsvizsgálattal ellenőrzi az összes pozíciót
- Célérték: 2n-1

### Konstruktív Algoritmus

#### Corner-First Stratégia

1. **Inicializálás**: Az első 13 kocka kritikus pontokra
2. **Iteráció** (kockánként):
   - **Lyuk megkeresése**: Az összes üres pont azonosítása
   - **Pozícióértékelés**: Legjobb 50 lyuk + 20 random pozíció
   - **Kiválasztás**: Legmagasabb pontszámú pozícióra helyezés

#### Pontszám Számítása

```
pontszám =
  - 1000 (ha kilóg az alapkockán)
  + (üres pontok száma az új kockában)
  + 0.01 × (távolság az origótól)
```

---

## Konfigurációs Paraméterek

### Fő Paraméterek

```python
n : int                # Kockák száma (8-tól)
population_size : int  # Populáció nagysága
generations : int      # Generációk száma (None vagy 0 = végtelenség)
mutation_rate : float  # Mutáció valószínűsége (0.0-1.0)
accuracy : int         # Tizedesjegyek száma (0-3)
reach : float          # Kritikus pontok távolsága (None = optimális)
fitness_mode : int     # 1 = Monte Carlo, 2 = Full Grid
strategy : str         # "corner_first", "layer_by_layer", "hybrid"
iterations : int       # Konstruktív iterációk száma
priority : int         # Folyamat prioritása
```

### Ajánlott Beállítások

**Kezdő teszteléshez (gyors):**
```python
n=10, population_size=20, generations=50, mutation_rate=0.1,
accuracy=0, fitness_mode=1
```

**Közepes kísérlethez:**
```python
n=12, population_size=50, generations=200, mutation_rate=0.15,
accuracy=1, fitness_mode=2
```

**Magas minőségű megoldáshoz (lassú):**
```python
n=15, population_size=100, generations=1000, mutation_rate=0.1,
accuracy=2, fitness_mode=2
```

---

## Fejlesztői Útmutató

### Projekt Struktúra

```
projektlabor/
├── cube.py                  # Kocka osztály
├── space.py                 # 3D tér osztály
├── cubesolver.py            # Absztrakt megoldó
├── genetic.py               # Genetikai algoritmus
├── constructive.py          # Konstruktív algoritmus
├── process.py               # Folyamat kezelés
├── server_application.py    # Szerver logika
├── mainGUI.py               # Tkinter GUI
├── main.py                  # GUI indítópont
├── web_app.py               # Flask web app
├── server.py                # FastAPI szerver
├── generate_basics.py       # Teszt script
│
├── results/                 # Kimeneti eredmények
│   └── <paraméterek>/
│       ├── spaces/          # JSON fájlok
│       └── plots/           # PNG képek
│
├── output_logs/             # Szöveges logok
├── static/                  # Web statikus fájlok
└── templates/               # HTML sablonok
```

### Saját Megoldó Implementálása

Új megoldót a `CubeSolver` absztrakt osztályból kell örökölni:

```python
from cubesolver import CubeSolver

class MyCustomSolver(CubeSolver):
    def __init__(self, n, custom_param=None):
        self.n = n
        self.custom_param = custom_param
        self.running = False
        self.results = []

    def to_json(self):
        return {
            "n": self.n,
            "custom_param": self.custom_param
        }

    def get_params_string(self):
        return f"custom_{self.n}_{self.custom_param}"

    def pause(self):
        self.running = False

    def resume(self):
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        # Generator, üzeneteket küld vissza
        self.running = True
        for i in range(100):
            yield f"Iteration {i}: Score {i*0.5}"
            if not self.running:
                break

        self.export_results()
        yield "Completed!"

    def export_results(self, indices=None):
        # Eredmények mentése
        pass
```

### Egyéni Fitnesz Függvény

```python
from space import Space

def custom_fitness(space: Space) -> float:
    """
    Egyéni fitnesz függvény

    Args:
        space: A Space objektum

    Returns:
        float: Fitnesz érték (nagyobb = jobb)
    """

    # Büntetés az érvénytelen elrendezésekre
    for cube in space.cubes[1:]:
        if space.is_cube_within_base_cube(cube):
            return -1000

    # Saját célfüggvény: például sarokpontokhoz való közelség
    score = 0
    for cube in space.cubes[1:]:
        center = cube.get_center()
        # Plusz pont ha a kocka közel van a tér széleihez
        score += abs(center[0]) + abs(center[1]) + abs(center[2])

    return score
```

### Hibakeresés

**Érdemes logok írása:**

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Cube position: {cube.x}, {cube.y}, {cube.z}")
logger.info(f"Generation {gen}: Best fitness = {best.fitness}")
logger.warning(f"Cube {i} out of bounds!")
logger.error(f"Algorithm failed: {e}")
```

**Output logok elemzése:**

```bash
# Az utolsó futtatás logja
tail -f output_logs/Process_*.txt
```

**Eredmények vizsgálata:**

```python
import json

# Egy futtatás eredményeinek betöltése
with open("results/.../spaces/space_1_best.json") as f:
    result = json.load(f)
    print(f"N={result['n']}")
    print(f"Fitness={result['result']}")
    for cube in result['cubes']:
        print(f"  Size {cube['size']}: ({cube['x']}, {cube['y']}, {cube['z']})")
```

### Tesztelés

**Unit tesztek írása:**

```python
import unittest
from space import Space

class TestSpace(unittest.TestCase):
    def test_space_initialization(self):
        space = Space(n=10)
        self.assertEqual(len(space.cubes), 10)
        self.assertEqual(space.cubes[0].size, 10)
        self.assertEqual(space.cubes[-1].size, 1)

    def test_cube_within_bounds(self):
        space = Space(n=10)
        # Az alapkocka és az első 13 kocka már helyezve van
        self.assertTrue(space.is_part_of_a_cube((5, 5, 5)))

if __name__ == '__main__':
    unittest.main()
```

### Performance Tuning

1. **Fitness Mode választása:**
   - Mode 1 (Monte Carlo): 2-3× gyorsabb
   - Mode 2 (Full Grid): Pontosabb, de lassabb

2. **Population Size:**
   - Kisebb populáció = gyorsabb, de gyengébb megoldások
   - Nagyobb populáció = jobb megoldások, de lassabb

3. **Mutation Rate:**
   - Túl alacsony: Konvergálhat az optimum körüli zónába
   - Túl magas: Instabil, sosem konvergál

4. **Accuracy:**
   - Nagyobb accuracy = finomabb rács, de exponenciálisan lassabb
   - Ajánlott: 0-1 a többség alkalmazáshoz

---

## Tájékoztató és Hozzájárulás

### Ismert Korlátok

- Layer-by-layer stratégia nem működik megfelelően
- Nagyobb n értékek (>20) exponenciálisan lassabbak
- Monte Carlo becslés kicsi n-nél (8-10) pontatlan lehet

### Lehetséges Fejlesztések

1. **Párhuzamosított Fitnesz Számítás**: Multi-threading vagy GPU
2. **Részecske-raj Optimalizálás (PSO)**: Alternatív algoritmus
3. **Utótöltési Stratégiák**: Helyes szírás az eredmények után
4. **Valós Idejű Vizualizáció**: Élő 3D előnézet
5. **Machine Learning**: Hiperparaméter optimalizálás

### Közreműködés

Az új funkciók, hibajavítások vagy optimalizációk érdekében:

1. Készítsen új ágat
2. Végezze el a módosításokat
3. Tesztelje a kódot
4. Készítsen pull requestet

### Licenc

Ez a projekt oktatási célokra szabad felhasználni.

---

## Gyakran Ismételt Kérdések (FAQ)

### K: Mi a "reach" paraméter?

**V:** A `reach` a kritikus pontok közötti minimális távolság. Az algoritmus ezt keresi az optimális értéket, de manuálisan is beállítható. Nagyobb reach = több hely a kockák között.

### K: Hogyan értelmezzem a fitnesz értékeket?

**V:** A fitnesz érték azt jelzi, hogy mekkora az a legnagyobb kocka, amely még elfér a tér kitöltött részében. Minél nagyobb, annál jobb.

### K: Miért különböznek az eredmények többszöri futtatás után?

**V:** A genetikai algoritmus sztochasztikus, így minden futtatás eltérő lehet. A paraméterekben az `accuracy` és `generations` növelésével növelhető a stabilitás.

### K: Hogyan lehet az algoritmusokat párhuzamosan futtatni?

**V:** A `ServerApplication` és `Process` osztályok ezt lehetővé teszik. Egyszerre csak egy aktív folyamat fut, de várólistára tehet több folyamatot, és azok várakoznak.

### K: Melyik módban (Monte Carlo vs Full Grid) fussak?

**V:**
- **Mode 1 (Monte Carlo)**: Gyors teszteléshez, közel azonnal (< 1 perc/generáció)
- **Mode 2 (Full Grid)**: Pontos megoldásokhoz, ha van ideje (5-30 perc/generáció n=11-nél)

### K: Létezik-e garantált optimális megoldás?

**V:** Nem. Ez NP-nehéz probléma. Az algoritmusok közelítő megoldásokat találnak, nem garantáltan optimálisokat.

---

## Referenciák és Források

### Tudományos Háttér

- Genetikai algoritmusok: Holland, J. H. (1975). "Adaptation in Natural and Artificial Systems"
- Kockapakolás: NP-teljes probléma, rokon a bin packing-gel
- Monte Carlo módszerek: Stochasztikus szimulálás

### Felhasznált Könyvtárak

- **NumPy**: Numerikus számítások
- **Matplotlib**: 3D vizualizáció
- **Flask**: Web keretrendszer
- **FastAPI**: RESTful API
- **Pydantic**: Adatvalidáció
- **Tkinter**: GUI keretrendszer

---

## Changelog

### v1.0 (Aktuális)

- ✅ Genetikai algoritmus implementáció
- ✅ Konstruktív algoritmus (corner-first)
- ✅ Web-alapú felület (Flask)
- ✅ REST API (FastAPI)
- ✅ GUI (Tkinter)
- ✅ 3D vizualizáció
- ✅ Eredménytárolás (JSON)
- ✅ Process menedzsment

### v0.9 (Tervezett)

- 🔄 Layer-by-layer stratégia javítása
- 🔄 Párhuzamosítás (threading pool)
- 🔄 Valós idejű viz
- 🔄 Machine learning-alapú hiperparaméter tuning

---

## Szerzők és Köszönetnyilvánítás

Ez a projekt egy egyetemi laborvizsgafeladat keretében készült.

---

## Támogatás és Kapcsolat

Kérdések vagy hibákéjelentés:
- Készítsen GitHub issue-t (ha elérhető)
- E-mail: [kapcsolat információ]

---

*Dokumentáció utoljára frissítve: 2025. november*

**Jólehet ezt a dokumentációt a projekt fejlődésével párhuzamosan kell frissíteni!**
