''' Utilidades para geometrías '''

def TieneElCódigo(g, código):
    '''Indica si la entidad tiene alguno de los códigos pasados por parámetro.
    Argumentos:
        entidad: Entidad sobre la que realizar la consulta.
        códigos: conjunto de códigos.
    Observaciones:
        Esta función devuelve verdadero si se encuentra al menos un código de los pasados por parámetros
        de entre los códigos que tiene la entidad.
    '''
    for codigoEntidad in g.Codes:
        if g.Name == código:
            return True
    return False

def TieneAlgúnCódigo(g, códigos):
    '''Indica si la entidad tiene alguno de los códigos pasados por parámetro.
    Argumentos:
        entidad: Entidad sobre la que realizar la consulta.
        códigos: conjunto de códigos.
    Observaciones:
        Esta función devuelve verdadero si se encuentra al menos un código de los pasados por parámetros
        de entre los códigos que tiene la entidad.
    '''
    códigosEntidad = { cod.Name for cod in g.Codes }
    return len(códigos.intersection(códigosEntidad)) > 0

''' Utilidades para secuencias de geometrías '''

def Eliminadas(geometrías):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que  están eliminadas.
    Argumentos:
        geometrías: Geometrías a analizar.
    '''
    return filter(lambda geometría : geometría.Deleted, geometrías)

def NoEliminadas(geometrías):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que no están eliminadas.
    Argumentos:
        geometrías: Geometrías a analizar.
    '''
    return filter(lambda geometría : not geometría.Deleted, geometrías)

