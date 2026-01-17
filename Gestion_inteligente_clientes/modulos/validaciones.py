import re
from .excepciones import EmailInvalidoError, TelefonoInvalidoError, DireccionInvalidaError


_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validar_no_vacio(valor: str, campo: str) -> None:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")


def validar_email(email: str) -> None:
    validar_no_vacio(email, "email")
    if not _EMAIL_RE.match(email.strip()):
        raise EmailInvalidoError("Email inválido. Ej: nombre@dominio.com")


def validar_telefono(telefono: str) -> None:
    validar_no_vacio(telefono, "teléfono")
    tel = telefono.strip().replace(" ", "")
    # Regla simple: 8 a 15 dígitos (puede empezar con +)
    if not re.match(r"^\+?\d{8,15}$", tel):
        raise TelefonoInvalidoError("Teléfono inválido. Usa 8-15 dígitos (opcional +).")


def validar_direccion(direccion: str) -> None:
    validar_no_vacio(direccion, "dirección")
    if len(direccion.strip()) < 5:
        raise DireccionInvalidaError("Dirección inválida. Debe tener al menos 5 caracteres.")
