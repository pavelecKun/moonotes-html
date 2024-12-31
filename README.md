# MooNotes-html

# ¿Qué es?
Una simple herramienta para convertir lo que subrrayas en Moon+ Reader a un hermoso archivo HTML.

# ¿Por qué?
Moon+ Reader es el lector de libros electrónicos más popular, y el que uso en mi flujo de lectura para resumir libros. Este nuevo archivo HTML te permitirá hacer más resúmenes o diagramas junto a la IA de tu predicción.

Este repositorio es una actualización y adaptación al español del trabajo de moonreader2html.


**Convertir el archivo de Moon+ Reader a un, muy agradable,  HTML leíble**

La app la puedes descargar desde [Moon+ Reader](https://play.google.com/store/apps/details?id=com.flyersoft.moonreaderp&hl=en&gl=US) por silo necesitas.

## Instalación
Clona estos repositorios e instala los paquetes python `jinja2` y `titlecase`.

## ¿Cómo usarlo?
1. Abre tu libro en Moon+ Reader por ejemplo `Sangurimas.epub` . Abre la pestaña Capítulos, ve a la pestaña Marcadores, haz clic en el icono compartir y elige en el menú la opción exportar a archivo.
2. Esto generará un `Sangurimas.mrexpt`, haz clic en Aceptar y guárdalo en tu teléfono, cópialo en un PC.
3. 3. Obtén la portada del libro de internet, debe tener el formato `.png` y el nombre `cover.png`.
4.  Ejecuta este script:
```bash
python moonotes.py Sangurimas.mrexpt
```

- Es posible que el nombre del libro y el autor no estén capturados, para añadirlos utiliza las banderas
```bash
python moonotes.py Sangurimas.mrexpt -a "José de la Cuadra"
```





# Aquí hay un ejemplo del archivo html de las líneas resaltadas.

<img src="./sample.png"></img>

### Opciones
**Depurar
Activado por defecto, y asegura que el libro y el nombre del archivo son únicos (añadiendo una marca de tiempo). Esto es para permitir múltiples exportaciones del mismo libro. Esto es conveniente para probar este script o para tener múltiples revisiones, pero puede desactivarlo siguiendo el siguiente código:
```bash
python ./moonotes.py --debug=false my-book-highlights.mrexpt
```

**`titlecap`**
Se activa por defecto y convierte los títulos de los capítulos (resaltados con notas como .h1/.h2/.h3) a *Title Cap* si son *ALL CAPITAL* o *all lowercase*. Esto no es específico de Moon+ Reader, pero es bueno poder hacer este cambio - muchos libros utilizan feas mayúsculas para los títulos de los capítulos por razones tipográficas, pero fuera del formato del libro no son tan agradables. Puedes desactivarlo de la siguiente manera:

```bash
python ./moonotes.py --titlecap=false my-book-highlights.mrexpt
```



**Autor
Especifica el autor o autores que no están disponibles en el archivo .mrexpt. Si no se especifica, el autor se escribe como "Desconocido".

---

Disfrute, hágame saber si hay algún problema o sugerencia mediante la presentación de cuestiones, y por supuesto pull requests son muy bienvenidos.

Actualizado Diciembre 2024