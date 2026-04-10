import reflex as rx
from club_marginalistas.utils import (
    get_all_posts_admin, get_pending_posts,
    delete_post, update_post_status, get_post_by_slug,
    get_all_usuarios,
    get_all_colaboradores, create_colaborador_completo,
    update_colaborador, delete_colaborador, get_colaborador_by_slug,
    send_newsletter_post,
)
from club_marginalistas.models import Post, Usuario, Colaborador
from club_marginalistas.pages.auth import AuthState
from club_marginalistas.styles import (
    page_wrapper, portal_navbar,
    section_header, input_style, textarea_style, select_style,
    btn_primary, btn_danger, panel, form_field,
    feedback_message, page_section_title,
    admin_content_wrapper, accent_divider,
    markdown_content, post_meta_header, C,
)


class AdminState(AuthState):
    posts:          list[Post]        = []
    pending_posts:  list[Post]        = []
    colaboradores:  list[Colaborador] = []
    preview_post:   Post              = Post()
    show_preview:   bool              = False

    # Contributor form fields
    col_slug:       str = ""
    col_email:      str = ""
    col_password:   str = ""
    col_name:       str = ""
    col_initials:   str = ""
    col_role:       str = ""
    col_bio:        str = ""
    col_skills:     str = ""
    col_languages:  str = ""
    col_linkedin:   str = ""
    col_github:     str = ""
    col_twitter:    str = ""
    col_instagram:  str = ""
    col_youtube:    str = ""
    col_email_pub:  str = ""
    col_order:      str = "0"

    message: str = ""

    # Edit modal state
    editing_slug:   str  = ""
    show_edit:      bool = False

    def set_col_slug(self, v):      self.col_slug = v
    def set_col_email(self, v):     self.col_email = v
    def set_col_password(self, v):  self.col_password = v
    def set_col_name(self, v):      self.col_name = v
    def set_col_initials(self, v):  self.col_initials = v
    def set_col_role(self, v):      self.col_role = v
    def set_col_bio(self, v):       self.col_bio = v
    def set_col_skills(self, v):    self.col_skills = v
    def set_col_languages(self, v): self.col_languages = v
    def set_col_linkedin(self, v):  self.col_linkedin = v
    def set_col_github(self, v):    self.col_github = v
    def set_col_twitter(self, v):   self.col_twitter = v
    def set_col_instagram(self, v): self.col_instagram = v
    def set_col_youtube(self, v):   self.col_youtube = v
    def set_col_email_pub(self, v): self.col_email_pub = v
    def set_col_order(self, v):     self.col_order = v

    def load_data(self):
        if not self.logged_in or self.user_role != "admin":
            return rx.redirect("/login")
        self.posts         = get_all_posts_admin()
        self.pending_posts = get_pending_posts()
        self.colaboradores = get_all_colaboradores()

    def preview(self, slug: str):
        for p in self.pending_posts:
            if p.slug == slug:
                self.preview_post = p
                self.show_preview = True
                return

    def close_preview(self):
        self.show_preview = False
        self.preview_post = Post()

    def approve_post(self, slug: str):
        update_post_status(slug, "published")
        post = get_post_by_slug(slug)
        if post:
            send_newsletter_post(post)
        self.message = "✅ Post approved and published."
        self.show_preview = False
        self.load_data()

    def reject_post(self, slug: str):
        update_post_status(slug, "draft")
        self.message = "🗑️ Post rejected."
        self.show_preview = False
        self.load_data()

    def confirm_delete_post(self, slug: str):
        delete_post(slug)
        self.message = "🗑️ Post deleted."
        self.load_data()

    def open_edit(self, slug: str):
        """Load contributor data from DB and open the modal."""
        c = get_colaborador_by_slug(slug)
        if not c:
            return
        self.editing_slug  = slug
        self.col_slug      = c.slug
        self.col_name      = c.name
        self.col_initials  = c.initials
        self.col_role      = c.role
        self.col_bio       = c.bio
        self.col_skills    = c.skills
        self.col_languages = c.languages
        self.col_linkedin  = c.linkedin
        self.col_github    = c.github
        self.col_twitter   = c.twitter
        self.col_instagram = c.instagram
        self.col_youtube   = c.youtube
        self.col_email_pub = c.email_public
        self.col_order     = str(c.order)
        self.show_edit     = True

    def close_edit(self):
        self.show_edit    = False
        self.editing_slug = ""

    def save_edit(self):
        if not self.col_name or not self.col_initials:
            self.message = "❌ Name and initials are required."
            return
        update_colaborador(self.editing_slug, {
            "name":         self.col_name,
            "initials":     self.col_initials,
            "role":         self.col_role,
            "bio":          self.col_bio,
            "skills":       self.col_skills,
            "languages":    self.col_languages,
            "linkedin":     self.col_linkedin,
            "github":       self.col_github,
            "twitter":      self.col_twitter,
            "instagram":    self.col_instagram,
            "youtube":      self.col_youtube,
            "email_public": self.col_email_pub,
            "order":        int(self.col_order or 0),
        })
        self.message = f"✅ Contributor {self.col_name} updated."
        self.show_edit = False
        self.load_data()

    def create_new_colaborador(self):
        if not self.col_slug or not self.col_name or not self.col_email or not self.col_password:
            self.message = "❌ Slug, name, email and password are required."
            return
        result = create_colaborador_completo(
            Colaborador(
                slug=self.col_slug, email=self.col_email,
                name=self.col_name, initials=self.col_initials,
                role=self.col_role, bio=self.col_bio,
                skills=self.col_skills, languages=self.col_languages,
                linkedin=self.col_linkedin, github=self.col_github,
                twitter=self.col_twitter, instagram=self.col_instagram,
                youtube=self.col_youtube, email_public=self.col_email_pub,
                order=int(self.col_order or 0),
            ),
            password=self.col_password,
        )
        if not result["ok"]:
            self.message = f"❌ {result['error']}"
            return
        self.message = f"✅ Contributor {self.col_name} created with portal access."
        self.col_slug = self.col_email = self.col_password = self.col_name = ""
        self.col_initials = self.col_role = self.col_bio = self.col_skills = ""
        self.col_languages = self.col_linkedin = self.col_github = ""
        self.col_twitter = self.col_instagram = self.col_youtube = ""
        self.col_email_pub = ""
        self.col_order = "0"
        self.load_data()

    def confirm_delete_colaborador(self, slug: str):
        delete_colaborador(slug)
        self.message = "🗑️ Contributor deleted."
        self.load_data()


