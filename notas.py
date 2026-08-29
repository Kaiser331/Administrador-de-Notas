import json
import os
from datetime import datetime

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_NOTAS = os.path.join(DIRECTORIO_BASE, "notas.json")
ARCHIVO_CONFIG = os.path.join(DIRECTORIO_BASE, "config.json")

LINEA = "─" * 42

CONTRASENA = "1234"
MAX_INTENTOS = 3

LOGO = r"""
   .-------------------.
  /   N O T A S         \
 |-----------------------|
 |  ___________________  |
 |  ___________________  |
 |  ___________________  |
 |  _______________      |
 |                        |
  \_______________________/
"""


def confirmar(pregunta):
    respuesta = input(pregunta).strip().lower()
    return respuesta in ("y", "yes", "s", "si", "sí")


def cargar_configuracion():
    if not os.path.exists(ARCHIVO_CONFIG):
        return {"usar_contrasena": True}
    try:
        with open(ARCHIVO_CONFIG, mode="r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"usar_contrasena": True}


def guardar_configuracion(config):
    with open(ARCHIVO_CONFIG, mode="w", encoding="utf-8") as archivo:
        json.dump(config, archivo, indent=4, ensure_ascii=False)


def obtener_contrasena(config):
    return config.get("contrasena", CONTRASENA)


def cambiar_configuracion_contrasena(config):
    print(f"\n{LINEA}\nConfiguración\n{LINEA}")
    estado_actual = "activada" if config.get("usar_contrasena", True) else "desactivada"
    print(f"La contraseña de inicio está {estado_actual}.")

    respuesta = confirmar("¿Quieres cambiarlo? (s/n): ")
    if respuesta:
        config["usar_contrasena"] = not config.get("usar_contrasena", True)
        guardar_configuracion(config)
        nuevo_estado = "activada" if config["usar_contrasena"] else "desactivada"
        print(f"[OK] Contraseña de inicio {nuevo_estado}.")
    else:
        print("Sin cambios.")


def cambiar_contrasena(config):
    print(f"\n{LINEA}\nCambiar contraseña\n{LINEA}")
    actual = input("Contraseña actual: ")

    if actual != obtener_contrasena(config):
        print("[!] Contraseña actual incorrecta.")
        return

    nueva = input("Nueva contraseña: ").strip()
    if not nueva:
        print("[!] La contraseña no puede estar vacía.")
        return

    confirmacion = input("Confirma la nueva contraseña: ").strip()
    if nueva != confirmacion:
        print("[!] Las contraseñas no coinciden.")
        return

    config["contrasena"] = nueva
    guardar_configuracion(config)
    print("[OK] Contraseña actualizada.")


def verificar_acceso(config):
    intentos = MAX_INTENTOS
    contrasena_actual = obtener_contrasena(config)

    while intentos > 0:
        clave = input("Contraseña: ")

        if clave == contrasena_actual:
            return True

        intentos -= 1
        print(f"[!] Contraseña incorrecta. Intentos restantes: {intentos}")

    return False


def cargar_notas():
    if not os.path.exists(ARCHIVO_NOTAS):
        guardar_notas([])
        print("[OK] No había archivo de notas, se creó uno nuevo.")
        return []

    try:
        with open(ARCHIVO_NOTAS, mode="r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, FileNotFoundError):
        os.remove(ARCHIVO_NOTAS)
        guardar_notas([])
        print("[!] notas.json estaba dañado, se eliminó y se creó uno nuevo.")
        return []


def guardar_notas(notas):
    with open(ARCHIVO_NOTAS, mode="w", encoding="utf-8") as archivo:
        json.dump(notas, archivo, indent=4, ensure_ascii=False)


def siguiente_id(notas):
    if not notas:
        return 1

    id_mas_alto = notas[0]["id"]
    for nota in notas:
        if nota["id"] > id_mas_alto:
            id_mas_alto = nota["id"]

    return id_mas_alto + 1


def obtener_nota_por_id(notas, id_nota):
    for nota in notas:
        if nota["id"] == id_nota:
            return nota
    return None


def pedir_id():
    try:
        return int(input("Id de la nota: ").strip())
    except ValueError:
        print("[!] Id inválido, debe ser un número.")
        return None


def agregar_nota(notas):
    print(f"\n{LINEA}\nAgregar nota\n{LINEA}")
    titulo = input("Título: ").strip()
    if not titulo:
        print("[!] El título no puede estar vacío.")
        return

    contenido = input("Contenido: ").strip()
    categoria = input("Categoría (Enter para 'General'): ").strip() or "General"

    nota = {
        "id": siguiente_id(notas),
        "titulo": titulo,
        "contenido": contenido,
        "categoria": categoria,
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    notas.append(nota)
    guardar_notas(notas)
    print(f"[OK] Nota agregada con id {nota['id']}")


def editar_nota(notas):
    print(f"\n{LINEA}\nEditar nota\n{LINEA}")
    id_nota = pedir_id()
    if id_nota is None:
        return

    nota = obtener_nota_por_id(notas, id_nota)
    if not nota:
        print("[!] No se encontró una nota con ese id.")
        return

    print(f"Título actual: {nota['titulo']}")
    nuevo_titulo = input("Nuevo título (Enter para dejar igual): ").strip()
    if nuevo_titulo:
        nota["titulo"] = nuevo_titulo

    print(f"Contenido actual: {nota['contenido']}")
    nuevo_contenido = input("Nuevo contenido (Enter para dejar igual): ").strip()
    if nuevo_contenido:
        nota["contenido"] = nuevo_contenido

    print(f"Categoría actual: {nota['categoria']}")
    nueva_categoria = input("Nueva categoría (Enter para dejar igual): ").strip()
    if nueva_categoria:
        nota["categoria"] = nueva_categoria

    guardar_notas(notas)
    print("[OK] Nota actualizada.")


def eliminar_nota(notas):
    print(f"\n{LINEA}\nEliminar nota\n{LINEA}")
    id_nota = pedir_id()
    if id_nota is None:
        return

    nota = obtener_nota_por_id(notas, id_nota)
    if not nota:
        print("[!] No se encontró una nota con ese id.")
        return

    confirmar_borrado = confirmar(f"¿Eliminar '{nota['titulo']}'? (s/n): ")
    if confirmar_borrado:
        notas.remove(nota)
        guardar_notas(notas)
        print("[OK] Nota eliminada.")
    else:
        print("Cancelado.")


def formato_nota(nota):
    return f"[{nota['id']}] {nota['titulo']}  ({nota['categoria']}) - {nota['fecha_creacion']}"


def listar_notas(notas):
    print(f"\n{LINEA}\nNotas guardadas\n{LINEA}")
    if not notas:
        print("No hay notas todavía.")
        return

    for nota in notas:
        print(formato_nota(nota))


def buscar_nota(notas):
    print(f"\n{LINEA}\nBuscar nota\n{LINEA}")
    texto = input("Palabra clave o categoría: ").strip().lower()

    resultados = []
    for nota in notas:
        if texto in nota["titulo"].lower() or texto in nota["contenido"].lower() or texto in nota["categoria"].lower():
            resultados.append(nota)

    if not resultados:
        print("No se encontraron notas.")
        return

    for nota in resultados:
        print(formato_nota(nota))


def mostrar_estadisticas(notas):
    print(f"\n{LINEA}\nEstadísticas\n{LINEA}")
    print(f"Total de notas: {len(notas)}")

    conteo_categorias = {}
    for nota in notas:
        categoria = nota["categoria"]
        conteo_categorias[categoria] = conteo_categorias.get(categoria, 0) + 1

    print("\nNotas por categoría:")
    for categoria, cantidad in conteo_categorias.items():
        print(f"  {categoria}: {cantidad}")


def mostrar_menu():
    print(f"\n{LINEA}")
    print("1) Agregar nota")
    print("2) Editar nota")
    print("3) Eliminar nota")
    print("4) Listar notas")
    print("5) Buscar nota")
    print("6) Ver estadísticas")
    print("7) Activar/desactivar contraseña de inicio")
    print("8) Cambiar contraseña")
    print("0) Salir")
    print(LINEA)


def main():
    print(LOGO)
    print("SISTEMA DE GESTIÓN DE NOTAS PERSONALES\n")

    config = cargar_configuracion()

    if config.get("usar_contrasena", True):
        if not verificar_acceso(config):
            print("\n[!] Acceso denegado.")
            return
        print("\n[OK] Acceso concedido.")

    notas = cargar_notas()

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            agregar_nota(notas)
        elif opcion == "2":
            editar_nota(notas)
        elif opcion == "3":
            eliminar_nota(notas)
        elif opcion == "4":
            listar_notas(notas)
        elif opcion == "5":
            buscar_nota(notas)
        elif opcion == "6":
            mostrar_estadisticas(notas)
        elif opcion == "7":
            cambiar_configuracion_contrasena(config)
        elif opcion == "8":
            cambiar_contrasena(config)
        elif opcion == "0":
            print("\nHasta luego.")
            break
        else:
            print("[!] Opción no válida.")


if __name__ == "__main__":
    main()