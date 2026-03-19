# 🚀 S3 Delete Marker Cleaner (dm-bucket)

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-S3-orange.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/s3/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Optimiza tus costos en AWS S3 mediante la gestión inteligente de Delete Markers.**

Esta herramienta de CLI profesional está diseñada para administradores de sistemas y DevOps que necesitan limpiar sus buckets de S3, eliminando "Delete Markers" que pueden acumular costos de almacenamiento innecesarios y dificultar la gestión de versiones.

---

## 🎯 El Problema
Cuando se habilita el versionado en S3, borrar un objeto no lo elimina físicamente, sino que crea un **Delete Marker**. Con el tiempo, miles de estos marcadores pueden acumularse, afectando el rendimiento de las consultas y generando costos ocultos.

## 🛠️ Solución
`dm-bucket` automatiza el escaneo, visualización y eliminación masiva de estos marcadores utilizando mejores prácticas de desarrollo y alto rendimiento.

### Características Principales:
- **🚀 Escaneo de Alto Rendimiento:** Utiliza `Boto3 Paginators` para procesar millones de objetos sin saturar la memoria.
- **📊 Visualización Rich:** Reportes detallados en consola con tablas interactivas (`Rich`).
- **🛡️ Eliminación Segura por Lotes:** Implementa `delete_objects` en chunks de 1000 (límite de AWS) para máxima eficiencia.
- **📝 Logging Robusto:** Seguimiento detallado de operaciones con rotación y compresión automática de logs (`Loguru`).
- **⚙️ Configuración Flexible:** Gestión de entornos mediante `Dynaconf`.

---

## 🏗️ Stack Tecnológico
- **Lenguaje:** Python 3.14+ (Aprovechando las últimas mejoras de rendimiento).
- **SDK:** `Boto3` (AWS SDK for Python).
- **CLI:** `Typer` para una interfaz de comandos intuitiva y autocompletado.
- **UI:** `Rich` para una experiencia de usuario premium en la terminal.
- **Logging:** `Loguru` para un manejo de errores y auditoría simplificado.
- **Configuración:** `Dynaconf` para soporte multi-entorno (TOML/YAML/ENV).

---

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.14 o superior.
- Credenciales de AWS configuradas (`~/.aws/credentials`).

### Configuración con `uv` (Recomendado)
```bash
uv sync
```

### Comandos Disponibles

1. **Escanear marcadores:**
   ```bash
   python main.py scan --profile mi-perfil --region us-east-1
   ```

2. **Eliminación Remota (Limpieza real):**
   ```bash
   python main.py remote-delete --profile mi-perfil --region us-east-1
   ```

---

## 📈 Impacto Técnico
Este proyecto demuestra habilidades avanzadas en:
- **Cloud Computing (AWS):** Gestión de ciclo de vida de objetos y optimización de S3.
- **Ingeniería de Software:** Patrones de diseño para CLI, paginación de datos masivos y manejo de batches.
- **DevOps/SRE:** Automatización de tareas de mantenimiento e infraestructura.

---

## 👨‍💻 Autor
**Mauricio Diaz Cabrera**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](www.linkedin.com/in/mauricio-diaz-cabrera)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/MauDiazC)

---
*Desarrollado con ❤️ para la comunidad de Cloud & DevOps.*
