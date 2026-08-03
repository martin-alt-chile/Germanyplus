# Germany+

Aplicación móvil de alemán A1 para **Lula**, construida con Python y Streamlit.

## Qué cambió en v1.1

- Interfaz rediseñada para acercarse al mockup: portada otoñal, silueta de Berlín, tarjeta oscura de lección, panel unificado de racha/progreso/XP, tarjetas de práctica, categorías y navegación inferior.
- Se eliminó completamente la fotografía de perfil; ahora aparece una insignia con la letra **L**.
- Corrección global de contraste: textos oscuros sobre fondos claros y textos blancos solo sobre superficies oscuras.
- Alternativas opacas, grandes y legibles, incluso después de responder.
- Feedback más natural: “¡Bien!” o “Casi”, seguido de una explicación breve, sin frases repetitivas como “Respuesta correcta: … El texto dice…”.
- Contenido A1 con traducciones, pronunciación aproximada y ayudas en español.
- Supabase actualizado para Secret keys (`sb_secret_...`) y compatible con `service_role` de proyectos antiguos.

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
