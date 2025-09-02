from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

class ParameterType(Enum):
    """Defines the data types for bank transaction parameters."""
    DATE = "calendar_date"
    TEXT = "text"
    CURRENCY = "currency"
    BOOLEAN = "boolean"

@dataclass(frozen=True)  # Make it hashable by making it immutable
class BankParamType:
    description: str
    parameter_type: ParameterType
    mandatory: bool
    
    def __hash__(self):
        """Make BankParamType hashable by hashing its attributes tuple"""
        return hash((self.description, self.parameter_type, self.mandatory))
    
    def __eq__(self, other):
        """Define equality for BankParamType"""
        if not isinstance(other, BankParamType):
            return False
        return (self.description == other.description and 
                self.parameter_type == other.parameter_type and 
                self.mandatory == other.mandatory)

@dataclass(frozen=True)  # Makes instances immutable and hashable
class Columns:
    #parameter_types = [ParameterType.DATE.value, ParameterType.TEXT.value, ParameterType.CURRENCY.value, ParameterType.BOOLEAN.value]
    
    # Define class variables as BankParamType instances
    date =              BankParamType("Fecha",                   ParameterType.DATE,                   True)  
    #bank =              BankParamType("Banco",                   ParameterType.TEXT,                  False)
    amount =            BankParamType("Importe",                 ParameterType.CURRENCY,               True)
    transaction_type =  BankParamType("Tipo de transacción",     ParameterType.TEXT,                   False)
    iban =              BankParamType("IBAN",                    ParameterType.TEXT,                   False)
    origin =            BankParamType("Origen",                  ParameterType.TEXT,                   False)
    description =       BankParamType("Descripción",             ParameterType.TEXT,                   True)
    info_extended =     BankParamType("Descripción extendida",   ParameterType.TEXT,                   False)
    unused =            BankParamType("Unused",                  ParameterType.TEXT,                   False)

    @classmethod
    def get_mandatory_columns(cls) -> Dict[str, BankParamType]:
        """
        Returns a dictionary of column objects that have mandatory=True.
        
        Returns:
            dict: Dictionary mapping column names to BankParamType objects
        """
        mandatory_cols = {}
        
        for attr_name in dir(cls):
            # Skip private/magic attributes
            if not attr_name.startswith('_'):
                attr_value = getattr(cls, attr_name)
                # Check if it's a BankParamType instance and if it's mandatory
                if isinstance(attr_value, BankParamType) and attr_value.mandatory:
                    mandatory_cols[attr_name] = attr_value
        return mandatory_cols
    
    @classmethod
    def get_all_columns(cls) -> Dict[str, BankParamType]:
        """
        Returns a dictionary of all column objects.
        
        Returns:
            dict: Dictionary mapping column names to BankParamType objects
        """
        all_cols = {}
        
        for attr_name in dir(cls):
            # Skip private/magic attributes
            if not attr_name.startswith('_'):
                attr_value = getattr(cls, attr_name)
                # Check if it's a BankParamType instance
                if isinstance(attr_value, BankParamType):
                    all_cols[attr_name] = attr_value

        return all_cols
    
    @classmethod
    def validate_column_mapping(cls, header_map: Dict) -> None:
        """Validates that all mandatory columns are present in the header mapping."""
        mandatory = cls.get_mandatory_columns()
        mapped_columns = set(header_map.values())
        
        missing = [name for name, col in mandatory.items() 
                  if col not in mapped_columns]
        
        if missing:
            missing_names = ", ".join(missing)
            raise ValueError(f"Missing mandatory columns: {missing_names}")


def create_unified_dataframe(df, bank):
    """
    Creates a unified DataFrame with standardized headers from a bank-specific DataFrame.
    
    Args:
        df (pd.DataFrame): Source DataFrame with bank-specific headers
        bank (Bank): Bank instance containing header mapping rules
        
    Returns:
        pd.DataFrame: New DataFrame with unified headers
    """
   

