from django.contrib.auth import get_user_model

from gdrive.models import GDFile
from gdrive.utils import save_files_to_db

User = get_user_model()

def get_default_user():
    pass
