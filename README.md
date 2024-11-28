# Guia de desarrollo: Sistema de Gestión de Mantenimiento

Este proyecto consiste en extender y personalizar las funcionalidades del módulo de mantenimiento en Odoo para cumplir con los requerimientos descritos. A continuación, se detallan los puntos implementados organizados por área.

## Requisitos Implementados

### Petición de Mantenimiento
1. **Campos adicionales**:
   - `partner_id`: Campo `Usuario portal solicitante`.
   - `department_id`: Campo `Departamento`, visible al seleccionar un equipamiento.
   - `acting_user_ids`: Campo relacionado con `res.users`, con widget `many2many_tags` y limitado a usuarios de equipos de mantenimiento.
   - `priority`: Campo `selection` que reemplaza el campo original de prioridad.
   - Tabla **Productos para mantenimiento**: Relaciona productos, cantidad y unidad de medida.

2. **Modificaciones a la vista**:
   - Esconder campos: `priority` (original), `maintenance_kind_id`, `proyecto`, `tarea` y `correo electrónico`.
   - Cambiar el label `notas` por `Descripción`, colocándolo antes de `instrucciones`.

3. **Secuencia**:
   - Extender el número de secuencia (`code`) a 8 dígitos.

4. **Reportes**:
   - Crear un nuevo reporte imprimible para las peticiones de mantenimiento.

5. **Notebook**:
   - Incluir una página llamada **Estructura del equipamiento** con el campo `Estructura de equipamiento`.

---

### Equipos de Mantenimiento
1. **Campos adicionales**:
   - `Estructura del equipo`: Relaciona productos, cantidad y unidad de medida.

2. **Acciones de servidor**:
   - **Generar peticiones de mantenimiento**: Genera peticiones para los planes de mantenimiento asignados.

---

### Plan de Mantenimiento
1. **Restricciones de calendario**:
   - Evitar generación de peticiones en días no laborables y feriados.

2. **Modificaciones de datos**:
   - Campo `fecha_prevista` configurado en horario UTC.
   - Campo **Productos para mantenimiento**: Relaciona productos con cantidad y unidad de medida.

3. **Modificaciones a la vista**:
   - Esconder `maintenance_kind_id` y el ítem de menú **Tipos de mantenimiento**.

---

### Portal de Mantenimiento
1. **Navegación**:
   - Incluir ítem **Peticiones de mantenimiento** en la vista home del portal, con contador de peticiones generadas por el usuario.

2. **Formulario de creación**:
   - Campos: `Nombre de la petición`, `Equipamiento`, `Prioridad` y `Descripción`.
   - Botón `Enviar petición` para crear la petición y redirigir al listado del usuario.

3. **Listado de peticiones**:
   - Tabla con las columnas requeridas y opciones para filtrar/ordenar.
   - Elementos clickeables que redirigen a la vista específica de la petición.

4. **Vista de descripción de petición**:
   - Título con el nombre de la petición y botones para avanzar etapas.

---

### Mesa de Ayuda
1. **Campos adicionales**:
   - `Listado de productos`: Vincula productos, cantidad y unidad de medida.
   - Campo relacionado a petición de mantenimiento que muestra código y nombre.

2. **Modificaciones**:
   - Renombrar `Ubicación` a `Departamento`.
   - Llenar automáticamente `Listado de productos` al seleccionar una petición.

3. **Portal**:
   - Reemplazar `Categoría de ticket` por `Tipo de ticket`.
   - Incluir campo `Equipo de mesa de ayuda`.

---

### Stock
1. **Campo relacionado**:
   - `Ticket relacionado`: Muestra materiales del ticket al seleccionarlo.

---

### Tipos de Ticket
1. **Campos adicionales**:
   - `Permiso de acceso`: Controla la visibilidad de los tipos de ticket en el portal.

---