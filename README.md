# Germany+ · v1.4 definitiva

Aplicación móvil de alemán A1 para **Lula**, construida con Python y Streamlit.

## Lo nuevo en v1.4

- El tema inicial **cambia automáticamente cada día** según la fecha. No depende de un botón, una nueva sesión del navegador ni una actualización del repositorio.
- La rotación avanza sola por todo el catálogo y vuelve a comenzar después de usar todos los temas.
- Lula puede hacer **todas las sesiones que quiera durante el día**.
- Las sesiones extra recorren todos los temas disponibles antes de repetir alguno.
- Al terminar aparece el botón **Hacer otra lección**, que abre inmediatamente el siguiente tema.
- En **Leer y entender**, el resumen aparece primero en alemán. La versión equivalente en español queda dentro de **Ver el mismo resumen en español**.
- Se mantiene el sistema de alternativas mediante botones visibles, sin `st.radio` en los quizzes.
- Supabase guarda cada sesión, XP, racha y progreso de vocabulario sin necesidad de crear una cuenta.

## Cómo funciona la rotación

Germany+ incluye ocho contextos A1: conversación, vida diaria, universidad, trabajo, viajes, comida, salud y tiempo libre.

1. Cada fecha recibe automáticamente un tema inicial.
2. En un ciclo de ocho días aparecen los ocho temas una vez.
3. Después del octavo tema comienza automáticamente un nuevo ciclo.
4. Si Lula estudia más de una vez el mismo día, recibe los demás temas antes de repetir.
5. Después de recorrer el catálogo completo puede seguir practicando; las preguntas, alternativas y vocabulario cambian de orden en cada sesión.

No hay que editar GitHub ni volver a desplegar la app para que cambie el tema diario.

## Funciones

- Lecciones de 10–15 minutos.
- Lectura breve en alemán con traducción española opcional.
- 10 preguntas de comprensión y 10 de vocabulario.
- Cuatro alternativas siempre visibles.
- Repetición espaciada, racha, XP, calendario y resultados.
- Persistencia en Supabase con respaldo local para desarrollo.

## Subir a GitHub

1. Crea un repositorio vacío, por ejemplo `germany-plus`.
2. Descomprime el ZIP.
3. Sube **todo el contenido interno**; `streamlit_app.py` debe quedar en la raíz.
4. En Streamlit Community Cloud usa `streamlit_app.py` como **Main file path**.

## Supabase

1. Ejecuta `supabase_setup.sql` en **Supabase → SQL Editor**.
2. Copia el contenido de `.streamlit/secrets.toml.example` en **Streamlit Cloud → App settings → Secrets**.
3. Completa Project URL y Secret key.
4. Sigue `SUPABASE_GUIA.md` para verificar la conexión.

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
germany_plus/schedule.py  rotación automática diaria y sesiones extra
germany_plus/srs.py       repetición espaciada
germany_plus/storage.py   Supabase y respaldo local
germany_plus/metrics.py   racha y métricas
germany_plus/theme.py     diseño visual
assets/                    ilustraciones SVG locales
supabase_setup.sql         tabla y fila inicial
SUPABASE_GUIA.md           pasos de conexión
tests/                     validaciones
```
