import digi3d
import digi3d.relations

'Utilidades que usan los controles de calidad'

def distancia_menor_que(a, b, calculadora, distancia):
    'Calcula la distancia entre los vértices de los puntos y devuelve True si se localiza algún par para el cual la distancia es inferior al valor pasado por parámetros.'
    for coordenada_a in a:
        for coordenada_b in b:
            if calculadora.calculate_distance_2d(coordenada_a, coordenada_b) < distancia:
                return True

    return False

def es_curva_fina_o_maestra(coordenada_z, equidistancia):
    return 0 == coordenada_z % equidistancia

def es_maestra(coordenada_z, equidistancia, intervalo_maestras=5):
    'Devuelve verdadero si la coordenada Z pasada por parámetro corresponde a la de una curva de nivel maestra para una equidistancia de curvas y un determinado intervalo de curvas de nivel'
    if not es_curva_fina_o_maestra(coordenada_z, equidistancia):
        return False

    return 0 == coordenada_z % (intervalo_maestras * equidistancia)

def es_fina(coordenada_z, equidistancia, intervalo_maestras=5):
    'Devuelve verdadero si la coordenada Z pasada por parámetro corresponde a la de una curva de nivel maestra para una equidistancia de curvas y un determinado intervalo de curvas de nivel'
    if not es_curva_fina_o_maestra(coordenada_z, equidistancia):
        return False

    return 0 != coordenada_z % (intervalo_maestras * equidistancia)

def es_area(g):
    'Devuelve verdadero si la geometría es de tipo área (polígono o línea cerrada)'

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
    'Analiza si la geometría tiene algún código de entre los códigos (de la tabla de códigos activa) que tienen asignada una determinada etiqueta'

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
    for codigo in nombre_codigo_o_etiqueta.split():
        if codigo[0] == '#':
            if tiene_algun_codigo_de_etiqueta(g, codigo[1:]):
                return True

        if tiene_el_codigo_con_comodines(g, codigo):
            return True
        
    return False

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

' Utilidades para secuencias de geometrías '

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
    'Itera por todas las geometrías del archivo de dibujo y devuelve verdadero si se localiza una con la que devuelvan True tanto la función callback_incluir_geometria como la función callback_concicion'
    for g in no_eliminadas(digi3d.current_view()):
        # No contamos la geometría que se está analizando
        if g == geometría_analizando:
            pass
        
        if not callback_incluir_geometria(g):
            continue

        if callback_condicion(g):
            return True

    return False

def algun_area_con_codigo(geometría_analizando, código_o_etiqueta_areas_analizar, callback_condicion):
    return alguna_geometria(geometría_analizando, lambda g: es_area(g) and tiene_el_codigo_o_etiqueta(g, código_o_etiqueta_areas_analizar), callback_condicion)

def alguna_linea_con_codigo(geometría_analizando, código_o_etiqueta_lineas_analizar, callback_condicion):
    return alguna_geometria(geometría_analizando, lambda g: type(g) is digi3d.Line and tiene_el_codigo_o_etiqueta(g, código_o_etiqueta_lineas_analizar), callback_condicion)

def alguna_linea_sin_codigo(geometría_analizando, código_o_etiqueta_lineas_analizar, callback_condicion):
    return alguna_geometria(geometría_analizando, lambda g: type(g) is digi3d.Line and not tiene_el_codigo_o_etiqueta(g, código_o_etiqueta_lineas_analizar), callback_condicion)

def algun_punto_con_codigo(geometría_analizando, código_o_etiqueta_puntos_analizar, callback_condicion):
    return alguna_geometria(geometría_analizando, lambda g: type(g) is digi3d.Point and tiene_el_codigo_o_etiqueta(g, código_o_etiqueta_puntos_analizar), callback_condicion)

def algun_texto_con_codigo(geometría_analizando, código_o_etiqueta_textos_analizar, callback_condicion):
    return alguna_geometria(geometría_analizando, lambda g: type(g) is digi3d.Text and tiene_el_codigo_o_etiqueta(g, código_o_etiqueta_textos_analizar), callback_condicion)

