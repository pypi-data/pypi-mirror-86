from catastro_finder import CatastroFinder

catastro = CatastroFinder()
provincias = catastro.get_provincias()
selected_provincia = provincias[30]
print(selected_provincia)
municipios = catastro.get_municipios(selected_provincia['Codigo'])
selected_municipio = municipios[68]
print(selected_municipio)
via_result = catastro.get_vias(selected_provincia['Codigo'],selected_municipio['Codigo'],"JACINTO")[0]
print(via_result)
via_numero = 2
inmueble_results = catastro.search_inmueble(via_result,via_numero,selected_provincia,selected_municipio)
print(inmueble_results[0])
     