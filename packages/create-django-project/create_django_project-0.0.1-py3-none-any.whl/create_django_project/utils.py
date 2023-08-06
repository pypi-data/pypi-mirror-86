from pathlib import Path
import re


def read_secret_key(settings_file: Path):
    settings = settings_file.read_text()
    pattern = re.compile(r"secret_key", re.IGNORECASE)
    results = [line for line in settings.rsplit('\n') if pattern.findall(line)]
    secret_key = results[0].split(' = ')[1]
    return secret_key
