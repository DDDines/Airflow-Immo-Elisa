from scraper.immoscraper import ImmoCrawler
import asyncio
import sys
import time
import threading
import os


def spinner():
    while True:
        for cursor in "|/-\\":
            sys.stdout.write(cursor)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b")


async def main():
    print("\nImmoCrawler is running...", end="", flush=True)
    threading.Thread(target=spinner, daemon=True).start()
    
    crawler = ImmoCrawler()
    await crawler.get_properties(1)
    
    # Defina um valor padrão para o caminho do diretório caso AIRFLOW_HOME não esteja disponível.
    default_raw_directory = 'C:\\Users\\Julio\\Desktop\\Airflow-Immo-Elisa\\plugins\\immo-eliza-scraper\\Data\\raw'
    plugins_directory = os.getenv('AIRFLOW_HOME', default_raw_directory)
    
    # Se AIRFLOW_HOME estiver definido, construa o caminho a partir dele, caso contrário, use o padrão.
    raw_directory = os.path.join(plugins_directory, 'Data', 'raw') if 'AIRFLOW_HOME' in os.environ else default_raw_directory

    # Verifica se o diretório existe
    if not os.path.exists(raw_directory):
        # Se não existe, cria o diretório
        os.makedirs(raw_directory)

    # Define o caminho completo para salvar o arquivo CSV
    cleaned_csv_path = os.path.join(raw_directory, 'final_raw')

    # Salva o DataFrame no arquivo CSV
    crawler.to_csv(cleaned_csv_path)
    print("Data cleaned and saved to", cleaned_csv_path)

if __name__ == "__main__":
    asyncio.run(main())