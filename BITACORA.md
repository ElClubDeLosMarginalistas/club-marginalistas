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