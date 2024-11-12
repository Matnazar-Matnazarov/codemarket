# config/management/commands/tags.py

from django.core.management.base import BaseCommand
from blog.models.model_blog_post import Tags, Post

class Command(BaseCommand):
    help = 'Create a tag and associate it with the first post'

    def handle(self, *args, **options):
        # Birinchi Post obyektini olish
        post = Post.objects.first()
        
        if not post:
            self.stdout.write(self.style.ERROR('No Post found'))
            return
        
        # Tags yaratish va postga bog'lash
        tag = Tags.objects.create(name="Python", slug="python")
        post.tags.add(tag)
        post.save()

        self.stdout.write(self.style.SUCCESS(f'Tag "{tag.name}" successfully added to post "{post.title}"'))