def QueTenganElCódigo(geometrías, código):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que tienen el código indicado.
    Argumentos:
        geometrías: Geometrías a analizar.
        código: Código a localizar
    '''
    return filter(lambda geometría : TieneElCódigo(geometría, código), geometrías)

def QueTenganAlgúnCódigo(geometrías, códigos):
    '''Devuelve el subconjunto de las geometrías pasadas por parámetro que tienen el código indicado.
    Argumentos:
        geometrías: Geometrías a analizar.
        código: Código a localizar
    '''
    return filter(lambda geometría : TieneAlgúnCódigo(geometría, códigos), geometrías)

''' Controles de calidad '''

def DebeSerPunto():
    '''
    Comunica un error si la geometría no es de tipo Punto
    '''
    global g
    if type(g) is not Point:
	    raise GeometryException('Las geometrías con este código deben ser de tipo Punto', g.Points[0])

def DebeSerLinea():
    '''
    Comunica un error si la geometría no es de tipo Línea
    '''
    global g
    if type(g) is not Line:
	    raise GeometryException('Las geometrías con este código deben ser de tipo Linea', g.Points[0])

def DebeSerTexto():
    '''
    Comunica un error si la geometría no es de tipo Texto
    '''
    global g
    if type(g) is not Text:
	    raise GeometryException('Las geometrías con este código deben ser de tipo Texto', g.Points[0])

def DebeSerPoligono():
    '''
    Comunica un error si la geometría no es de tipo Polígono
    '''
    global g
    if type(g) is not Polygon:
	    raise GeometryException('Las geometrías con este código deben ser de tipo Polígono', g.Points[0])

def DebeSerComplejo():
    '''
    Comunica un error si la geometría no es de tipo Complejo
    '''
    global g
    if type(g) is not Complex:
	    raise GeometryException('Las geometrías con este código deben ser de tipo Complejo', g.Points[0])

def DebeTenerUnUnicoCodigo():
    '''
    Comunica un error si la geometría tiene más de un código
    '''
    if g.Codes.Count > 1:
	    raise GeometryException('Las geometrías con este código deben tener un único código', g.Points[0])

def DebeTenerXCodigos(x):
    '''
    Comunica un error si la geometría no tiene X códigos
    '''
    if g.Codes.Count != x:
	    raise GeometryException('Las geometrías con este código deben tener {} códigos'.format(x), g.Points[0])

def DebeTenerAlMenosXCodigos(x):
    '''
    Comunica un error si la geometría no tiene al menos X códigos
    '''
    if g.Codes.Count < x:
	    raise GeometryException('Las geometrías con este código deben tener al menos {} códigos'.format(x), g.Points[0])

def DebeTenerMasDeXCodigos(x):
    '''
    Comunica un error si la geometría no tiene más de X códigos
    '''
    if g.Codes.Count <= x:
	    raise GeometryException('Las geometrías con este código deben tener más de {} códigos'.format(x), g.Points[0])

def DebeTenerUnAreaSuperiorA(valor):
    '''
    Comunica un error si la geometría tiene un área inferior a X
    '''
    global g
    if type(g) is not Line and type(g) is not Polygon:
        return
    
    if g.Area <= valor:
	    raise GeometryException('Las geometrías con este código deben tener un área superior a {}'.format(valor), g.Points[0])

def DebeTenerUnAreaSuperiorOIgualA(valor):
    '''
    Comunica un error si la geometría tiene un área inferior a X
    '''
    global g
    if type(g) is not Line and type(g) is not Polygon:
        return
    
    if g.Area < valor:
	    raise GeometryException('Las geometrías con este código deben tener un área superior o igual a {}'.format(valor), g.Points[0])

def DebeTenerUnAreaInferiorA(valor):
    '''
    Comunica un error si la geometría tiene un área superior o igual a X
    '''
    global g
    if type(g) is not Line and type(g) is not Polygon:
        return
    
    if g.Area >= valor:
	    raise GeometryException('Las geometrías con este código deben tener un área inferior a {}'.format(valor), g.Points[0])

def DebeTenerUnAreaInferiorOIgualAA(valor):
    '''
    Comunica un error si la geometría tiene un área superior o igual a X
    '''
    global g
    if type(g) is not Line and type(g) is not Polygon:
        return
    
    if g.Area > valor:
	    raise GeometryException('Las geometrías con este código deben tener un área inferior o igual a {}'.format(valor), g.Points[0])

def NoPuedeTenerVerticeConZSuperiorAVerticeAnterior():
    '''Analiza los vértices de la geometría y comunica un error si se localiza un vértice cuya coordenada Z sea
    superior a la coordenada Z del vértice anterior.
    '''
    global g
    zPrevia = g.Points[0].Z

    for vertice in range(1, g.Points.Count):
        zActual = g.Points[vertice].Z

        if zActual > zPrevia:
            raise GeometryException("Vértice con la Z superior al anterior", g.Points[vertice])

        zPrevia = zActual

def NoPuedeTenerVerticeConZSuperiorOIgualAVerticeAnterior():
    '''
    Analiza los vértices de la geometría y comunica un error si se localiza un vértice cuya coordenada Z sea
    superior o igual a la coordenada Z del vértice anterior.
    '''
    global g
    zPrevia = g.Points[0].Z

    for vertice in range(1, g.Points.Count):
        zActual = g.Points[vertice].Z

        if zActual >= zPrevia:
            raise GeometryException("Vértice con la Z superior o igual al anterior", g.Points[vertice])

        zPrevia = zActual

def NoPuedeTenerVerticeConZInferiorAVerticeAnterior():
    '''
    Analiza los vértices de la geometría y comunica un error si se localiza un vértice cuya coordenada Z sea
    inferior a la coordenada Z del vértice anterior.
    '''
    global g
    zPrevia = g.Points[0].Z

    for vertice in range(1, g.Points.Count):
        zActual = g.Points[vertice].Z

        if zActual < zPrevia:
            raise GeometryException("Vértice con la Z inferior al anterior", g.Points[vertice])

        zPrevia = zActual

def NoPuedeTenerVerticeConZInferiorOIgualAVerticeAnterior():
    '''
    Analiza los vértices de la geometría y comunica un error si se localiza un vértice cuya coordenada Z sea
    inferior o igual a la coordenada Z del vértice anterior.
    '''
    global g
    zPrevia = g.Points[0].Z

    for vertice in range(1, g.Points.Count):
        zActual = g.Points[vertice].Z

        if zActual <= zPrevia:
            raise GeometryException("Vértice con la Z inferior o igual al anterior", g.Points[vertice])

        zPrevia = zActual
