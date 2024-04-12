import pandas as pd
import os

# Clean EPC column
def extract_epc(value):
    if isinstance(value, str) and '_' in value:
        parts = value.split('_')
        return parts[-1]
    else:
        return value
    
def map_to_numerical(column, mapping):
    return column.map(mapping)

def clean():
    # No início do seu script
    AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', 'C:\\Users\\Julio\\Desktop\\Airflow-Immo-Elisa')

    plugins_directory = os.path.join(AIRFLOW_HOME, 'plugins', 'immo-eliza-scraper')

    # Caminho para o arquivo CSV raw
    raw_csv_path = os.path.join(plugins_directory, 'Data', 'raw', 'final_raw.csv')

    # Lê o arquivo CSV
    immo = pd.read_csv(raw_csv_path)

    #remove unnecessary columns
    immo_c = immo.drop(columns=["Unnamed: 0",  "link", "country", "public_sales", "notary_sales"], axis=1)

    # Replace empty values with NaN
    immo_c.replace('', pd.NA, inplace=True)

    immo_c.head()
    #clean EPC
    immo_c['epc'] = immo_c['epc'].apply(extract_epc)
    immo_c['epc'].value_counts().to_frame()

    #Custom mappings
    epc_mapping = {'A++': 9, 'A+': 8, 'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1}
    state_mapping = {'JUST_RENOVATED': 6, 'AS_NEW': 5, 'GOOD': 4, 'TO_BE_DONE_UP': 3, 'TO_RENOVATE': 2, 'TO_RESTORE': 1}
    propert_type={'APARTMENT': 1, 'HOUSE': 0}
    # Apply mappings to create new numerical columns
    immo_c["epc"] = map_to_numerical(immo_c["epc"], epc_mapping)
    immo_c["state_building"] = map_to_numerical(immo_c["state_building"], state_mapping)
    immo_c["property_type"] = map_to_numerical(immo_c["property_type"], propert_type)


    # Create a dictionary with the different regions. 
    belgium_regions = {
        'Antwerp': 'Flanders',
        'Limburg': 'Flanders',
        'East Flanders': 'Flanders',
        'Flemish Brabant': 'Flanders',
        'West Flanders': 'Flanders',
        'Hainaut': 'Wallonia',
        'Walloon Brabant': 'Wallonia',
        'Namur': 'Wallonia',
        'Liège': 'Wallonia',
        'Luxembourg': 'Wallonia',
        'Brussels': 'Brussels-Capital'
    }

    # Create a new data set and map it with belgium_regions
    immo_c["region"] = immo_c["province"].map(belgium_regions)

    # Primeiro, remova as linhas com valores NA onde necessário.
    immo_c.dropna(subset=['total_area_m2', 'price'], inplace=True)

    # Agora, calcule 'price_square' diretamente em 'immo_c'.
    immo_c["price_square"] = immo_c["price"] / immo_c["total_area_m2"]

    immo_c.rename(columns={
        "floodZoneType": "fl_floodzone",
        "primaryEnergyConsumptionPerSqm": "primary_energy_consumption_sqm",
        "total_area_m2": "total_area_sqm",
        "furnished": "fl_furnished",
        "open_fire": "fl_open_fire",
        "terrace": "fl_terrace",
        "garden": "fl_garden",
        "surface_land": "surface_land_sqm",
        "swimming_pool": "fl_swimming_pool",
        "Double_Glazing": "fl_double_glazing",
        "Number_of_frontages": "nbr_frontages",
        "bedroom_count": "nbr_bedrooms"
    }, inplace=True)

    cols = [
        "id",
        "price",
        "property_type",
        "subproperty_type",
        "region", "province", "locality", "zip_code", "latitude", "longitude",
        "construction_year",
        "total_area_sqm", "surface_land_sqm",
        "nbr_frontages",
        "nbr_bedrooms",
        "equipped_kitchen",
        "fl_furnished",
        "fl_open_fire", 
        "fl_terrace", "terrace_sqm",
        "fl_garden", "garden_sqm",
        "fl_swimming_pool",
        "fl_floodzone",
        "state_building",
        "primary_energy_consumption_sqm", "epc", "heating_Type",
        "fl_double_glazing",
        "cadastral_income"
    ]

    immo_c = immo_c[cols]
    immo_c.head()

    # Caminho para o diretório onde o arquivo será salvo
    cleaned_directory = os.path.join(plugins_directory, 'Data', 'cleaned')

    # Verifica se o diretório existe
    if not os.path.exists(cleaned_directory):
        # Se não existe, cria o diretório
        os.makedirs(cleaned_directory)

    # Define o caminho completo para salvar o arquivo CSV limpo
    cleaned_csv_path = os.path.join(cleaned_directory, 'cleaned.csv')

    # Salva o DataFrame no arquivo CSV
    immo_c.to_csv(cleaned_csv_path)
    print("Data cleaned and saved to", cleaned_csv_path)

if __name__ == "__main__":
    clean()