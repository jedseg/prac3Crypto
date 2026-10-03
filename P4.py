import base64
import random
import hashlib

from P1 import point_addition, point_doubling
from P2 import LR

# Parámetros de la curva NIST P-256
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = p - 3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
Gx = 48439561293906451759052585252797914202762949526041747995844080717082404635286
Gy = 36134250956749795798585127919587881956611106672985015071877198253568414405109
G = (Gx, Gy, 1)


# Función 2: Generación de firma
def signatureGeneration(archivo_priv, archivo_mensaje, archivo_firma):
    with open(archivo_priv) as f:
        d = base64_a_int(f.read().strip())

    with open(archivo_mensaje, "rb") as f:
        contenido = f.read()
    hash_bytes = hashlib.sha256(contenido).digest()
    m = int.from_bytes(hash_bytes, byteorder='big') % n

    kE = random.randint(1, n - 1)
    R = LR(a, b, p, kE, G)
    r = R[0] % n
    s = (m + d * r) * pow(kE, -1, n) % n

    with open(archivo_firma, "w") as f:
        f.write(int_a_base64(r) + "\n")
        f.write(int_a_base64(s) + "\n")

    print(f"Firma guardada en: {archivo_firma}")
    return r, s


def int_a_base64(valor, longitud=32):
    datos_binarios = valor.to_bytes(longitud, byteorder='big')
    return base64.b64encode(datos_binarios).decode('ascii')

def base64_a_int(s):
    datos_binarios = base64.b64decode(s)
    return int.from_bytes(datos_binarios, byteorder='big')

# Función 3: Veriricación de firma
def signatureVerification(archivo_pub, archivo_mensaje, archivo_firma):
    with open(archivo_pub, "r") as f:
        lineas = f.readlines()
    p = base64_a_int(lineas[0].strip())
    a = base64_a_int(lineas[1].strip())
    b = base64_a_int(lineas[2].strip())
    n = base64_a_int(lineas[3].strip())
    Gx = base64_a_int(lineas[4].strip())
    Gy = base64_a_int(lineas[5].strip())
    G = (Gx, Gy)
    Bx = base64_a_int(lineas[6].strip())
    By = base64_a_int(lineas[7].strip())
    B = (Bx, By)
    
    with open(archivo_firma, "r") as f:
        lineas = f.readlines()
    r = base64_a_int(lineas[0].strip())
    s = base64_a_int(lineas[1].strip())

    with open(archivo_mensaje, "rb") as f:
        contenido = f.read()
    hash_bytes = hashlib.sha256(contenido).digest()
    m = int.from_bytes(hash_bytes, byteorder='big') % n

    w = pow(s, -1, n) % n
    u1 = w * m % n
    u2 = w * r % n
    P = point_addition(a, b, p, LR(a, b, p, u1, G), LR(a, b, p, u2, B))
    Px = P[0]

    return Px == (r % n)


# Función 1: Generación de llaves
def keyGeneration(p, a, b, n, G, archivo_priv, archivo_pub):
    d = random.randint(1, n - 1)
    B = LR(a, b, p, d, G)

    with open(archivo_priv, "w") as f:
        f.write(int_a_base64(d) + "\n")

    valores_pub = [p, a, b, n, G[0], G[1], B[0], B[1]]
    with open(archivo_pub, "w") as f:
        for valor in valores_pub:
            f.write(int_a_base64(valor) + "\n")

    print(f"Llave privada guardada en: {archivo_priv}")
    print(f"Llave pública guardada en: {archivo_pub}")
    return d, (p, a, b, n, G, B)


# Menú

if __name__ == "__main__":
    archivo_firma = ""
    archivo_mensaje = ""
    archivo_pub = ""
    archivo_priv = ""

    while True:
        print("1) Generar llaves\n2) Generar firma\n3) Verificar firma")
        opc = int(input("Elige una opción: "))
        if opc == 1:
            print("\n--- Generación de llaves ---")
            archivo_priv = input("Nombre del archivo para la llave privada: ")
            archivo_pub = input("Nombre del archivo para la llave pública: ")

            d, keyPub = keyGeneration(p, a, b, n, G, archivo_priv, archivo_pub)
            break

        elif opc == 2:
            print("\n--- Generación de firma ---")
            archivo_mensaje = input("Nombre del archivo a firmar: ")
            archivo_firma = input("Nombre del archivo para guardar la firma: ")
            r, s = signatureGeneration(archivo_priv, archivo_mensaje, archivo_firma)
            print(f"r, s = {r}, {s}")
            break

        elif opc == 3:
            print("\n--- Verificación de firma ---")
            print(signatureGeneration(archivo_pub, archivo_mensaje, archivo_firma))
            