# ============================================
# UI COMPONENTS
# ============================================

def post_preview_modal() -> rx.Component:
    return rx.cond(
        AdminState.show_preview,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        page_section_title("PREVIEW", AdminState.preview_post.title),
                        rx.button(
                            "✕", on_click=AdminState.close_preview,
                            background="transparent", color=C["muted"],
                            border="none", font_size="1.2em", cursor="pointer",
                            _hover={"color": C["text"]},
                        ),
                        justify="between", align="center", width="100%",
                    ),
                    accent_divider(),
                    post_meta_header(
                        AdminState.preview_post.category,
                        AdminState.preview_post.date,
                        AdminState.preview_post.title,
                        AdminState.preview_post.author,
                    ),
                    markdown_content(AdminState.preview_post.content),
                    accent_divider(),
                    rx.hstack(
                        btn_primary("✅ Approve and publish", on_click=AdminState.approve_post(AdminState.preview_post.slug)),
                        btn_danger("❌ Reject", on_click=AdminState.reject_post(AdminState.preview_post.slug)),
                        spacing="3",
                    ),
                    align_items="start", width="100%", spacing="4",
                ),
                background=C["surface"], border=f"1px solid {C['border']}",
                border_radius="8px", padding="2em",
                max_width="760px", width="90%",
                max_height="85vh", overflow_y="auto",
            ),
            position="fixed", top="0", left="0",
            width="100%", height="100%",
            background="rgba(0,0,0,0.75)",
            display="flex", align_items="center", justify_content="center",
            z_index="200",
        ),
    )


