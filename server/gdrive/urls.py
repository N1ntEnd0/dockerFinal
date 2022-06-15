from django.urls import path

from gdrive.views import GDriveViewSet



copy_file = GDriveViewSet.as_view({
    'post': 'download'
})

google_files = GDriveViewSet.as_view({
    'get': 'get_from_google'
})

urlpatterns = [
    path('', google_files, name='google-file'),
    path('<str:id>/download/', copy_file, name='copy-file'),

]