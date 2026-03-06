import glob
import frontmatter
from club_marginalistas.models import Post


def get_all_posts() -> list[Post]:
    posts = []
    for path in sorted(glob.glob("posts/*.md"), reverse=True):
        raw = frontmatter.load(path)
        slug = path.split("/")[-1].replace(".md", "")
        posts.append(Post(
            slug=slug,
            title=raw.get("title", "Sin título"),
            description=raw.get("description", ""),
            author=raw.get("author", "Anónimo"),
            date=str(raw.get("date", "")),
            image=raw.get("image", ""),
            category=raw.get("category", "General"),
            content=raw.content,
        ))
    return posts


def get_post_by_slug(slug: str) -> Post | None:
    for post in get_all_posts():
        if post.slug == slug:
            return post
    return None