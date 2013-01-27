from django.core.management.base import BaseCommand, CommandError
from ...parser import get_themes_ids, get_theme_content, save_new_theme

class Command(BaseCommand):
    args = 'number of pages for parsing'
    help = 'Parse jedi forum for new themes'

    def handle(self, number_of_pages, *args, **options):
        ids = get_themes_ids(int(number_of_pages))
        for id in ids:
            theme_content = get_theme_content(id)
            save_new_theme(theme_content)
        self.stdout.write('Successfully parsed')

