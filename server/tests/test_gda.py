import unittest

import google.oauth2.credentials
from django.conf import settings
from django.contrib.auth import get_user_model
from googleapiclient.discovery import build

from gdrive.models import GDFile
from gdrive.utils import copy_file, get_user_file

User = get_user_model()

class TestGDrive(unittest.TestCase):

    # @classmethod
    # def setUpTestData(cls):
    #     user = User.objects.create_user(username='pochikalin', password='12345', email='pochikalin@gmail.com')
    #     data = {"user": 1, "provider": "google-oauth2", "uid": "pochikalin@gmail.com", "extra_data": "{\"auth_time\": 1635771099, \"refresh_token\": \"1//0cwQBertPB7YOCgYIARAAGAwSNwF-L9Irlxx-YrqAZaV07dJCCvmEX0rnBI24w7MrWUUrXP_YEEY1SSyIsczINAAoAcbCDwurn1g\", \"expires\": 3599, \"token_type\": \"Bearer\", \"access_token\": \"ya29.a0ARrdaM8mfWmPTqvhehaS13EqcpurA-sch-XAjegFtIY2ZfG4qBVPrDlzV5EQGPp3PhyeDwlzeI6z_ayKbYVh32j6fbJwgQnczO1yWprH1OZcsA-5peOf09Sw04aSViOVO0TVuhoqp0XA8E7qpI1G2Y9T-OxoHA\"}", "created": "2021-10-31T13:42:27.552Z", "modified": "2021-11-01T12:51:39.396Z"}
    #     file = {'id': '1T60gPq79wFkBa1Q7iNPtZJk26S71b1ifut57jJH-_Uc', 'name': 'file1', 'social_id': 1}
    #     user.social_user.create(**data)
    #     GDFile.objects.create(**file)
    #     super().setUpTestData()

    def test_files(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/drive']
        social = User.objects.get(id=4).social_auth.get(provider='google-oauth2')
        # print(social.refresh_token(load_strategy()))
        # strategy = load_strategy('google-oauth2')
        # print(social.refresh(strategy))
        USER_INFO = {
            'scopes': SCOPES,
            'token': social.extra_data['access_token']
        }

        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        # print(social.get_access_token(load_strategy()))

        creds = google.oauth2.credentials.Credentials(**USER_INFO)
        # print(creds.refresh_token())
        service = build('drive', 'v3', credentials=creds, always_use_jwt_access=True)
        # Call the Drive v3 API
        results = service.files().list().execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        assert True

    def test_copy(self):
        user = User.objects.get(username='fakedriveapi')
        # file_id = '1_5NqR-Ht6hpZ6ncTAMJfj6UDrmYL23RyGVtbFNz0ejA'
        file_id = '1ktuawwARugAgie_-suicaGwj0vpo3Vcgf9f_0dpk8ps'
        copy_file(user, 'google-oauth2', settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE, file_id)
        assert True

    def test_get_file(self):
        user = User.objects.get(username='pochikalin')
        file_id = '1T60gPq79wFkBa1Q7iNPtZJk26S71b1ifut57jJH-_Uc'
        file = get_user_file(user, 'google-oauth2', settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE, file_id)
        assert file.id == '1rYpm45wpXQylMTo5dgg7ldYSGXsXudfL1my2YQtTOd0'

    def test_single_file(self):
        user = User.objects.get(username='pochikalin')
        file_id = '12IE4eIVjzUKtVg_XjgymVuzPHsFdTj0q-1XCh9IRZKE'
        file = get_user_file(user, 'google-oauth2', settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE, file_id)
        assert file.id == file_id

    def test_file_changing(self):
        user = User.objects.get(username='pochikalin')
        file_id = '1Y_uBwQaq_lDeqQbd-_9Jdhibxfb69Jqq0Sq61DrAEm8'
        file = get_user_file(user, 'google-oauth2', settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE, file_id)
        assert file.id == file_id
        print(file_id)
        assert file is None
