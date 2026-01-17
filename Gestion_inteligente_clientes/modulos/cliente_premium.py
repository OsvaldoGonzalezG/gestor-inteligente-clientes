from .cliente import Cliente
from .validaciones import validar_no_vacio


class ClientePremium(Cliente):
    def __init__(self, id: int, nombre: str, email: str, telefono: str, direccion: str, nivel: str = "gold"):
        super().__init__(id, nombre, email, telefono, direccion)
        self.nivel = nivel

    @property
    def nivel(self) -> str:
        return self._nivel

    @nivel.setter
    def nivel(self, valor: str) -> None:
        validar_no_vacio(valor, "nivel")
        self._nivel = valor.strip().lower()

    def beneficio_exclusivo(self) -> dict:
        tabla = {
            "silver": {"descuento": 5, "sla_horas": 24, "envio_gratis": False},
            "gold": {"descuento": 10, "sla_horas": 8, "envio_gratis": True},
            "platinum": {"descuento": 15, "sla_horas": 2, "envio_gratis": True},
        }
        nivel = self.nivel.lower()
        return tabla.get(nivel, {"descuento": 5, "sla_horas": 24, "envio_gratis": False})

    def mostrar_info(self) -> str:
        b = self.beneficio_exclusivo()
        envio = "Sí" if b["envio_gratis"] else "No"
        return (
            f"[Premium-{self.nivel}] ID: {self.id} | {self.nombre} | {self.email} | "
            f"{self.telefono} | {self.direccion} | Desc: {b['descuento']}% | SLA: {b['sla_horas']}h | Envío: {envio}"
        )

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["tipo"] = "premium"
        d["nivel"] = self.nivel
        return d
