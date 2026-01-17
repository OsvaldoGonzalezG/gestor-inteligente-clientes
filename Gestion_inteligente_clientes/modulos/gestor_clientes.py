from .excepciones import ClienteExistenteError, ClienteNoEncontradoError
from .logger_config import get_logger


class GestorClientes:
    def __init__(self):
        self._clientes = []
        self._log = get_logger()

    def listar(self):
        return list(self._clientes)

    def existe_email(self, email: str, excluir_id: int = None) -> bool:
        e = email.strip().lower()
        for c in self._clientes:
            if c.email == e and (excluir_id is None or c.id != excluir_id):
                return True
        return False

    def agregar(self, cliente):
        if any(c.id == cliente.id for c in self._clientes):
            self._log.warning(f"Intento de alta duplicada por ID: {cliente.id}")
            raise ClienteExistenteError(f"Ya existe un cliente con ID {cliente.id}")

        if self.existe_email(cliente.email):
            self._log.warning(f"Intento de alta duplicada por email: {cliente.email}")
            raise ClienteExistenteError(f"Ya existe un cliente con email {cliente.email}")

        self._clientes.append(cliente)
        self._log.info(f"Alta cliente: {cliente.id} ({cliente.__class__.__name__})")

    def buscar_por_id(self, id: int):
        for c in self._clientes:
            if c.id == int(id):
                return c
        raise ClienteNoEncontradoError(f"No existe cliente con ID {id}")

    def actualizar(self, id: int, **campos):
        cliente = self.buscar_por_id(id)

        # prevenir email duplicado si se cambia
        if "email" in campos and campos["email"] is not None:
            if self.existe_email(campos["email"], excluir_id=cliente.id):
                self._log.warning(f"Intento de actualización con email duplicado: {campos['email']}")
                raise ClienteExistenteError(f"Ya existe un cliente con email {campos['email']}")

        for k, v in campos.items():
            if v is None:
                continue
            if hasattr(cliente, k):
                setattr(cliente, k, v)
            else:
                # ignoramos campos que no apliquen (o podrías lanzar error)
                pass

        self._log.info(f"Actualización cliente: {cliente.id}")
        return cliente

    def eliminar(self, id: int):
        cliente = self.buscar_por_id(id)
        self._clientes.remove(cliente)
        self._log.info(f"Baja cliente: {id}")

    def resumen_por_tipo(self) -> dict:
        resumen = {"regular": 0, "premium": 0, "corporativo": 0}
        for c in self._clientes:
            nombre = c.__class__.__name__.lower()
            if "premium" in nombre:
                resumen["premium"] += 1
            elif "corporativo" in nombre:
                resumen["corporativo"] += 1
            else:
                resumen["regular"] += 1
        resumen["total"] = len(self._clientes)
        return resumen
