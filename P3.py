
# Hecho por Alexis Pozos González
# Grupo 7CV1

# Este programa implementa el algoritmo ECDSA (Elliptic Curve Digital Signature Algorithm) 
# para la generación de claves y la firma de mensajes utilizando curvas elípticas.

# ECDSA

# Key generation FOR ECDSA
from P1 import point_addition
from P2 import LR
import random

# Función 1 - Key Generation

def keyGeneration(p, a, b, q, G):
    d = random.randint (1, q-1)
    B = LR (a, b, p, d, G)

    keyPub = (p, a, b, q, G, B)

    return d, keyPub

# Función 2 - Signature Generation

def signatureGeneration(a, b, p, d, G, q, m):   

    kE= random.randint(1, q-1)
    R = LR (a, b, p, kE,G)
    r = R[0] % q
    s = (m + d*r) * pow(kE, -1, q) % q

    return r, s

# Función 3 - Verification

def verification (p, a, b, q, G, B, m, r, s):
    w = pow (s, -1, q)
    u1 = (w*m) % q 
    u2 = (w*r) % q 
    P = point_addition(a, b, p, LR(a, b, p, u1, G), LR(a, b, p, u2, B))

    if P[2] == 0:
        return False

    xp = P[0] % q

    if xp == r % q:
        return True
    else:
        return False


if __name__ == "__main__":
    p = int(input("p: "))
    a = int(input("a: "))
    b = int(input("b: "))
    q = int(input("q: "))
    x = int(input("x de G: "))
    y = int(input("y de G: "))
    z = int(input("z de G: "))
    G = (x, y, z)

    # 1. Generación de llaves
    d, keyPub = keyGeneration(p, a, b, q, G)
    print(f"key Private = {d}")
    print(f"key Public = {keyPub}")

    # 2. Generación de la firma
    m = int(input("Mensaje m a firmar (0 < m < q): "))
    r, s = signatureGeneration(a, b, p, d, G, q, m)
    print(f"Firma (r, s) = ({r}, {s})")

    # 3. Verificación de la firma
    p, a, b, q, G, B = keyPub
    if verification(p, a, b, q, G, B, m, r, s):
        print("La firma es válida")
    else:
        print("La firma NO es válida")
