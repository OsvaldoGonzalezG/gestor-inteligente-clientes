from modulos.gestor_clientes import GestorClientes
from modulos.cliente_regular import ClienteRegular
from modulos.cliente_premium import ClientePremium
from modulos.cliente_corporativo import ClienteCorporativo
from modulos.archivos import exportar_csv, importar_csv, generar_reporte_txt
from modulos.excepciones import GICError

RUTA_ENTRADA = "datos/clientes_entradas.csv"
RUTA_SALIDA = "datos/clientes.csv"
RUTA_REPORTE = "reportes/resumen.txt"


def pedir_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("❌ Debes ingresar un número entero.")


def pedir_texto(msg: str, permitir_vacio: bool = False):
    valor = input(msg).strip()
    if permitir_vacio and valor == "":
        return None
    return valor


def crear_cliente():
    tipo = input("Tipo (regular/premium/corporativo): ").strip().lower()
    id_ = pedir_int("ID: ")
    nombre = pedir_texto("Nombre: ")
    email = pedir_texto("Email: ")
    telefono = pedir_texto("Teléfono: ")
    direccion = pedir_texto("Dirección: ")

    if tipo == "premium":
        nivel = pedir_texto("Nivel (silver/gold/platinum): ")
        return ClientePremium(id_, nombre, email, telefono, direccion, nivel=nivel)

    if tipo == "corporativo":
        empresa = pedir_texto("Empresa: ")
        contacto = pedir_texto("Contacto/Ejecutivo: ")
        return ClienteCorporativo(id_, nombre, email, telefono, direccion, empresa=empresa, contacto=contacto)

    return ClienteRegular(id_, nombre, email, telefono, direccion)


def mostrar_beneficios(cliente):
    # Premium
    if isinstance(cliente, ClientePremium):
        b = cliente.beneficio_exclusivo()
        envio = "Sí" if b["envio_gratis"] else "No"
        print(f"🎁 Beneficios Premium ({cliente.nivel}): {b['descuento']}% desc | SLA {b['sla_horas']}h | Envío gratis: {envio}")
        return

    # Corporativo
    if isinstance(cliente, ClienteCorporativo) and hasattr(cliente, "beneficio_corporativo"):
        b = cliente.beneficio_corporativo()
        print(f"🏢 Beneficios Corporativo: {b['descuento_volumen']}% desc volumen | Facturación {b['facturacion_dias']} días | Ejecutivo: {b['ejecutivo']}")
        return

    # Regular (opcional)
    if hasattr(cliente, "beneficio_regular"):
        print(f"🎫 Beneficio Regular: {cliente.beneficio_regular()}")


def menu():
    print("\n=== Gestor Inteligente de Clientes (GIC) ===")
    print("1) Agregar cliente")
    print("2) Listar clientes")
    print("3) Buscar cliente por ID")
    print("4) Actualizar cliente")
    print("5) Eliminar cliente")
    print("6) Importar desde CSV (clientes_entradas.csv)")
    print("7) Exportar a CSV (clientes.csv)")
    print("8) Generar reporte TXT (resumen.txt)")
    print("0) Salir")


def main():
    gestor = GestorClientes()

    while True:
        menu()
        op = input("Opción: ").strip()

        try:
            if op == "1":
                c = crear_cliente()
                gestor.agregar(c)
                print("✅ Cliente agregado.")
                mostrar_beneficios(c)

            elif op == "2":
                clientes = gestor.listar()
                if not clientes:
                    print("📭 No hay clientes cargados.")
                else:
                    for c in clientes:
                        print(c.mostrar_info())

            elif op == "3":
                id_ = pedir_int("ID a buscar: ")
                c = gestor.buscar_por_id(id_)
                print("✅ Encontrado:")
                print(c.mostrar_info())
                mostrar_beneficios(c)

            elif op == "4":
                id_ = pedir_int("ID a actualizar: ")
                print("Deja vacío para no modificar un campo.")
                nombre = pedir_texto("Nuevo nombre: ", permitir_vacio=True)
                email = pedir_texto("Nuevo email: ", permitir_vacio=True)
                telefono = pedir_texto("Nuevo teléfono: ", permitir_vacio=True)
                direccion = pedir_texto("Nueva dirección: ", permitir_vacio=True)

                c = gestor.buscar_por_id(id_)
                extra = {}

                if isinstance(c, ClientePremium):
                    extra["nivel"] = pedir_texto("Nuevo nivel (silver/gold/platinum): ", permitir_vacio=True)

                if isinstance(c, ClienteCorporativo):
                    extra["empresa"] = pedir_texto("Nueva empresa: ", permitir_vacio=True)
                    extra["contacto"] = pedir_texto("Nuevo contacto/ejecutivo: ", permitir_vacio=True)

                gestor.actualizar(
                    id_,
                    nombre=nombre,
                    email=email,
                    telefono=telefono,
                    direccion=direccion,
                    **extra
                )

                c2 = gestor.buscar_por_id(id_)
                print("✅ Cliente actualizado:")
                print(c2.mostrar_info())
                mostrar_beneficios(c2)

            elif op == "5":
                id_ = pedir_int("ID a eliminar: ")
                gestor.eliminar(id_)
                print("✅ Cliente eliminado.")

            elif op == "6":
                nuevos = importar_csv(RUTA_ENTRADA)
                agregados = 0
                for c in nuevos:
                    try:
                        gestor.agregar(c)
                        agregados += 1
                    except GICError:
                        pass
                print(f"✅ Importación lista. Agregados: {agregados}")

            elif op == "7":
                exportar_csv(RUTA_SALIDA, gestor.listar())
                print(f"✅ Exportado a {RUTA_SALIDA}")

            elif op == "8":
                generar_reporte_txt(RUTA_REPORTE, gestor)
                print(f"✅ Reporte generado en {RUTA_REPORTE}")

            elif op == "0":
                print("👋 Saliendo...")
                break
            else:
                print("❌ Opción inválida.")

        except GICError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
