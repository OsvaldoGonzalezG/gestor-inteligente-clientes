from .cliente import Cliente
from .validaciones import validar_no_vacio


class ClienteCorporativo(Cliente):
    def __init__(
        self,
        id: int,
        nombre: str,
        email: str,
        telefono: str,
        direccion: str,
        empresa: str,
        contacto: str,
    ):
        super().__init__(id, nombre, email, telefono, direccion)
        self.empresa = empresa
        self.contacto = contacto

    @property
    def empresa(self) -> str:
        return self._empresa

    @empresa.setter
    def empresa(self, valor: str) -> None:
        validar_no_vacio(valor, "empresa")
        self._empresa = valor.strip()

    @property
    def contacto(self) -> str:
        return self._contacto

    @contacto.setter
    def contacto(self, valor: str) -> None:
        validar_no_vacio(valor, "contacto")
        self._contacto = valor.strip()

    def beneficio_corporativo(self) -> dict:
        return {"descuento_volumen": 12, "facturacion_dias": 30, "ejecutivo": self.contacto}

    def mostrar_info(self) -> str:
        b = self.beneficio_corporativo()
        return (
            f"[Corporativo] ID: {self.id} | {self.nombre} | {self.email} | {self.telefono} | "
            f"{self.direccion} | Empresa: {self.empresa} | Ejecutivo: {b['ejecutivo']} | "
            f"Desc Vol: {b['descuento_volumen']}% | Fact: {b['facturacion_dias']}d"
        )

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["tipo"] = "corporativo"
        d["empresa"] = self.empresa
        d["contacto"] = self.contacto
        return d
