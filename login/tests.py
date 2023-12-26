"""
REFERENCES:

Title: How can I test google.maps.Geocoder?
URL: https://stackoverflow.com/questions/58439971/how-can-i-test-google-maps-geocoder

"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import AdminAccount, Lost_Item
from .forms import UploadItemForm
from django.test import override_settings
import googlemaps

'''from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase'''


# Create your tests here.
class PinTestCase(TestCase):
    def testEmptyLost_Item(self):
        size=Lost_Item.objects.count()
        url = 'welcome/upload_an_item'

        form_data = {
            'name': '',
            'location': '',
            'description': '',
        }

        response = self.client.post(url, form_data)

        newSize=Lost_Item.objects.count()
        self.assertEqual(newSize-size, 0) 
    
    def testEmptyNameLost_Item(self):
        size=Lost_Item.objects.count()
        url = 'welcome/upload_an_item'

        form_data = {
            'name': '',
            'location': '85 Engineer\'s Way, Charlottesville, VA 22903, USAs',
        }

        response = self.client.post(url, form_data)

        newSize=Lost_Item.objects.count()
        self.assertEqual(newSize-size, 0) 
    
    def testGeoLocator(self):
        GOOGLE_API_KEY = 'AIzaSyAVNiQY02xsXtQ4S-IzIcnDiPSEZNzQ8wg'
        gmaps = googlemaps.Client(key= GOOGLE_API_KEY)
        result = gmaps.geocode(str('Rice Hall, Engineer\'s Way, Charlottesville, VA, USA'))
        lat = result[0]["geometry"]["location"]["lat"]
        lon = result[0]["geometry"]["location"]["lng"]
        self.assertAlmostEqual(lat, 38.031979, 3)
        self.assertAlmostEqual(lon, -78.511192, 3)



@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestWebPage(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='email@email.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
    def testWelcome(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome.html')

    def testHomeLogin(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome.html')
    
    def testUserUploads(self):
        response=self.client.get(reverse('my_uploads'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user-my-uploads.html')

    def testUpload(self):
        response = self.client.get(reverse('upload_item'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')

    def testSuccess(self):
        response = self.client.get(reverse('success_upload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')

    def testAdminWelcome(self):
        q=AdminAccount.objects.create(email='email@email.com')
        q.save()
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin.html')
    
    def testAdminUpload(self):
        q=AdminAccount.objects.create(email='email@email.com')
        q.save()
        response = self.client.get(reverse('upload_item_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin-upload.html')
    
    def testAdminWelcome(self):
        q=AdminAccount.objects.create(email='email@email.com')
        q.save()
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin.html')
    
    def testAdminUploads(self):
        q=AdminAccount.objects.create(email='email@email.com')
        q.save()
        response = self.client.get(reverse('my_uploads_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin-my-uploads.html')

    def testAdminUploadSuccess(self):
        q=AdminAccount.objects.create(email='email@email.com')
        q.save()
        response = self.client.get(reverse('admin_success_upload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_success.html')
