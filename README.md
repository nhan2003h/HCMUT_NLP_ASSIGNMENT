# Natural Language Processing Assignment

- Full Name: `Nhan Vo Ngoc Thanh`

- Student ID: `2114278`

- Address: `Faculty of Computer Science and Engineering -
University of Technology - VNUHCM`

## PART I: Writing grammar, generating sentences from grammar and parsing the sentences

This project is the first part of the Natural Language Processing assignment. It involves generating and parsing sentences based on a given grammar.

## Library Usage

The following libraries are required for this project:

- `openpyxl>=3.0.5` (for saving Excel files with pandas)
- `xlrd>=1.2.0`
- `Click>=7.1.2`
- `deprecation>=2.1.0`
- `pandas>=1.1.4`
- `numpy>=1.19.4`
- `scipy>=1.5.4`
- `matplotlib>=3.3.2`
- `nltk>=3.5` (additional compared to the source that was downloaded)
- `pyvi>=0.1` (additional compared to the source that was downloaded)

## Core Processing of part I

The core processing for Task 1 is located in the file `nlp/app/task_1.py`.

It includes some main functions described as below:

### 1. `generate_sentences(grammar, num_sentences=10000)`

#### Parameters:

`grammar`: The grammar rules used to generate sentences.

`num_sentences`: The number of sentences to generate (default is 10,000).

#### Functionality:
- Generates sentences based on the provided grammar.
- Writes the generated sentences to nlp/output/samples.txt.
- Prints a confirmation message upon successful completion.

### 2. `parse(grammar, sentence)`:

#### Parameters:

`grammar`: The grammar rules used to parse the sentence.

`sentence`: The sentence to be parsed.
#### Functionality:
- Tokenizes the sentence using ViTokenizer.
- Replaces underscores with spaces in the tokens.
- Parses the tokenized sentence using nltk.ChartParser.
- Returns the parse tree if parsing is successful; otherwise, returns None.

### 3. `parse_sentences(grammar, file_path)`:

#### Parameters:

`grammar`: The grammar rules used to parse the sentences.

`file_path`: The path to the file containing sentences to be parsed.

#### Functionality:

- Reads sentences from the specified file.
- Parses each sentence using the parse function.
- Writes the parse results to nlp/output/parsed-results.txt.

## Grammar Rules

The grammar rules are defined in the file `nlp/data/rules.txt`.

## Parsing input
The input of parser is in `nlp/data/sentences.txt`

-----------

## PART II: Semantic representation and response
### Objective
Implement a simple question-answering system based on customer queries regarding tour details.

### Steps

1. **Build a Dependency Parser**
   - Parse customer queries to extract syntactic and semantic relationships.
   - Example: For the query *"đi từ Hồ Chí Minh tới Nha Trang hết bao lâu?"*, extract:
     - Action: `đi`
     - Start: `Ho Chi Minh`
     - End: `Nha Trang`
     - Attribute: `bao lâu`

2. **Parse and Extract Semantic Relations**
   - Map the extracted components to database fields.

3. **Define Grammar and Database Mapping**
   - Establish rules to map queries into database relationships.
   - Example mapping:  
     Query: *"đi từ Hồ Chí Minh tới Nha Trang hết bao lâu?"*  
     Logic: `QUERY(RUN-TIME, start="HCM", end="NT")`

4. **Retrieve Data and Generate Responses**
   - Access the local database to fetch information:
     - Example: `"RUN-TIME(HCM, NT)" → "5:00 HR"`
   - Generate a natural language response:
     - Output: *"Đi từ HCM đến Nha_Trang mất 5:00 HR."*

5. **Output Results**
   - Save results for each query to files: `output/p2-q-$i.txt`
     - Example: Query 1 → `output/p2-q-1.txt`

## Core Processing of part II

Core Processing of this part is in folder `models`

The `models` folder contains the core processing logic for the question-answering system. Here is a breakdown of each file and its core processing:

