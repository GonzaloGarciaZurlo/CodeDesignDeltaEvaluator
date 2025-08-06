import subprocess
import json
from collections import defaultdict

# Lista de PRs
pr_numbers = [6922, 6921, 6920, 6919, 6918, 6917, 6916, 6915, 6914, 6913]

# Inicializar estructura
all_metrics = {
    "global": defaultdict(list),
    "per-class": defaultdict(list),
    "per-package": defaultdict(list)
}

for pr in pr_numbers:
    print(f"Procesando PR #{pr}...")

    # Ejecutar el comando
    subprocess.run([
        "cdde",
        "https://github.com/cortexproject/cortex",
        str(pr),
        "src/queries/cypher.yml",
        "src/queries/derived_metrics.yml",
        "--lang", "go"
    ])

    # Leer resultados
    with open("results.json") as f:
        data = json.load(f)

    # --- GLOBAL ---
    global_metrics = data.get("global", {})
    for metric, value in global_metrics.items():
        all_metrics["global"][metric].append(value)

    # --- PER-CLASS ---
    for key, value in data.get("per-class", {}).items():
        all_metrics["per-class"][key].append(value)

    # --- PER-PACKAGE ---
    for key, value in data.get("per-package", {}).items():
        all_metrics["per-package"][key].append(value)


# Rellenar con None si faltaron claves en alguna PR
num_prs = len(pr_numbers)
for section in ["per-class", "per-package"]:
    for key, values in all_metrics[section].items():
        while len(values) < num_prs:
            values.append(None)

# Guardar el archivo final
with open("cortex_results.json", "w") as f:
    json.dump(all_metrics, f, indent=4)
