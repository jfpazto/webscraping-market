import requests
import json
import os
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
        Realiza solicitudes a la API de Makro para obtener todos los productos en oferta paginados.

        :return: Lista completa de productos en oferta.
        """
        all_products = []
        current_page = 1
        total_pages = 1  # Inicialmente asumimos 1, pero lo actualizaremos

        while current_page <= total_pages:
            print(f"🔄 Obteniendo página {current_page} de {total_pages}...")

            payload = json.dumps([
                {
                    "operationName": "GetProductsByCategory",
                    "variables": {
                        "getProductsByCategoryInput": {
                            "categoryReference": "CT_01_18",
                            "clientId": "MAKRO",
                            "storeReference": "08ABO",
                            "currentPage": current_page,
                            "pageSize": 100  # Se puede ajustar según la API
                        }
                    },
                    "query": """query GetProductsByCategory($getProductsByCategoryInput: GetProductsByCategoryInput!) {
                        getProductsByCategory(getProductsByCategoryInput: $getProductsByCategoryInput) {
                            category {
                                products {
                                    name
                                    price
                                    promotion {
                                        conditions {
                                            price
                                            priceBeforeTaxes
                                        }
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
                            pagination {
                                page
                                pages
                                total {
                                    value
                                }
                            }
                        }
                    }"""
                }
            ])

            try:
                response = requests.post(self.api_url, headers=self.headers, data=payload)

                if response.status_code == 200:
                    data = response.json()

                    # Extraer los productos de la respuesta
                    products = self.extract_products_from_api(data)
                    all_products.extend(products)  # Agregar productos a la lista completa

                    # Actualizar la cantidad total de páginas
                    pagination_info = data[0].get("data", {}).get("getProductsByCategory", {}).get("pagination", {})
                    total_pages = pagination_info.get("pages", 1)  # Actualizar total de páginas

                    # Avanzar a la siguiente página
                    current_page += 1
                else:
                    print(f"❌ Error en la solicitud: {response.status_code}")
                    break  # Detener en caso de error
            except Exception as e:
                print(f"❌ Error al realizar la petición: {e}")
                break  # Detener en caso de error crítico

        print(f"✅ Se obtuvieron {len(all_products)} productos en total.")
        return all_products


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
                valida_promocion=True
                promotion = product.get("promotion")
                if promotion is None:
                    promotion = "Sin promocion"
                    valida_promocion=False
                else:
                    valida_promocion=True
                #start_date = product.get("promotion", {}).get("startDateTime", "Fecha no disponible")
                #end_date = product.get("promotion", {}).get("endDateTime", "Fecha no disponible")
                image = product.get("photosUrl", "Sin imagen")
                stock = product.get("stock", "Desconocido")
                available = product.get("isAvailable", False)
                brand = product.get("brand", "Sin marca")


                products.append({
                    "name": name,
                    "price": price,
                    "promotion":valida_promocion,
                    "promotion_detail": promotion,
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

def save_products_to_json(products, filename="outputs/products.json"):
    """
    Guarda la lista de productos en un archivo JSON.

    :param products: Lista de productos obtenida de la API.
    :param filename: Ruta del archivo donde se guardarán los datos.
    """
    try:
        # Asegurar que la carpeta 'outputs' exista
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Guardar los datos en formato JSON
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(products, file, indent=4, ensure_ascii=False)

        print(f"✅ Datos guardados correctamente en {filename}")

    except Exception as e:
        print(f"❌ Error al guardar el archivo JSON: {e}")
