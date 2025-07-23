import pandas as pd
import yaml


N_pubs = 10
df = pd.read_json('data/pubs.json').iloc[:N_pubs]

# Load existing YAML config file
with open("config_template.yaml", "r") as f:
    config = yaml.safe_load(f)

# Build highlighted_pubs dictionary from DataFrame
highlighted_pubs = {
    i + 1: {
        "title": row["Title"],
        "year": int(row["Year"]),
        "journal": row["Journal"],
        "link": f"https://doi.org/{row['DOI']}",
    }
    for i, row in df.iterrows()
}

# Replace highlighted_pubs section
config["params"]["highlighted_pubs"] = highlighted_pubs

# Save updated YAML to a new file
with open("config.yaml", "w") as f:
    yaml.dump(config, f, sort_keys=False, allow_unicode=True, default_flow_style=False)
