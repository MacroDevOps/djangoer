from django.conf.urls import url

from .views import uploadOSS_simple, uploadOSSConfigZip, uploadOSS_common_file, uploadECPHConfigZip, \
    uploadOSSMiniGamePackage,uploadECPHCommonFile

app_name = 'SIService'

urlpatterns = [
    url(r'^uploadOSSsimple$', uploadOSS_simple),
    url(r'^uploadOSSConfigZip$', uploadOSSConfigZip),
    url(r'^uploadOSSCommonFile', uploadOSS_common_file),
    url(r'^uploadECPHCommonFile', uploadECPHCommonFile),
    url(r'^uploadECPHConfigZip', uploadECPHConfigZip),
    url(r'^uploadOSSMiniGamePackage', uploadOSSMiniGamePackage),
]
