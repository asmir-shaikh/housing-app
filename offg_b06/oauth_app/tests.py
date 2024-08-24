
from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .models import Housing
from .views import home
from django.urls import reverse
from .views import favorites, fav_add
# Create your tests here.


class OauthLoginTests(TestCase):
    def setUpUser(self):
        User = get_user_model()
        user = User.objects.create(username='testuser')
        user.set_password('!Password!@')
        user.save()

    def test_landing_page_for_logged_out_user(self):
        c = Client()
        response = c.get('')
        content = response.content.decode('utf-8')

        self.assertTrue("Login With Google" in content)

    def testLoggedInUser(self):
        c = Client()
        c.login(username='testuser', password='!Password!@')
        User = get_user_model()
        user = User.objects.create(username='testuser')
        self.assertTrue(user.is_authenticated)


class HousingModelTests(TestCase):
    def testHousingCreation(self):
        Housing.objects.create(title = 'Wertland', rent = 2000, location = '216 14th St NW', bed = 4, bath = 2)
        self.assertTrue(Housing.objects.exists())

    def test2HousesCreation(self):
        Housing.objects.create(title = 'Wertland', rent = 2000, location = '216 14th St NW', bed = 4, bath = 2)
        Housing.objects.create(title = 'Test', rent = 3000, location = '100 14th St NW', bed = 2, bath = 1)
      
        self.assertTrue(Housing.objects.all().count() > 1)

    def testHouseDeletion(self):
        Housing.objects.create(title = 'Wertland', rent = 2000, location = '216 14th St NW', bed = 4, bath = 2)
        h = Housing.objects.get(title = 'Wertland')
        h.delete()
        self.assertFalse(Housing.objects.exists())


class FavoriteTests(TestCase):     

    def testAddFavorites(self):
        User = get_user_model()
        user = User.objects.create(username='testuser')
        user.set_password('!Password!@')
        user.save()  
        Housing.objects.create(title = 'Wertland', rent = 2000, location = '216 14th St NW', bed = 4, bath = 2)
        h = Housing.objects.get(title = 'Wertland')
        h.favorites.add(user)
        self.assertTrue(h in Housing.objects.filter(favorites = user))

    def testAdd2Favorites(self):
        User = get_user_model()
        user = User.objects.create(username='testuser')
        user.set_password('!Password!@')
        user.save()  
        Housing.objects.create(title = 'Wertland', rent = 2000, location = '216 14th St NW', bed = 4, bath = 2)
        Housing.objects.create(title = 'Test', rent = 3000, location = '100 14th St NW', bed = 2, bath = 1)
        h = Housing.objects.get(title = 'Wertland')
        h.favorites.add(user)
        h2 = Housing.objects.get(title = 'Test')
        h2.favorites.add(user)
        self.assertTrue(h, h2 in Housing.objects.filter(favorites = user))

    def test2UsersButOnly1Fav(self):
        User = get_user_model()
        user = User.objects.create(username='testuser')
        user.set_password('!Password!@')
        user.save() 

        user2 = User.objects.create(username='testuser2')
        user2.set_password('!Password!@2')
        user2.save() 

        Housing.objects.create(title = 'Wertland', rent = 2000, location = '216 14th St NW', bed = 4, bath = 2)
        h = Housing.objects.get(title = 'Wertland')
        h.favorites.add(user2)

        self.assertTrue(h in Housing.objects.filter(favorites = user2) and 
            h not in Housing.objects.filter(favorites = user))

    def testRemoveFave(self):
        User = get_user_model()
        user = User.objects.create(username='testuser')
        user.set_password('!Password!@')
        user.save()  
        Housing.objects.create(title = 'Wertland', rent = 2000, location = '216 14th St NW', bed = 4, bath = 2)
        h = Housing.objects.get(title = 'Wertland')
        h.favorites.add(user)
        h.favorites.remove(user)
        self.assertFalse(h in Housing.objects.filter(favorites = user))

    def testRemoveOneButNotTheOther(self):
        User = get_user_model()
        user = User.objects.create(username='testuser')
        user.set_password('!Password!@')
        user.save()  
        Housing.objects.create(title = 'Wertland', rent = 2000, location = '216 14th St NW', bed = 4, bath = 2)
        Housing.objects.create(title = 'Test', rent = 3000, location = '100 14th St NW', bed = 2, bath = 1)
        h = Housing.objects.get(title = 'Wertland')
        h.favorites.add(user)
        h2 = Housing.objects.get(title = 'Test')
        h2.favorites.add(user)

        h.favorites.remove(user)
        self.assertTrue(h not in Housing.objects.filter(favorites = user) and 
            h2 in Housing.objects.filter(favorites = user))
        

class HousingSearchTests(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='!Password!@')
        user.save()

        Housing.objects.create(title='Wertland', rent=2000, location='216 14th St NW', bed=4, bath=2, official=True)
        Housing.objects.create(title='Venable', rent=3000, location='100 14th St NW', bed=2, bath=2, official=True)

        self.client.login(username='testuser', password='!Password!@')

    def testTitleSearch(self):
        response = self.client.get(reverse("oauth_app:home"), {"title": "Wertland"})

        self.assertEqual(response.context['housing'].count(), 1)
        self.assertQuerysetEqual(response.context['housing'], Housing.objects.filter(title="Wertland"))

    def testBedSearch(self):
        response = self.client.get(reverse("oauth_app:home"), {"beds": 4})

        self.assertEqual(response.context['housing'].count(), 1)
        self.assertQuerysetEqual(response.context['housing'], Housing.objects.filter(bed=4))

    def testBathSearch(self):
        response = self.client.get(reverse("oauth_app:home"), {"baths": 2})

        self.assertEqual(response.context['housing'].count(), 2)
        self.assertQuerysetEqual(response.context['housing'], Housing.objects.filter(bath=2), ordered=False)

    def testPriceMinSearch(self):
        response = self.client.get(reverse("oauth_app:home"), {"price_min": 3000})

        self.assertEqual(response.context['housing'].count(), 1)
        self.assertQuerysetEqual(response.context['housing'], Housing.objects.filter(rent__gte=3000))

    def testPriceMaxSearch(self):
        response = self.client.get(reverse("oauth_app:home"), {"price_max": 2000})

        self.assertEqual(response.context['housing'].count(), 1)
        self.assertQuerysetEqual(response.context['housing'], Housing.objects.filter(rent__lte=2000))

    def testEmptySearch(self):
        response = self.client.get(reverse("oauth_app:home"), {"title": "Incorrect Title"})

        self.assertEqual(response.context['housing'].count(), 0)
        self.assertQuerysetEqual(response.context['housing'], Housing.objects.none())
        self.assertContains(response, "No housing options matched your search criteria :(")

    def testSearch(self):
        response = self.client.get(reverse("oauth_app:home"),
                                   {"title": "Venable", "beds": 2, "baths": 2, "price_min": 1000, "price_max": 5000}
                                   )

        self.assertEqual(response.context['housing'].count(), 1)
        self.assertQuerysetEqual(response.context['housing'], Housing.objects.filter(title="Venable"))
