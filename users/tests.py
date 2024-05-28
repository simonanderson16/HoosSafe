from django.http import QueryDict
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User, AnonymousUser
from users.models import CustomUser, Report
from users.views import index, report_form, file_uploads


class IndexViewTests(TestCase):
    def test_index_admin_user(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        admin = CustomUser.objects.create(email="abc@gmail.com", is_site_admin=True)
        admin.save()
        admin_user = User(email="abc@gmail.com")
        response.user = admin_user
        self.assertEqual(index(response).url, "/admin_home/")

    def test_index_normal_user(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        normal = CustomUser.objects.create(email="abc@gmail.com", is_site_admin=False)
        normal.save()
        normal_user = User(email="abc@gmail.com")
        response.user = normal_user
        self.assertEqual(index(response).url, "/user_home/")

    def test_index_anon_user(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        response.user = AnonymousUser()
        response.META = {"REMOTE_ADDR": "127.0.0.1"}
        response.session = self.client.session
        response.POST = QueryDict("a=1&a=2&c=3")
        response.GET = QueryDict("a=1&a=2&c=3")
        self.assertEqual(index(response).status_code, 200)


class ReportFormTests(TestCase):
    def test_report_is_admin(self):
        response = self.client.get(reverse("report_form"))
        self.assertEqual(response.status_code, 200)
        admin = CustomUser.objects.create(email="abc@gmail.com", is_site_admin=True)
        admin.save()
        admin_user = User(email="abc@gmail.com")
        response.user = admin_user
        self.assertEqual(report_form(response).url, "/admin_home/")


class FileUploadTests(TestCase):
    def test_report_is_not_admin(self):
        response = self.client.get(reverse("file_uploads"))
        normal = CustomUser.objects.create(email="abc@gmail.com", is_site_admin=False)
        normal.save()
        normal_user = User(email="abc@gmail.com")
        response.user = normal_user
        self.assertEqual(file_uploads(response).url, "/user_home/")

    def test_report_is_admin(self):
        response = self.client.get(reverse("file_uploads"))
        admin = CustomUser.objects.create(email="abc@gmail.com", is_site_admin=True)
        admin.save()
        admin_user = User(email="abc@gmail.com")
        response.user = admin_user
        response.META = {"REMOTE_ADDR": "127.0.0.1"}
        response.session = self.client.session
        report = Report.objects.create(user=admin)
        report.date = "2025-3-15"
        report.time = "9:45"
        report.save()
        f = open("background.png")
        report.file = f
        admin.save()
        self.assertEqual(file_uploads(response).status_code, 200)
        f.close()


class AdminFullReportTests(TestCase):
    def setUp(self):
        self.report = Report.objects.create(status=0, note="")
        self.admin_user = CustomUser.objects.create(email="abc@gmail.com", is_site_admin=True)

    def test_change_report_status_on_view(self):
        response = self.client.get(reverse('admin_full_report', kwargs={'report_id': self.report.id}))
        response.user = self.admin_user
        updated_report = Report.objects.get(pk=self.report.id)
        updated_report.status = 1
        self.assertEqual(updated_report.status, 1)

    def test_change_report_status_to_resolved_with_note(self):
        response = self.client.get(reverse('admin_full_report', kwargs={'report_id': self.report.id}))
        response.user = self.admin_user
        updated_report = Report.objects.get(pk=self.report.id)
        updated_report.status = 1
        updated_report.note = "Admin Note"
        updated_report.status = 2
        self.assertEqual(updated_report.note, "Admin Note")
        self.assertEqual(updated_report.status, 2)
