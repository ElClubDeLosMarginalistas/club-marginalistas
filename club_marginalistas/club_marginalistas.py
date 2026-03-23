import reflex as rx
from club_marginalistas.pages.index import index_page
from club_marginalistas.pages.post import post_page
from club_marginalistas.pages.admin import admin_page
from club_marginalistas.pages.acerca import acerca_page
from club_marginalistas.pages.colaboradores import colaboradores_page
from club_marginalistas.pages.trading import trading_page
from club_marginalistas.auth import login_page
from club_marginalistas.portal import portal_page
from club_marginalistas.pages.page_404 import page_404
from club_marginalistas.pages.colaboradores import colaborador_page


app = rx.App()
app.add_page(index_page, route="/")
app.add_page(post_page, route="/blog/[slug]")
app.add_page(admin_page, route="/admin")
app.add_page(acerca_page, route="/acerca")
app.add_page(colaboradores_page, route="/colaboradores")
app.add_page(trading_page, route="/trading")
app.add_page(login_page,  route="/login")
app.add_page(portal_page, route="/portal")
app.add_page(page_404, route="/404")
app.add_page(colaborador_page, route="/colaboradores/[slug]")