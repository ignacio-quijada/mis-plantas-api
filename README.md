# 🌱 MisPlantas-API | Bitácora Botánica & API REST

API RESTful construida con **Python, Django y Django REST Framework (DRF)** para gestionar colecciones botánicas caseras, métodos de propagación (sustrato, agua, suelo) y el seguimiento cronológico de eventos fenológicos y de cuidado (riegos, aparición de raíces, brotes y podas).

Además de gestionar la base de datos relacional local, la API se conecta en tiempo real con servicios externos como **GBIF (Global Biodiversity Information Facility)** para validación taxonómica y **Open-Meteo** para monitoreo de condiciones ambientales locales.

---

## 🎯 Objetivos de Aprendizaje y Arquitectura
* **Diseño de Base de Datos Relacional (SQL):** Modelado de relaciones Uno a Muchos (`1:N`) mediante llaves foráneas (`ForeignKey`) entre ejemplares botánicos y su historial de eventos.
* **Serialización de Datos (`JSON`):** Transformación de consultas del ORM de Django y modelos relacionales en respuestas JSON anidadas (`Nested Serializers`).
* **Consultas SQL Avanzadas y Optimización:** Implementación de `prefetch_related` y `select_related` para evitar problemas de consultas $N+1$, junto con agregaciones (`COUNT`, `GROUP BY`) mediante `annotate`.
* **Consumo de APIs Externas (`requests`):** Integración servidor-a-servidor con APIs públicas científicas y meteorológicas.

---

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3
* **Framework Web & API:** Django & Django REST Framework (DRF)
* **Filtros y Búsqueda:** `django-filter`
* **Cliente HTTP:** `requests`
* **Base de Datos:** SQLite

---

## 🚀 Endpoints Principales

| Método HTTP | Endpoint | Descripción |
|---|---|---|
| `GET`, `POST` | `/api/plantas/` | Lista todos los ejemplares (con su historial de eventos anidado) o registra una nueva planta. Soporta filtros por método de cultivo, ubicación y búsqueda de texto. |
| `GET`, `PUT`, `DELETE` | `/api/plantas/<id>/` | Obtiene, actualiza o elimina un ejemplar específico. |
| `GET` | `/api/plantas/resumen/` | **Agregación SQL + Clima:** Devuelve estadísticas de la colección (`COUNT` por método de cultivo y ranking de cuidados) junto con la temperatura y humedad actual vía **Open-Meteo API**. |
| `GET` | `/api/plantas/<id>/taxonomia_gbif/` | **Integración Externa:** Toma el nombre científico/común de la base de datos SQL y consulta la **API de GBIF** para retornar su Reino, División, Clase, Orden y Familia validados. |
| `GET`, `POST` | `/api/eventos/` | Lista o registra nuevos eventos de cuidado (`RIEGO`, `RAIZ`, `HOJA`, `ABONO`, `PODA`). |

---
