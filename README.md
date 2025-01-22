# API de Impresión de Tickets

// ...existing code...

## Introducción

¡Hola a todos! 🌟 En este video, te mostraré cómo he desarrollado un API en Python 🐍 para imprimir directamente desde un sistema web 🖥️ hacia una impresora térmica de tickets 🖨️ de manera silenciosa y eficiente. Este API permite realizar impresiones sin necesidad de diálogos de impresión, haciendo el proceso rápido y sencillo. 🚀

// ...existing code...

## Instalación

Para utilizar la funcionalidad de impresión USB, es necesario instalar la biblioteca `pyusb`. Puedes hacerlo ejecutando el siguiente comando:

```sh
pip install pyusb
```

## Uso

Para generar un ejecutable del programa utilizando `pyinstaller`, ejecuta el siguiente comando:

```sh
pyinstaller --onefile main.py
```

Esto creará un archivo ejecutable único en el directorio `dist`.

### Ejemplo

Para probar la funcionalidad, puedes ejecutar el programa de la siguiente manera:

```sh
python main.py
```

Esto imprimirá un ticket de prueba con el texto "This is a test ticket. Thank you for your purchase!".

// ...existing code...
