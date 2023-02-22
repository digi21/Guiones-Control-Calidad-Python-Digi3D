import digi3d
import digi3d.relations

''' Utilidades que usan los controles de calidad '''

def es_area(g):
    '''Devuelve verdadero si la geometría es de tipo área (polígono o línea cerrada)'''

    if type(g) is digi3d.Polygon:
        return True

    if type(g) is digi3d.Line and g.closed_2d:
        return True

    return False

def compara_codigos_con_comodines(codigo_a, codigo_b):
    ''' Compara dos códigos utilizando comodines.
        El comodín * indica que el resto de la cadena es válido.
        El comodín ? sustituye cualquier carácter.

        Ej: 12?45 devuelve verdadero para 12a45, 12b45, 12045, 12945, etc.
            12* devuelve verdadero para cualquier código que comience con 12, como por ejemplo 12abcdefg 
    '''
    tamanoCodigoA = len(codigo_a)
    tamanoCodigoB = len(codigo_b)
    for i in range(min(tamanoCodigoA, tamanoCodigoB)):
        if codigo_a[i] == '*' or codigo_b[i] == '*':
            return True
        if codigo_a[i] == '?' or codigo_b[i] == '?':
            continue
        if codigo_a[i] != codigo_b[i]:
            return False
    if tamanoCodigoA == tamanoCodigoB:
        return True
    return False

def tiene_el_codigo(g, nombre_código):
    '''Indica si la entidad tiene el código pasado por parámetro. 
    Argumentos:
        entidad: Entidad sobre la que realizar la consulta.
        código: Código buscado.
    '''
    for codigo in g.codes:
        if codigo.name == nombre_código:
            return True
    return False

def tiene_el_codigo_con_comodines(g, nombre_código):
    '''Indica si la entidad tiene el código pasado por parámetro. 
    Argumentos:
        entidad: Entidad sobre la que realizar la consulta.
        código: Código buscado.
    '''
    for codigo in g.codes:
        if compara_codigos_con_comodines(codigo.name, nombre_código) :
            return True
    return False

def tiene_algun_codigo_de_etiqueta(g, etiqueta):
    ''' Analiza si la geometría tiene algún código de entre los códigos (de la tabla de códigos activa) que tienen asignada una determinada etiqueta
    '''
    tabla_codigos = digi3d.current_view().digi_tab

    for codigo in tabla_codigos:
        if not tabla_codigos[codigo].contains_tag(etiqueta):
            continue
    
        if tiene_el_codigo(g, codigo):
            return True

    return False

def tiene_el_codigo_o_etiqueta(g, nombre_codigo_o_etiqueta):
    ''' Indica si la entidad tiene el código pasado por parámetro.
        Si el código pasado es una etiqueta, se devuelve verdadero si la geometría tiene un código de entre los que tienen asignada dicha etiqueta en la tabla de códigos activa.
        Si el código pasado no es una etiqueta, se busca con comodines, de manera que se puede poner por ejemplo 0204*
    '''

    if nombre_codigo_o_etiqueta[0] == '#':
        return tiene_algun_codigo_de_etiqueta(g, nombre_codigo_o_etiqueta[1:])

    return tiene_el_codigo_con_comodines(g, nombre_codigo_o_etiqueta)

def tiene_algun_codigo(g, códigos):
    '''Indica si la entidad tiene alguno de los códigos pasados por parámetro.
    Argumentos:
        entidad: Entidad sobre la que realizar la consulta.
        códigos: conjunto de códigos.
    Observaciones:
        Esta función devuelve verdadero si se encuentra al menos un código de los pasados por parámetros
        de entre los códigos que tiene la entidad.
    '''
    return len(códigos.intersection(g.codes.keys())) > 0

def tiene_algun_codigo_con_comodines(g, códigos_con_comodines):
    '''Indica si la entidad tiene alguno de los códigos pasados por parámetro.
    Argumentos:
        entidad: Entidad sobre la que realizar la consulta.
        códigos: conjunto de códigos.
    Observaciones:
        Esta función devuelve verdadero si se encuentra al menos un código de los pasados por parámetros
        de entre los códigos que tiene la entidad.
    '''
    for codigo in g.codes:
        for codigoComparar in códigos_con_comodines:
            if compara_codigos_con_comodines(codigo, codigoComparar):
                return True

    return False