def pending_list() -> rx.Component:
    return panel(
        rx.vstack(
            section_header("PENDING APPROVAL"),
            rx.foreach(
                AdminState.pending_posts,
                lambda post: rx.hstack(
                    rx.vstack(
                        rx.text(post.title,  font_weight="500", font_size="0.9em", color=C["text"]),
                        rx.text(post.author, font_size="0.75em", color=C["muted"]),
                        align_items="start", spacing="0",
                    ),
                    rx.hstack(
                        btn_primary("View post", on_click=AdminState.preview(post.slug)),
                        btn_danger("Reject",     on_click=AdminState.reject_post(post.slug)),
                        spacing="2",
                    ),
                    justify="between", align="center", width="100%",
                    padding="1em 0", border_bottom=f"1px solid {C['border']}",
                ),
            ),
            align_items="start", width="100%", spacing="0",
        ),
        margin_top="2em",
    )


def posts_list() -> rx.Component:
    return panel(
        rx.vstack(
            section_header("ALL POSTS"),
            rx.foreach(
                AdminState.posts,
                lambda post: rx.hstack(
                    rx.vstack(
                        rx.text(post.title, font_weight="500", color=C["text"], font_size="0.9em"),
                        rx.hstack(
                            rx.text(post.slug,     color=C["dim"],    font_size="0.72em"),
                            rx.text("·",           color=C["border"], font_size="0.72em"),
                            rx.text(post.category, color=C["accent"], font_size="0.72em"),
                            rx.text("·",           color=C["border"], font_size="0.72em"),
                            rx.text(post.status,   color=C["muted"],  font_size="0.72em"),
                            spacing="2",
                        ),
                        align_items="start", spacing="0",
                    ),
                    rx.alert_dialog.root(
                        rx.alert_dialog.trigger(btn_danger("Delete")),
                        rx.alert_dialog.content(
                            rx.alert_dialog.title("Delete this post?"),
                            rx.alert_dialog.description("This action cannot be undone."),
                            rx.hstack(
                                rx.alert_dialog.cancel(rx.button("Cancel", background="transparent", color=C["muted"], border=f"1px solid {C['border']}", cursor="pointer")),
                                rx.alert_dialog.action(btn_danger("Yes, delete", on_click=AdminState.confirm_delete_post(post.slug))),
                                spacing="3", justify="end",
                            ),
                            background=C["surface"], color=C["text"], border=f"1px solid {C['border']}",
                        ),
                    ),
                    justify="between", align="center", width="100%",
                    padding="1em 0", border_bottom=f"1px solid {C['border']}",
                ),
            ),
            align_items="start", width="100%", spacing="0",
        ),
        margin_top="2em",
    )


