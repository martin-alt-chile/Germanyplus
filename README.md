# Germany+

Aplicación móvil de práctica diaria de alemán para **Lula**, construida con Python y Streamlit.

## Qué incluye

- Nivel inicial **A1**.
- Saludo principal: **Hallo Lula 🍂**.
- Diseño claro inspirado en negro, rojo y dorado de Alemania, sin fotografía de perfil.
- Sesiones de 10–15 minutos.
- Lectura breve de 2–3 párrafos.
- 10 preguntas de comprensión con cuatro alternativas siempre visibles.
- 10 preguntas de vocabulario.
- Ayudas, traducciones y explicaciones en español.
- Pronunciación aproximada pensada para una hispanohablante.
- Repetición espaciada para palabras correctas e incorrectas.
- Racha, XP, calendario y resultados recientes.
- Ocho contextos generales: conversación, vida diaria, universidad, trabajo, viajes, comida, salud y tiempo libre.
- Supabase opcional para que el progreso sobreviva reinicios y despliegues.

## Subir a GitHub

1. Crea un repositorio vacío, por ejemplo `germany-plus`.
2. Sube **el contenido del ZIP**, no la carpeta comprimida completa dentro del repositorio.
3. Confirma que `streamlit_app.py` quede en la raíz.

## Desplegar en Streamlit Community Cloud

1. Entra a Streamlit Community Cloud y selecciona `Create app`.
2. Elige el repositorio y la rama `main`.
3. Usa `streamlit_app.py` como `Main file path`.
4. Despliega.

La app funciona de inmediato en modo local. En Streamlit Cloud, ese modo puede perder progreso cuando el servidor se reinicia. Para persistencia real, conecta Supabase.

## Conectar Supabase

1. Crea un proyecto en Supabase.
2. Abre `SQL Editor` y ejecuta `supabase_setup.sql`.
3. En Streamlit Cloud abre `App settings > Secrets`.
4. Copia el formato de `.streamlit/secrets.toml.example` y completa:

```toml
SUPABASE_URL = "https://TU-PROYECTO.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "TU_SERVICE_ROLE_KEY"
```

La **service role key** debe permanecer solo en los secretos de Streamlit. Nunca la subas a GitHub.

## Ejecutar localmente

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Pruebas

```bash
python tests/smoke_test.py
python tests/smoke_streamlit_stub.py
python -m pytest -q
```

## Estructura

```text
streamlit_app.py          interfaz y flujo de estudio
germany_plus/content.py  contenido A1 curado
germany_plus/srs.py      repetición espaciada
germany_plus/storage.py  Supabase + respaldo local
germany_plus/metrics.py  racha y métricas
germany_plus/theme.py    diseño visual móvil
supabase_setup.sql        tabla de persistencia
tests/                    validaciones automáticas
```
