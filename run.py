# Importamos la funcion create_app, 'una instancia'
from todor import create_app

# A traves de la condicion podemos ejecutar el codigo
app=create_app()
if __name__ == "__main__":
    
    app.run()
