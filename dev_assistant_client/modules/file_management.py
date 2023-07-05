import os


def read_file(file_path):
    # Verifique se o arquivo existe
    if not os.path.isfile(file_path):
        raise Exception("File not found")

    # Tente abrir e ler o arquivo
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        raise Exception(str(e))
