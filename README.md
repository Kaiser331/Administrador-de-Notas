# Sistema de Gestión de Notas Personales

Programa de consola en Python para crear, editar, eliminar, listar y buscar notas personales. Los datos se guardan en `notas.json`.

## Requisitos

- Python 3.10 o superior (no usa librerías externas)

## Cómo ejecutarlo

```bash
python notas.py
```

## Contraseña de inicio (opcional)

Por defecto el programa pide una contraseña al abrir (máximo 3 intentos). La contraseña por defecto es:

```
1234
```

Se puede cambiar editando la constante `CONTRASEÑA` al inicio de `notas.py`.

Esta protección se puede **activar o desactivar** desde el menú, opción `7) Activar/desactivar contraseña de inicio`. La preferencia se guarda en `config.json` y se recuerda la próxima vez que se ejecute el programa. Si `config.json` no existe todavía (por ejemplo, la primera vez que se descarga el proyecto), la contraseña está activada por defecto.

## Menú

```
   .-------------------.
  /   N O T A S         \
 |-----------------------|
 |  ___________________  |
 |  ___________________  |
 |  ___________________  |
 |  _______________      |
 |                        |
  \_______________________/

SISTEMA DE GESTIÓN DE NOTAS PERSONALES

──────────────────────────────────────────
1) Agregar nota
2) Editar nota
3) Eliminar nota
4) Listar notas
5) Buscar nota
6) Ver estadísticas
7) Activar/desactivar contraseña de inicio
0) Salir
──────────────────────────────────────────
Elige una opción:
```

## Confirmaciones de sí/no

Las preguntas que se responden con sí o no (eliminar una nota, actualizar calificaciones, activar o desactivar la contraseña) usan una función `confirmar()` que reconoce varias formas de escribir "sí": `y`, `yes`, `s`, `si`, `sí` (con o sin tilde, mayúsculas o minúsculas). Cualquier otra respuesta se toma como "no".

## Notas de categoría "Calificaciones"

Si al agregar o editar una nota se usa la categoría `Calificaciones`, el programa pide una lista de calificaciones separadas por coma y calcula automáticamente el promedio y si está aprobado (promedio mayor o igual a 70).

## Ejemplo de uso

**Agregar una nota de calificaciones:**

```
Elige una opción: 1
Título: Parcial de Python
Contenido:
Categoría (Enter para 'General'): Calificaciones
Calificaciones separadas por coma: 85, 62, 91, 55
[OK] Nota agregada con id 3
```

**Listar notas:**

```
Elige una opción: 4
[1] Compras del super  (Hogar) - 2026-08-28 22:07:58
[2] Repasar Git  (Escuela) - 2026-08-28 22:07:58
[3] Parcial de Python  (Calificaciones) - 2026-08-28 22:07:58
     Promedio: 73.25  -> Aprobado
```

**Buscar por palabra clave o categoría:**

```
Elige una opción: 5
Palabra clave o categoría: escuela
[2] Repasar Git  (Escuela)
```

**Ver estadísticas:**

```
Elige una opción: 6
Total de notas: 4

Notas por categoría:
  Hogar: 1
  Escuela: 1
  Calificaciones: 2

Notas de calificaciones: 2
  Aprobadas: 1
  Reprobadas: 1
```

**Activar/desactivar contraseña:**

```
Elige una opción: 7
La contraseña de inicio está activada.
¿Quieres cambiarlo? (s/n): s
[OK] Contraseña de inicio desactivada.
```

## Estructura de una nota

Cada nota se guarda como un diccionario dentro de `notas.json`. Una nota normal:

```json
{
    "id": 2,
    "titulo": "Repasar Git",
    "contenido": "Revisar comandos add, commit y push",
    "categoria": "Escuela",
    "fecha_creacion": "2026-08-28 22:07:58"
}
```

Una nota de calificaciones incluye además `calificaciones`, `promedio` y `aprobado`:

```json
{
    "id": 3,
    "titulo": "Parcial de Python",
    "contenido": "",
    "categoria": "Calificaciones",
    "fecha_creacion": "2026-08-28 22:07:58",
    "calificaciones": [85.0, 62.0, 91.0, 55.0],
    "promedio": 73.25,
    "aprobado": true
}
```

## Manejo de errores

- Si `notas.json` no existe, el programa lo crea automáticamente vacío al iniciar.
- Si `notas.json` existe pero está dañado (JSON inválido), el programa lo elimina y crea uno nuevo vacío, avisando en pantalla.
- Si `notas.json` existe y es válido, se usa tal cual, sin tocarlo.
- Si `config.json` está corrupto, se avisa y se continúa con valores por defecto.
- Si se ingresa un id no numérico o una opción de menú inválida, se muestra un mensaje y se vuelve a mostrar el menú sin cerrar el programa.
- Si se ingresa una contraseña incorrecta 3 veces, el programa termina sin dar acceso.
- Si se escribe una calificación que no es un número, se omite y se avisa cuál fue.

## Git y privacidad de las notas

El repositorio incluye un `notas.json` de ejemplo (con datos de prueba) para que se pueda ver la estructura y probar el programa apenas se clone. Sin embargo, **no queremos que las notas personales de quien use el programa después terminen subidas al repositorio**, así que `.gitignore` incluye:

```
notas.json
config.json
```

**Importante:** Git tiene una particularidad: `.gitignore` solo funciona para archivos que *todavía no* han sido parte de ningún commit. Como `notas.json` ya viene incluido en la entrega inicial (para cumplir con el requisito de entregar el archivo de datos), Git seguirá detectando cambios en él aunque esté en `.gitignore`, hasta que se le indique explícitamente que deje de rastrearlo.

Para dejar de rastrear `notas.json` (y que a partir de ahí las notas que se agreguen ya no se suban), ejecuta **una sola vez**, después de la entrega:

```bash
git rm --cached notas.json
git commit -m "Dejar de rastrear notas.json para proteger notas personales"
```

Esto elimina el archivo del control de versiones (no de la computadora) — el programa lo sigue usando normalmente, solo que Git ya no lo vuelve a subir en los siguientes commits. `config.json` no necesita este paso porque no viene incluido en la entrega inicial: al no haber sido parte de ningún commit, `.gitignore` lo ignora desde el principio.

## Cómo subirlo a GitHub

```bash
git init
git add .
git commit -m "Entrega inicial del proyecto"
git branch -M main
git remote add origin <URL-del-repositorio>
git push -u origin main
```
