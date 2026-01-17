import csv
import os

from .excepciones import ArchivoError
from .cliente_regular import ClienteRegular
from .cliente_premium import ClientePremium
from .cliente_corporativo import ClienteCorporativo


FIELDNAMES = ["tipo", "id", "nombre", "email", "telefono", "direccion", "nivel", "empresa", "contacto"]


def _safe_str(value) -> str:
    """Convierte None a '', y limpia espacios."""
    if value is None:
        return ""
    return str(value).strip()


def exportar_csv(ruta: str, clientes: list) -> None:
    """
    Exporta lista de clientes a CSV con columnas fijas.
    Siempre escribe: tipo,id,nombre,email,telefono,direccion,nivel,empresa,contacto
    """
    try:
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

            for c in clientes:
                d = c.to_dict()

                # Asegurar columnas fijas y valores por defecto
                row = {
                    "tipo": _safe_str(d.get("tipo", "")),
                    "id": _safe_str(d.get("id", "")),
                    "nombre": _safe_str(d.get("nombre", "")),
                    "email": _safe_str(d.get("email", "")),
                    "telefono": _safe_str(d.get("telefono", "")),
                    "direccion": _safe_str(d.get("direccion", "")),
                    "nivel": _safe_str(d.get("nivel", "")),
                    "empresa": _safe_str(d.get("empresa", "")),
                    "contacto": _safe_str(d.get("contacto", "")),
                }

                writer.writerow(row)

    except Exception as e:
        raise ArchivoError(f"Error exportando CSV ({ruta}): {e}") from e


