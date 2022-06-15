from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from social_django.models import UserSocialAuth

from gdrive.models import CopyGDFile, GDFile
from users.models import User
from users.utils import check_and_refresh_token

User = get_user_model()


def get_folder_id(name=settings.DEFAULT_SHARED_FOLDER):
    service = get_global_gdrive_service()
    folder = service.files().list(q='mimeType=\'application/vnd.google-apps.folder\' and name = \'{}\''.format(name)).execute()
    folder_id = folder.get('files', [])[0].get('id')
    return folder_id


def create_permissions(username):
    user = User.objects.get(username=username)
    service = get_global_gdrive_service()
    folder_id = get_folder_id()
    user_permission = {
        'type': 'group',
        'role': 'writer',
        'emailAddress': user.email
    }
    service.permissions().create(
        fileId=folder_id,
        body=user_permission
    ).execute()


def get_global_gdrive_service():
    user = User.objects.get(username=settings.DEFAULT_SHARED_USER)
    return get_gdrive_service(user=user, provider='google-oauth2', scopes=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE)


def get_admin_sdk_service():
    user = User.objects.get(username=settings.DEFAULT_SHARED_USER)
    service = get_gdrive_service(user, provider='google-oauth2',
                                 scopes=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE, service_type='admin', version='directory_v1')
    return service


def get_gdrive_service(user=None, provider=None, scopes=None, service_type='drive', version='v3'):
    check_and_refresh_token(user, provider)
    social = user.social_auth.get(provider=provider)
    credentials = Credentials(token=social.extra_data['access_token'], scopes=scopes)
    service = build(service_type, version, credentials=credentials)
    return service


# NOT WORKING
def get_user_file(user=None, provider=None, scopes=None, file_id=None):
    file = GDFile.objects.get(id=file_id)
    queryset = file.original_file.all()
    print(len(queryset))
    if len(queryset) != 0:
        return queryset.first().copy
    return file


def get_user_files(provider=None, scopes=None):
    user = User.objects.get(username=settings.DEFAULT_SHARED_USER)
    service = get_gdrive_service(user, provider, scopes)
    # folder_id = get_folder_id()
    # print('\'{}\' in parents'.format(folder_id))
    # results = service.files().list(q='\'{}\' in parents and trashed = false'.format(folder_id),
    #     fields='files(id, name, mimeType, iconLink, webViewLink)'
    # ).execute()
    results = service.files().list(q='mimeType!=\'application/vnd.google-apps.folder\' and trashed = false', fields='files(id, name, mimeType, iconLink, webViewLink)').execute()
    items = results.get('files', [])
    # copies_id = GDFile.objects.all().values_list("id", flat=True)
    print(items)
    # add search algorithm
    # for i, item in enumerate(items):
    #     for c_id in copies_id:
    #         if item.get("id") == c_id:
    #             print("copy")
    #             items.remove(item)
    # for i in items:
    #     if i.get('exportLinks') is None:
    #         url = 'https://drive.google.com/uc?id={}&authuser=0&export=download'
    #         i['exportLinks'] = url.format(i['id'])
    print(items)
    return items


def save_files_to_db(user=None, provider=None, scopes=None):
    files = get_user_files(provider, scopes)
    GDFile.objects.bulk_create([
        GDFile(id=f.get('id'), name=f.get('name'), mimetype=f.get('mimeType'), social=user.social_auth.get(provider='google-oauth2')) for f in files
    ])


