
# Hecho por Alexis Pozos González
# Grupo 7CV1

# Programa: ECDH

from P1 import point_addition, point_doubling

# Función 1: Derecha a Izquierda (Right to Left, RL)
def RL(a, b, p, k, P):
    Q = (0, 1, 0)  # punto al infinito 
    bits = bin(k)[2:][::-1]  # binario de k que lo voltea para procesarlo de derecha a izquierda
    for ki in bits:
        if ki == '1':
            Q = point_addition(a, b, p, Q, P)
        P = point_doubling(a, b, p, P)
    return Q


# Función 2: Izquierda a Derecha (Left to Right, LR)
def LR(a, b, p, k, P):
    Q = (0, 1, 0)  # punto al infinito
    bits = bin(k)[2:]  # binario de k en orden normal
    for ki in bits:
        Q = point_doubling(a, b, p, Q) # construye la escalera de potencias de 2
        if ki == '1':
            Q = point_addition(a, b, p, Q, P) # ecide, bit por bit, cuáles de esas potencias realmente se incluyen en el resultado final
    return Q


if __name__ == "__main__":
    while True:
        print("\n--- Menú ---")
        print("1. Probar RL (Right to Left)")
        print("2. Probar LR (Left to Right)")
        print("3. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1" or opcion == "2":
            a = int(input("a: "))
            b = int(input("b: "))
            p = int(input("p: "))
            x = int(input("x de P: ")); y = int(input("y de P: ")); z = int(input("z de P: "))
            k = int(input("k: "))
            P = (x, y, z)

            if opcion == "1":
                resultado = RL(a, b, p, k, P)
            else:
                resultado = LR(a, b, p, k, P)

            print(f"{k}P = {resultado}")

        elif opcion == "3":
            print("Saliendo")
            break

        else:
            print("Opción inválida, intenta de nuevo.")