def colaborador_form() -> rx.Component:
    return panel(
        rx.vstack(
            # Portal access
            section_header("PORTAL ACCESS"),
            rx.grid(
                form_field("Email",    rx.input(value=AdminState.col_email,    on_change=AdminState.set_col_email,    placeholder="email@address.com",  type="email",    **input_style)),
                form_field("Password", rx.input(value=AdminState.col_password, on_change=AdminState.set_col_password, placeholder="Initial password",    type="password", **input_style)),
                columns="2", spacing="4", width="100%",
            ),
            accent_divider(),
            # Profile data
            section_header("PUBLIC PROFILE"),
            rx.grid(
                form_field("Full name",   rx.input(value=AdminState.col_name,     on_change=AdminState.set_col_name,     placeholder="Diego Herrera Castañeda",        **input_style)),
                form_field("Slug (URL)",  rx.input(value=AdminState.col_slug,     on_change=AdminState.set_col_slug,     placeholder="diego-herrera",                  **input_style)),
                form_field("Initials",    rx.input(value=AdminState.col_initials, on_change=AdminState.set_col_initials, placeholder="DH",                             **input_style)),
                form_field("Title / Role", rx.input(value=AdminState.col_role,    on_change=AdminState.set_col_role,     placeholder="Economist · Data Analyst",       **input_style)),
                form_field("Skills",      rx.input(value=AdminState.col_skills,   on_change=AdminState.set_col_skills,   placeholder="Python,SQL,Power BI",            **input_style)),
                form_field("Languages",   rx.input(value=AdminState.col_languages,on_change=AdminState.set_col_languages,placeholder="Spanish (Native),English (C1)",  **input_style)),
                form_field("Order",       rx.input(value=AdminState.col_order,    on_change=AdminState.set_col_order,    placeholder="0",                              **input_style)),
                form_field("Public email", rx.input(value=AdminState.col_email_pub,on_change=AdminState.set_col_email_pub,placeholder="contact@address.com",           **input_style)),
                columns="2", spacing="4", width="100%",
            ),
            form_field("Bio / Professional summary",
                rx.text_area(value=AdminState.col_bio, on_change=AdminState.set_col_bio,
                             placeholder="Professional summary...", **textarea_style),
            ),
            accent_divider(),
            # Social media
            section_header("SOCIAL MEDIA (optional)"),
            rx.grid(
                form_field("LinkedIn",  rx.input(value=AdminState.col_linkedin,  on_change=AdminState.set_col_linkedin,  placeholder="https://linkedin.com/in/...", **input_style)),
                form_field("GitHub",    rx.input(value=AdminState.col_github,    on_change=AdminState.set_col_github,    placeholder="https://github.com/...",     **input_style)),
                form_field("X/Twitter", rx.input(value=AdminState.col_twitter,   on_change=AdminState.set_col_twitter,   placeholder="https://x.com/...",          **input_style)),
                form_field("Instagram", rx.input(value=AdminState.col_instagram, on_change=AdminState.set_col_instagram, placeholder="https://instagram.com/...",  **input_style)),
                form_field("YouTube",   rx.input(value=AdminState.col_youtube,   on_change=AdminState.set_col_youtube,   placeholder="https://youtube.com/...",    **input_style)),
                columns="2", spacing="4", width="100%",
            ),
            btn_primary("Create contributor", on_click=AdminState.create_new_colaborador),
            align_items="start", width="100%", spacing="4",
        ),
    )


def edit_modal() -> rx.Component:
    return rx.cond(
        AdminState.show_edit,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        page_section_title("EDIT", AdminState.col_name),
                        rx.button(
                            "✕", on_click=AdminState.close_edit,
                            background="transparent", color=C["muted"],
                            border="none", font_size="1.2em", cursor="pointer",
                            _hover={"color": C["text"]},
                        ),
                        justify="between", align="center", width="100%",
                    ),
                    accent_divider(),
                    rx.grid(
                        form_field("Full name",    rx.input(value=AdminState.col_name,      on_change=AdminState.set_col_name,      **input_style)),
                        form_field("Initials",     rx.input(value=AdminState.col_initials,  on_change=AdminState.set_col_initials,  **input_style)),
                        form_field("Title / Role", rx.input(value=AdminState.col_role,      on_change=AdminState.set_col_role,      **input_style)),
                        form_field("Skills",       rx.input(value=AdminState.col_skills,    on_change=AdminState.set_col_skills,    **input_style)),
                        form_field("Languages",    rx.input(value=AdminState.col_languages, on_change=AdminState.set_col_languages, **input_style)),
                        form_field("Order",        rx.input(value=AdminState.col_order,     on_change=AdminState.set_col_order,     **input_style)),
                        form_field("Public email", rx.input(value=AdminState.col_email_pub, on_change=AdminState.set_col_email_pub, **input_style)),
                        form_field("LinkedIn",     rx.input(value=AdminState.col_linkedin,  on_change=AdminState.set_col_linkedin,  **input_style)),
                        form_field("GitHub",       rx.input(value=AdminState.col_github,    on_change=AdminState.set_col_github,    **input_style)),
                        form_field("X/Twitter",    rx.input(value=AdminState.col_twitter,   on_change=AdminState.set_col_twitter,   **input_style)),
                        form_field("Instagram",    rx.input(value=AdminState.col_instagram, on_change=AdminState.set_col_instagram, **input_style)),
                        form_field("YouTube",      rx.input(value=AdminState.col_youtube,   on_change=AdminState.set_col_youtube,   **input_style)),
                        columns="2", spacing="4", width="100%",
                    ),
                    form_field("Bio",
                        rx.text_area(value=AdminState.col_bio, on_change=AdminState.set_col_bio,
                                     min_height="120px", **input_style),
                    ),
                    rx.hstack(
                        btn_primary("Save changes", on_click=AdminState.save_edit),
                        rx.button("Cancel", on_click=AdminState.close_edit,
                                  background="transparent", color=C["muted"],
                                  border=f"1px solid {C['border']}", cursor="pointer",
                                  border_radius="4px", padding="0.65em 1.75em"),
                        spacing="3",
                    ),
                    align_items="start", width="100%", spacing="4",
                ),
                background=C["surface"], border=f"1px solid {C['border']}",
                border_radius="8px", padding="2em",
                max_width="760px", width="90%",
                max_height="85vh", overflow_y="auto",
            ),
            position="fixed", top="0", left="0",
            width="100%", height="100%",
            background="rgba(0,0,0,0.75)",
            display="flex", align_items="center", justify_content="center",
            z_index="200",
        ),
    )


