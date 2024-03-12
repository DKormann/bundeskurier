

def get_key(file: str, key: str) -> str:
    with open(file, "r") as f:
        for line in f:
            if line.startswith(key):
                return line.split("=")[1].strip()
    return None
