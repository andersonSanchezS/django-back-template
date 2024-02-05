from django.core.management.base import BaseCommand, CommandError
import os
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Migrar toda la data de los fixtures a la base de datos.'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str, help='Nombre de la app')

    def handle(self, *args, **options):
        arg = options['app']
        fixtures_dir = os.path.join('apps', arg, 'fixtures')
        for fixture in os.listdir(fixtures_dir):
            if fixture.endswith('.json'):
                fixture_path = os.path.join(fixtures_dir, fixture)
                print(f'Cargando fixture {fixture_path}')
                call_command('loaddata', fixture_path)
        self.stdout.write(self.style.SUCCESS('Data cargada con éxito'))