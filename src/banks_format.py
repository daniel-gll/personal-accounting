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
    
    def __init__(self, name="Bank",  header_map=None, csv_encoding="utf-8", csv_delimiter=",", description="", csv_header_row=0, csv_last_row=0, csv_filename="importar.csv"):
        self.name = name
        self.description = description
        if header_map is None:
            self.header_map = {}
        else:
            self.header_map = header_map
        for key, value in self.header_map.items():
            if not isinstance(value, udb.BankEntryType):
                raise ValueError(f"Header mapping for '{key}' must be a udb.BankParamType instance, got {type(value)} instead.")

        self.csv_encoding = csv_encoding
        if csv_encoding not in self.CSV_ENCODINGS:
            raise ValueError(f"Invalid encoding '{csv_encoding}' for bank '{name}'. Available options: {self.CSV_ENCODINGS}")
        
        self.csv_delimiter = csv_delimiter
        if csv_delimiter not in self.CSV_DELIMITERS:
            raise ValueError(f"Invalid delimiter '{csv_delimiter}' for bank '{name}'. Available options: {self.CSV_DELIMITERS}")
        
        self.csv_header_row = csv_header_row
        if not isinstance(csv_header_row, int) or csv_header_row < 0:
            raise ValueError(f"Invalid header row index '{csv_header_row}' for bank '{name}'. It should be a non-negative integer.")
        
        self.csv_last_row = csv_last_row
        if not isinstance(csv_last_row, int) or csv_last_row > 0:
            raise ValueError(f"Invalid last row index '{csv_last_row}' for bank '{name}'. It should be a negative or 0 integer (e.g., -1 for last row) or zero.")
        
        self.csv_filename = csv_filename
        if (
            not isinstance(csv_filename, str)
            or not csv_filename
            or not csv_filename.lower().endswith(".csv")):
            raise ValueError(
                f"Invalid CSV filename '{csv_filename}' for bank '{name}'. It should be a non-empty string ending with '.csv'."
        )

        #Validates that all mandatory columns are present in the header mapping
        udb.UnifiedHeaders.validate_column_mapping(self.header_map)

    def __str__(self):
        return f"{self.name}"

def check_mandatory_columns(self):
    """
    Checks if all mandatory unified_format columns are mapped in the bank's header_map.
    Raises an error if any mandatory columns are not mapped.
    
    Raises:
        ValueError: If any mandatory columns are not mapped in header_map
    """
    # Get all mandatory column attributes from udb.columns
    mandatory_columns = udb.UnifiedHeaders.get_mandatory_columns()

    # Get all columns that are mapped in the header_map
    mapped_columns = list(self.header_map.values())
    
    # Find unmapped mandatory columns
    unmapped_mandatory = {attr: col for col, attr in mandatory_columns.items() 
                         if col not in mapped_columns}
    
    # Raise error if there are unmapped mandatory columns
    if unmapped_mandatory:
        mandatory_names = ", ".join(f"'{attr}'" for attr in unmapped_mandatory.keys())
        raise ValueError(
            f"Missing mandatory column mappings in {self.name}'s header_map: {mandatory_names}. "
            f"These columns must be mapped to CSV headers."
        )
        

    @classmethod
    def get_banks_list(cls):
        return [subcls.__name__ for subcls in cls.__subclasses__()]
    
    @classmethod
    def get_encodings_options(cls):
        return cls.CSV_ENCODINGS
    
    @classmethod
    def get_delimiters_options(cls):
        return cls.CSV_DELIMITERS

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
            header_map = {
                #"Date":                     udb.columns.date,
                #"Account number":           udb.columns.iban,
                #"Transaction type":         udb.columns.transaction_type,
                #"Payment reference":        udb.columns.description,
                #"Amount (EUR)":             udb.columns.amount,
                #"Amount (Foreign Currency)": udb.columns.unused,
                #"Type Foreign Currency":    udb.columns.unused,
                #"Exchange Rate":            udb.columns.unused,
                "Booking Date":             udb.UnifiedHeaders.date,
                "Value Date":               udb.UnifiedHeaders.unused,
                "Partner Name":             udb.UnifiedHeaders.origin,
                "Partner Iban":             udb.UnifiedHeaders.iban,
                "Type":                     udb.UnifiedHeaders.transaction_type,
                "Payment Reference":        udb.UnifiedHeaders.description,
                "Account Name":             udb.UnifiedHeaders.unused,
                "Amount (EUR)":             udb.UnifiedHeaders.amount,
                "Original Amount":          udb.UnifiedHeaders.unused,
                "Original Currency":        udb.UnifiedHeaders.unused,
                "Exchange Rate":            udb.UnifiedHeaders.unused,
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
            header_map = {
                "Fecha ctble":      udb.UnifiedHeaders.date,
                "Fecha valor":      udb.UnifiedHeaders.unused,
                "Concepto":         udb.UnifiedHeaders.description,
                "Importe":          udb.UnifiedHeaders.amount,
                "Moneda":           udb.UnifiedHeaders.unused,
                "Saldo":            udb.UnifiedHeaders.unused, # TODO saldo!
                "Moneda 2":         udb.UnifiedHeaders.unused,
                "Concepto ampliado":udb.UnifiedHeaders.info_extended,
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
            header_map = {
                "Buchungstag":                  udb.UnifiedHeaders.date,
                "Wert":                         udb.UnifiedHeaders.unused, #Date 2
                "Umsatzart":                    udb.UnifiedHeaders.transaction_type,
                "Begünstigter / Auftraggeber":  udb.UnifiedHeaders.origin,
                "Verwendungszweck":             udb.UnifiedHeaders.description,
                "IBAN":                         udb.UnifiedHeaders.iban,
                "BIC":                          udb.UnifiedHeaders.info_extended,
                "Kundenreferenz":               udb.UnifiedHeaders.info_extended,
                "Mandatsreferenz ":             udb.UnifiedHeaders.unused,
                "Gläubiger ID":                 udb.UnifiedHeaders.unused,
                "Fremde Gebühren":              udb.UnifiedHeaders.unused,
                "Betrag":                       udb.UnifiedHeaders.amount,
                "Abweichender Empfänger":       udb.UnifiedHeaders.unused,
                "Abweichender Auftraggeber":    udb.UnifiedHeaders.unused,
                "Anzahl der Aufträge":          udb.UnifiedHeaders.unused,
                "Anzahl der Schecks":           udb.UnifiedHeaders.unused,
                "Soll":                         udb.UnifiedHeaders.amount,
                "Haben":                        udb.UnifiedHeaders.unused,
                "Währung":                      udb.UnifiedHeaders.unused
            }
        )