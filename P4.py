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
        "p": 269599466671506397946670150870196306735579162600263086435106239900559,
        "a": 269599466671506397946670150870196306735579162600263086435106239900556,
        "b": 18905828627574206439453239380926721920426770159525997098793319985955,
        "n": 269599466671506397946670150870196306735579162600263086435106199996533,
        "Gx": 1948587475159388770836501807316187916312802219482073199874410885141,
        "Gy": 26617761266100310619420063234914285101297961042831552572115160699059
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
        "p": 39402006196394479212279040100143613805079739270465446667948293404245721771496870329046946958996537856025074511374650,
        "a": 39402006196394479212279040100143613805079739270465446667948293404245721771496870329046946958996537856025074511374647,
        "b": 27580193559995963468354469439372816930391941002931448510899329705299331006536554629168449912061139414555815615707736,
        "n": 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398056303588235075420255059474287,
        "Gx": 29124239461559247653373514051933924151747794326105430154865768564177524021285496464670267441221374465942735749329243,
        "Gy": 35305141091599865181747372225380579979737194600216515228511749667794270216573887469324545564883441589178970477146593
    },
    "P-521": {
        "p": 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151,
        "a": 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057148,
        "b": 1095955363900417251474963125215037989396347393433602556512683935293678079080536761502120050849767856691685827666285093707831034337223689408018903823439063546,
        "n": 6864797660130609714981900799081393217269435300143305409394463459185543183397655463960538969877150502844113099033575932064119934149247778953495861198595914619,
        "Gx": 2684545455246726210344465435987179069507985395639149020464977284144368564023602058693888568019020473843513681655659850125866160139162953258525049964516007421,
        "Gy": 3614055649067524785499252014790044810656093414845578759530472403598466107384589255866115933614760234771746613303649089531853406263592866946077303036836709848
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
        print("[Error] Opción inválida.")
        return
        
    nombre_curva = mapa_curvas[opc_curva]
    c = CURVAS_NIST[nombre_curva]
    
    p_c = c["p"]
    a_c = c["a"]
    b_c = c["b"]
    n_c = c["n"]
    G_c = (c["Gx"], c["Gy"])
    
    print(f"\n[+] Curva seleccionada: {nombre_curva}")
    
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
    B_leido = (Bx_leido, By_leido)
    
    K_alice = LR(a_c, b_c, p_c, priv_a, B_leido)

    #LADO DE BOB
    with open(archivo_pub_alice, "r") as f:
        lineas_alice = f.readlines()
    Ax_leido = base64_a_int(lineas_alice[0].strip())
    Ay_leido = base64_a_int(lineas_alice[1].strip())
    A_leido = (Ax_leido, Ay_leido)
    
    K_bob = LR(a_c, b_c, p_c, priv_b, A_leido)

    #Verificación de K
    if K_alice[0] == K_bob[0] and K_alice[1] == K_bob[1]:
        print("\n[K coincide en ambos extremos.")
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
    
    print(f"[*] Llave derivada k (256 bits) en base64: {k_base64}")
    
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
            print(signatureVerification(archivo_pub, archivo_mensaje, archivo_firma))

        elif opc == 4:
            ecdh()

        else:
            print("Opción no válida. Intente de nuevo.")