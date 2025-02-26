from parser import Parser, save_products_to_json  # Importamos la clase Parser

if __name__ == "__main__":
    parser = Parser()  # Inicializamos la clase Parser

    # Obtener productos en oferta desde la API
    products_on_sale = parser.fetch_products_on_sale()

    # Guarda en formato json los productos
    save_products_to_json(products_on_sale)
    print("Productos guardados")
