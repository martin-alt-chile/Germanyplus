# Conectar Germany+ con Supabase

Germany+ usa una sola fila JSON para guardar el progreso de Lula: lecciones, racha, XP y repetición espaciada. No necesita registro ni contraseña.

## 1. Crear el proyecto

1. En Supabase crea un proyecto nuevo.
2. Espera a que termine de preparar la base de datos.
3. Abre **SQL Editor** y selecciona **New query**.
4. Copia todo el contenido de `supabase_setup.sql`, ejecútalo y confirma que la consulta final muestre una fila con `user_id = lula`.

## 2. Copiar las credenciales

En Supabase abre **Project Settings → API Keys** o el panel **Connect**.

Necesitas:

- **Project URL**: tiene formato `https://xxxxx.supabase.co`.
- **Secret key**: normalmente comienza con `sb_secret_`.

La Secret key es de servidor y no debe aparecer en GitHub, capturas ni código. En proyectos antiguos también funciona la clave `service_role`.

## 3. Pegarlas en Streamlit Cloud

1. Abre la app en Streamlit Community Cloud.
2. Entra a **App settings → Secrets**.
3. Pega este bloque reemplazando los valores:

```toml
[supabase]
url = "https://TU-PROYECTO.supabase.co"
secret_key = "sb_secret_TU_CLAVE_SECRETA"
```

4. Guarda los secretos y reinicia la app.

## 4. Verificar

En la parte inferior de Germany+ debe aparecer:

> **Datos: Supabase · Progreso guardado en Supabase.**

Completa una respuesta, vuelve a Supabase y abre **Table Editor → germany_plus_state**. La columna `updated_at` debe cambiar y el JSON de `state` debe contener el progreso.

## Errores típicos

### `401` o `403`

La URL o la clave no corresponden al mismo proyecto, o se pegó una clave pública en lugar de la Secret key.

### `relation "germany_plus_state" does not exist`

No se ejecutó `supabase_setup.sql` en ese proyecto.

### La app dice `Local de respaldo`

Germany+ no pudo llegar a Supabase. Abre **Ver detalle técnico del almacenamiento**, corrige el secreto y reinicia.

### Importante

- Nunca subas `.streamlit/secrets.toml` a GitHub.
- La app acepta tanto el formato `[supabase]` de esta guía como las variables antiguas `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY`.
- El archivo `.gitignore` ya excluye los secretos y el respaldo local.
