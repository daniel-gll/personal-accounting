import pandas as pd
import yaml_management as yaml_config

#Load base_path from local_settings.yaml
local_settings = yaml_config.load_local_settings()
banks_base_path = local_settings["banks_base_path"]

#Load bank configuration
bank_config = yaml_config.load_config()
banks_list = bank_config["Banks"]
header_list = bank_config["Headers"]

print(f"{banks_base_path}\{banks_list[0]}\importar.csv")
df = pd.read_csv(f"{banks_base_path}\\{banks_list[0]}\\importar.csv", delimiter=';')



