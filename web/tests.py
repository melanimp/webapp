from django.test import TestCase, Client
from django.urls import reverse
from django.test import RequestFactory
from web.models import Usuario, Evidence, Actividad, Type, Rol
from web.apirest import send_sactivities

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class ManageActivitiesJATest(LiveServerTestCase):
    def setUp(self):
        self.jefe_anno = Rol.objects.create(name="Jefe Año", path='/src/principal/principal.html')
        self.tipo_actividad = Type.objects.create(name='Deportivo')
        self.rol_estudiante = Rol.objects.create(name="Estudiante", path='/src/principal/principal.html')
        self.user = Usuario.objects.create(email="admin@test.com", passwd='12345', rol=self.jefe_anno)
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # def test_auth_fail(self):
    #     self.browser.get(self.live_server_url + '/src/login/login.html')
    #     time.sleep(2)
    #     email_input = self.browser.find_element(By.XPATH, '//*[@id="email"]')
    #     email_input.send_keys("userfail@fail.io")
    #     time.sleep(2)

    #     password_input = self.browser.find_element(By.XPATH, '//*[@id="pwd"]')
    #     password_input.send_keys("12345678")
    #     time.sleep(2)

    #     element = self.browser.find_element(By.XPATH, '/html/body/div/form/button')
    #     time.sleep(2)
    #     element.click()
    #     time.sleep(2)
    #     expected_url = self.live_server_url + '/src/login/login.html'
    #     self.assertEquals(self.browser.current_url, expected_url)

    # def test_auth_jefe_anno(self):
    #     self.browser.get(self.live_server_url + '/src/login/login.html')
    #     time.sleep(3)
    #     email_input = self.browser.find_element(By.XPATH, '//*[@id="email"]')
    #     email_input.send_keys(self.user.email)
    #     time.sleep(2)

    #     password_input = self.browser.find_element(By.XPATH, '//*[@id="pwd"]')
    #     password_input.send_keys(self.user.passwd)
    #     time.sleep(2)

    #     element = self.browser.find_element(By.XPATH, '/html/body/div/form/button')
    #     time.sleep(2)
    #     element.click()

    #     expected_url = self.live_server_url + self.jefe_anno.path
    #     self.assertEqual(self.browser.current_url, expected_url)

    def test_manage_activities(self):
        self.browser.get(self.live_server_url + '/src/login/login.html')
        time.sleep(2)
        correo_input = self.browser.find_element(By.XPATH, '//*[@id="email"]')
        correo_input.send_keys(self.user.email)
        password_input = self.browser.find_element(By.XPATH, '//*[@id="pwd"]')
        password_input.send_keys(self.user.passwd)
        entrar = self.browser.find_element(By.XPATH, '/html/body/div/form/button')
        entrar.click()
        expected_url = self.live_server_url + self.jefe_anno.path
        self.assertEqual(self.browser.current_url, expected_url)

        time.sleep(2)
        actividades = self.browser.find_element(By.XPATH, '/html/body/div/div[1]/div/a')
        self.assertTrue(actividades)
        actividades.click()
        expected_url = self.live_server_url + "/src/activities/activities.html"
        self.assertEqual(self.browser.current_url, expected_url)
        
        time.sleep(2)
        add_actividad = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/a')
        add_actividad.click()
        nombre_actividad = self.browser.find_element(By.XPATH, '//*[@id="uname"]')
        nombre_actividad.send_keys("Juegos Mella")
        tipo_actividad = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div/div[2]/select')
        tipo_actividad.click()
        select_tipo = Select(tipo_actividad)
        select_tipo.select_by_visible_text(self.tipo_actividad.name) # select_by_value(self.tipo_actividad.name)
        fecha_actividad = self.browser.find_element(By.XPATH, '//*[@id="fecha"]')
        fecha_actividad.send_keys('2023-04-01')
        save_actividad = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/button')
        save_actividad.click()
        elemento = Actividad.objects.filter(uname="Juegos Mella").first()
        self.assertIsNotNone(elemento)
        time.sleep(2)

        editar_actividad = self.browser.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr[1]/td[4]/a[1]')
        time.sleep(2)
        editar_actividad.click()
        nombre_actividad = self.browser.find_element(By.XPATH, '//*[@id="uname"]')
        nombre_actividad.clear()
        time.sleep(5)
        nombre_nuevo = "Juegos Mellas 2024"
        nombre_actividad.send_keys(nombre_nuevo)
        fecha_actividad = self.browser.find_element(By.XPATH, '//*[@id="fecha"]')
        fecha_actividad.send_keys('2024-09-10')
        time.sleep(2)
        elemento = Actividad.objects.filter(uname=nombre_nuevo).first()
        print(elemento)
        # self.assertIsNotNone(elemento)
        save_actividad = self.browser.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr[1]/td[4]/div[1]/div/div/div[2]/form/button')
        time.sleep(2)
        save_actividad.click()
        time.sleep(2)

        eliminar_actividad = self.browser.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr[1]/td[4]/a[2]')
        time.sleep(2)
        eliminar_actividad.click()
        confirmar_eliminar = self.browser.find_element(By.XPATH, '//*[@id="dmodal-aceptar"]')
        time.sleep(2)
        confirmar_eliminar.click()
        elemento = Actividad.objects.filter(uname="Juegos Mellas 2024").first()
        self.assertIsNone(elemento)
        time.sleep(10)


class CRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Asegúrate de crear instancias de modelos necesarios para las pruebas
        self.rol = Rol.objects.create(name='Ejemplo')
        self.usuario = Usuario.objects.create(email='example@example.com', passwd='example', rol=self.rol)
        self.actividad = Actividad.objects.create(uname='Actividad de prueba', date='2024-03-30')
        self.type = Type.objects.create(name='Tipo de ejemplo')

    def test_login_fail(self):
        # Prueba para la vista de inicio de sesión
        response = self.client.post(reverse('login'), {'email': 'example@example.co', 'pswd': 'example'})
        self.assertEqual(response.status_code, 302)
        
    def test_login_ok(self):
        # Prueba para la vista de inicio de sesión
        response = self.client.post(reverse('login'), {'email': 'example@example.com', 'pswd': 'example'}, follow=True)
        self.assertEqual(response.status_code, 200)   # Verifica redireccionamiento después del inicio de sesión

    def test_logout(self):
        # Prueba para la vista de cierre de sesión
        # self.client.force_login(self.usuario)
        self.client.post(reverse('login'), {'email': 'example@example.com', 'pswd': 'example'}, follow=True)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Verifica redireccionamiento después del cierre de sesión

    def test_send_evidence(self):
        # Prueba para la vista de envío de evidencias
        # self.client.force_login(self.usuario)
        response = self.client.get(reverse('send_evidence'))
        self.assertEqual(response.status_code, 200)  # Verifica si la vista se carga correctamente
