from .cliente import Cliente


class ClienteRegular(Cliente):
    def mostrar_info(self) -> str:
        return f"[Regular] ID: {self.id} | {self.nombre} | {self.email} | {self.telefono} | {self.direccion}"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["tipo"] = "regular"
        return d
    def beneficio_regular(self) -> str:
        return "Acceso a promociones estándar (sin descuento fijo)."