def importar_csv(ruta: str) -> list:
    """
    Importa clientes desde CSV.
    Tolera archivos que no tengan todas las columnas; si faltan, usa ''.
    """
    if not os.path.exists(ruta):
        raise ArchivoError(f"No existe el archivo: {ruta}")

    clientes = []
    try:
        with open(ruta, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Si el CSV viene sin header o viene vacío
            if reader.fieldnames is None:
                raise ArchivoError("El CSV no tiene encabezados (header).")

            for row in reader:
                # Saltar filas totalmente vacías
                if not row or all((_safe_str(v) == "" for v in row.values())):
                    continue

                tipo = _safe_str(row.get("tipo", "regular")).lower()
                id_ = int(_safe_str(row.get("id", "0")))
                nombre = _safe_str(row.get("nombre", ""))
                email = _safe_str(row.get("email", ""))
                telefono = _safe_str(row.get("telefono", ""))
                direccion = _safe_str(row.get("direccion", ""))

                if tipo == "premium":
                    nivel = _safe_str(row.get("nivel", "gold")) or "gold"
                    clientes.append(ClientePremium(id_, nombre, email, telefono, direccion, nivel=nivel))

                elif tipo == "corporativo":
                    empresa = _safe_str(row.get("empresa", ""))
                    contacto = _safe_str(row.get("contacto", ""))
                    clientes.append(ClienteCorporativo(id_, nombre, email, telefono, direccion, empresa=empresa, contacto=contacto))

                else:
                    # default: regular
                    clientes.append(ClienteRegular(id_, nombre, email, telefono, direccion))

        return clientes

    except ValueError as e:
        # típicamente falla int(id)
        raise ArchivoError(f"Error leyendo CSV (ID inválido o dato no numérico): {e}") from e
    except Exception as e:
        raise ArchivoError(f"Error importando CSV ({ruta}): {e}") from e


def generar_reporte_txt(ruta: str, gestor) -> None:
    """
    Reporte TXT:
    - Totales por tipo (requisito)
    - Extra:
      * Premium: distribución por nivel, promedio descuento, tabla de clientes
      * Corporativo: promedio desc/facturación, tabla con empresa y ejecutivo
      * Regular: listado simple + beneficio estándar
    """
    import os

    from .excepciones import ArchivoError

    try:
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        clientes = gestor.listar()
        resumen = gestor.resumen_por_tipo()

        # Listas para "tablas"
        premium_rows = []
        corp_rows = []
        regular_rows = []

        # Métricas
        premium_por_nivel = {"silver": 0, "gold": 0, "platinum": 0, "otro": 0}
        premium_descuentos = []
        corp_descuentos = []
        corp_fact = []

        # Helpers
        def avg(nums):
            return (sum(nums) / len(nums)) if nums else 0

        for c in clientes:
            cls = c.__class__.__name__.lower()

            if "premium" in cls:
                nivel = getattr(c, "nivel", "otro") or "otro"
                nivel = str(nivel).strip().lower()
                if nivel in premium_por_nivel:
                    premium_por_nivel[nivel] += 1
                else:
                    premium_por_nivel["otro"] += 1

                desc = sla = None
                envio = None
                if hasattr(c, "beneficio_exclusivo"):
                    b = c.beneficio_exclusivo()
                    if isinstance(b, dict):
                        desc = b.get("descuento")
                        sla = b.get("sla_horas")
                        envio = b.get("envio_gratis")
                        if isinstance(desc, (int, float)):
                            premium_descuentos.append(desc)

                premium_rows.append({
                    "id": c.id,
                    "nombre": c.nombre,
                    "nivel": getattr(c, "nivel", ""),
                    "descuento": desc,
                    "sla": sla,
                    "envio": envio,
                    "email": c.email
                })

            elif "corporativo" in cls:
                desc_vol = fact_dias = None
                ejecutivo = getattr(c, "contacto", "")
                empresa = getattr(c, "empresa", "")

                if hasattr(c, "beneficio_corporativo"):
                    b = c.beneficio_corporativo()
                    if isinstance(b, dict):
                        desc_vol = b.get("descuento_volumen")
                        fact_dias = b.get("facturacion_dias")
                        ejecutivo = b.get("ejecutivo", ejecutivo)
                        if isinstance(desc_vol, (int, float)):
                            corp_descuentos.append(desc_vol)
                        if isinstance(fact_dias, (int, float)):
                            corp_fact.append(fact_dias)

                corp_rows.append({
                    "id": c.id,
                    "nombre": c.nombre,
                    "empresa": empresa,
                    "ejecutivo": ejecutivo,
                    "descuento_vol": desc_vol,
                    "facturacion": fact_dias,
                    "email": c.email
                })

            else:
                # Regular (default)
                regular_rows.append({
                    "id": c.id,
                    "nombre": c.nombre,
                    "email": c.email
                })

        # Ordenar por ID para que se vea ordenado
        premium_rows.sort(key=lambda x: x["id"])
        corp_rows.sort(key=lambda x: x["id"])
        regular_rows.sort(key=lambda x: x["id"])

        with open(ruta, "w", encoding="utf-8") as f:
            # ===== Sección requerida =====
            f.write("Reporte resumen - GIC\n")
            f.write("=====================\n\n")
            f.write(f"Total clientes: {resumen.get('total', 0)}\n")
            f.write(f"Regular: {resumen.get('regular', 0)}\n")
            f.write(f"Premium: {resumen.get('premium', 0)}\n")
            f.write(f"Corporativo: {resumen.get('corporativo', 0)}\n")

            # ===== Extra =====
            f.write("\n--- Detalle y Beneficios (extra) ---\n")

            # -------- PREMIUM --------
            f.write("\n[Premium]\n")
            f.write("Distribución por nivel:\n")
            f.write(f"  - Silver: {premium_por_nivel['silver']}\n")
            f.write(f"  - Gold: {premium_por_nivel['gold']}\n")
            f.write(f"  - Platinum: {premium_por_nivel['platinum']}\n")
            if premium_por_nivel["otro"] > 0:
                f.write(f"  - Otro: {premium_por_nivel['otro']}\n")
            f.write(f"Descuento promedio premium: {avg(premium_descuentos):.2f}%\n\n")

            if premium_rows:
                f.write("ID | Nombre | Nivel | Desc% | SLA(h) | Envío Gratis | Email\n")
                f.write("-" * 78 + "\n")
                for r in premium_rows:
                    desc = r["descuento"] if r["descuento"] is not None else "N/A"
                    sla = r["sla"] if r["sla"] is not None else "N/A"
                    envio = "Sí" if r["envio"] is True else ("No" if r["envio"] is False else "N/A")
                    f.write(f"{r['id']} | {r['nombre']} | {r['nivel']} | {desc} | {sla} | {envio} | {r['email']}\n")
            else:
                f.write("No hay clientes premium.\n")

            # -------- CORPORATIVO --------
            f.write("\n\n[Corporativo]\n")
            f.write(f"Descuento volumen promedio: {avg(corp_descuentos):.2f}%\n" if corp_descuentos else "Descuento volumen promedio: N/A\n")
            f.write(f"Facturación promedio: {avg(corp_fact):.2f} días\n\n" if corp_fact else "Facturación promedio: N/A\n\n")

            if corp_rows:
                f.write("ID | Nombre | Empresa | Ejecutivo | DescVol% | Fact(d) | Email\n")
                f.write("-" * 82 + "\n")
                for r in corp_rows:
                    descv = r["descuento_vol"] if r["descuento_vol"] is not None else "N/A"
                    fact = r["facturacion"] if r["facturacion"] is not None else "N/A"
                    f.write(f"{r['id']} | {r['nombre']} | {r['empresa']} | {r['ejecutivo']} | {descv} | {fact} | {r['email']}\n")
            else:
                f.write("No hay clientes corporativos.\n")

            # -------- REGULAR --------
            f.write("\n\n[Regular]\n")
            f.write("Beneficio: acceso a promociones estándar (sin descuento fijo).\n\n")
            if regular_rows:
                f.write("ID | Nombre | Email\n")
                f.write("-" * 50 + "\n")
                for r in regular_rows:
                    f.write(f"{r['id']} | {r['nombre']} | {r['email']}\n")
            else:
                f.write("No hay clientes regulares.\n")

            f.write("\n\nFin del reporte.\n")

    except Exception as e:
        raise ArchivoError(f"Error generando reporte TXT ({ruta}): {e}") from e


