# Mini-Manual MIMAC
## 📚 Documentación Interna - Crear nuevos parámetros y widgets

---

## 1. Crear nuevo widget

- Ir a `resources/pyresources/configs.py`, sección correspondiente (`SetupWindow`):
  - Añadir la configuración del nuevo widget (LabelEntry, LabelCombobox o CheckBox).


## 2. Definir la clave en Names

- Ir a `resources/pyresources/names.py`, dentro de:
  - `LabelEntry`, `LabelCombobox` o `CheckBoxes`.
- Añadir la nueva clave en la sección (`MAIN_FILE_F`, `GEOMETRY_F`, `SOURCE_F`, etc.).
- Seguir nomenclatura consistente (`lbe1`, `lcb1`, `cb1`, etc.).


## 3. Registrar la variable en __ini_setupVars()

- Dentro de `gui_sim_setup.py`, método `__ini_setupVars()`:
  - Añadir el nuevo widget en el diccionario de su categoría.
  - Ejemplo para un nuevo parámetro en `geometry`:

```python
'geometry': {
    ...
    'lbe11': 'WorldRotation',
},
```

- El sistema creará automáticamente el `tk.Variable` adecuado.


## 4. La vinculación se hace automáticamente

- Gracias al método `__vincule_vars()`, no es necesario hacer nada extra para conectar el widget con la variable.


## 5. (Opcional) Mostrar en resumen de simulación

- Si se quiere mostrar en la pestaña de resumen:
  - Añadir una entrada nueva en `self.__summary_label_map`:

```python
'World rotation:': 'WorldRotation',
```

- El sistema actualizará automáticamente el resumen cuando cambie el valor.


## 6. (Opcional) Añadir lógica de control

- Para reglas de activación/desactivación dinámica:
  - Añadir una nueva regla en `cfg.Rules.setup_gui_rules`.
  - Ejemplo:

```python
{
    "trigger": "geometry_cb5",
    "expected": True,
    "action": "normal",
    "targets": ["geometry_lbe11"]
}
```

- Soporta acciones: `disable`, `normal`, `set`.


---

# 👩‍💻 Ejemplo rápido: Añadir WorldRotation

1. Definir el widget `lbe11` en `cfg.SetupWindow.geometry`.
2. Crear clave `GEOMETRY_F["lbe11"] = "WorldRotation"` en `names.py`.
3. Añadir `lbe11` en `__ini_setupVars()` dentro de `geometry`.
4. (Opcional) Añadir a `__summary_label_map`.
5. (Opcional) Añadir regla en `cfg.Rules.setup_gui_rules`.

✅ El sistema hará todo el resto de forma automática.

