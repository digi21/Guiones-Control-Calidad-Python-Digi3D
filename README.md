# Guiones de control de calidad en Digi3D.NET

Bienvenido al repositorio **comunitario** de controles de calidad para [Digi3D.NET](https://www.digi21.net).

Aquí encontrarás guiones de Python que puedes pegar en la pestaña **Python** del programa
[Editor de Tablas de Códigos](https://ayuda.digi21.net/digi3d-net/referencia/editor-de-tablas-de-codigos)
y luego asignar en el campo **Controles de calidad a aplicar** de cada código. Así puedes validar tus
geometrías (durante la digitalización o a petición) de forma muy sencilla, sin tener que programar nada
si ya existe el control que necesitas.

## ✍️ ¿Quieres colaborar?

¡Tus controles de calidad son bienvenidos! Si has escrito uno que te resulta útil, compártelo con el resto
de la comunidad:

1. Haz un **_fork_** de este repositorio (o clónalo).
2. Añade tu función de control de calidad (siguiendo las normas que se describen más abajo: decorador
   `@quality_control`, parámetros obligatorios y una línea de documentación con la descripción).
3. Abre un **_pull request_**. Lo revisaremos e integraremos 😉.

¿Tienes una idea, una duda o has encontrado un fallo? Abre una
[_issue_](https://github.com/digi21/Guiones-Control-Calidad-Python-Digi3D/issues) y lo comentamos.

A continuación tienes la **referencia completa** para escribir tus propios controles de calidad.

## Declaración de un control de calidad

El _Editor de Tablas de Códigos_ de _Digi3D.NET_ y el propio _Digi3D.NET_ localizan las funciones que realizan controles de calidad enumerando todas las que estén definidas en el entorno _Python_ que cumplan con las siguientes condiciones:

1. Que están decoradas o envueltas con el _function\_wrapper_ denominado __@quality_control__ 
2. Que reciban al menos los parámetros `geometry`, `adding_geometry` y `code_index`.
3. Que tengan una descripción.

### Function wrapper

Si la función no está precedida por el function wrapper __@quality_control__ no será considerada una función de control de calidad.

### Parámetros obligatorios

La función de control de calidad tiene que tener como mínimo los siguientes parámetros:

|nombre|descripción|
|--|--|
|geometry|Geometría que se está analizando|
|adding_geometry|Booleano que indica si el control de calidad se está ejecutando porque el usuario acaba de dibujar la geometría (aún no se ha añadido al archivo de dibujo) o si se está ejecutando porque el usuario lo ha solicitado mediante las órdenes de control de calidad que aparecen en el menú de _Control de Calidad_ del programa. El comportamiento puede ser diferente, porque si se está ejecutando desde el menú, tenemos que devolver todos los posibles errores localizados (por ejemplo un control de calidad que devuelve como errores todas las intersecciones entre dos líneas), sin embargo, si se está ejecutando el control de calidad porque el usuario está dibujando la geometría, con el primer error es suficiente.|
|code_index|Índice del código que se está ejecutando. Este parámetro es fundamental para ciertos escenarios, como por ejemplo aquellos controles de calidad que analizan los atributos de base de datos de un determinado código. Si la geometría tiene 2 códigos, el control de calidad tiene que saber cual de los dos códigos analizar.|

La función puede recibir sus propios parámetros, como códigos, distancias, etc. Estos parámetros adicionales son los que aparecen en el cuadro de diálogo de configuración del control de calidad al añadir un control de calidad a un código.

### Descripción del control de calidad

El _Editor de Tablas de códigos_ extrae la descripción que va a mostrar en la columna _Descripción_ del cuadro de diálogo que aparece al pulsar sobre el botón de _Controles de calidad_ de cada código de la primera línea de documentación de la función de control de calidad. 
Es obligatorio que las funciones de control de calidad tengan al menos una línea de documentación.

### Comunicando a Digi3D.NET que la geometría ha pasado el control de calidad sin problemas

Si la geometría analizada no presenta problemas para un control de calidad en particular, tan solo hay que salir de la función con un `return`

Ejemplo de una función de control de calidad que no hace nada, pero que aparece en el listado de controles de calidad y que se puede asignar a un código.

```python
@quality_control()
def este_control_de_calidad_no_hace_nada(geometry, adding_geometry, code_index):
    'Este control de calidad nunca devuelve un error a Digi3D.NET.'
    return
```

## Comunicación de advertencias y errores

Si la función de control de calidad determina que la geometría que se está analizando tiene errores, puede comunicárselo a Digi3D.NET devolviendo cualquiera de los siguientes objetos:

- `digi3d.GeometryWarning`
- `digi3d.GeometryError`
- `digi3d.GeometryRelationError`
- `digi3d.DatabaseFieldError`

Si se desea, se puede devolver también una lista que contenga cualquiera de estos cuatro tipos de error como por ejemplo:

```python
@quality_control()
def control_calidad_a_anadir_a_codigos_con_los_que_no_se_deberia_dibujar_nada(geometry, adding_geometry, code_index):
    'Si se asigna este control a cualquier código, se comunicará tanto un error como una advertencia'
    errores = []
    errores.append(digi3d.GeometryError('No deberías haber almacenado esta geometría'))
    errores.append(digi3d.GeometryWarning('Se donde vives...'))

    return errores
```
### Comunicando a Digi3D.NET advertencias

Si la función de control de calidad quiere informar de una advertencia (aparecerá con el icono de advertencia en el panel de tareas en vez de con el icono de error), tiene que devolver una instancia de `digi3d.GeometryWarning`.

El constructor de esta clase admite un único parámetro que es el mensaje a mostrar al usuario al hacer doble clic sobre la tarea que se añadirá al panel de tareas.

Ejemplo:

```python
@quality_control()
def muestra_advertencia_si_la_linea_tiene_menos_de_X_vertices(geometry, adding_geometry, code_index, numero_vertices):
    'Muestra una advertencia si el número de vértices de la línea es inferior al pasado por parámetros'
    if type(geometry) is not digi3d.Line:
        return

    if len(geometry) < numero_vertices:
	    return digi3d.GeometryWarning('Esta línea tiene menos de {} vértices.'.format(numero_vertices))
```


### Comunicando a Digi3D.NET que la geometría tiene un error por sí misma (sin tener en cuenta otras geometrías del archivo de dibujo)

En este caso la función de control de calidad tiene que devolver una instancia del objeto `digi3d.GeometryError`.

Este objeto tiene dos constructores posibles:

|Parámetro|Descripción|
|--|--|
|Mensaje|Mensaje a comunicar al usuario|

Si se devuelve este objeto, Digi3D.NET hará un zoom extendido a la geometría si el usuario hace doble click en la tarea con el error que aparecerá en el panel de tareas.

|Parámetro|Descripción|
|--|--|
|Mensaje|Mensaje a comunicar al usuario|
|Coordenadas|Tupla con coordenadas (x,y,z)|

Si se devuelve este objeto, Digi3D.NET desplazará la cámara a las coordenadas especificadas si el usuario hace doble click en la tarea con el error que aparecerá en el panel de tareas.

Veamos un ejemplo muy sencillo de control de calidad que devuelve `digi3d.GeometryError`:

```python
@quality_control()
def debe_ser_punto(geometry, adding_geometry, code_index):
    'Comunica un error si la geometría no es de tipo Punto'
    if type(geometry) is not digi3d.Point:
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser de tipo Punto'.format(geometry.codes[0].code))
```

### Comunicando a Digi3D.NET que la geometría tiene un error en relación con otra geometría

Si queremos relacionar dos geometrías en el error, como por ejemplo en el caso de que una geometría esté muy cerca de otra por ejemplo, tenemos que devolver una instancia del objeto `digi3d.GeometryRelationError`. 

Si devolvemos este objeto, en el panel de tareas se añadirá una subtarea a la tarea con el error que nos permitirá centrar o una geometría o la otra de entre las involucradas en el error.

Este objeto dispone de cuatro constructores:

|Parámetro|Descripción|
|--|--|
|Otra|La otra geometría involucrada en el problema detectado por el control de calidad|
|Mensaje|Mensaje a comunicar al usuario|

Si se devuelve este objeto, Digi3D.NET hará un zoom extendido a la geometría si el usuario hace doble click en la tarea con el error que aparecerá en el panel de tareas.

|Parámetro|Descripción|
|--|--|
|Otra|La otra geometría involucrada en el problema detectado por el control de calidad|
|Mensaje|Mensaje a comunicar al usuario|
|Coordenadas|Tupla con coordenadas (x,y,z)|

Si se devuelve este objeto, Digi3D.NET desplazará la cámara a las coordenadas especificadas si el usuario hace doble click en la tarea con el error que aparecerá en el panel de tareas.

|Parámetro|Descripción|
|--|--|
|Otras|Lista de geometrías que están involucradas en el problema detectado por el control de calidad|
|Mensaje|Mensaje a comunicar al usuario|

Si se devuelve este objeto, Digi3D.NET hará un zoom extendido a la geometría si el usuario hace doble click en la tarea con el error que aparecerá en el panel de tareas.

|Parámetro|Descripción|
|--|--|
|Otras|Lista de geometrías que están involucradas en el problema detectado por el control de calidad|
|Mensaje|Mensaje a comunicar al usuario|
|Coordenadas|Tupla con coordenadas (x,y,z)|

Si se devuelve este objeto, Digi3D.NET desplazará la cámara a las coordenadas especificadas si el usuario hace doble click en la tarea con el error que aparecerá en el panel de tareas.

Ejemplo:

```python
@quality_control()
def no_puede_punto_estar_a_menos_de_distancia_de_cualquier_otro_punto(geometry, adding_geometry, code_index, distancia):
    'Si la geometría que se está analizando es de tipo punto, comprueba su distancia al resto de puntos del archivo de dibujo y devuelve error en caso de que esta sea inferior al parámetro distancia'
    if type(geometry) is not digi3d.Point:
        return

    geometriasNoEliminadas = filter(lambda geometría : not geometría.deleted, digi3d.current_view())
    puntosArchivoDibujo = filter(lambda geometría : type(geometría) is digi3d.Point, geometriasNoEliminadas)

    # No podemos calcular la distancia entre puntos sin más, porque puede que la ventana de dibujo esté en coordenadas elipsoidales, de manera que las
    # coordenadas que nos van a llegar no son ortométricas, sino ángulos. La ventana de dibujo proporciona una calculadora geográfica que calcula 
    # distancias correctamente
    calculadora  = digi3d.current_view().geographic_calculator

    for punto in puntosArchivoDibujo:
        distancia_entre_los_puntos = calculadora.calculate_distance_2d(geometry[0], punto[0])
        if distancia_entre_los_puntos < distancia:
            return digi3d.GeometryRelationError(punto, 'Estos dos puntos están a una distancia {} que es inferior a {}'.format(distancia_entre_los_puntos, distancia))

```

El ejemplo anterior no estaría finalizado del todo, pues estamos parando en el primer error detectado. Si el usuario selecciona la opción del menú de control de calidad, quiere ver todos los errores de una geometría. Para ello podemos utilizar cualquiera de las dos sobrecaras del constructor de `digi3d.GeometryRelationError` que reciben una lista de geometrías como por ejemplo:

```python
@quality_control()
def no_puede_punto_estar_a_menos_de_distancia_de_cualquier_otro_punto(geometry, adding_geometry, code_index, distancia):
    'Si la geometría que se está analizando es de tipo punto, comprueba su distancia al resto de puntos del archivo de dibujo y devuelve error en caso de que esta sea inferior al parámetro distancia'
    if type(geometry) is not digi3d.Point:
        return

    geometriasNoEliminadas = filter(lambda geometría : not geometría.deleted, digi3d.current_view())
    puntosArchivoDibujo = filter(lambda geometría : type(geometría) is digi3d.Point, geometriasNoEliminadas)

    # No podemos calcular la distancia entre puntos sin más, porque puede que la ventana de dibujo esté en coordenadas elipsoidales, de manera que las
    # coordenadas que nos van a llegar no son ortométricas, sino ángulos. La ventana de dibujo proporciona una calculadora geográfica que calcula 
    # distancias correctamente
    calculadora  = digi3d.current_view().geographic_calculator

    lista_de_puntos_cercanos = []

    for punto in puntosArchivoDibujo:
        distancia_entre_los_puntos = calculadora.calculate_distance_2d(geometry[0], punto[0])
        if distancia_entre_los_puntos < distancia:
            lista_de_puntos_cercanos.append(punto)

            if adding_geometry:
                # Estamos en modo interactivo: El usuario está digitalizando una geometría, de manera que con detectar el primer error es suficiente
                break

    if( len(lista_de_puntos_cercanos) > 0):
        return digi3d.GeometryRelationError(lista_de_puntos_cercanos, 'Este punto está muy cerca de estos puntos')
```

### Comunicando a Digi3D.NET que la geometría tiene un error de base de datos

Si el control de calidad analiza los atributos de base de datos de un determinado código y encuentra un error, puede comunicárselo a Digi3D.NET devolviendo una instancia de `digi3d.DatabaseFieldError`.

Si estamos en modo interactivo, Digi3D.NET mostrará un cuadro de diálogo para que el usuario corrija el error de base de datos y vuelva a probar a almacenar la geometría.

El constructor de este objeto recibe los siguientes parámetros:

|Parámetro|Descripción|
|--|--|
|Mensaje|Mensaje a comunicar al usuario|
|Indice del código|Índice del código (de entre los códigos que tiene la geometría) en el que se ha localizado el error|
|Campo|Nombre del campo en el que se ha detectado el error|

Ejemplo:

```python
@quality_control()
def atributo_bbdd_no_puede_ser_nulo(geometry, adding_geometry, code_index, nombre_atributo):
    'Comunica un error si el código que se está analizando no tiene entre sus atributos el atributo pasado por parámetros o si el valor de este atributo es nulo'
    atributosCodigo = geometry.codes[code_index].attributes

    if nombre_atributo not in atributosCodigo:
        return digi3d.GeometryError('Se esperaba que el código {} de esta geometría tuviera un atributo con nombre {} pero no lo tiene'.format(geometry.codes[code_index].code, nombre_atributo))

    if atributosCodigo[nombre_atributo] is None:
        return digi3d.DatabaseFieldError('Atributo con valor nulo', code_index, nombre_atributo)
```