def cuyas_maximas_minimas_solapen_con(geometrías, geometria):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que no están eliminadas.
    Argumentos:
        geometrías: Geometrías a analizar.
    '''
    return filter(lambda g : g.maxmin_overlaps_2d(geometria), geometrías)

'Controles de calidad'

@quality_control()
def si_es_area_debe_ser_adyacente_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un área, comunica un error si no se localiza ningún área en el archivo de dibujo que sea adyacente al área que se está analizando'
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.adjacent(área, geometry)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_area_debe_estar_completamente_dentro_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un área, comunica un error si no se localiza en el archivo de dibujo otro área que dentro de la cual esté la geometría que se está analizando (no se admite que determinados vértices de este área coincidan con la del otro área)'
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.completely_within(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_area_debe_estar_dentro_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un área, comunica un error si no se localiza en el archivo de dibujo otro área que dentro de la cual esté la geometría que se está analizando (se admite que determinados vértices de este área coincidan con la del otro área)'
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.within(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_area_debe_ser_estar_separado_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un área, comunica un error si se localiza en el archivo de dibujo otra área que no sea disjunta (es decir, que solape, cruce, esté en el interior...) de la geometría ques e está analizando'
    if not es_area(geometry):
        return

    if algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: not digi3d.relations.AreaArea.disjoint(área, geometry)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_area_debe_ser_igual_a_otra_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un área, comunica un error si no se localiza en el archivo de dibujo otro área que sea idéntica a la geometría que se está analizando'
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.equal(área, geometry)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_area_debe_unirse_con_otra_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un área, comunica un error si no se localiza en el archivo de dibujo un área que se una con la geometría que se está analizando'
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.join(área, geometry)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_area_debe_solapar_otra_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un área, comunica un error si no se localiza en el archivo de dibujo un área que solape el área que se está analizando.'
    if not es_area(geometry):
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.overlap(geometry, área)[0]):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_area_no_puede_solapar_otra_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un área, comunica un error si se localiza en el archivo de dibujo un área que solape el área que se está analizando.'
    if not es_area(geometry):
        return

    if algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.AreaArea.overlap(geometry, área)[0]):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_tener_asignado_un_atributo(geometry, adding_geometry, code_index, nombre_atributo, valor_esperado, mensaje):
    'Comunica un error si el código que se está analizando no tiene entre sus atributos el atributo pasado por parámetros o si el valor de este atributo no coincide con el del valor esperado'
    atributos = geometry.attributes

    if nombre_atributo not in atributos:
        return digi3d.GeometryError('Se esperaba que esta geometría tuviera un atributo con nombre {} pero no lo tiene'.format(nombre_atributo))

@quality_control()
def debe_tener_asignado_un_atributo_con_valor_igual_a(geometry, adding_geometry, code_index, nombre_atributo, valor_esperado, mensaje):
    'Comunica un error si el código que se está analizando no tiene entre sus atributos el atributo pasado por parámetros o si el valor de este atributo no coincide con el del valor esperado'
    atributos = geometry.attributes

    if nombre_atributo not in atributos:
        return digi3d.GeometryError('Se esperaba que esta geometría tuviera un atributo con nombre {} pero no lo tiene'.format(nombre_atributo))

    if atributos[nombre_atributo] != valor_esperado:
        return digi3d.GeometryError(mensaje)

@quality_control()
def atributo_bbdd_no_puede_ser_nulo(geometry, adding_geometry, code_index, nombre_atributo):
    'Comunica un error si el código que se está analizando no tiene entre sus atributos el atributo pasado por parámetros o si el valor de este atributo es nulo'
    atributosCodigo = geometry.codes[code_index].attributes

    if nombre_atributo not in atributosCodigo:
        return digi3d.GeometryError('Se esperaba que el código {} de esta geometría tuviera un atributo con nombre {} pero no lo tiene'.format(geometry.codes[code_index].name, nombre_atributo))

    if atributosCodigo[nombre_atributo] is None:
        return digi3d.DatabaseFieldError('Atributo con valor nulo', code_index, nombre_atributo)

@quality_control()
def atributo_bbdd_debe_ser_igual(geometry, adding_geometry, code_index, nombre_atributo, valor_esperado, mensaje):
    'Comunica un error si el código que se está analizando no tiene entre sus atributos el atributo pasado por parámetros o si el valor de este atributo no coincide con el del valor esperado'
    atributosCodigo = geometry.codes[code_index].attributes

    if nombre_atributo not in atributosCodigo:
        return digi3d.GeometryError('Se esperaba que el código {} de esta geometría tuviera un atributo con nombre {} pero no lo tiene'.format(geometry.codes[code_index].name, nombre_atributo))

    if atributosCodigo[nombre_atributo] is None or atributosCodigo[nombre_atributo] != valor_esperado:
        return digi3d.DatabaseFieldError(mensaje, code_index, nombre_atributo)

@quality_control()
def atributo_bbdd_debe_ser_mayor_o_igual(geometry, adding_geometry, code_index, nombre_atributo, valor, mensaje):
    'Comunica un error si el código que se está analizando no tiene entre sus atributos el atributo pasado por parámetros o si el valor de este atributo es menor que el valor esperado'
    atributosCodigo = geometry.codes[code_index].attributes

    if nombre_atributo not in atributosCodigo:
        return digi3d.GeometryError('Se esperaba que el código {} de esta geometría tuviera un atributo con nombre {} pero no lo tiene'.format(geometry.codes[code_index].name, nombre_atributo))

    if atributosCodigo[nombre_atributo] is None or atributosCodigo[nombre_atributo] < valor:
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_ser_adyacente_a_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si no se localiza en el archivo de dibujo un área que solape dicha línea.'
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.adjacent(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_estar_completamente_dentro_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si no se localiza en el archivo de dibujo un área que solape dicha línea. '
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.within(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_cruzar_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si esta no cruza ningún área del archivo de dibujo. '
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.across(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_cruzar_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si esta no cruza ningún área del archivo de dibujo.'
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.across(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_estar_separado_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si esta toca (cruza, está dentro, etc) algún área del archivo de dibujo.'
    if type(geometry) is not digi3d.Line:
        return

    if algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: not digi3d.relations.LineArea.disjoint(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_estar_separado_de_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si se encuentra en el archivo de dibujo otra línea que no sea disjunta con esta.'
    if type(geometry) is not digi3d.Line:
        return

    if alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: not digi3d.relations.LineLine.disjoint(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_ser_igual_a_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si se encuentra en el archivo de dibujo otra línea que no sea igual que esta.'
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.equal(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_unirse_con_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si esta no se une con algún área del archivo de dibujo.'
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.join(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_unirse_con_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error ésta no se une con ninguna línea del archivo de dibujo.'
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.join(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_solapar_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error ésta no solapa con ninguna línea del archivo de dibujo.'
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.overlap(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_terminar_dentro_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si esta no termina dentro de un área del archivo de dibujo.'
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.terminates_within(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_terminar_en_borde_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si esta no termina en el borde de un área del archivo de dibujo.'
    if type(geometry) is not digi3d.Line:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.LineArea.endpoint_join(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_terminar_en_extremo_de_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error ésta no termina en el extremo de otra línea del archivo de dibujo.'
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.endpoint_join_endpoint(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_linea_debe_terminar_en_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error ésta no termina en otra línea del archivo de dibujo.'
    if type(geometry) is not digi3d.Line:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.endpoint_join_excluding_endpoints(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_punto_debe_coincidir_con_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un punto, comunica un error si este no coincide con un área del archivo de dibujo.'
    if type(geometry) is not digi3d.Point:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.PointArea.coincident(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_punto_debe_coincidir_con_extremo_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es un punto, comunica un error si este no termina en el extremo de otra línea del archivo de dibujo.'
    if type(geometry) is not digi3d.Point:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.PointLine.coincident_and_terminate(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_punto_debe_coincidir_con_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es un punto, comunica un error si este no termina en una línea (excluyendo sus extremos) del archivo de dibujo.'
    if type(geometry) is not digi3d.Point:
        return

    if not alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.PointLine.coincident(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_punto_debe_coincidir_con_punto(geometry, adding_geometry, code_index, código_o_etiqueta_puntos_analizar, mensaje):
    'Si la geometría que se está analizando es un punto, comunica un error si este no coincide con otro punto del archivo de dibujo.'
    if type(geometry) is not digi3d.Point:
        return

    if not algun_punto_con_codigo(geometry, código_o_etiqueta_puntos_analizar, lambda punto: digi3d.relations.PointPoint.coincident(geometry, punto)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_punto_debe_estar_separado_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un punto, comunica un error si este no es disjunto con algún área del archivo de dibujo.'
    if type(geometry) is not digi3d.Point:
        return

    if algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: not digi3d.relations.PointArea.disjoint(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_punto_debe_estar_separado_de_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es un punto, comunica un error si este no es disjunto con alguna línea del archivo de dibujo.'
    if type(geometry) is not digi3d.Point:
        return

    if alguna_linea_con_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: not digi3d.relations.PointLine.disjoint(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_punto_debe_estar_separado_de_punto(geometry, adding_geometry, code_index, código_o_etiqueta_puntos_analizar, mensaje):
    'Si la geometría que se está analizando es un punto, comunica un error si este no es disjunto con otro punto del archivo de dibujo.'
    if type(geometry) is not digi3d.Point:
        return

    if algun_punto_con_codigo(geometry, código_o_etiqueta_puntos_analizar, lambda punto: not digi3d.relations.PointPoint.disjoint(geometry, punto)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def si_es_punto_debe_estar_en_el_interior_de_area(geometry, adding_geometry, code_index, código_o_etiqueta_areas_analizar, mensaje):
    'Si la geometría que se está analizando es un punto, comunica un error si este no está en el interior de algún área del archivo de dibujo.'
    if type(geometry) is not digi3d.Point:
        return

    if not algun_area_con_codigo(geometry, código_o_etiqueta_areas_analizar, lambda área: digi3d.relations.PointArea.within(geometry, área)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def debe_ser_area(geometry, adding_geometry, code_index):
    'Comunica un error si la geometría no es de tipo área (polígonos o líneas cerradas)'
    if not es_area(geometry):
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser polígonos o líneas cerradas'.format(geometry.codes[0].name))

@quality_control()
def debe_ser_complejo(geometry, adding_geometry, code_index):
    'Comunica un error si la geometría no es de tipo Complejo'
    if type(geometry) is not digi3d.Complex:
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser de tipo Texto'.format(geometry.codes[0].name))

@quality_control()
def debe_ser_linea(geometry, adding_geometry, code_index):
    'Comunica un error si la geometría no es de tipo Línea'
    if type(geometry) is not digi3d.Line:
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser de tipo Línea'.format(geometry.codes[0].name))

@quality_control()
def debe_ser_poligono(geometry, adding_geometry, code_index):
    'Comunica un error si la geometría no es de tipo Polígono'
    if type(geometry) is not digi3d.Polygon:
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser de tipo Polígono'.format(geometry.codes[0].name))

@quality_control()
def debe_ser_punto(geometry, adding_geometry, code_index):
    'Comunica un error si la geometría no es de tipo Punto'
    if type(geometry) is not digi3d.Point:
	    return digi3d.GeometryError('Las geometrías con el código {} deben ser de tipo Punto'.format(geometry.codes[0].name))

@quality_control()
def debe_ser_texto(geometry, adding_geometry, code_index):
    'Comunica un error si la geometría no es de tipo Texto'
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
    'Comunica un error si localiza un vértice con la coordenada Z distinta de la del vértice anterior'
    if not digi3d.same_coordinates(geometry.min[2], geometry.max[2]):
        return digi3d.GeometryError('Las geometrías con este código deben tener todos los vértices con la misma coordenada Z {} ({})'.format(coordenada[2], zInicial), coordenada)

@quality_control()
def debe_tener_coordenadas_z_crecientes(geometry, adding_geometry, code_index):
    'Comunica un error si se localiza un vértice cuya coordenada Z sea inferior o igual a la coordenada Z del vértice anterior.'
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
    'Comunica un error si se localiza un vértice cuya coordenada Z sea inferior a la coordenada Z del vértice anterior.'
    zPrevia = geometry[0][2]

    for coordenada in geometry:
        zActual = coordenada[2]

        if zActual < zPrevia:
            return digi3d.GeometryError("Vértice con la Z inferior al anterior", coordenada)

        zPrevia = zActual

@quality_control()
def debe_tener_coordenadas_z_decrecientes(geometry, adding_geometry, code_index):
    'Comunica un error si se localiza un vértice cuya coordenada Z sea superior o igual a la coordenada Z del vértice anterior.'
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
    'Comunica un error si se localiza un vértice cuya coordenada Z sea superior a la coordenada Z del vértice anterior.'
    zPrevia = geometry[0][2]

    for coordenada in geometry:
        zActual = coordenada[2]

        if zActual > zPrevia:
            return digi3d.GeometryError("Vértice con la Z superior al anterior", coordenada)

        zPrevia = zActual

@quality_control()
def al_tocar_lineas_debe_haber_una_diferencia_de_z_inferior_a(geometry, adding_geometry, code_index, código_o_etiqueta_analizar, tolerancia):
    'Comunica un error si se localiza un cruce con otra línea y la diferencia en coordenadas Z entre las dos líneas es superior a una tolerancia.'
    candidatos = no_eliminadas(digi3d.current_view())
    candidatos = cuyas_maximas_minimas_solapen_con(candidatos, geometry)
    candidatos = que_tengan_el_codigo_o_etiqueta(candidatos, código_o_etiqueta_analizar)

    errores_detectados = []

    intersecciones = digi3d.get_intersections(geometry, candidatos)
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
            if diferenciaZ >= tolerancia:
                errores_detectados.append(digi3d.GeometryError("Las geometrías se tocan con una diferencia en la coordenada Z de {} (superior o igual a {})".format(diferenciaZ, tolerancia), coordenada_de_geometria_analizando))

                if adding_geometry:
                    # Si estamos en modo interactivo, nos sobra con informarle al usuario del primer error
                    return errores_detectados

    return errores_detectados

@quality_control()
def al_tocar_lineas_debe_haber_una_diferencia_de_z_inferior_o_igual_a(geometry, adding_geometry, code_index, código_o_etiqueta_analizar, tolerancia):
    'Comunica un error si se localiza un cruce con otra línea y la diferencia en coordenadas Z entre las dos líneas es superior a una tolerancia.'
    candidatos = no_eliminadas(digi3d.current_view())
    candidatos = cuyas_maximas_minimas_solapen_con(candidatos, geometry)
    candidatos = que_tengan_el_codigo_o_etiqueta(candidatos, código_o_etiqueta_analizar)
    
    errores_detectados = []

    intersecciones = digi3d.get_intersections(geometry, candidatos)
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
                errores_detectados.append(digi3d.GeometryError("Las geometrías se tocan con una diferencia en la coordenada Z de {} (superior a {})".format(diferenciaZ, tolerancia), coordenada_de_geometria_analizando))

                if adding_geometry:
                    # Si estamos en modo interactivo, nos sobra con informarle al usuario del primer error
                    return errores_detectados

    return errores_detectados

@quality_control()
def al_tocar_lineas_debe_haber_una_diferencia_de_z_superior_a(geometry, adding_geometry, code_index, código_o_etiqueta_analizar, tolerancia):
    'Comunica un error si se localiza un cruce con otra línea y la diferencia en coordenadas Z entre las dos líneas es superior a una tolerancia.'
    candidatos = no_eliminadas(digi3d.current_view())
    candidatos = cuyas_maximas_minimas_solapen_con(candidatos, geometry)
    candidatos = que_tengan_el_codigo_o_etiqueta(candidatos, código_o_etiqueta_analizar)
    
    errores_detectados = []

    intersecciones = digi3d.get_intersections(geometry, candidatos)
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
                errores_detectados.append(digi3d.GeometryError("Las geometrías se tocan con una diferencia en la coordenada Z de {} (inferior o igual a {})".format(diferenciaZ, tolerancia), coordenada_de_geometria_analizando))

                if adding_geometry:
                    # Si estamos en modo interactivo, nos sobra con informarle al usuario del primer error
                    return errores_detectados

    return errores_detectados

@quality_control()
def al_tocar_lineas_debe_haber_una_diferencia_de_z_superior_o_igual_a(geometry, adding_geometry, code_index, código_o_etiqueta_analizar, tolerancia):
    'Comunica un error si se localiza un cruce con otra línea y la diferencia en coordenadas Z entre las dos líneas es superior a una tolerancia.'
    candidatos = no_eliminadas(digi3d.current_view())
    candidatos = cuyas_maximas_minimas_solapen_con(candidatos, geometry)
    candidatos = que_tengan_el_codigo_o_etiqueta(candidatos, código_o_etiqueta_analizar)
    
    errores_detectados = []

    intersecciones = digi3d.get_intersections(geometry, candidatos)
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
            if diferenciaZ < tolerancia:
                errores_detectados.append(digi3d.GeometryError("Las geometrías se tocan con una diferencia en la coordenada Z de {} (inferior a {})".format(diferenciaZ, tolerancia), coordenada_de_geometria_analizando))

                if adding_geometry:
                    # Si estamos en modo interactivo, nos sobra con informarle al usuario del primer error
                    return errores_detectados

    return errores_detectados

@quality_control()
def al_tocar_lineas_debe_haber_una_diferencia_de_z_igual_a(geometry, adding_geometry, code_index, código_o_etiqueta_analizar, tolerancia):
    'Comunica un error si se localiza un cruce con otra línea y la diferencia en coordenadas Z entre las dos líneas es superior a una tolerancia.'
    candidatos = no_eliminadas(digi3d.current_view())
    candidatos = cuyas_maximas_minimas_solapen_con(candidatos, geometry)
    candidatos = que_tengan_el_codigo_o_etiqueta(candidatos, código_o_etiqueta_analizar)
    
    errores_detectados = []

    intersecciones = digi3d.get_intersections(geometry, candidatos)
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
            if diferenciaZ != tolerancia:
                errores_detectados.append(digi3d.GeometryError("Intersección en la que la diferencia en coordenada Z es {} (distinto a {})".format(diferenciaZ, tolerancia), coordenada_de_geometria_analizando))

                if adding_geometry:
                    # Si estamos en modo interactivo, nos sobra con informarle al usuario del primer error
                    return errores_detectados

    return errores_detectados

@quality_control()
def si_es_linea_no_puede_cruzar_linea(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error si esta se cruza con otra línea.'
    if type(geometry) is not digi3d.Line:
        return

    candidatos = no_eliminadas(digi3d.current_view())
    candidatos = cuyas_maximas_minimas_solapen_con(candidatos, geometry)
    candidatos = que_tengan_el_codigo_o_etiqueta(candidatos, código_o_etiqueta_lineas_analizar)

    errores_detectados = []

    for candidato in candidatos:
        if candidato == geometry:
            continue

        vertices_de_cruce = digi3d.relations.LineLine.get_cross_vertices(geometry, candidato, adding_geometry)
        if len(vertices_de_cruce) == 0:
            continue
        
        if adding_geometry:
            return digi3d.GeometryRelationError(candidato, mensaje, geometry[vertices_de_cruce[0]])

        for vertice in vertices_de_cruce:
            errores_detectados.append(digi3d.GeometryRelationError(candidato, mensaje, geometry[vertice]))

    if len(errores_detectados) == 0:
        return

    return errores_detectados  

@quality_control()
def no_puede_estar_a_menor_distancia_que(geometry, adding_geometry, code_index, código_o_etiqueta_puntos_analizar, distancia):
    'Si la geometría que se está analizando es de tipo punto, comprueba su distancia al resto de puntos del archivo de dibujo y devuelve error en caso de que esta sea inferior al parámetro distancia'
    if type(geometry) is not digi3d.Point:
        return

    v = digi3d.current_view()

    # No podemos calcular la distancia entre puntos sin más, porque puede que la ventana de dibujo esté en coordenadas elipsoidales, de manera que las
    # coordenadas que nos van a llegar no son ortométricas, sino ángulos. La ventana de dibujo proporciona una calculadora geográfica que calcula 
    # distancias correctamente
    calculadora  = v.geographic_calculator

    lista_de_puntos_cercanos = []
    
    for otra_geometria in que_tengan_algun_codigo_de_etiqueta(no_eliminadas(v), código_o_etiqueta_puntos_analizar):
        if otra_geometria == geometry:
            continue

        if distancia_menor_que(geometry, otra_geometria, calculadora, distancia):
            lista_de_puntos_cercanos.append(otra_geometria)

            if adding_geometry:
                # Estamos en modo interactivo: El usuario está digitalizando una geometría, de manera que con detectar el primer error es suficiente
                break

    if( len(lista_de_puntos_cercanos) > 0):
        return digi3d.GeometryRelationError(lista_de_puntos_cercanos, 'Este punto está muy cerca de estos puntos')

@quality_control()
def si_es_linea_solo_puede_continuar_con_lineas_con_codigo(geometry, adding_geometry, code_index, código_o_etiqueta_lineas_analizar, mensaje):
    'Si la geometría que se está analizando es una línea, comunica un error ésta continua con otra que no tenga el código o códigos especificados.'
    if type(geometry) is not digi3d.Line:
        return

    if alguna_linea_sin_codigo(geometry, código_o_etiqueta_lineas_analizar, lambda línea: digi3d.relations.LineLine.endpoint_join_endpoint(geometry, línea)):
        return digi3d.GeometryError(mensaje)

@quality_control()
def marcar_error_si_diferencia_z_al_proyectar_mdt_superior_a(geometry, adding_geometry, code_index, distancia):
    'Proyecta los vértices de la geometría contra los MDTs cargados y genera un error si la diferencia en la coordenada Z entre un vértice y algún MDT es superior a una distancia'
    v = digi3d.current_view()

    for coordenada in geometry:
        z_proyectada = v.project(coordenada)

        if z_proyectada is None:
            continue

        distancia_calculada = abs(z_proyectada - coordenada[2])
        if distancia_calculada > distancia:
            return digi3d.GeometryError('Vértice de la geometría con una diferencia en Z con respecto al MDT de: {} que es superior a: {}'.format(distancia_calculada, distancia), coordenada)

@quality_control()
def marcar_error_si_diferencia_z_al_proyectar_mdt_inferior_a(geometry, adding_geometry, code_index, distancia):
    'Proyecta los vértices de la geometría contra los MDTs cargados y genera un error si la diferencia en la coordenada Z entre un vértice y algún MDT es inferior a una distancia'
    v = digi3d.current_view()

    for coordenada in geometry:
        z_proyectada = v.project(coordenada)

        if z_proyectada is None:
            continue

        distancia_calculada = abs(z_proyectada - coordenada[2])
        if distancia_calculada < distancia:
            return digi3d.GeometryError('Vértice de la geometría con una diferencia en Z con respecto al MDT de: {} que es inferior a: {}'.format(distancia_calculada, distancia), coordenada)

@quality_control()
def la_coordenada_z_del_primer_vertice_debe_ser_el_de_una_curva_maestra(geometry, adding_geometry, code_index):
    'Comunica un error si la coordenada Z del primer vértice de la geometría no coincide con las de las curvas de nivel maestras para la equidistancia actual y para un intervalo de curvas de 5'
    if not es_maestra(geometry[0][2], digi3d.current_view().equidistance):
        return digi3d.GeometryError('No es maestra')

@quality_control()
def la_coordenada_z_del_primer_vertice_debe_ser_el_de_una_curva_fina(geometry, adding_geometry, code_index):
    'Comunica un error si la coordenada Z del primer vértice de la geometría no coincide con las de las curvas de nivel finas para la equidistancia actual y para un intervalo de curvas de 5'
    if not es_fina(geometry[0][2], digi3d.current_view().equidistance):
        return digi3d.GeometryError('No es fina')

@quality_control()
def debe_tener_ancho_y_alto_mayor_o_igual_valor_o_linea(geometry, adding_geometry, code_index, ancho, alto):
    'Comunica un error si el ancho y el largo no son mayores que los parámetros'
    ancho_geometria, alto_geometria, _ = geometry.max - geometry.min

    if min(ancho_geometria, alto_geometria) >= ancho and max(ancho_geometria, alto_geometria) >= alto:
        return

    return digi3d.GeometryError('Esta geometría tiene un ancho inferior a {} y un largo inferior a {} y por lo tanto debería haberse digitalizado como una línea')