### I. `answer.py`

1. **`answer(procedure: Procedure)`**
- **Purpose:** Processes a query defined by a `Procedure` object and generates an answer string based on preloaded data (e.g., tours, departure/arrival times, runtime, transportation method).
- **Key Functionalities:**
  - **Data Querying:** Handles various query types such as:
    - `"PRINT-ALL"` for listing tours.
    - `"RUN-TIME"` for calculating travel duration.
    - `"BY"` for transportation methods.
    - `"DATE"` for available travel dates.
  - **Result Construction:** Constructs human-readable responses with Vietnamese text for queried tour details.
  - **Sub-functions:**
    - `ignore_escape(string: str)`: Removes escape characters (e.g., `"`).
    - `get_date(string: str)`: Extracts the date from a string.

2. **`load_data(path=None)`**
- **Purpose:** Loads and parses data from a specified file (default: `"nlp/input/database.txt"`) into dictionaries for use in the `answer` function.
- **Key Functionalities:**
  - **Data Parsing:** Extracts and processes data for:
    - `TOUR`: Mapping of tour codes to their names.
    - `ATIME`: Arrival times for tours.
    - `DTIME`: Departure times for tours.
    - `RUNTIME`: Travel time between locations.
    - `BY`: Transportation methods.
  - **Data Cleaning:** Handles special cases such as replacing `HCMC` with `HCM` and removing extra characters.
- **Output:** Returns five dictionaries: `TOUR`, `ATIME`, `DTIME`, `RUNTIME`, and `BY`.
### II. `malt_parser.py`

#### 1. **Class: `Dependency`**

* **Purpose:** Represents a syntactic dependency between two words in a sentence.
* **Key Attributes:**
  * `relation (str)`: The syntactic relation type (e.g., "subject", "object").
  * `head (str)`: The governing word in the dependency.
  * `tail (str)`: The dependent word in the dependency.
* **Key Methods:**
  * `__str__`: Returns a string representation of the dependency in the format `"head" --relation-> "tail"`.

---

#### 2. **Class: `MaltParser`**

* **Purpose:** Implements a simplified version of dependency parsing based on a stack-buffer mechanism and a set of rules for forming arcs.

---

##### a. **Static Constants**

* **`ROOT`**: Special token representing the root of the dependency tree.
* **`RIGHT_ARC`**: Dictionary defining the valid syntactic relationships where the buffer word depends on the stack word.
* **`LEFT_ARC`**: Dictionary defining valid syntactic relationships where the stack word depends on the buffer word.

---

##### b. **`tokenize(text: str, debug: bool = False) -> list[str]`**

* **Purpose:** Prepares and tokenizes a sentence into a list of valid tokens.
* **Key Functionalities:**
  * **Normalization and Preprocessing:**
    * Converts text to NFC form and lowercase.
    * Removes extra spaces and ensures proper handling of punctuation (e.g., spacing before `?`).
  * **Token Replacement:** Applies a predefined dictionary (`TOKEN_DICT`) to replace certain substrings with standard tokens.
  * **Token Filtering:** Keeps only tokens that exist in the `POS` dictionary.
* **Parameters:**
  * `text (str)`: Input sentence to be tokenized.
  * `debug (bool)`: If `True`, prints the tokens and their parts of speech (POS).
* **Returns:** List of valid tokens.

---

##### c. **`parse_dependencies(tokens: list[str]) -> list[Dependency]`**

