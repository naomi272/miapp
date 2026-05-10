import sqlite3
import bcrypt

# CONEXIÓN
conn = sqlite3.connect("database.db", check_same_thread=False)

cursor = conn.cursor()

# TABLA GASTOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    nombre TEXT,
    categoria TEXT,
    monto REAL,
    fecha TEXT,
    metodo_pago TEXT,
    descripcion TEXT
)
""")

conn.commit()

# TABLA INGRESOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingresos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    nombre TEXT,
    monto REAL,
    fecha TEXT,
    fuente TEXT,
    descripcion TEXT
)
""")

conn.commit()

# TABLA DE USUARIOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()

# TABLA METAS
cursor.execute("""
CREATE TABLE IF NOT EXISTS metas (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    meta REAL

)
""")

# INSERTAR GASTO
def insertar_gasto(
    usuario_id,
    nombre,
    categoria,
    monto,
    fecha,
    metodo_pago,
    descripcion
):

    cursor.execute("""
    INSERT INTO gastos (
        usuario_id,
        nombre,
        categoria,
        monto,
        fecha,
        metodo_pago,
        descripcion
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        usuario_id,
        nombre,
        categoria,
        monto,
        fecha,
        metodo_pago,
        descripcion
    ))

    conn.commit()

# OBTENER GASTOS
def obtener_gastos(usuario_id):

    cursor.execute("""
    SELECT * FROM gastos
    WHERE usuario_id = ?
    ORDER BY id DESC
    """, (
        usuario_id,
    ))

    return cursor.fetchall()

# INSERTAR INGRESO
def insertar_ingreso(
    usuario_id,
    nombre,
    monto,
    fecha,
    fuente,
    descripcion
):

    cursor.execute("""
    INSERT INTO ingresos (
        usuario_id,
        nombre,
        monto,
        fecha,
        fuente,
        descripcion
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        usuario_id,
        nombre,
        monto,
        fecha,
        fuente,
        descripcion
    ))

    conn.commit()

# OBTENER INGRESOS
def obtener_ingresos(usuario_id):

    cursor.execute("""
    SELECT * FROM ingresos
    WHERE usuario_id = ?
    ORDER BY id DESC
    """, (
        usuario_id,
    ))

    return cursor.fetchall()

# ELIMINAR GASTO
def eliminar_gasto(id):

    cursor.execute(
        "DELETE FROM gastos WHERE id = ?",
        (id,)
    )

    conn.commit()


# ACTUALIZAR GASTO
def actualizar_gasto(
    id,
    nombre,
    categoria,
    monto,
    fecha,
    metodo_pago,
    descripcion
):

    cursor.execute("""
    UPDATE gastos
    SET
        nombre = ?,
        categoria = ?,
        monto = ?,
        fecha = ?,
        metodo_pago = ?,
        descripcion = ?
    WHERE id = ?
    """, (
        nombre,
        categoria,
        monto,
        fecha,
        metodo_pago,
        descripcion,
        id
    ))

    conn.commit()


# ELIMINAR INGRESO
def eliminar_ingreso(id):

    cursor.execute(
        "DELETE FROM ingresos WHERE id = ?",
        (id,)
    )

    conn.commit()


# ACTUALIZAR INGRESO
def actualizar_ingreso(
    id,
    nombre,
    monto,
    fecha,
    fuente,
    descripcion
):

    cursor.execute("""
    UPDATE ingresos
    SET
        nombre = ?,
        monto = ?,
        fecha = ?,
        fuente = ?,
        descripcion = ?
    WHERE id = ?
    """, (
        nombre,
        monto,
        fecha,
        fuente,
        descripcion,
        id
    ))

    conn.commit()

# REGISTRAR USUARIO
def registrar_usuario(usuario, password):

    try:

        # HASH PASSWORD
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        cursor.execute("""
        INSERT INTO usuarios (
            usuario,
            password
        )
        VALUES (?, ?)
        """, (
            usuario,
            password_hash
        ))

        conn.commit()

        return True

    except:

        return False


# LOGIN
def login_usuario(usuario, password):

    cursor.execute("""
    SELECT * FROM usuarios
    WHERE usuario = ?
    """, (
        usuario,
    ))

    usuario_db = cursor.fetchone()

    if usuario_db:

        password_guardada = usuario_db[2]

        if bcrypt.checkpw(
            password.encode("utf-8"),
            password_guardada
        ):

            return usuario_db

    return None

# GUARDAR META
def guardar_meta(usuario_id, meta):

    cursor.execute("""
    DELETE FROM metas
    WHERE usuario_id = ?
    """, (usuario_id,))

    cursor.execute("""
    INSERT INTO metas (
        usuario_id,
        meta
    )
    VALUES (?, ?)
    """, (
        usuario_id,
        meta
    ))

    conn.commit()


# OBTENER META
def obtener_meta(usuario_id):

    cursor.execute("""
    SELECT meta
    FROM metas
    WHERE usuario_id = ?
    """, (usuario_id,))

    return cursor.fetchone()