def download_file(user=None, provider=None, scopes=None, file_id=None):
    copy_id = None
    try:
        original = GDFile.objects.get(id=file_id) # getting original file
    except GDFile.DoesNotExist:
        default_user = User.objects.get(username=settings.DEFAULT_SHARED_USER).social_auth.get(provider='google-oauth2')
        original = GDFile.objects.create(id=file_id, owner=default_user)
    else:
        if original.original_copies.count() != 0:
            try:
                copy = CopyGDFile.objects.get(original_id=file_id, owner__user_id=user.id)
                return new_download_url(user, provider, scopes, copy.id)
            except CopyGDFile.DoesNotExist:
                copy = CopyGDFile.objects.filter(original_id=file_id).first()
                copy_id = copy.id
        
        # if original.original_copies:
    # if res.
    # if res:
    #     print(True)
    #     if GDFile.objects.filter(original_id=file_id, owner_id=user.id):
    #         return new_download_url(user, provider, scopes, res.id)
    #     copy_file_id = test_copy_file(user, provider, scopes, res.id, original_file_id=file_id)
    # else:
    #     print(False)
    #     copy_file_id = test_copy_file(user, provider, scopes, file_id, original_file_id=file_id)
    copy_file_id = test_copy_file(user, provider, scopes, file_id=file_id, copy_id=copy_id)
    new_create_permissions(user, provider, scopes, copy_file_id)
    return new_download_url(user, provider, scopes, copy_file_id)


    # file_id_copy = test_copy_file(user, provider, scopes, file_id)

    # return get_download_url(user, provider, scopes, file.id)
    # return get_download_url(user, provider, scopes, file_id_copy)


def new_download_url(user, provider, scopes, file_id):
    service = get_gdrive_service(user, provider, scopes)
    results = service.files().get(fileId=file_id, fields='id,exportLinks,mimeType').execute()
    return results.get('exportLinks').get('application/pdf')


def new_create_permissions(user, provider, scopes, file_id):
    # user = User.objects.get(username=username)
    service = get_gdrive_service(user, provider, scopes)
    user_permission = {
        'role': 'reader',
        'type': 'anyone',
    }
    service.permissions().create(
        fileId=file_id,
        body=user_permission
    ).execute()


# todo new (deprecated)
def check_download(user=None, provider=None, scopes=None, file_id=None):
    service = get_gdrive_service(user, provider, scopes)
    results = service.files().list(fields='files(id, name, mimeType, iconLink, webViewLink)').execute()
    items = results.get('files', [])
    copies_id = GDFile.objects.filter(original_id=file_id)
    for item in items:
        for c_id in copies_id:
            if item.get("id") == c_id.id:
                print("true")
                return get_download_url(user, provider, scopes, c_id.id)
    print("false")
    test_create_permissions(user, file_id)
    file_id_copy = test_copy_file(user, provider, scopes, file_id)
    return get_download_url(user, provider, scopes, file_id_copy)


def get_download_url(user, provider, scopes, file_id):
    service = get_gdrive_service(user, provider, scopes)
    result = service.files().get(fileId=file_id, fields='exportLinks').execute()
    if result.get('exportLinks') is None:
        url = 'https://drive.google.com/uc?id={}&authuser=0&export=download'
        result['exportLinks'] = url.format(file_id)
        return result['exportLinks']
    return result.get('exportLinks').get('application/pdf')


def test_create_permissions(username, file_id):
    user = User.objects.get(username=username)
    service = get_global_gdrive_service()
    # folder_id = get_folder_id()x

    user_permission = {
        'role': 'reader',
        'type': 'anyone',
    }
    # user_permission = {
    #     'type': 'user',
    #     'role': 'reader',
    #     'emailAddress': user.email
    # }
    service.permissions().create(
        fileId=file_id,
        body=user_permission
    ).execute()


def test_copy_file(user=None, provider=None, scopes=None, file_id=None, copy_id=None):
    service = get_gdrive_service(user, provider, scopes)
    file_id_to_copy = file_id
    if copy_id:
        file_id_to_copy = copy_id
        
    result = service.files().copy(fileId=file_id_to_copy).execute()
    print(result.get('id'))
    CopyGDFile.objects.create(original_id=file_id, id=result.get('id'), copy_id=copy_id, owner_id=user.social_auth.get(provider='google-oauth2').id)
    return result.get('id')


def copy_file(user=None, provider=None, scopes=None, file_id=None):
    service = get_gdrive_service(user, provider, scopes)
    result = service.files().copy(fileId=file_id).execute()  # TODO add name
    GDFile.objects.create(owner=user.social_auth.get(provider=provider), original_id=file_id, id=result.get('id'))
    file = GDFile.objects.filter(original_id=file_id).first()
    return file


def get_file_by_id(user, provider, scopes, file_id):
    service = get_gdrive_service(user, provider, scopes)
    file = service.files().get(fileId=file_id, fields='files(id, name, mimeType, thumbnailLink, webViewLink)').execute()
    return file

