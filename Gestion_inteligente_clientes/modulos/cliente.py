from .validaciones import validar_no_vacio, validar_email, validar_telefono, validar_direccion


class Cliente:
    def __init__(self, id: int, nombre: str, email: str, telefono: str, direccion: str):
        self._id = int(id)
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        validar_no_vacio(valor, "nombre")
        self._nombre = valor.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        validar_email(valor)
        self._email = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        validar_telefono(valor)
        self._telefono = valor.strip()

    @property
    def direccion(self) -> str:
        return self._direccion

    @direccion.setter
    def direccion(self, valor: str) -> None:
        validar_direccion(valor)
        self._direccion = valor.strip()

    def mostrar_info(self) -> str:
        return f"[Cliente] ID: {self.id} | {self.nombre} | {self.email} | {self.telefono} | {self.direccion}"

    def to_dict(self) -> dict:
        return {
            "tipo": "regular",  # default si serializan desde base
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
        }

    def __str__(self) -> str:
        return self.mostrar_info()
