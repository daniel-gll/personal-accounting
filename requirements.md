
# Definitions

- BETD: (BD1) Bank-specific transaction data in CSV format. "The excel or cvs that you can download from your bank's webpage"
- BATD: (BD2) Bank-agnostic transaction data format. A common, pre-defined format that aims to be common across banks.
- BD3: Transaction database with several BD1.

## Aggregator-app

1. The system shall be able to convert BD1 data into BD2
  1.1 The system shall support different BD1 input formats, without any prior knowledge of the format (within reasonable limits).
    1.1.1 The system shall be able to detect the BD1 format automatically. (headers languages, date and time formats...)
    1.1.2 The system shall be able to detect the BD1 format by user input and pre-defined formats
       and allow the user to add new formats and to edit existing formats.
  1.2 The system shall be able to add new entries from BD1 into an existing BD2 database.
  1.3 The system shall be able to detect pre-existing (duplicate) entries in BD2 when updating the
    database with new BD1 data. Duplicate entries shall be handled appropriately.
  1.5 The system shall check the data cells for value consistency and format consistency. (e.g. "." instead of "," in decimals)
  1.4 The system shall throw a warning of potential gaps when updating the DB2 with new BD1 data. This is to prevent gaps in BD2, e.g. BD2 last entry is in January, but BD1 starts in March.

2. The system shall support multiple BD1 formats into the common BD2 format

## Classify-app

1. The system shall be able to classify L2 data into categories and group categories
  1.1 Categories and group categories shall be definable by the user.
  1.2 Categorization of data will be done by keyword searching.

## Otros

- N26 ha quitado una columna. ¿Cómo se comporta el programa?
- Abanca tiene algunos campos vacíos (que deberían estar llenos) en  "Comentario" -> cómo se clasifica bien?
TODO
