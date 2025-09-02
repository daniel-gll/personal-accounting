from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
import banks_format as banks
import pandas as pd

class ParameterType(Enum):
    """Defines the data types for bank transaction parameters."""
    DATE = "calendar_date"
    TEXT = "text"
    CURRENCY = "currency"
    BOOLEAN = "boolean"

@dataclass(frozen=True)  # Make it hashable by making it immutable
class BankEntryType:
    description: str
    parameter_type: ParameterType
    mandatory: bool
    
    def __hash__(self):
        """Make BankParamType hashable by hashing its attributes tuple"""
        return hash((self.description, self.parameter_type, self.mandatory))
    
    def __eq__(self, other):
        """Define equality for BankParamType"""
        if not isinstance(other, BankEntryType):
            return False
        return (self.description == other.description and 
                self.parameter_type == other.parameter_type and 
                self.mandatory == other.mandatory)

@dataclass(frozen=True)  # Makes instances immutable and hashable
class UnifiedHeaders:
    #parameter_types = [ParameterType.DATE.value, ParameterType.TEXT.value, ParameterType.CURRENCY.value, ParameterType.BOOLEAN.value]
    
    # Define class variables as BankParamType instances
    date =              BankEntryType("Fecha",                   ParameterType.DATE,                   True)  
    #bank =              BankParamType("Banco",                   ParameterType.TEXT,                  False)
    amount =            BankEntryType("Importe",                 ParameterType.CURRENCY,               True)
    transaction_type =  BankEntryType("Tipo de transacción",     ParameterType.TEXT,                   False)
    iban =              BankEntryType("IBAN",                    ParameterType.TEXT,                   False)
    origin =            BankEntryType("Origen",                  ParameterType.TEXT,                   False)
    description =       BankEntryType("Descripción",             ParameterType.TEXT,                   True)
    info_extended =     BankEntryType("Descripción extendida",   ParameterType.TEXT,                   False)
    unused =            BankEntryType("Unused",                  ParameterType.TEXT,                   False)

    @classmethod
    def get_mandatory_columns(cls) -> Dict[str, BankEntryType]:
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
                if isinstance(attr_value, BankEntryType) and attr_value.mandatory:
                    mandatory_cols[attr_name] = attr_value
        return mandatory_cols
    
    @classmethod
    def get_all_columns(cls) -> Dict[str, BankEntryType]:
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
                if isinstance(attr_value, BankEntryType):
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


# def create_unified_dataframe(df: pd.DataFrame, bank: banks.Bank) -> pd.DataFrame:
#     """
#     Creates a unified DataFrame with standardized headers from a bank-specific DataFrame.
    
#     Args:
#         df (pd.DataFrame): Source DataFrame with bank-specific headers
#         bank (Bank): Bank instance containing header mapping rules
        
#     Returns:
#         pd.DataFrame: New DataFrame with unified headers
#     """
    
#     unified_df = pd.DataFrame(columns=list(UnifiedHeaders.get_all_columns().keys()))
        
#     return unified_df

