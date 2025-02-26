import requests
import json

class Parser:
    """Clase encargada de analizar el HTML o extraer datos de la API."""

    def __init__(self):
        """
        Constructor de la clase Parser.
        No requiere HTML ya que ahora también manejamos la API directamente.
        """
        self.api_url = "https://nextgentheadless.instaleap.io/api/v3"  # URL de la API
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
            "Accept": "*/*",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "https://tienda.makro.com.co/",
            "Content-Type": "application/json",
            "Apollographql-Client-Name": "Ecommerce",
            "Apollographql-Client-Version": "3.57.109",
            "Dpl-Api-Key": "",  # Agregar clave si es necesaria
        }

    def fetch_products_on_sale(self):
        """
        Realiza una solicitud a la API de Makro para obtener productos en oferta.
        
        :return: Lista de productos en oferta.
        """
        # Payload de la solicitud
        payload = json.dumps([
            {
                "operationName": "GetProductsByCategory",
                "variables": {
                    "getProductsByCategoryInput": {
                        "categoryReference": "CT_01_18",
                        "categoryId": "null",
                        "clientId": "MAKRO",
                        "storeReference": "08ABO",
                        "currentPage": 1,
                        "pageSize": 100,
                        "filters": {},
                        "googleAnalyticsSessionId": ""
                    }
                },
                "query": """query GetProductsByCategory($getProductsByCategoryInput: GetProductsByCategoryInput!) {
                    getProductsByCategory(getProductsByCategoryInput: $getProductsByCategoryInput) {
                        category {
                            products {
                                name
                                price
                                promotion {
                                    description
                                    endDateTime
                                    startDateTime
                                }
                                photosUrl
                                stock
                                isAvailable
                                brand
                            }
                        }
                    }
                }"""
            }
        ])

        try:
            # Realizar la petición POST
            response = requests.post(self.api_url, headers=self.headers, data=payload)
            # Validar si la respuesta es correcta
            if response.status_code == 200:
                data = response.json()  # Convertir a JSON
                return self.extract_products_from_api(data)
            else:
                print(f"Error en la solicitud: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error al realizar la petición: {e}")
            return []

    def extract_products_from_api(self, data):
        """
        Extrae los productos de la respuesta de la API.

        :param data: Respuesta JSON de la API.
        :return: Lista de productos con nombre, precio y promociones.
        """
        products = []
        try:
            # Validar si la API devolvió una lista y contiene datos
            if not data or not isinstance(data, list) or len(data) == 0:
                print("⚠️ La API devolvió un formato inesperado (no es una lista válida).")
                return []

            # Acceder al primer elemento de la lista
            api_response = data[0]  # 📌 Acceder directamente al diccionario dentro de la lista

            # Extraer la estructura correcta
            category_data = api_response.get("data", {}).get("getProductsByCategory", {}).get("category", {})

            if not category_data or "products" not in category_data:
                print("⚠️ No se encontraron productos en la respuesta de la API.")
                return []

            # Extraer productos
            for product in category_data["products"]:
                name = product.get("name", "Sin nombre")
                price = product.get("price", "Precio no disponible")
                #promotion = product.get("promotion", {}).get("description", "Sin promoción")
                #start_date = product.get("promotion", {}).get("startDateTime", "Fecha no disponible")
                #end_date = product.get("promotion", {}).get("endDateTime", "Fecha no disponible")
                image = product.get("photosUrl", "Sin imagen")
                stock = product.get("stock", "Desconocido")
                available = product.get("isAvailable", False)
                brand = product.get("brand", "Sin marca")

                products.append({
                    "name": name,
                    "price": price,
                    #"promotion": promotion,
                    #"start_date": start_date,
                    #"end_date": end_date,
                    "image": image,
                    "stock": stock,
                    "available": available,
                    "brand": brand
                })
        except Exception as e:
            print(f"❌ Error al extraer productos: {e}")

        return products


