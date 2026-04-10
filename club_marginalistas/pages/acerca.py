import reflex as rx
from club_marginalistas.newsletter_state import NewsletterState
from club_marginalistas.styles import (
    page_wrapper, page_content, page_hero,
    navbar, footer, newsletter,
    panel, section_header, info_card, accent_divider,
)


def acerca_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        page_hero("ABOUT US", "About the Club"),
        page_content(
            rx.vstack(
                # Intro
                rx.vstack(
                    rx.text(
                        "El Club de los Marginalistas is an independent economic analysis space. "
                        "We publish essays, current affairs analysis and theoretical reflections on economics, "
                        "financial markets and economic policy from a rigorous and academic perspective.",
                        line_height="1.85",
                    ),
                    rx.text(
                        "The name pays homage to the marginalist economists of the 19th century — Jevons, Menger, Walras — "
                        "who transformed the discipline by introducing marginal analysis as a central tool "
                        "of economic thought. That same spirit of rigor, intellectual independence and willingness "
                        "to question the consensus guides every publication.",
                        line_height="1.85",
                    ),
                    align_items="start", spacing="5", width="100%",
                ),

                # What we do
                rx.box(height="2.5em"),
                section_header("WHAT WE DO"),
                accent_divider(),
                rx.box(height="1em"),
                rx.grid(
                    info_card("Economic Theory",    "Analysis of the major currents of economic thought: Austrian school, Keynesianism, monetarism and their current implications."),
                    info_card("Market Analysis",    "Tracking of global financial markets with a focus on equities, currencies, commodities and interest rates."),
                    info_card("Macroeconomics",     "Fiscal, monetary and exchange rate policy. Economic outlook for Colombia and Latin America in a global perspective."),
                    info_card("Microeconomics",     "Consumer theory, industrial organization, competition and regulation. Practical cases and real-world applications."),
                    columns="2", spacing="4", width="100%",
                ),

                # Editorial principles
                rx.box(height="2.5em"),
                section_header("EDITORIAL PRINCIPLES"),
                accent_divider(),
                rx.box(height="1em"),
                panel(
                    rx.vstack(
                        info_card("Independence", "No political affiliations or commercial interests. The analysis follows the evidence, not convenience."),
                        info_card("Rigor",        "Every argument is supported by empirical evidence or solid theoretical foundations."),
                        info_card("Clarity",      "Economic knowledge should be accessible. We write for intelligent readers, not necessarily specialists."),
                        info_card("Long-term",    "We avoid short-term noise. We are interested in structural trends, cycles and patterns that endure."),
                        align_items="start", spacing="3", width="100%",
                    ),
                ),

                # Contact
                rx.box(height="2.5em"),
                section_header("CONTACT"),
                accent_divider(),
                rx.box(height="1em"),
                panel(
                    rx.hstack(
                        rx.text("For collaborations, suggestions or inquiries:"),
                        rx.link("elclubdelosmarginalistas@gmail.com", href="mailto:elclubdelosmarginalistas@gmail.com"),
                        spacing="2", align="center", flex_wrap="wrap",
                    ),
                ),

                align_items="start", width="100%", spacing="0",
            ),
        ),
        newsletter(
            NewsletterState.email,
            NewsletterState.set_email,
            NewsletterState.subscribe,
            NewsletterState.message,
        ),
        footer(),
    )