''' Utilidades para secuencias de geometrías '''

def eliminadas(geometrías):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que  están eliminadas.
    Argumentos:
        geometrías: Geometrías a analizar.
    '''
    return filter(lambda geometría : geometría.deleted, geometrías)

def no_eliminadas(geometrías):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que no están eliminadas.
    Argumentos:
        geometrías: Geometrías a analizar.
    '''
    return filter(lambda geometría : not geometría.deleted, geometrías)

def que_tengan_el_codigo(geometrías, nombre_codigo):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que tienen el código indicado.
    Argumentos:
        geometrías: Geometrías a analizar.
        código: Código a localizar
    '''
    return filter(lambda geometría : tiene_el_codigo(geometría, nombre_codigo), geometrías)

def que_tengan_el_codigo_con_comodines(geometrías, nombre_codigo_con_comodines):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que tienen el código indicado.
    Argumentos:
        geometrías: Geometrías a analizar.
        código: Código a localizar
    '''
    return filter(lambda geometría : tiene_el_codigo_con_comodines(geometría, nombre_codigo_con_comodines), geometrías)

def que_tengan_el_codigo_o_etiqueta(geometrías, nombre_codigo_o_etiqueta):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que tienen el código indicado.
    Argumentos:
        geometrías: Geometrías a analizar.
        código: Código a localizar
    '''
    return filter(lambda geometría : tiene_el_codigo_o_etiqueta(geometría, nombre_codigo_o_etiqueta), geometrías)

def que_tengan_algun_codigo(geometrías, nombres_codigos):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que tienen el código indicado.
    Argumentos:
        geometrías: Geometrías a analizar.
        código: Código a localizar
    '''
    return filter(lambda geometría : tiene_algun_codigo(geometría, nombres_codigos), geometrías)