def colaboradores_list() -> rx.Component:
    return panel(
        rx.vstack(
            section_header("REGISTERED CONTRIBUTORS"),
            rx.foreach(
                AdminState.colaboradores,
                lambda c: rx.hstack(
                    rx.vstack(
                        rx.text(c.name, font_weight="500", font_size="0.9em", color=C["text"]),
                        rx.hstack(
                            rx.text(c.slug,  font_size="0.72em", color=C["dim"]),
                            rx.text("·",     font_size="0.72em", color=C["border"]),
                            rx.text(c.email, font_size="0.72em", color=C["accent"]),
                            spacing="2",
                        ),
                        align_items="start", spacing="0",
                    ),
                    rx.hstack(
                        btn_primary("Edit", on_click=AdminState.open_edit(c.slug)),
                        rx.alert_dialog.root(
                            rx.alert_dialog.trigger(btn_danger("Delete")),
                            rx.alert_dialog.content(
                                rx.alert_dialog.title("Delete this contributor?"),
                                rx.alert_dialog.description("This action removes the profile and portal access."),
                                rx.hstack(
                                    rx.alert_dialog.cancel(rx.button("Cancel", background="transparent", color=C["muted"], border=f"1px solid {C['border']}", cursor="pointer")),
                                    rx.alert_dialog.action(btn_danger("Yes, delete", on_click=AdminState.confirm_delete_colaborador(c.slug))),
                                    spacing="3", justify="end",
                                ),
                                background=C["surface"], color=C["text"], border=f"1px solid {C['border']}",
                            ),
                        ),
                        spacing="2",
                    ),
                    justify="between", align="center", width="100%",
                    padding="1em 0", border_bottom=f"1px solid {C['border']}",
                ),
            ),
            align_items="start", width="100%", spacing="0",
        ),
        margin_top="2em",
    )


def admin_page() -> rx.Component:
    return page_wrapper(
        portal_navbar("ADMIN PANEL", AdminState.logout),
        post_preview_modal(),
        edit_modal(),
        admin_content_wrapper(
            page_section_title("POSTS", "Manage posts"),
            feedback_message(AdminState.message),
            pending_list(),
            posts_list(),
            accent_divider(),
            page_section_title("CONTRIBUTORS", "Manage contributors"),
            colaborador_form(),
            colaboradores_list(),
        ),
        on_mount=AdminState.load_data,
    )