* **Purpose:** Parses a list of tokens into a dependency tree using the stack-buffer parsing mechanism.
* **Key Functionalities:**
  * **Stack-Buffer Initialization:** Initializes the stack with the `ROOT` and the buffer with the tokens.
  * **Parsing Loop:**
    * Processes tokens by examining the top of the stack and the first item in the buffer.
    * Forms dependencies based on the `RIGHT_ARC` and `LEFT_ARC` rules.
    * Applies parsing actions (`SHIFT`, `REDUCE`, etc.) based on the stack and buffer states.
  * **Root Verb Handling:** Ensures proper handling of ambiguous parts of speech (POS) based on the first verb identified as the root.
  * **Action Handling:**
    * **RIGHT_ARC:** Links the top of the stack to the front of the buffer.
    * **LEFT_ARC:** Links the front of the buffer to the top of the stack.
    * **SHIFT:** Moves the front of the buffer to the stack.
    * **REDUCE:** Removes the top of the stack.
* **Returns:** List of `Dependency` objects representing the parsed tree.

---

##### d. **`parse(sentence: str) -> list[Dependency]`**

* **Purpose:** Tokenizes a sentence and parses it into a list of syntactic dependencies.
* **Key Functionalities:**
  * Calls `tokenize` to preprocess and tokenize the sentence.
  * Passes the tokens to `parse_dependencies` to generate the dependency tree.
* **Returns:** List of `Dependency` objects.

### III. `dependency_to_semantic.py`

#### 1. **Class: `Relation`**

* **Purpose:** Represents a relationship between two entities in a semantic structure.
* **Attributes:**
  * `type (str)`: The type of relationship (e.g., AGENT).
  * `left (str)`: The left entity in the relationship (e.g., s1).
  * `right (str)`: The right entity in the relationship (e.g., đến).
* **Methods:**
  * `__str__`: Returns a string representation of the relationship in the format `"(left relation_type right)"`.

---

#### 2. **Class: `SEM`**

* **Purpose:** Represents a semantic structure with a predicate, a variable, and optional relations.
* **Attributes:**
  * `predicate (str)`: The main predicate (e.g., "verb").
  * `variable (str)`: A variable used in the semantic structure.
  * `relations (list)`: A list of relations related to the predicate.
* **Methods:**
  * `__str__`: Returns a string representation of the semantic structure, including the predicate, variable, and relations.

---

#### 3. **Function: `create_variable(name: str, existing_vars: "list[str]") -> str`**

* **Purpose:** Creates a unique variable name based on the given name and existing variables.
* **Key Functionalities:**
  * Uses the first letter of `name` as the variable prefix.
  * Iterates over possible variable names by appending an index (e.g., `s1`, `s2`).
  * Returns a unique variable name that doesn't exist in `existing_vars`.
* **Parameters:**
  * `name (str)`: The base name for creating a variable.
  * `existing_vars (list[str])`: A list of existing variable names.
* **Returns:** A unique variable name.

---

#### 4. **Function: `create_sem(word: str, variables: "list[str]") -> tuple`**

* **Purpose:** Creates a semantic structure (SEM) or returns the original word if it is not a NAME.
* **Key Functionalities:**
  * Calls `create_variable` to create a unique variable name.
  * Checks if the `POS[word]` is not "NAME".
  * If the word is a "NAME", it creates a semantic structure.
* **Parameters:**
  * `word (str)`: The word to create a semantic structure for.
  * `variables (list[str])`: A list of existing variables.
* **Returns:** A tuple containing the semantic structure (if the word is a NAME) or the original word with `None`.

---

#### 5. **Function: `handle_dependent_sem(dependent: str, variables: "list[str]", relation_type: str) -> tuple`**

* **Purpose:** Handles the creation of a semantic structure for a dependent and updates variables.
* **Key Functionalities:**
  * Calls `create_sem` to create a semantic structure for the dependent word.
  * Updates the list of variables if a new variable is created.
  * Creates and returns a `Relation` object with the specified relation type.
* **Parameters:**
  * `dependent (str)`: The dependent word.
  * `variables (list[str])`: A list of existing variables.
  * `relation_type (str)`: The type of relationship (e.g., "SRC", "THEME").
* **Returns:** A `Relation` object representing the relationship between the dependent and the semantic structure.

---

