# Gestor Inteligente de Clientes (GIC)

Sistema desarrollado en Python que permite la gestión de distintos tipos de clientes aplicando
los principios de la Programación Orientada a Objetos (POO).

El proyecto fue desarrollado como parte de un módulo académico, incorporando buenas prácticas
de diseño, validación de datos, manejo de excepciones y persistencia mediante archivos.

---

## 📌 Características principales

- Gestión de clientes mediante operaciones CRUD (crear, leer, actualizar y eliminar).
- Tipos de clientes:
  - Cliente Regular
  - Cliente Premium (con niveles de beneficio)
  - Cliente Corporativo
- Aplicación de beneficios diferenciados según el tipo de cliente.
- Importación y exportación de datos en formato CSV.
- Generación de reportes en formato TXT.
- Registro de eventos del sistema mediante logging.
- Menú interactivo por consola.

---

## 🧱 Estructura del proyecto

## 🧱 Estructura del proyecto


Gestion_inteligente_clientes/
├── main.py
├── diagrama_clases.puml
├── modulos/
│   ├── cliente.py
│   ├── cliente_regular.py
│   ├── cliente_premium.py
│   ├── cliente_corporativo.py
│   ├── gestor_clientes.py
│   ├── validaciones.py
│   ├── archivos.py
│   ├── excepciones.py
│   └── logger_config.py
├── datos/
├── reportes/
└── logs/



---

## ▶️ Ejecución del proyecto

Desde la carpeta raíz del proyecto:


python main.py

📊 Archivos generados

datos/clientes.csv
Exportación de clientes registrados en el sistema.

reportes/resumen.txt
Reporte resumen con información de clientes y beneficios.

logs/app.log
Registro de eventos relevantes del sistema (altas, bajas y modificaciones).

🧠 Diseño del sistema

El sistema fue diseñado utilizando un diagrama de clases UML, el cual se encuentra
disponible en el archivo diagrama_clases.puml.
Este diagrama representa la estructura del sistema, las relaciones entre clases y
la aplicación de herencia y polimorfismo.

📄 Documentación

El proyecto cuenta con un informe detallado que describe el diseño, funcionamiento,
pruebas realizadas y conclusiones del sistema.

✍️ Autor

Osvaldo González
