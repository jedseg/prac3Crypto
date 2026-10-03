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

# Parámetros oficiales de las curvas NIST (SP800-186)
CURVAS_NIST = {
    "P-224": {
        "p": 26959946667150639794667015087019630673557916260026308143510066298881,
        "a": 26959946667150639794667015087019630673557916260026308143510066298878,
        "b": 18958286285566608000408668544493926415504680968679321075787234672564,
        "n": 26959946667150639794667015087019625940457807714424391721682722368061,
        "Gx": 19277929113566293071110308034699488026831934219452440156649784352033,
        "Gy": 19926808758034470970197974370888749184205991990603949537637343198772
    },
    "P-256": {
        "p": 115792089210356248762697446949407573530086143415290314195533631308867097853951,
        "a": 115792089210356248762697446949407573530086143415290314195533631308867097853948, 
        "b": 41058363725152142129326129780047268409114441015993725554835256314039467401291,
        "n": 115792089210356248762697446949407573529996955224135760342422259061068512044369,
        "Gx": 48439561293906451759052585252797914202762949526041747995844080717082404635286,
        "Gy": 36134250956749795798585127919587881956611106672985015071877198253568414405109
    },
    "P-384": {
        "p": 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319,
        "a": 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112316,
        "b": 27580193559959705877849011840389048093056905856361568521428707301988689241309860865136260764883745107765439761230575,
        "n": 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643,
        "Gx": 26247035095799689268623156744566981891852923491109213387815615900925518854738050089022388053975719786650872476732087,
        "Gy": 8325710961489029985546751289520108179287853048861315594709205902480503199884419224438643760392947333078086511627871
    },
    "P-521": {
        "p": 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151,
        "a": 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057148,
        "b": 1093849038073734274511112390766805569936207598951683748994586394495953116150735016013708737573759623248592132296706313309438452531591012912142327488478985984,
        "n": 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449,
        "Gx": 2661740802050217063228768716723360960729859168756973147706671368418802944996427808491545080627771902352094241225065558662157113545570916814161637315895999846,
        "Gy": 3757180025770020463545507224491183603594455134769762486694567779615544477440556316691234405012945539562144444537289428522585666729196580810124344277578376784
    }
}


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


def int_a_base64(valor):
    longitud = (valor.bit_length() + 7) // 8
    longitud = max(1, longitud) 
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
    G = (Gx, Gy, 1)
    Bx = base64_a_int(lineas[6].strip())
    By = base64_a_int(lineas[7].strip())
    B = (Bx, By, 1)
    
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

# Función 4:
def ecdh():
    print("\nSelección de Curva NIST para ECDH")
    print("1) P-224")
    print("2) P-256")
    print("3) P-384")
    print("4) P-521")
    
    opc_curva = input("Elige una opción de curva (1-4): ")
    
    mapa_curvas = {"1": "P-224", "2": "P-256", "3": "P-384", "4": "P-521"}
    
    if opc_curva not in mapa_curvas:
        print("Opción inválida.")
        return
        
    nombre_curva = mapa_curvas[opc_curva]
    c = CURVAS_NIST[nombre_curva]
    
    p_c = c["p"]
    a_c = c["a"]
    b_c = c["b"]
    n_c = c["n"]
    G_c = (c["Gx"], c["Gy"], 1)
    
    print(f"\nCurva seleccionada: {nombre_curva}")
    
    priv_a = random.randint(1, n_c - 1)
    priv_b = random.randint(1, n_c - 1)
    
    A = LR(a_c, b_c, p_c, priv_a, G_c)
    B = LR(a_c, b_c, p_c, priv_b, G_c)
    
    archivo_pub_alice = "alice_pub.txt"
    archivo_pub_bob = "bob_pub.txt"
    
    #Guardar en base64 en archivos de texto
    with open(archivo_pub_alice, "w") as f:
        f.write(int_a_base64(A[0]) + "\n")
        f.write(int_a_base64(A[1]) + "\n")
        
    with open(archivo_pub_bob, "w") as f:
        f.write(int_a_base64(B[0]) + "\n")
        f.write(int_a_base64(B[1]) + "\n")
        
    print(f"Valores públicos aG y bG guardados en '{archivo_pub_alice}' y '{archivo_pub_bob}'")
    #LADO DE ALICE

    with open(archivo_pub_bob, "r") as f:
        lineas_bob = f.readlines()
    Bx_leido = base64_a_int(lineas_bob[0].strip())
    By_leido = base64_a_int(lineas_bob[1].strip())
    B_leido = (Bx_leido, By_leido, 1)
    
    K_alice = LR(a_c, b_c, p_c, priv_a, B_leido)

    #LADO DE BOB
    with open(archivo_pub_alice, "r") as f:
        lineas_alice = f.readlines()
    Ax_leido = base64_a_int(lineas_alice[0].strip())
    Ay_leido = base64_a_int(lineas_alice[1].strip())
    A_leido = (Ax_leido, Ay_leido, 1)
    
    K_bob = LR(a_c, b_c, p_c, priv_b, A_leido)

    #Verificación de K
    if K_alice[0] == K_bob[0] and K_alice[1] == K_bob[1]:
        print("\nK coincide en ambos extremos.")
    else:
        print("\nLos secretos compartidos no coinciden.")
        return

    #Derivacion
    K_x = K_alice[0]
    K_y = K_alice[1]

    longitud_bytes = (p_c.bit_length() + 7) // 8
    
    bytes_x = K_x.to_bytes(longitud_bytes, byteorder='big')
    bytes_y = K_y.to_bytes(longitud_bytes, byteorder='big')
    K_punto_bytes = bytes_x + bytes_y
    
    K_base64 = base64.b64encode(K_punto_bytes).decode('ascii')
    print(f"Secreto compartido K en base64: {K_base64}")

    hash_kdf = hashlib.sha256(K_punto_bytes).digest()
    k_base64 = base64.b64encode(hash_kdf).decode('ascii')
    
    print(f"Llave derivada k (256 bits) en base64: {k_base64}")
    
    return K_base64, k_base64
                

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
        print("1) Generar llaves\n2) Generar firma\n3) Verificar firma\n4) ECDH")
        opc = int(input("Elige una opción: "))
        if opc == 1:
            print("\n--- Generación de llaves ---")
            archivo_priv = input("Nombre del archivo para la llave privada: ")
            archivo_pub = input("Nombre del archivo para la llave pública: ")

            d, keyPub = keyGeneration(p, a, b, n, G, archivo_priv, archivo_pub)
            break

        elif opc == 2:
            print("\n--- Generación de firma ---")
            archivo_priv = input("Nombre del archivo de la llave privada: ")
            archivo_mensaje = input("Nombre del archivo a firmar: ")
            
            mensaje = input("Escribe el mensaje que deseas firmar: ")
            with open(archivo_mensaje, "w") as f:
                f.write(mensaje)

            archivo_firma = input("Nombre del archivo para guardar la firma: ")
            r, s = signatureGeneration(archivo_priv, archivo_mensaje, archivo_firma)
            print(f"r, s = {r}, {s}")
            break

        elif opc == 3:
            print("\n--- Verificación de firma ---")
            archivo_pub = input("Nombre del archivo de la llave pública: ") # LÍNEA AÑADIDA
            archivo_mensaje = input("Nombre del archivo a verificar: ") # LÍNEA AÑADIDA
            archivo_firma = input("Nombre del archivo de la firma: ") # LÍNEA AÑADIDA
            print(signatureVerification(archivo_pub, archivo_mensaje, archivo_firma))
            break

        elif opc == 4:
            ecdh()
            break 

        else:
            print("Opción no válida. Intente de nuevo.")