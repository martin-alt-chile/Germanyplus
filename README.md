# Germany+ · v1.3

Aplicación móvil de alemán A1 para **Lula**, construida con Python y Streamlit.

## Qué cambió en v1.2

- Se eliminaron los íconos de parlante que parecían reproducir audio, pero no tenían una acción real.
- El **Quiz rápido de Inicio ahora funciona**: Lula puede seleccionar una alternativa, responder y recibir una explicación breve y natural.
- La respuesta correcta ya no aparece marcada antes de contestar.
- La navegación inferior fue corregida para mantener cada nombre en una sola línea y ocultar los círculos negros del control interno de Streamlit.
- Se agregaron íconos compactos a Inicio, Aprender, Repaso y Progreso sin cambiar la lógica de navegación.
- Se conserva la conexión con Supabase, el respaldo local y todas las correcciones de contraste de v1.1.

## Funciones

- Lecciones de 10–15 minutos.
- Lectura breve en alemán.
- 10 preguntas de comprensión y 10 de vocabulario.
- Cuatro alternativas siempre visibles.
- Ocho contextos: conversación, vida diaria, universidad, trabajo, viajes, comida, salud y tiempo libre.
- Repetición espaciada, racha, XP, calendario y resultados.
- Persistencia en Supabase con respaldo local para desarrollo.

## Subir a GitHub

1. Crea un repositorio vacío, por ejemplo `germany-plus`.
2. Descomprime el ZIP.
3. Sube **todo el contenido interno**; `streamlit_app.py` debe quedar en la raíz.
4. En Streamlit Community Cloud usa `streamlit_app.py` como **Main file path**.

## Supabase

1. Ejecuta `supabase_setup.sql` en **Supabase → SQL Editor**.
2. Copia `.streamlit/secrets.toml.example` en **Streamlit Cloud → App settings → Secrets**.
3. Completa Project URL y Secret key.
4. Sigue `SUPABASE_GUIA.md` para la verificación y solución de errores.

## Ejecutar localmente

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Sin secretos, la app funciona en modo local y guarda un respaldo en `.local/`.

## Pruebas

```bash
python tests/smoke_test.py
python tests/smoke_streamlit_stub.py
python -m pytest -q
```

## Estructura

```text
streamlit_app.py           interfaz y flujo de estudio
germany_plus/content.py   contenido A1
germany_plus/srs.py       repetición espaciada
germany_plus/storage.py   Supabase y respaldo local
germany_plus/metrics.py   racha y métricas
germany_plus/theme.py     diseño visual
assets/                    ilustraciones SVG locales
supabase_setup.sql         tabla y fila inicial
SUPABASE_GUIA.md           pasos de conexión
tests/                     validaciones
```


## Corrección v1.3

- Las alternativas ya no usan `st.radio`, porque sus etiquetas podían quedar invisibles en algunos despliegues móviles.
- El quiz rápido, comprensión, vocabulario y repaso usan botones de alternativa de alto contraste.
- La opción elegida queda marcada antes de presionar **Responder**.
- Después de responder se muestran claramente la alternativa correcta y, si corresponde, la selección incorrecta.
