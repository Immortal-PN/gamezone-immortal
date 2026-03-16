from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import GalleryImage, Game, Genre, Platform


class Command(BaseCommand):
    help = "Seed GameZone with premium demo content."

    def handle(self, *args, **options):
        genre_data = [
            ("Action", "#FF6B2C", "bolt"),
            ("Racing", "#47D7AC", "track"),
            ("Horror", "#F04F78", "moon"),
            ("Sports", "#6C8CFF", "arena"),
            ("RPG", "#FDBB2D", "quest"),
            ("Indie", "#E8E1D9", "spark"),
        ]
        platform_names = ["PC", "PlayStation 5", "Xbox Series X", "Nintendo Switch"]

        genres = {}
        for name, color, icon in genre_data:
            genres[name], _ = Genre.objects.get_or_create(
                slug=slugify(name),
                defaults={"name": name, "accent_color": color, "icon": icon},
            )

        platforms = {}
        for name in platform_names:
            platforms[name], _ = Platform.objects.get_or_create(
                slug=slugify(name),
                defaults={"name": name},
            )

        games = [
            {
                "title": "Neon Rift",
                "tagline": "Hyper-charged tactical action inside a living megacity.",
                "short_description": "Glide between districts, outsmart syndicates, and turn every rooftop into a spectacle.",
                "description": "Neon Rift blends slick traversal, cinematic firefights, and reactive world events into a stylish action campaign built for players who love momentum.",
                "studio": "Pulse Forge",
                "release_year": 2026,
                "playtime": "22 hrs",
                "age_rating": "16+",
                "price": 59.99,
                "discount_price": 44.99,
                "critic_score": 94,
                "player_rating": 4.9,
                "is_featured": True,
                "is_trending": True,
                "is_new_release": True,
                "is_editors_pick": True,
                "hero_badge": "Live Now",
                "cover_url": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=900&q=80",
                "banner_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1600&q=80",
                "trailer_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "genres": ["Action", "RPG"],
                "platforms": ["PC", "PlayStation 5", "Xbox Series X"],
            },
            {
                "title": "Midnight Apex",
                "tagline": "Street racing with luxury visuals and midnight drama.",
                "short_description": "Build your lineup, chase citywide legends, and own the night.",
                "description": "Midnight Apex delivers precision driving, lavish car culture, and a soundtrack-forward campaign with social rivalries and relentless style.",
                "studio": "Velocity Ritual",
                "release_year": 2025,
                "playtime": "18 hrs",
                "age_rating": "13+",
                "price": 49.99,
                "discount_price": 39.99,
                "critic_score": 90,
                "player_rating": 4.7,
                "is_trending": True,
                "is_new_release": True,
                "cover_url": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=900&q=80",
                "banner_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=80",
                "genres": ["Racing", "Indie"],
                "platforms": ["PC", "PlayStation 5"],
            },
            {
                "title": "Velvet Eclipse",
                "tagline": "An atmospheric horror odyssey shaped by your fear threshold.",
                "short_description": "Explore a haunted resort where memory is more dangerous than monsters.",
                "description": "Velvet Eclipse leans into tension, lavish sound design, and branching narrative choices to create a prestige horror experience.",
                "studio": "Obsidian Bloom",
                "release_year": 2025,
                "playtime": "14 hrs",
                "age_rating": "18+",
                "price": 54.99,
                "critic_score": 88,
                "player_rating": 4.6,
                "is_editors_pick": True,
                "cover_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
                "banner_url": "https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?auto=format&fit=crop&w=1600&q=80",
                "genres": ["Horror", "RPG"],
                "platforms": ["PC", "Xbox Series X"],
            },
            {
                "title": "Crown District FC",
                "tagline": "A fashion-forward football sim with club culture at its center.",
                "short_description": "Manage talent, shape tactics, and build a dynasty that looks as good as it plays.",
                "description": "Crown District FC mixes strategy, story, and editorial-grade presentation into a sports sim built for modern players.",
                "studio": "Goldline Interactive",
                "release_year": 2026,
                "playtime": "40 hrs",
                "age_rating": "3+",
                "price": 69.99,
                "critic_score": 91,
                "player_rating": 4.8,
                "is_new_release": True,
                "cover_url": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=900&q=80",
                "banner_url": "https://images.unsplash.com/photo-1517927033932-b3d18e61fb3a?auto=format&fit=crop&w=1600&q=80",
                "genres": ["Sports"],
                "platforms": ["PC", "PlayStation 5", "Nintendo Switch"],
            },
        ]

        for payload in games:
            game, _ = Game.objects.update_or_create(
                slug=slugify(payload["title"]),
                defaults={
                    key: value
                    for key, value in payload.items()
                    if key not in {"genres", "platforms"}
                },
            )
            game.genres.set([genres[name] for name in payload["genres"]])
            game.platforms.set([platforms[name] for name in payload["platforms"]])
            if not game.gallery.exists():
                GalleryImage.objects.create(
                    game=game,
                    image_url=game.banner_url,
                    caption="Signature key art",
                    sort_order=1,
                )
                GalleryImage.objects.create(
                    game=game,
                    image_url=game.cover_url,
                    caption="Cover frame",
                    sort_order=2,
                )

        self.stdout.write(self.style.SUCCESS("GameZone demo content is ready."))
