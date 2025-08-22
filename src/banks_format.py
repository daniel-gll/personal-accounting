# This file contains a list of banks and their configurations for CSV processing.
# E.g. each bank has a name, CSV encoding, delimiter, header mapping, and other configurations.
# To add support for a new bank, create a new subclass of the Bank class with the appropriate configurations.
# Each bank is represented as a subclass of the Bank class.

from dataclasses import dataclass
from typing import Dict, List
import unified_format as udb

@dataclass
class Bank:
    CSV_ENCODINGS = ["utf-8", "cp1252", "ISO-8859-1"]
    CSV_DELIMITERS = [";", ","]
    
    header_mapping: Dict[str, udb.column_t]
    name: str = "Bank"
    csv_encoding: str = "utf-8"
    csv_delimiter: str = ","
    description: str = ""
    csv_header_row: int = 0
    csv_last_row: int = 0
    csv_filename: str = "importar.csv"
    

    def __init__(self, name="Bank",  header_mapping=None, csv_encoding="utf-8", csv_delimiter=",", description="", csv_header_row=0, csv_last_row=0, csv_filename="importar.csv"):
        self.name = name
        self.description = description
        if header_mapping is None:
            self.header_mapping = {}
        else:
            self.header_mapping = header_mapping
        for key, value in self.header_mapping.items():
            if not isinstance(value, udb.column_t):
                raise ValueError(f"Header mapping for '{key}' must be a udb.column_t instance, got {type(value)} instead.")

        self.csv_encoding = csv_encoding
        # Data validation
        if csv_encoding not in self.CSV_ENCODINGS:
            raise ValueError(f"Invalid encoding '{csv_encoding}' for bank '{name}'. Available options: {self.CSV_ENCODINGS}")
        self.csv_delimiter = csv_delimiter
        if csv_delimiter not in self.CSV_ENCODINGS:
            raise ValueError(f"Invalid delimiter '{csv_delimiter}' for bank '{name}'. Available options: {self.CSV_ENCODINGS}")
        self.csv_header_row = csv_header_row
        if not isinstance(csv_header_row, int) or csv_header_row < 0:
            raise ValueError(f"Invalid header row index '{csv_header_row}' for bank '{name}'. It should be a non-negative integer.")
        self.csv_last_row = csv_last_row
        if not isinstance(csv_last_row, int) or csv_last_row > 0:
            raise ValueError(f"Invalid header row index '{csv_last_row}' for bank '{name}'. It should be a negative integer.")
        self.csv_filename = csv_filename
        if (
            not isinstance(csv_filename, str)
            or not csv_filename
            or not csv_filename.lower().endswith(".csv")):
            raise ValueError(
                f"Invalid CSV filename '{csv_filename}' for bank '{name}'. It should be a non-empty string ending with '.csv'."
        )
        self.header_map = header_mapping
        self.check_mandatory_columns()
    
    def __str__(self):
        return f"{self.name}"

    # Check that all mandatory columns are mapped in header_mapping
    def check_mandatory_columns(self):
        # Get all column_t attributes from udb.columns where mandatory is True
        mandatory_columns = [
            getattr(udb.columns, attr)
            for attr in dir(udb.columns)
            if not attr.startswith("__")
            and isinstance(getattr(udb.columns, attr), udb.column_t)
            and getattr(udb.columns, attr).mandatory
        ]
        mapped_columns = set(self.header_mapping.values())
        missing = [col for col in mandatory_columns if col not in mapped_columns]
        if missing:
            raise ValueError(f"Missing mandatory columns in header_mapping: {[col.header_text for col in missing]}")

    @classmethod
    def get_banks_list(cls):
        return [subcls.__name__ for subcls in cls.__subclasses__()]
    
    @classmethod
    def get_encodings_options(cls):
        return cls.CSV_ENCODINGS

    def get_info(self):
        return {
            "name": self.name,
            "csv_encoding": self.csv_encoding,
            "csv_delimiter": self.csv_delimiter,
            "csv_header_row": self.csv_header_row,
            "csv_filename": self.csv_filename
        }
    

class N26(Bank):
    def __init__(self):
        super().__init__(
            name="N26",
            csv_encoding="utf-8",
            csv_delimiter=",",
            csv_header_row=0,
            csv_filename="importar.csv",
            header_mapping = {
				"Date":                 udb.columns.date,
                "Payee":                udb.columns.origin,
                "Account number":       udb.columns.iban,
                "Transaction type":     udb.columns.transaction_type,
                "Payment reference":    udb.columns.description,
                "Amount (EUR)":         udb.columns.amount,
                "Amount (Foreign Currency)": udb.columns.unused,
                "Type Foreign Currency": udb.columns.unused,
                "Exchange Rate":        udb.columns.unused,
                "Booking Date":         "Date",
                "Value Date":           "Unused",
                "Partner Name":         "Origen",
                "Partner Iban":         "IBAN",
                "Type":                 "TransactionType",
                "Payment Reference":    "Reference",
                "Account Name":         "Unused",
                "Amount (EUR)":         "Amount",
                "Original Amount":      "Unused",
                "Original Currency":    "Unused",
                "Exchange Rate":        "Unused",
            } 
        )

class Abanca(Bank):
    def __init__(self):
        super().__init__(
            name="Abanca",
            csv_encoding="utf-8",
            csv_delimiter=";",
            csv_header_row=0,
            csv_filename="importar.csv",
            header_mapping = {
                "Fecha ctble":      udb.columns.date,
                "Fecha valor":      udb.columns.unused,
                "Concepto":         udb.columns.description,
                "Importe":          udb.columns.amount,
                "Moneda":           udb.columns.unused,
                "Saldo":            udb.columns.unused, # TODO saldo!
                "Moneda 2":         udb.columns.unused,
                "Concepto ampliado":udb.columns.info_extended,
            }
        )
        
class DB(Bank):
    def __init__(self):
        super().__init__(
            name="DB",
            description="Deutsche Bank",
            csv_encoding="cp1252",
            csv_delimiter=";",
            csv_header_row=4,
            csv_last_row=-1,
            csv_filename="importar.csv",
            header_mapping = {
                "Buchungstag":                  udb.columns.date,
                "Wert":                         udb.columns.unused, #Date 2
                "Umsatzart":                    udb.columns.transaction_type,
                "Begünstigter / Auftraggeber":  udb.columns.origin,
                "Verwendungszweck":             udb.columns.description,
                "IBAN":                         udb.columns.iban,
                "BIC":                          udb.columns.info_extended,
                "Kundenreferenz":               udb.columns.info_extended,
                "Mandatsreferenz ":             udb.columns.unused,
                "Gläubiger ID":                 udb.columns.unused,
                "Fremde Gebühren":              udb.columns.unused,
                "Betrag":                       udb.columns.amount,
                "Abweichender Empfänger":       udb.columns.unused,
                "Abweichender Auftraggeber":    udb.columns.unused,
                "Anzahl der Aufträge":          udb.columns.unused,
                "Anzahl der Schecks":           udb.columns.unused,
                "Soll":                         udb.columns.amount,
                "Haben":                        udb.columns.unused,
                "Währung":                      udb.columns.unused
            }
        )