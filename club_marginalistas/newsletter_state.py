import reflex as rx
from club_marginalistas.utils import subscribe_newsletter


class NewsletterState(rx.State):
    email: str = ""
    message: str = ""

    def set_email(self, v: str):
        self.email = v

    def subscribe(self):
        if not self.email or "@" not in self.email:
            self.message = "Please enter a valid email."
            return
        result = subscribe_newsletter(self.email)
        if result["ok"]:
            self.message = "✅ Subscription successful!"
            self.email = ""
        else:
            self.message = "❌ Subscription error. Please try again."
