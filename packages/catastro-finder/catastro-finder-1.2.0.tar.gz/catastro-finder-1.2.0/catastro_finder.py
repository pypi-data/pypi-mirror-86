import requests
import json
from bs4 import BeautifulSoup

class CatastroFinder:
    """CatastroFinder"""

    def __init__(self,catastro_dict_path=None):
        """

        Args:
            catastro_dict_path (str, optional): Json file with catastro urls to scrap. Defaults to "./catastro_artifacts.json".
        """
        if catastro_dict_path:
            with open(catastro_dict_path) as json_file:
                self.catastro_dict=json.load(json_file)
        else:
            self.catastro_dict={
                                "provincias": {
                                    "url": "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCBusqueda.aspx/ObtenerProvincias",
                                    "headers": {
                                    "authority": "www1.sedecatastro.gob.es",
                                    "accept": "application/json, text/javascript, */*; q=0.01",
                                    "x-requested-with": "XMLHttpRequest",
                                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                                    "content-type": "application/json; charset=UTF-8",
                                    "origin": "https://www1.sedecatastro.gob.es",
                                    "sec-fetch-site": "same-origin",
                                    "sec-fetch-mode": "cors",
                                    "sec-fetch-dest": "empty",
                                    "referer": "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCBusqueda.aspx?from=NuevoVisor",
                                    "accept-language": "es-ES,es;q=0.9"
                                    }
                                },
                                "municipios": {
                                    "url": "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCBusqueda.aspx/ObtenerMunicipios",
                                    "headers": {
                                    "authority": "www1.sedecatastro.gob.es",
                                    "accept": "application/json, text/javascript, */*; q=0.01",
                                    "x-requested-with": "XMLHttpRequest",
                                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                                    "content-type": "application/json; charset=UTF-8",
                                    "origin": "https://www1.sedecatastro.gob.es",
                                    "sec-fetch-site": "same-origin",
                                    "sec-fetch-mode": "cors",
                                    "sec-fetch-dest": "empty",
                                    "referer": "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCBusqueda.aspx?from=NuevoVisor",
                                    "accept-language": "es-ES,es;q=0.9"
                                    }
                                },
                                "vias": {
                                    "url": "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCBusqueda.aspx/ObtenerVias",
                                    "headers": {
                                    "authority": "www1.sedecatastro.gob.es",
                                    "accept": "application/json, text/javascript, */*; q=0.01",
                                    "x-requested-with": "XMLHttpRequest",
                                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                                    "content-type": "application/json; charset=UTF-8",
                                    "origin": "https://www1.sedecatastro.gob.es",
                                    "sec-fetch-site": "same-origin",
                                    "sec-fetch-mode": "cors",
                                    "sec-fetch-dest": "empty",
                                    "referer": "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCBusqueda.aspx?from=NuevoVisor",
                                    "accept-language": "es-ES,es;q=0.9"
                                    }
                                },
                                "inmuebles": {
                                    "url": "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCListaBienes.aspx",
                                    "headers": {
                                    "authority": "www1.sedecatastro.gob.es",
                                    "cache-control": "max-age=0",
                                    "upgrade-insecure-requests": "1",
                                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                                    "sec-fetch-site": "none",
                                    "sec-fetch-mode": "navigate",
                                    "sec-fetch-user": "?1",
                                    "sec-fetch-dest": "document",
                                    "accept-language": "es-ES,es;q=0.9"
                                    }
                                }
                                }


    def get_provincias(self,filtro=""):
        """get_provincias

        Args:
            filtro (str, optional): Filtro. Defaults to "".

        Returns:
            (list): List of items with Codigo and Denominacion. ['Codigo': 15, 'Denominacion': 'A CORUÑA'}...]

        """
        url=self.catastro_dict["provincias"]["url"]
        headers=self.catastro_dict["provincias"]["headers"]
        payload = "{ 'filtro': '"+filtro+"'}"
        response = requests.request("POST", url, headers=headers, data = payload)
        return json.loads(response.content)['d']

    def get_municipios(self,provincia):
        """get_municipios

        Args:
            provincia (str): Provincia code to search.

        Returns:
            (list): List of items with Codigo and Denominacion. ['Codigo': 121, 'Denominacion': 'SANTA POLA'}...]
        
        """
        url=self.catastro_dict["municipios"]["url"]
        headers=self.catastro_dict["municipios"]["headers"]
        payload = "{\"filtro\":\"\",\"provincia\":"+str(provincia)+"}"
        response = requests.request("POST", url, headers=headers, data = payload)
        return json.loads(response.content)['d']

    def get_vias(self,provincia,municipio,input_via):
        """get_vias

        Args:
            provincia (str): Provincia code to search.
            municipio (str): Municipio code to search.
            input_via (str): Via input to search.
         
        Returns:
            (list): List of items with Codigo, Sigla, TipoVia, DenominacionCompleta and Denominacion. {'Codigo': 1212, 'Sigla': 'CL', 'TipoVia': 'CALLE', 'Denominacion': 'SANTA CRISTINA', 'DenominacionCompleta': 'SANTA CRISTINA (CALLE)'}

        """
        url=self.catastro_dict["vias"]["url"]
        headers=self.catastro_dict["vias"]["headers"]
        payload = "{\"filtro\":\""+str(input_via)+"\",\"provincia\":"+str(provincia)+",\"municipio\":"+str(municipio)+"}"
        response = requests.request("POST", url, headers=headers, data = payload)
        return json.loads(response.content)['d']

    def search_inmueble(self,via_result,via_numero,selected_provincia,selected_municipio,tipur="U",pest="urbana"):
        """search inmueble

        Args:
            via_result (dict): [description]
            via_numero (str): [description]
            selected_provincia (dict): [description]
            selected_municipio ([dict): [description]
            tipur (str, optional): tipur. Defaults to "U".
            pest (str, optional): pest. Defaults to "urbana".

        Returns:
            (list): List of inmuebles
        """
        url=self.catastro_dict["inmuebles"]["url"]
        headers=self.catastro_dict["inmuebles"]["headers"]
        via = via_result['Denominacion'].replace(" ","@")
        params = (
            ('via', str(via)),
            ('tipoVia', str(via_result['Sigla'])),
            ('numero', str(via_numero)),
            ('kilometro', ''),
            ('bloque', ''),
            ('escalera', ''),
            ('planta', ''),
            ('puerta', ''),
            ('DescProv', str(selected_provincia['Denominacion'])),
            ('prov', str(selected_provincia['Codigo'])),
            ('muni', str(selected_municipio['Codigo'])),
            ('DescMuni', str(selected_municipio['Denominacion'])),
            ('TipUR', str(tipur)),
            ('codvia', str(via_result['Codigo'])),
            ('comVia', str(via_result['DenominacionCompleta'])),
            ('pest', str(pest)),
            ('from', 'OVCBusqueda'),
            ('nomusu', ' '),
            ('tipousu', ''),
            ('ZV', 'NO'),
            ('ZR', 'NO'),
        )

        response = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(response.content,features="html.parser")
        inmueble_results = soup.find_all("div", "panel-heading")
        cleaned_results = []
        for inmueble in inmueble_results:
            results_item = {}
            for element in inmueble.find_all("span"):
                if "title" in element.attrs:
                    if element.attrs["title"] == "Localización":
                        results_item["Localización"] = element.text
                    if element.attrs["title"] == "Año construcción":
                        results_item["Año construcción"] = element.text.replace(" ","")
                    if element.attrs["title"] == "Uso":
                        results_item["Uso"] = element.text
                    if element.attrs["title"] == "Coeficiente de participación":
                        results_item["Coeficiente de participación"] = element.text.replace(" ","")
                    if element.attrs["title"] == "Superficie construida":
                        results_item["Superficie construida"] = element.text.replace(" ","")
            if results_item:
                cleaned_results.append(results_item)
        return cleaned_results

