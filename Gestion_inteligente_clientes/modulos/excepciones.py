class GICError(Exception):
    """Excepción base del sistema GIC."""


class EmailInvalidoError(GICError):
    pass


class TelefonoInvalidoError(GICError):
    pass


class DireccionInvalidaError(GICError):
    pass


class ClienteExistenteError(GICError):
    pass


class ClienteNoEncontradoError(GICError):
    pass


class ArchivoError(GICError):
    pass
