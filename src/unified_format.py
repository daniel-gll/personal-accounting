from dataclasses import dataclass
from enum import Enum

class ColumnFormat(Enum):
    DATE = "calendar_date"
    TEXT = "text"
    CURRENCY = "currency"
    BOOLEAN = "boolean"

@dataclass
class column_t:
    header_text: str
    column_format: ColumnFormat
    mandatory: bool

class columns:
    column_format_types = [ColumnFormat.DATE.value, ColumnFormat.TEXT.value, ColumnFormat.CURRENCY.value, ColumnFormat.BOOLEAN.value]
    
    # Define class variables as column_t instances
    date =              column_t("Fecha",                   ColumnFormat.DATE,                   True)  
    #bank =              column_t("Banco",                   ColumnFormat.TEXT,                  False)
    amount =            column_t("Importe",                 ColumnFormat.CURRENCY,               True)
    transaction_type =  column_t("Tipo de transacción",     ColumnFormat.TEXT,                   False)
    iban =              column_t("IBAN",                    ColumnFormat.TEXT,                   False)
    origin =            column_t("Origen",                  ColumnFormat.TEXT,                   False)
    description =       column_t("Descripción",             ColumnFormat.TEXT,                   True)
    info_extended =     column_t("Descripción extendida",   ColumnFormat.TEXT,                   False)
    unused =            column_t("Unused",                  ColumnFormat.TEXT,                   False)

