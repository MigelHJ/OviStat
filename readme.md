# OviStat Project Overview Prompt

## Project summary
OviStat is a Python desktop application for managing a registry of children and generating administrative/statistical summaries for an early-childhood institution. The app is built with CustomTkinter and allows users to create, edit, delete, and save child records, then switch to a statistics view that calculates age distribution, local vs commuter children, special support categories, meal types, and health-related indicators.

The project is primarily Hungarian-language and is designed for day-to-day use by staff who need a local, lightweight tool without a database backend.

## Core purpose
The application’s purpose is to:
- maintain a list of children with their core personal data,
- capture enrollment and classification information,
- validate date entries,
- persist data locally in CSV format,
- generate summary reports for management or operational planning.

## Main application flow
1. Launch the app from `main.py`.
2. The application loads `gyerek_adatok.csv` if it exists.
3. The user can add multiple child records from the main screen.
4. Each child record contains fields like name, date of birth, commuting route, gender, chronic illness status, meal type, and special needs flags.
5. The user can save the entire dataset or delete all records with confirmation dialogs.
6. The user can switch to a statistics page to review total counts and category breakdowns.

## Technical architecture
### Entry point
- `main.py`
  - Initializes the `App` window.
  - Sets theme and app icon.
  - Manages view switching between the input page and the statistics page.
  - Loads and saves CSV data.

### UI modules
- `mainpage.py`
  - Defines the `MainPage` class.
  - Shows a scrollable list of child cards.
  - Provides buttons for adding new child entries, saving all data, deleting all records, and opening the statistics page.

- `gyerek.py`
  - Defines `GyerekAdatlap`, the per-child form widget.
  - Contains fields for:
    - child name,
    - date of birth,
    - commute location,
    - gender,
    - chronic illness status,
    - meal type,
    - checkbox flags such as large family, SNI, BTM, HH, HHH.
  - Includes validation and save/delete methods.

- `statisztika.py`
  - Defines `StatisztikaNezet`.
  - Processes the child dataset and computes summary statistics.
  - Renders dashboard-style cards for:
    - total children,
    - local vs commuter children,
    - age distribution by gender,
    - legal/special status categories,
    - meal types,
    - health conditions.
  - Allows date-based recalculation with a date selection control.

- `alert.py`
  - Defines `AlertPopup`, a confirmation modal used before destructive actions such as deleting records or saving all changes.

### Styling and assets
- `custom_theme.json`
  - Custom theme configuration for the CustomTkinter UI.
- `OviStat.ico`
  - Application icon.

## Data model
The app stores records in memory as dictionaries, with each child represented roughly like this:

- `id`
- `gyerek_neve`
- `szuletesi_datum`
- `bejaras`
- `nem`
- `tartosbeteg`
- `etkezes`
- `nagycsalados`
- `sni`
- `btm`
- `hh`
- `hhh`

Persistence is done as CSV rows in `gyerek_adatok.csv` rather than a relational database.

## Functional requirements reflected in the code
- Add multiple children to the registry.
- Fill in repeated data-entry cards for each child.
- Keep a unique ID for each card.
- Validate date fields before saving data.
- Persist all children as CSV output.
- Show confirmation before overwriting file data or clearing the registry.
- Compute statistics for the current dataset.
- Filter out empty child entries from statistical calculations.
- Support switching between data entry and reporting views.

## Dependencies and runtime environment
The project uses Python and GUI libraries. The code is centered around:
- `customtkinter`
- `ctkdateentry`

The repository’s `requirements.txt` currently lists only `PySide6`, which appears outdated/inconsistent with the actual imports. In practice, the project likely depends on `customtkinter` and `ctkdateentry` as well.

## How to run
From the project root:

```bash
python main.py
```

If dependencies are missing, install the required packages before running the app.

## Known implementation notes
- The project is Hungarian-language oriented, so labels, messages, and field names are written in Hungarian.
- Some code paths refer to additional flags like `HH` and `HHH`, but they are not consistently stored or loaded across all modules.
- There are a few inconsistencies in CSV parsing logic, which suggests the app may still be evolving or was partially refactored.
- The app is a lightweight local utility rather than a full web application or multi-user system.

## Prompt-ready summary
This project is a local desktop application for tracking children and generating summary statistics. It is built in Python with CustomTkinter, stores data in a CSV file, and includes both a data-entry interface and a reporting dashboard. The app is organized around a central `App` controller, a main page with child cards, a per-child form widget, and a statistics view that calculates age, category, health, and meal-based summaries from the current dataset.
