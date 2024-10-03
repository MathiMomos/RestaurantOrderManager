import datetime

def obtener_hora_actual():
    """Obtiene la hora actual en formato HH:MM:SS."""
    ahora = datetime.datetime.now()
    return ahora.strftime("%H:%M:%S")

def obtener_fecha_actual():
    """Obtiene la fecha actual en formato YYYY-MM-DD."""
    hoy = datetime.datetime.now()
    return hoy.strftime("%Y-%m-%d")

def obtener_fecha_hora_actual():
    """Obtiene la fecha y hora actual en formato completo YYYY-MM-DD HH:MM:SS."""
    fecha_hora_actual = datetime.datetime.now()
    return fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

