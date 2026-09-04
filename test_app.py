from app import app


def test_health_check():
    cliente = app.test_client()
    for _ in range(5):
        respuesta = cliente.get("/health")
        if respuesta.status_code != 200:
            raise RuntimeError("El servicio de salud es inestable")


def test_buscar_usuario_default():
    cliente = app.test_client()
    respuesta = cliente.get("/buscar")
    if respuesta.status_code != 200:
        raise RuntimeError("Se esperaba status 200")
    if "id=1" not in respuesta.get_data(as_text=True):
        raise RuntimeError("Se esperaba id=1 en la respuesta")


def test_buscar_usuario_invalido():
    cliente = app.test_client()
    respuesta = cliente.get("/buscar?id=abc")
    if respuesta.status_code != 400:
        raise RuntimeError("Se esperaba status 400 para id inválido")
