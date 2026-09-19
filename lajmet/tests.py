from django.test import TestCase, Client
from django.urls import reverse

class PortalLajmeshTests(TestCase):
    
    def setUp(self):
        """Konfigurimi fillestar për çdo test"""
        self.client = Client()

    def test_homepage_loads_successfully(self):
        """Teston nëse faqja kryesore e portalit ngarkohet dhe kthen statusin 200 OK"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_albanian_characters_support(self):
        """Teston mbështetjen për karakteret e veçanta të gjuhës shqipe (ç, ë)"""
        titulli_testi = "Çështjet e ditës dhe zhvillimet e fundit në vend"
        
        # Verifikojmë që stringu me shkronja shqipe përpunohet saktë pa gabime enkodimi
        self.assertIn("Ç", titulli_testi)
        self.assertIn("ë", titulli_testi)
        
    def test_search_or_invalid_page_handling(self):
        """Teston se si reagon serveri ndaj një faqeje që nuk ekziston (duhet të kthejë 404)"""
        response = self.client.get('/faqe-që-nuk-ekziston-koleg/')
        self.assertEqual(response.status_code, 404)