def que_tengan_algun_codigo_de_etiqueta(geometrías, etiqueta):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que tienen el código indicado.
    Argumentos:
        geometrías: Geometrías a analizar.
        código: Código a localizar
    '''
    return filter(lambda geometría : tiene_algun_codigo_de_etiqueta(geometría, etiqueta), geometrías)

def alguna_geometria(geometría_analizando, callback_incluir_geometria, callback_condicion):
    ''' Itera por todas las geometrías del archivo de dibujo y devuelve verdadero si se localiza una con la
    que devuelvan True tanto la función callback_incluir_geometria como la función callback_concicion
    '''
    for g in no_eliminadas(digi3d.current_view()):
        if not callback_incluir_geometria(g):
            continue

        if callback_condicion(g):
            return True

    return False

def algun_area_con_codigo(geometría_analizando, código_o_etiqueta_areas_analizar, callback_condicion):
    return alguna_geometria(geometría_analizando, lambda g: es_area(g) and tiene_el_codigo_o_etiqueta(g, código_o_etiqueta_areas_analizar), callback_condicion)

def alguna_linea_con_codigo(geometría_analizando, código_o_etiqueta_lineas_analizar, callback_condicion):
    return alguna_geometria(geometría_analizando, lambda g: type(g) is digi3d.Line and tiene_el_codigo_o_etiqueta(g, código_o_etiqueta_lineas_analizar), callback_condicion)

def algun_punto_con_codigo(geometría_analizando, código_o_etiqueta_puntos_analizar, callback_condicion):
    return alguna_geometria(geometría_analizando, lambda g: type(g) is digi3d.Point and tiene_el_codigo_o_etiqueta(g, código_o_etiqueta_puntos_analizar), callback_condicion)

def algun_texto_con_codigo(geometría_analizando, código_o_etiqueta_textos_analizar, callback_condicion):
    return alguna_geometria(geometría_analizando, lambda g: type(g) is digi3d.Text and tiene_el_codigo_o_etiqueta(g, código_o_etiqueta_textos_analizar), callback_condicion)

''' Controles de calidad '''

@quality_control()
def debe_area_adyacente_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un área, comunica un error si no se localiza ningún área en el archivo de dibujo que sea adyacente al área que se está analizando
    '''
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.adjacent(área, geometry)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_area_completamente_dentro_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un área, comunica un error si no se localiza en el archivo de dibujo otro área que dentro de la cual esté la geometría que se está analizando (no se admite que determinados vértices de este área coincidan con la del otro área)
    '''
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.completely_within(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_area_dentro_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un área, comunica un error si no se localiza en el archivo de dibujo otro área que dentro de la cual esté la geometría que se está analizando (se admite que determinados vértices de este área coincidan con la del otro área)
    '''
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.within(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_area_disjunta_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un área, comunica un error si se localiza en el archivo de dibujo otra área que no sea disjunta (es decir, que solape, cruce, esté en el interior...) de la geometría ques e está analizando
    '''
    if not es_area(geometry):
        return

    if algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: not digi3d.relations.AreaArea.disjoint(área, geometry)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_area_igual_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un área, comunica un error si no se localiza en el archivo de dibujo otro área que sea idéntica a la geometría que se está analizando
    '''
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.equal(área, geometry)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_area_se_une_con_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un área, comunica un error si no se localiza en el archivo de dibujo un área que se una con la geometría que se está analizando
    '''
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.join(área, geometry)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_area_solapa_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un área, comunica un error si no se localiza en el archivo de dibujo un área que solape el área que se está analizando. 
    '''
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.overlap(geometry, área)[0]):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_atributo_igual_valor(geometry, adding_geometry, code_index, nombre_atributo, valor_esperado, mensaje):
    '''
    Comunica un error si el código que se está analizando no tiene entre sus atributos el atributo pasado por parámetros o si el valor de este atributo no coincide con el del valor esperado
    '''
    atributos = geometry.attributes

    if nombre_atributo not in atributos:
        return digi3d.GeometryError('Se esperaba que esta geometría tuviera un atributo con nombre {} pero no lo tiene'.format(nombre_atributo))

    if atributos[nombre_atributo] != valor_esperado:
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_atributo_bbdd_igual_valor(geometry, adding_geometry, code_index, nombre_atributo, valor_esperado, mensaje):
    '''
    Comunica un error si el código que se está analizando no tiene entre sus atributos el atributo pasado por parámetros o si el valor de este atributo no coincide con el del valor esperado
    '''
    atributosCodigo = geometry.codes[code_index].attributes

    if nombre_atributo not in atributosCodigo:
        return digi3d.GeometryError('Se esperaba que el código {} de esta geometría tuviera un atributo con nombre {} pero no lo tiene'.format(geometry.codes[code_index].name, nombre_atributo))

    if atributosCodigo[nombre_atributo] is None or atributosCodigo[nombre_atributo] != valor_esperado:
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_atributo_bbdd_mayor_igual_valor(geometry, adding_geometry, code_index, nombre_atributo, valor, mensaje):
    '''
    Comunica un error si el código que se está analizando no tiene entre sus atributos el atributo pasado por parámetros o si el valor de este atributo es menor que el valor esperado
    '''
    atributosCodigo = geometry.codes[code_index].attributes

    if nombre_atributo not in atributosCodigo:
        return digi3d.GeometryError('Se esperaba que el código {} de esta geometría tuviera un atributo con nombre {} pero no lo tiene'.format(geometry.codes[code_index].name, nombre_atributo))

    if atributosCodigo[nombre_atributo] is None or atributosCodigo[nombre_atributo] < valor:
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_adyacente_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error si no se localiza en el archivo de dibujo un área que solape dicha línea. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.adjacent(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_completamente_dentro_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error si no se localiza en el archivo de dibujo un área que solape dicha línea. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.within(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_cruza_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error si esta no cruza ningún área del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.across(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_cruza_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error si esta no cruza ningún área del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.across(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_disjunta_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error si esta toca (cruza, está dentro, etc) algún área del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: not digi3d.relations.LineArea.disjoint(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_disjunta_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error si se encuentra en el archivo de dibujo otra línea que no sea disjunta con esta. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: not digi3d.relations.LineLine.disjoint(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_igual_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error si se encuentra en el archivo de dibujo otra línea que no sea igual que esta. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.equal(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_se_une_con_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error si esta no se une con algún área del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.join(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_se_une_con_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error ésta no se une con ninguna línea del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.join(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_solapa_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error ésta no solapa con ninguna línea del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.overlap(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_termina_dentro_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error si esta no termina dentro de un área del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.terminates_within(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_termina_en_borde_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error si esta no termina en el borde de un área del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.endpoint_join(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_termina_en_extremo_de_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error ésta no termina en el extremo de otra línea del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.endpoint_join_endpoint(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_linea_termina_en_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es una línea, comunica un error ésta no termina en otra línea del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.endpoint_join_excluding_endpoints(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_punto_coincide_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un punto, comunica un error si este no coincide con un área del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Point:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.PointArea.coincident(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_punto_coincide_extremo_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un punto, comunica un error si este no termina en el extremo de otra línea del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Point:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.PointLine.coincident_and_terminate(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_punto_coincide_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un punto, comunica un error si este no termina en una línea (excluyendo sus extremos) del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Point:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.PointLine.coincident(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_punto_coincide_punto(geometry, adding_geometry, code_index, código_o_etiqueta_puntos_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un punto, comunica un error si este no coincide con otro punto del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Point:
        return

    if not algun_punto_con_codigo(geometry, código_o_etiqueta_puntos_analizar, lambda punto: digi3d.relations.PointPoint.coincident(geometry, punto)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_punto_disjunto_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un punto, comunica un error si este no es disjunto con algún área del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Point:
        return

    if algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: not digi3d.relations.PointArea.disjoint(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_punto_disjunto_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un punto, comunica un error si este no es disjunto con alguna línea del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Point:
        return

    if alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: not digi3d.relations.PointLine.disjoint(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_punto_disjunto_punto(geometry, adding_geometry, code_index, código_o_etiqueta_puntos_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un punto, comunica un error si este no es disjunto con otro punto del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Point:
        return

    if algun_punto_con_codigo(geometry, código_o_etiqueta_puntos_analizar, lambda punto: not digi3d.relations.PointPoint.disjoint(geometry, punto)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_punto_en_el_interior_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    '''
    Si la geometría que se está analizando es un punto, comunica un error si este no está en el interior de algún área del archivo de dibujo. 
    '''
    if type(geometry) is not digi3d.Point:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.PointArea.within(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_ser_area(geometry, adding_geometry, code_index):
    '''
    Comunica un error si la geometría no es de tipo área (polígonos o líneas cerradas)
    '''
    if not es_area(geometry):
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser polígonos o líneas cerradas'.format(geometry.codes[0].name))

@quality_control()
def debe_ser_complejo(geometry, adding_geometry, code_index):
    '''
    Comunica un error si la geometría no es de tipo Complejo
    '''
    if type(geometry) is not digi3d.Complex:
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser de tipo Texto'.format(geometry.codes[0].name))

@quality_control()
def debe_ser_linea(geometry, adding_geometry, code_index):
    '''
    Comunica un error si la geometría no es de tipo Línea
    '''
    if type(geometry) is not digi3d.Line:
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser de tipo Línea'.format(geometry.codes[0].name))

@quality_control()
def debe_ser_poligono(geometry, adding_geometry, code_index):
    '''
    Comunica un error si la geometría no es de tipo Polígono
    '''
    if type(geometry) is not digi3d.Polygon:
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser de tipo Polígono'.format(geometry.codes[0].name))

@quality_control()
def debe_ser_punto(geometry, adding_geometry, code_index):
    '''
    Comunica un error si la geometría no es de tipo Punto
    '''
    if type(geometry) is not digi3d.Point:
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser de tipo Punto'.format(geometry.codes[0].name))

@quality_control()
def debe_ser_texto(geometry, adding_geometry, code_index):
    '''
    Comunica un error si la geometría no es de tipo Texto
    '''
    if type(geometry) is not digi3d.Text:
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser de tipo Texto'.format(geometry.codes[0].name))

@quality_control()
def debe_tener_area_igual_o_mayor(geometry, adding_geometry, code_index, area_minima):
    'Tiene que tener un perímetro superior a un valor'

    if type(geometry) is not digi3d.Line and type(geometry) is not digi3d.Polygon:
        return

    if geometry.area < area_minima:
        return digi3d.GeometryError('Las geometrías con el código {} deben ser tener un área mayor o igual que {}'.format(geometry.codes[0].name, area_minima))

@quality_control()
def debe_tener_perimetro_mayor_o_igual(geometry, adding_geometry, code_index, perimetro):
    'Tiene que tener un perímetro mayor o igual que el valor pasado por parámetros'
    if geometry.perimeter_2d >= perimetro:
        return
    return digi3d.GeometryError('Las geometrías con el código {} deben ser tener un perímetro mayor o igual que {}'.format(geometry.codes[0].name, perimetro))

@quality_control()
def debe_tener_perimetro_mayor(geometry, adding_geometry, code_index, perimetro):
    'Tiene que tener un perímetro mayor a un valor'
    if geometry.perimeter_2d > perimetro:
        return
    return digi3d.GeometryError('Las geometrías con el código {} deben ser tener un perímetro mayor que {}'.format(geometry.codes[0].name, perimetro))

@quality_control()
def debe_tener_todos_los_vertices_con_la_misma_coordenada_z(geometry, adding_geometry, code_index):
    '''Comunica un error si localiza un vértice con la coordenada Z distinta de la del vértice anterior
    '''
    zInicial = geometry[0][2]

    for coordenada in geometry:
        if coordenada[2] != zInicial:
            return digi3d.GeometryError('Las geometrías con este código deben tener todos los vértices con la misma coordenada Z', coordenada)

@quality_control()
def debe_tener_coordenadas_z_crecientes(geometry, adding_geometry, code_index):
    '''
    Comunica un error si se localiza un vértice cuya coordenada Z sea inferior o igual a la coordenada Z del vértice anterior.
    '''
    zPrevia = None

    for coordenada in geometry:
        if zPrevia is None:
            zPrevia = coordenada[2]
            continue

        zActual = coordenada[2]

        if zActual <= zPrevia:
            return digi3d.GeometryError("Vértice con la Z inferior o igual al anterior", coordenada)

        zPrevia = zActual

@quality_control()
def debe_tener_coordenadas_z_crecientes_moderado(geometry, adding_geometry, code_index):
    '''
    Comunica un error si se localiza un vértice cuya coordenada Z sea inferior a la coordenada Z del vértice anterior.
    '''
    zPrevia = geometry[0][2]

    for coordenada in geometry:
        zActual = coordenada[2]

        if zActual < zPrevia:
            return digi3d.GeometryError("Vértice con la Z inferior al anterior", coordenada)

        zPrevia = zActual

@quality_control()
def debe_tener_coordenadas_z_decrecientes(geometry, adding_geometry, code_index):
    '''
    Comunica un error si se localiza un vértice cuya coordenada Z sea superior o igual a la coordenada Z del vértice anterior.
    '''
    zPrevia = None

    for coordenada in geometry:
        if zPrevia is None:
            zPrevia = coordenada[2]
            continue
            
        zActual = coordenada[2]

        if zActual >= zPrevia:
            return digi3d.GeometryError("Vértice con la Z superior o igual al anterior", coordenada)

        zPrevia = zActual

@quality_control()
def debe_tener_coordenadas_z_decrecientes_moderado(geometry, adding_geometry, code_index):
    '''Comunica un error si se localiza un vértice cuya coordenada Z sea superior a la coordenada Z del vértice anterior.
    '''
    zPrevia = geometry[0][2]

    for coordenada in geometry:
        zActual = coordenada[2]

        if zActual > zPrevia:
            return digi3d.GeometryError("Vértice con la Z superior al anterior", coordenada)

        zPrevia = zActual

def cuyas_maximas_minimas_solapen_con(geometrías, geometria):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que no están eliminadas.
    Argumentos:
        geometrías: Geometrías a analizar.
    '''
    return filter(lambda g : g.maxmin_overlaps(geometria), geometrías)


@quality_control()
def al_cruzar_con_lineas_debe_haber_una_diferencia_de_z_inferior_a(geometry, adding_geometry, code_index, código_o_etiqueta_analizar, tolerancia):
    '''
    Comunica un error si se localiza un cruce con otra línea y la diferencia en coordenadas Z entre las dos líneas es superior a una tolerancia.
    '''
    candidatos = no_eliminadas(digi3d.current_view())
    candidatos2 = cuyas_maximas_minimas_solapen_con(candidatos, geometry)
    candidatos3 = que_tengan_el_codigo_o_etiqueta(candidatos2, código_o_etiqueta_analizar)
    
    intersecciones = digi3d.get_intersections(geometry, candidatos3)
    for coordenadas_interseccion in intersecciones:
        geometrias_que_llegan_a_esta_interseccion = intersecciones[coordenadas_interseccion]
        vertice_geometria_analizando = geometrias_que_llegan_a_esta_interseccion[geometry]
        coordenada_de_geometria_analizando = geometry[vertice_geometria_analizando]
        coordenada_z_comparar = coordenada_de_geometria_analizando[2]

        for otra_geometria in geometrias_que_llegan_a_esta_interseccion:
            if otra_geometria == geometry:
                continue

            vertice_otra_geometria = geometrias_que_llegan_a_esta_interseccion[otra_geometria]
            coordenada_z_otra_geometria = otra_geometria[vertice_otra_geometria][2]

            diferenciaZ = abs(coordenada_z_otra_geometria - coordenada_z_comparar)
            if diferenciaZ > tolerancia:
                return digi3d.GeometryError("Intersección en la que la diferencia en coordenada Z es {} (superior a {})".format(diferenciaZ, tolerancia), coordenada_de_geometria_analizando)

@quality_control()
def al_cruzar_con_lineas_debe_haber_una_diferencia_de_z_superior_a(geometry, adding_geometry, code_index, código_o_etiqueta_analizar, tolerancia):
    '''
    Comunica un error si se localiza un cruce con otra línea y la diferencia en coordenadas Z entre las dos líneas es superior a una tolerancia.
    '''
    candidatos = no_eliminadas(digi3d.current_view())
    candidatos2 = cuyas_maximas_minimas_solapen_con(candidatos, geometry)
    candidatos3 = que_tengan_el_codigo_o_etiqueta(candidatos2, código_o_etiqueta_analizar)
    
    intersecciones = digi3d.get_intersections(geometry, candidatos3)
    for coordenadas_interseccion in intersecciones:
        geometrias_que_llegan_a_esta_interseccion = intersecciones[coordenadas_interseccion]
        vertice_geometria_analizando = geometrias_que_llegan_a_esta_interseccion[geometry]
        coordenada_de_geometria_analizando = geometry[vertice_geometria_analizando]
        coordenada_z_comparar = coordenada_de_geometria_analizando[2]

        for otra_geometria in geometrias_que_llegan_a_esta_interseccion:
            if otra_geometria == geometry:
                continue

            vertice_otra_geometria = geometrias_que_llegan_a_esta_interseccion[otra_geometria]
            coordenada_z_otra_geometria = otra_geometria[vertice_otra_geometria][2]

            diferenciaZ = abs(coordenada_z_otra_geometria - coordenada_z_comparar)
            if diferenciaZ <= tolerancia:
                return digi3d.GeometryError("Intersección en la que la diferencia en coordenada Z es {} (inferior a {})".format(diferenciaZ, tolerancia), coordenada_de_geometria_analizando)
