import subprocess
from pathlib import Path, WindowsPath

from .utils import read_secret_key


class ProjectSetup:

    def __init__(self, params: dict):
        self.working_dir = params.pop('Path')
        self.venv_name = params.pop('venv_name')
        self.project_name = params.pop('project_name')
        self.virtualenv_dir = self.working_dir / f'{self.venv_name}'
        self.project_dir = None

        if self.working_dir == WindowsPath('.'):
            self.working_dir = Path.cwd()

    def create_virtualenv(self):
        if not self.virtualenv_dir.exists():
            print(f'Create virtual environment - {self.venv_name}.. \n')
            subprocess.run(['virtualenv', f'{self.venv_name}'], text=True)
        else:
            self.activate_virtualenv()

    def activate_virtualenv(self):
        print(f'Activating virtual environment - {self.venv_name}..')
        assert self.virtualenv_dir.exists()
        activate_this_file = self.virtualenv_dir / 'Scripts/activate_this.py'
        exec(open(activate_this_file).read(),
             dict(__file__=activate_this_file))

    def install_packages(self):
        print('Installing packages: Django django-decouple')
        subprocess.run(['pip', 'install', 'Django==3.1.3', 'django-decouple'])

    def create_project(self):
        """
        Check if there is an existing project in the working dir
        by checking the `manage.py` file.

        if `manage.py` file not exists, it creates a new project.
        """
        try:
            manage_file = [file for file in self.working_dir.rglob(
                'manage.py')][0]
        except IndexError:
            manage_file = None

        if manage_file:
            # project exists
            self.project_dir = manage_file.parent
            print(f'Project found in "{self.project_dir}"')
        else:
            # start project
            print(f'Creating Django Project - {self.project_name} ', end='')
            subprocess.run(['django-admin', 'startproject',
                            f'{self.project_name}'])
            print('\t\t\t\tDone')
            self.project_dir = self.working_dir / f'{self.project_name}'

    def outer_folder_rename(self):
        """
        If default project name `config` is used, the outer folder is
        renamed to `src`.
        """
        if self.project_dir.name == 'config':
            print('\nRename `config` to `src`')
            self.project_dir = self.project_dir.rename('src')

    def prepopulate_env_variables(self):
        print('\nPrepopulate enviromental variables.\n')
        # read settings.py
        settings_file = self.project_dir / f'{self.project_name}/settings.py'

        django_secret_key = read_secret_key(settings_file)

        # create `.env` for managing enviromental variables
        # `.env` file
        env_file = self.project_dir / '.env'

        # prepopulate some values in `.env` file
        env_file.write_text(
            f'''
DJANGO_SECRET_KEY={django_secret_key}
DEBUG=True
ALLOWED_HOSTS=.localhost
        ''')

    def execute(self):
        self.create_virtualenv()
        self.activate_virtualenv()
        self.create_project()
        self.install_packages()
        self.outer_folder_rename()
        self.prepopulate_env_variables()
