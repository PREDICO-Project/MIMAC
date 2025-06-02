# Mini-Manual MIMAC
## 📚 Documentación Interna - Modificar el contenido del Summary

---

# 🔍 ¿Qué es el Summary?

- Es la pestaña de "Resumen de Simulación" que muestra parámetros clave elegidos.
- El contenido se define y actualiza automáticamente en base a un mapeo interno.


# 🔹 ¿Dónde se configura?

- Dentro de `gui_sim_setup.py`, atributo:

```python
self.__summary_label_map = { ... }
```

- El método que actualiza el resumen es:

```python
__update_sim_summary()
```

- Los valores mostrados vienen de:

```python
self.__get_updated_params()
```


# 🔹 ¿Cómo modificar el contenido del Summary?


## 1. Para añadir un nuevo campo

- Asegúrate de que el parámetro existe en `self.params`.
- Añade una nueva entrada en `self.__summary_label_map`.

Ejemplo:
```python
'Rotation angle:': 'WorldRotation',
```


## 2. Para eliminar un campo

- Simplemente **borra** la entrada correspondiente del `self.__summary_label_map`.

Ejemplo:
```python
# Borrar esta línea si ya no quieres mostrarlo
'Voxelized phantom:': 'DICOMGeom',
```


## 3. Para cambiar el texto que aparece

- Cambia la **clave** en `self.__summary_label_map`.

Ejemplo:
```python
# Antes
'World file:': 'WorldFile',

# Después
'Phantom world file:': 'WorldFile',
```


## 4. Para mostrar otro parámetro diferente

- Cambia el **valor** de la clave en el mapeo.

Ejemplo:
```python
# Antes
'Distribution direction:': 'Distribution'

# Después
'Distribution direction:': 'NewDistributionDirection'
```


---

# ✅ Checklist rápido para modificar el Summary

```
☑ Editar self.__summary_label_map
☑ Añadir, borrar o modificar entradas
☑ Asegurarse de que el parámetro existe en self.params
☑ No es necesario tocar más código
```


---

# 🔹 Nota importante

- Si el parámetro no existe en `self.params`, no se mostrará ningún valor en el resumen.
- El sistema resalta automáticamente en amarillo los cambios recientes durante 1 segundo para mejor visualización.

---

# 🔹 Ejemplo rápido: Añadir "Rotation Angle"

1. Asegúrate de que `WorldRotation` esté en `self.params`.
2. Añadir a `self.__summary_label_map`:

```python
'Rotation angle:': 'WorldRotation',
```

✅ Y el valor aparecerá automáticamente en el resumen.