#### 6. **Function: `relation_extract(dependencies: "list[Dependency]") -> "list[Relation]"`**

* **Purpose:** Extracts semantic relationships from a list of dependencies.
* **Key Functionalities:**
  * Iterates over the list of `dependencies` and processes each dependency based on its relation type.
  * Handles various cases (e.g., `query`, `noun_query`, `root`, `subj`, `nmod`, `pobj`) and constructs corresponding `Relation` objects.
  * Uses `handle_dependent_sem` to create relations for dependent words.
  * Updates the list of variables during the extraction process.
* **Parameters:**
  * `dependencies (list[Dependency])`: A list of dependencies representing syntactic relationships between words.
* **Returns:** A list of `Relation` objects representing the semantic relationships.

---
### IV. `semantic_parser.py`
- **`generate_procedures(sem: SEM)`:** Creates a list of procedures based on extracted semantic roles (e.g., subject, source, destination).
- **`extract_subject(sem: SEM)`:** Identifies the main query type (e.g., TOUR, RUN-TIME).
- **`extract_destination(sem: SEM)`:** Extracts the destination from the semantic structure.
- **`extract_source(sem: SEM)`:** Extracts the source location.
- **`find_semantic_unit_by_predicate(sem: SEM, predicate: str)`:** Searches for a semantic unit matching a given predicate.

---

### V. `logical_parser.py`
#### **logical_parse(relations: "list[Relation]")**
- **Purpose:** Parses a list of `Relation` objects into a semantic representation (`SEM`) to capture the logical structure of a query.
- **Key Features:**
  - Maps relations (`Relation`) to specific semantic roles (`SEM`) based on their type (e.g., QUERY, THEME, SRC, DES).
  - Constructs nested `SEM` objects to represent the structure of the input relations.
  - Handles different query types like:
    - **"tour"** → Associated with `WHICH` queries.
    - **"bao_lâu"** → Maps to duration (`HOW-LONG`).
    - **"bao_nhiêu"** → Maps to quantity (`HOW-MANY`).
    - **"phương_tiện"** → Maps to transportation (`INSTR`).
    - **"ngày"** → Maps to date (`DATE`).
  - Adds co-queries if present (`CO_QUERY`) to extend semantic relations.
  - Supports various predicates (e.g., `PRED`) with additional roles:
    - **THEME**: Main focus or subject.
    - **SRC**: Source location.
    - **DES**: Destination location.
    - **AGENT**: Associated actor or agent.

- **Logic Flow:**
  1. **Relation Mapping:** Maps input relations by their type for easy lookup.
  2. **Agent Semantic:** Creates `agent_sem` based on the `QUERY` relation type.
  3. **Theme Handling:** Adds theme or co-theme relationships if present.
  4. **Predicate Construction:** Builds `SEM` for predicates using:
     - **THEME**: For main subjects.
     - **SRC/DES**: For source and destination relationships.
     - **AGENT**: For actor associations.
  5. **Final Assembly:** Combines all components into a `WH-QUERY` root `SEM`.

- **Output:** Returns a structured `SEM` object representing the parsed logical query.

## Changes in `util.sh`

There were a few changes made to the `util.sh` script to address issues with mounting folders. The original script mounted the `nlp` folder at the same level as `src`, but the Dockerfile sets the working directory to `src`. This caused issues with the absolute path in Docker, preventing access to the `nlp` folder outside `src`.

### Original Mount Command

```sh
docker run --rm -v $S_OUT:/nlp/output -v $S_IN:/nlp/input nlp222
```

### Modified Mount Command

```sh
docker run --rm -v $S_OUT:/src/nlp/output -v $S_IN:/src/nlp/input nlp222
```


After this change, the `output_path` will be in `nlp/output/.`

## Running the project
Use the modified `util.sh` script to run the Docker container with the correct volume mounts.

### Example:
```sh
bash util.sh test
```