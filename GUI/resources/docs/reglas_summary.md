# Mini-Manual MIMAC
## 📚 Documentación Interna - Resumen Dinámico Unificado

---

# 🔹 Introducción

A partir de la versión avanzada de MIMAC GUI, el resumen de simulación (Summary) se gestiona mediante un único diccionario llamado `self.__summary_map`.

Esto simplifica y unifica toda la lógica de presentación de valores en la interfaz gráfica.


# 🔹 Estructura del resumen

- `self.__summary_map` contiene todas las reglas de visualización.
- Cada entrada tiene:
  - **Clave**: etiqueta a mostrar (por ejemplo, "Phantom file:").
  - **Valor**:
    - **String** si es un parámetro directo (por ejemplo, `'NEvents'`).
    - **Función lambda** si requiere evaluación especial.


# 🔹 Ejemplo de self.__summary_map

```python
self.__summary_map = {
    'Number of events:': 'NEvents',
    'World file:': 'WorldFile',
    'Voxelized phantom:': 'DICOMGeom',
    'Phantom file:': lambda params: params['VoxelPhantom'] if params.get('DICOMGeom') == 'Yes' else params.get('GeomtryPhantom', ''),
    'Physical detector:': lambda params: 'Yes' if params.get('DetectorModel') == 'MCD' else 'No',
    'Physics list:': 'PhysicList',
    'Spectrum file:': 'Spectra',
    'Source distribution:': 'Distribution',
    'Align source automatically:': 'AlignSource',
    'Auto-size source:': 'AutoSizeSource',
    'Detector model:': 'DetectorModel',
    'Anti-scatter grid:': 'UseAntiScatterGrid'
}
```


# 🔹 Actualización del resumen (__update_sim_summary)

En el método `__update_sim_summary()`:

- Se busca la etiqueta en `self.__summary_map`.
- Si el valor es **una función**, se ejecuta pasando `params`.
- Si el valor es **un string**, se usa como clave en `params`.

```python
if callable(rule):
    new_value = rule(current_params)
else:
    new_value = current_params.get(rule, '')
```


# ✅ Beneficios del sistema unificado

- Un solo diccionario.
- Centralización de toda la lógica de resumen.
- Fácil de añadir o modificar campos.
- Compatible con condiciones dinámicas complejas.


# 📅 Ejemplo de nueva entrada con condición

Mostrar "High Energy Mode:" si la energía es mayor a 50 keV:

```python
self.__summary_map['High Energy Mode:'] = lambda params: 'Yes' if params.get('Energy', 0) > 50 else 'No'
```


# ✅ Checklist para añadir/modificar campos del Summary

```
☑ Añadir nueva entrada a self.__summary_map
☑ Usar string si es parámetro directo
☑ Usar lambda si necesita lógica condicional
☑ No es necesario tocar més métodos
```


---

# 🔹 Nota importante

- Las funciones lambda deben manejar casos seguros (usar `.get()` con valores por defecto).
- Se recomienda mantener las etiquetas (ítems) del Summary coherentes en estilo y longitud.


---

# 👍 Con este sistema, el resumen de MIMAC es 100% modular, profesional y escalable.

