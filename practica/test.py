# Importar las funciones de los módulos
from mi_paquete.modulo1 import funcion_modulo1
from mi_paquete.modulo2 import funcion_modulo2

def main():
    # Probar la función del módulo 1
    print("Probando funcion_modulo1:")
    funcion_modulo1()
    
    # Probar la función del módulo 2
    print("Probando funcion_modulo2:")
    funcion_modulo2()

if __name__ == "__main__":
    main() 