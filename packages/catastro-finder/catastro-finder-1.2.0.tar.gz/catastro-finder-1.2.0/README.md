# Catastro Finder

Unofficial Catastro Finder. No API keys required

---

## Installation

```bash
pip install catastro-finder
```

## Usage

```bash
from catastro_finder import CatastroFinder
catastro = CatastroFinder()
```

### Get provinces

```bash
provincias = catastro.get_provincias()
# Select one
selected_provincia = provincias[30]
```

### Get municipalities

```bash
municipios = catastro.get_municipios(selected_provincia['Codigo'])
# Select one
selected_municipio = municipios[68]
```

### Get streets candidates

```bash
via_result = catastro.get_vias(selected_provincia['Codigo'],selected_municipio['Codigo'],"JACINTO")[0]
```

### Search a property

```bash
# Choose property number
via_numero = 2
inmueble_results = catastro.search_inmueble(via_result,via_numero,selected_provincia,selected_municipio)
```
