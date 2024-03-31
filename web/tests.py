from django.test import TestCase, Client
from django.urls import reverse
from web.models import Usuario, Evidence, Actividad, Type, Rol

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

   # def test_edit_evidence(self):
        # Agrega más pruebas según sea necesario para otras vistas CRUD
    #     # Prueba para la vista de edición de evidencias
    #     pass

    # def test_revidence(self):
    #     # Prueba para la vista de eliminación de evidencias
    #     pass

    # def test_send_csv(self):
    #     # Prueba para la vista de envío de CSV
    #     pass

    # def test_subir_evidence(self):
    #     # Prueba para la vista de subida de evidencias
    #     pass

    # def test_send_sactivities(self):
    #     # Prueba para la vista de envío de actividades
    #     pass

    # def test_send_type(self):
    #     # Prueba para la vista de envío de tipos
    #     pass

    # def test_send_rol(self):
    #     # Prueba para la vista de envío de roles
    #     pass

    # def test_send_activities(self):
    #     # Prueba para la vista de envío de actividades
    #     pass

    # def test_send_users(self):
    #     # Prueba para la vista de envío de usuarios
    #     pass

    # def test_rusers(self):
    #     # Prueba para la vista de eliminación de usuarios
    #     pass

    # def test_add_users(self):
    #     # Prueba para la vista de agregar usuarios
    #     pass

    # def test_edit_users(self):
    #     # Prueba para la vista de edición de usuarios
    #     pass

    # def test_send_asistencia(self):
    #     # Prueba para la vista de envío de asistencia
    #     pass

    # def test_subir_sactivities(self):
    #     # Prueba para la vista de subida de actividades por parte de estudiantes
    #     pass

    # def test_edit_sactivities(self):
    #     # Prueba para la vista de edición de actividades
    #     pass

    # def test_add_sactivities(self):
    #     # Prueba para la vista de agregar actividades
    #     pass

    # def test_ractivities(self):
    #     # Prueba para la vista de eliminación de actividades
    #     pass

    # def test_upload_evidence(self):
    #     # Prueba para la vista de subida de evidencias por parte de estudiantes
    #     pass


# Create your tests here.

# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time

# class FunctionalTests(StaticLiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = webdriver.Chrome(executable_path='/ruta/a/tu/webdriver/chromedriver')  # Reemplaza con la ubicación de tu webdriver
#         cls.selenium.implicitly_wait(10)

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     def test_inicio_sesion(self):
#         self.selenium.get('%s%s' % (self.live_server_url, 'webapp/static/src/login/login.html'))
#         # Ingresa las credenciales y presiona enter
#         username_input = self.selenium.find_element_by_name("email")
#         username_input.send_keys("tu_email@example.com")
#         password_input = self.selenium.find_element_by_name("pswd")
#         password_input.send_keys("tu_contraseña" + Keys.RETURN)

#         # Verifica que la página de inicio de sesión sea exitosa redireccionando a alguna otra página
#         self.assertIn('/src/otra/pagina', self.selenium.current_url)

#     def test_logout(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/src/logout'))
#         # Verifica que el usuario sea redirigido a la página de inicio de sesión después del cierre de sesión
#         self.assertIn('webapp/static/src/login/login.html', self.selenium.current_url)

#     def test_envio_evidencia(self):
#         # Suponiendo que tienes un usuario autenticado
#         self.selenium.get('%s%s' % (self.live_server_url, '/src/envio/evidencia'))
#         # Simula el envío de una evidencia
#         file_input = self.selenium.find_element_by_name("file")
#         file_input.send_keys("/ruta/a/tu/evidencia.png")  # Reemplaza con la ubicación de tu archivo de evidencia
#         # Completa otros campos si es necesario y envía el formulario
#         submit_button = self.selenium.find_element_by_id("submit_button")
#         submit_button.click()

#         # Verifica si la evidencia se ha enviado correctamente redireccionando a alguna otra página
#         self.assertIn('/src/otra/pagina', self.selenium.current_url)

#     # Agrega más pruebas según sea necesario para otras funcionalidades de tu aplicación
