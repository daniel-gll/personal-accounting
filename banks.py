class Bank:
    cvs_encodings_options = ["utf-8", "cp1252", "ISO-8859-1"]
    csv_encoding_options = [";", ","]
    
    def __init__(self, name, csv_encoding, cvs_delimiter, description="", cvs_header_row=0, csv_filename="importar.csv"):
        self.name = name
        self.description = description
        self.csv_encoding = csv_encoding
        if csv_encoding not in self.cvs_encodings_options:
            raise ValueError(f"Invalid encoding '{csv_encoding}' for bank '{name}'. Available options: {self.cvs_encodings_options}")
        self.cvs_delimiter = cvs_delimiter
        if cvs_delimiter not in self.csv_encoding_options:
            raise ValueError(f"Invalid delimiter '{cvs_delimiter}' for bank '{name}'. Available options: {self.csv_encoding_options}")
        self.cvs_header_row = cvs_header_row
        if not isinstance(cvs_header_row, int) or cvs_header_row < 0:
            raise ValueError(f"Invalid header row index '{cvs_header_row}' for bank '{name}'. It should be a non-negative integer.")
        self.csv_filename = csv_filename
        if (
            not isinstance(csv_filename, str)
            or not csv_filename
            or not csv_filename.lower().endswith(".csv")):
            raise ValueError(
                f"Invalid CSV filename '{csv_filename}' for bank '{name}'. It should be a non-empty string ending with '.csv'."
        )
    
    def __str__(self):
        return f"{self.name}"

    @classmethod
    def get_banks_list(cls):
        return [subcls.__name__ for subcls in cls.__subclasses__()]
    
    @classmethod
    def get_encodings_options(cls):
        return cls.cvs_encodings_options

    def get_info(self):
        return {
            "name": self.name,
            "csv_encoding": self.csv_encoding,
            "cvs_delimiter": self.cvs_delimiter,
            "cvs_header_row": self.cvs_header_row,
            "csv_filename": self.csv_filename
        }

class N26(Bank):
    def __init__(self):
        super().__init__(
            name="N26",
            csv_encoding="utf-8",
            cvs_delimiter=",",
            cvs_header_row=0,
            csv_filename="importar.csv", 
        )

class Abanca(Bank):
    def __init__(self):
        super().__init__(
            name="Abanca",
            csv_encoding="utf-8",
            cvs_delimiter=";",
            cvs_header_row=0,
            csv_filename="importar.csv",
        )
        
class DB(Bank):
    def __init__(self):
        super().__init__(
            name="DB",
            description="Deutsche Bank",
            csv_encoding="cp1252",
            cvs_delimiter=";",
            cvs_header_row=4,
            csv_filename="importar.csv",
        )