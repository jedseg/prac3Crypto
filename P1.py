
# cat "/Users/alex/Documents/ESCOM/Semestre 8/Cripto2/ec_p_a_b.txt"

# Hecho por Alexis Pozos González

from sympy import randprime
import random

# ----------- SECTIOM 1 ----------- 

# Funciones premilinares s

# FUNCION 1

def quadratic_residues(p):
    qr_dict = {}
    for x in range (0 , p):
        r = (x*x) % p

        if r not in qr_dict:
            qr_dict[r] = [x]
            if x != 0:
                qr_dict[r].append(-x % p)
        else:
            break
        
    print ("QR mod p:")
    for r in qr_dict:
        print (f"{r}: {qr_dict[r]}")

    return qr_dict

# FUNCION 2

def elliptic_curve_points(p, a, b):

    qr_dict = quadratic_residues(p)
    points = []
    points.append((0, 1, 0))

    for x in range(0, p):
        fx=(x**3 + a*x + b) % p
        if fx in qr_dict:
            for y in qr_dict[fx]:
                points.append((x, y, 1))

    with open(f"/Users/alex/Documents/ESCOM/Semestre 8/Cripto2/ec_{p}_{a}_{b}.txt", "w") as f:
        f.write(f"p = {p}\n")
        f.write(f"a = {a}\n")
        f.write(f"b = {b}\n")
        f.write("Points:\n")
        for point in points:
            f.write(f"{point}\n")

    print(f"Número de puntos racionales: {len(points)}")

    return points


# ----------- SECTIOM 2 ----------- 

# Funcion 1

def generate_curve(n):
    p = randprime(2**(n-1), 2**n)

    while True:
        a = random.randint(0, p-1)
        b = random.randint(0, p-1)
        if (4*a**3 + 27*b**2) % p != 0:
            break

    print(f"Curva generada: p={p}, a={a}, b={b}")
    return p, a, b

# Funcion 2

def is_on_curve(a, b, p, P):
    x, y, z = P
    if z == 0:
        return True  # punto al infinito
    return (y*y) % p == (x**3 + a*x + b) % p

def point_addition(a, b, p, P, Q):
    if not is_on_curve(a, b, p, P) or not is_on_curve(a, b, p, Q):
        print("Error: P o Q no pertenecen a la curva")
        return None
    x1, y1, z1 = P
    x2, y2, z2 = Q
    if z1 == 0:
        return Q
    if z2 == 0:
        return P
    if x1 == x2 and (y1 + y2) % p == 0:
        return (0, 1, 0)
    if x1 == x2 and y1 == y2:          # <-- NUEVO: P y Q son el mismo punto
        return point_doubling(a, b, p, P)
    lam = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
    x3 = (lam*lam - x1 - x2) % p
    y3 = (lam*(x1 - x3) - y1) % p
    return (x3, y3, 1)

# Funcion 3

def point_doubling(a, b, p, P):
    if not is_on_curve(a, b, p, P):
        print("Error: P no pertenece a la curva")
        return None

    x1, y1, z1 = P

    if z1 == 0:
        return (0, 1, 0)  # 2·infinito = infinito

    if y1 == 0:
        return (0, 1, 0)  # tangente vertical -> resultado es infinito

    lam = ((3*x1*x1 + a) * pow(2*y1, -1, p)) % p
    x3 = (lam*lam - 2*x1) % p
    y3 = (lam*(x1 - x3) - y1) % p

    return (x3, y3, 1)




# ----------- MENU ----------- 


if __name__ == "__main__":
    while True:
        print("\n--- Menú ---")
        print("1. Probar quadratic_residues")
        print("2. Probar elliptic_curve_points")
        print("3. Probar generate_curve")
        print("4. Probar point_addition")
        print("5. Probar point_doubling")
        print("6. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            p = int(input("Ingresa un número primo p > 3: "))
            quadratic_residues(p)

        elif opcion == "2":
            p = int(input("Ingresa un número primo p > 3: "))
            a = int(input("Ingresa el valor de a: "))
            b = int(input("Ingresa el valor de b: "))
            elliptic_curve_points(p, a, b)

        elif opcion == "3":
            n = int(input("Ingresa el número de bits n: "))
            generate_curve(n)

        elif opcion == "4":
            a = int(input("a: "))
            b = int(input("b: "))
            p = int(input("p: "))
            x1 = int(input("x1: ")); y1 = int(input("y1: ")); z1 = int(input("z1: "))
            x2 = int(input("x2: ")); y2 = int(input("y2: ")); z2 = int(input("z2: "))
            resultado = point_addition(a, b, p, (x1, y1, z1), (x2, y2, z2))
            print(f"P + Q = {resultado}")

        elif opcion == "5":
            a = int(input("a: "))
            b = int(input("b: "))
            p = int(input("p: "))
            x1 = int(input("x1: ")); y1 = int(input("y1: ")); z1 = int(input("z1: "))
            resultado = point_doubling(a, b, p, (x1, y1, z1))
            print(f"2P = {resultado}")

        elif opcion == "6":
            print("Saliendo")
            break

        else:
            print("Opción inválida, intenta de nuevo")



    