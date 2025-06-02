# Mini-Manual MIMAC
## 📚 Documentación Interna - Eliminar parámetros y widgets

---

# 🔍 Pasos para eliminar un parámetro de MIMAC GUI


## 1. Eliminar la configuración en configs

- Ir a `resources/pyresources/configs.py`.
- Buscar el parámetro en la sección correspondiente (`SetupWindow`).
- Borrar o comentar la configuración del widget.

Ejemplo:
```python
# 'lbe11': {'type': 'LabelEntry', 'text': 'World rotation', ...}
```


## 2. Eliminar la clave en Names

- Ir a `resources/pyresources/names.py`.
- Buscar la clave en `LabelEntry`, `LabelCombobox` o `CheckBoxes`.
- Borrar la línea correspondiente.

Ejemplo:
```python
# GEOMETRY_F["lbe11"] = "WorldRotation"
```


## 3. Eliminar del mapeo de variables

- En `gui_sim_setup.py`, método `__ini_setupVars()`.
- Buscar el diccionario de su categoría (`geometry`, `source`, etc.).
- Borrar la entrada.

Ejemplo:
```python
# 'lbe11': 'WorldRotation',
```


## 4. (Opcional) Eliminar del resumen de simulación

- En `gui_sim_setup.py`, atributo `self.__summary_label_map`.
- Si aparece una entrada relacionada, eliminarla.

Ejemplo:
```python
# 'World rotation:': 'WorldRotation',
```


## 5. (Opcional) Eliminar reglas de control

- En `resources/pyresources/configs.py`, dentro de `Rules.setup_gui_rules`.
- Si hay una regla donde el parámetro sea `trigger` o `target`, eliminarla o ajustarla.

Ejemplo:
```python
# {
#   "trigger": "geometry_cb5",
#   "expected": True,
#   "action": "normal",
#   "targets": ["geometry_lbe11"]
# }
```


---

# ✅ Checklist rápido

```
☑ Borrar configuración en configs.py
☑ Borrar clave en names.py
☑ Borrar del mapping en __ini_setupVars()
☑ (Opcional) Borrar del resumen
☑ (Opcional) Borrar reglas lógicas
```


---

# 💡 Nota

- Si tienes dudas, puedes comentar las entradas primero en lugar de borrarlas para probar sin romper el flujo.
- El sistema de MIMAC está preparado para ignorar referencias que no existan, pero lo ideal es limpiar todo para evitar confusiones futuras.

---

# 🔹 Ejemplo rápido: eliminar WorldRotation

1. Borrar configuración en `configs.py`.
2. Borrar clave en `names.py`.
3. Borrar variable en `__ini_setupVars()`.
4. (Opcional) Borrar del `__summary_label_map`.
5. (Opcional) Borrar reglas en `setup_gui_rules`.

✅ El parámetro queda completamente eliminado.

