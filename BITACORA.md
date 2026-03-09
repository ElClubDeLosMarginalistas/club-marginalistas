Bitácora — El Club de los Marginalistas

Sesión 1 — 05 Mar 2025

Entorno instalado:

Python 3.12, VSCode, extensión Python + Pylance
Reflex + python-frontmatter
Entorno virtual en .venv

Proyecto creado:
/home/diego-herrera/club-marginalistas/

Estructura actual:

club-marginalistas/
├── posts/
│   └── 2025-03-01-bienvenida.md
├── club_marginalistas/
│   ├── __init__.py
│   ├── club_marginalistas.py   ← app principal + rutas
│   ├── models.py               ← dataclass Post
│   ├── utils.py                ← lector de .md
│   └── pages/
│       ├── __init__.py
│       ├── index.py            ← grid de tarjetas
│       └── post.py             ← página individual
├── rxconfig.py
└── requirements.txt

Funcionando:

Página principal con tarjetas de posts
Página individual al hacer click
Botón volver al blog
Posts en Markdown con frontmatter

Sesión 2 — 06 Mar 2025

Infraestructura y cuentas:

Dominio elclubdelosmarginalistas.com en Namecheap ✅
Gmail elclubdelosmarginalistas@gmail.com creado ✅
Cuenta GitHub ElClubDeLosMarginalistas creada ✅
Azure descartado
Zoho y Private Email descartados (sin tier gratis)

Control de versiones:

Git 2.43.0 instalado en Ubuntu ✅
Git configurado con nombre y correo del proyecto ✅
Repositorio club-marginalistas creado en GitHub (privado) ✅
.gitignore configurado ✅
Primer commit: 13 archivos, 307 líneas ✅
Código subido a GitHub con token de acceso ✅

Sesión 3 — 07 Mar 2025

Base de datos:

Cuenta Supabase creada y vinculada con GitHub ✅
Base de datos PostgreSQL en Supabase ✅
Conexión via Session Pooler (IPv4 compatible) ✅
Archivo .env con credenciales configurado ✅
Tabla post creada con SQLModel ✅
Post de bienvenida migrado a la base de datos ✅
Commit y push a GitHub ✅