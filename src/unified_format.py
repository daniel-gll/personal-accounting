class ubd:
    unified_headers = {
        "Date":             "YYYY-MM-DD",   # Fecha
        "Bank":             "string",       # Banco
        "Amount":           "currency",     # Importe
        "TransactionType":  "string",       # Tipo de transacción
        "IBAN":             "string",       # IBAN
        "Origin":           "string",       # Origen
        "Description":      "string",       # Concepto
        "Reference":        "string",       # Referencia
        "Balance":          "currency",     # Balance, if applicable
        "Unused":           "string",       # Unused column, can be empty
    }
    
    headers_spanish = {
        "Fecha":                "Date",         # Date 
        "Banco":                "Bank",         # Bank
        "Importe":              "Amount",       # Amount 
        "Tipo de transacción":  "TransactionType",  # Transaction Type
        "IBAN":                 "IBAN",         # IBAN
        "Origen":               "Origin",       # Origin
        "Concepto":             "Description",  # Description
        "Referencia":           "Reference",    # Reference
    }
        
        
    def __init__(self, db):
        self.db = db

    def get(self, key):
        return self.db.get(key)

    def set(self, key, value):
        self.db.set(key, value)

    def delete(self, key):
        self.db.delete(key)

    def exists(self, key):
        return self.db.exists(key)

    def keys(self):
        return self.db.keys()