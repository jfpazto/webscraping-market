from parser import Parser  # Importamos la clase Parser

if __name__ == "__main__":
    parser = Parser()  # Inicializamos la clase Parser

    # Obtener productos en oferta desde la API
    products_on_sale = parser.fetch_products_on_sale()

    # Imprimir los primeros 5 productos en oferta
    for product in products_on_sale[:5]:
        print(product)
