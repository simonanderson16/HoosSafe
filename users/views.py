from datetime import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Report, ReportFile
from .forms import ReportForm,AdminForm
from django.db import transaction


def is_site_admin(email):
    return CustomUser.objects.get(email=email).is_site_admin


def index(request):
    if request.user.is_authenticated:
        if is_site_admin(request.user.email):
            return redirect("admin_home")
        else:
            return redirect("user_home")
    return render(request, "index.html")


def user_home(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if is_site_admin(request.user.email):
        return redirect("admin_home")
    return render(request, 'user_home.html')


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not is_site_admin(request.user.email):
        return redirect("user_home")
    return render(request, 'admin_home.html')


def logout_view(request):
    logout(request)
    return redirect("index")


def report_form(request):
    if request.user.is_authenticated:
        if is_site_admin(request.user.email):
            return redirect("admin_home")
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            if request.user.is_authenticated:
                user = CustomUser.objects.get(email=request.user.email)
                if not user:
                    user = CustomUser.objects.create(email=request.user.email)
                report.user = user
            report.save()
            files = request.FILES.getlist('files')  # Get list of uploaded files
            for file in files:
                ReportFile.objects.create(report=report, file=file)  # Create ReportFile objects
            return redirect("report_confirmation")
    else:
        form = ReportForm()
    return render(request, 'report_form.html', {'form': form})


def report_confirmation(request):
    return render(request, 'report_confirmation.html')


def file_uploads(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not is_site_admin(request.user.email):
        return redirect("user_home")
    else:
        reports = Report.objects.all().order_by('-pub_date_report')
        for report in reports:
            report.date = convert_date(report.date)
            report.time = convert_time(report.time)
        # files_info = [(report, report.file.url) for report in reports if report.file]
        file_context = {'files_info': reports}
        return render(request, 'file_uploads.html', file_context)
    
def file_uploads_new(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not is_site_admin(request.user.email):
        return redirect("user_home")
    else:
        reports = Report.objects.filter(status = 0)
        reports = reports.order_by('-pub_date_report')
        for report in reports:
            report.date = convert_date(report.date)
            report.time = convert_time(report.time)
        # files_info = [(report, report.file.url) for report in reports if report.file]
        file_context = {'files_info': reports}
        return render(request, 'file_uploads.html', file_context)
    
def file_uploads_in_progress(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not is_site_admin(request.user.email):
        return redirect("user_home")
    else:
        reports = Report.objects.filter(status = 1)
        reports = reports.order_by('-pub_date_report')
        for report in reports:
            report.date = convert_date(report.date)
            report.time = convert_time(report.time)
        # files_info = [(report, report.file.url) for report in reports if report.file]
        file_context = {'files_info': reports}
        return render(request, 'file_uploads.html', file_context)
    
def file_uploads_resolved(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not is_site_admin(request.user.email):
        return redirect("user_home")
    else:
        reports = Report.objects.filter(status = 2)
        reports = reports.order_by('-pub_date_report')
        for report in reports:
            report.date = convert_date(report.date)
            report.time = convert_time(report.time)
        # files_info = [(report, report.file.url) for report in reports if report.file]
        file_context = {'files_info': reports}
        return render(request, 'file_uploads.html', file_context)


def convert_time(time):
    time = time.split(':')
    hour = int(time[0])
    minute = time[1]
    if hour < 12:
        return str(hour) + ':' + minute + ' a.m.'
    elif hour == 12:
        return str(hour) + ':' + minute + ' p.m.'
    else:
        return str(hour - 12) + ':' + minute + ' p.m.'


def convert_date(date):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    date = date.split('-')
    year = date[0]
    month = int(date[1])
    day = date[2]
    return months[month - 1] + ' ' + day + ', ' + year


def my_reports(request):
    if not request.user.is_authenticated:
        return redirect("index")
    reports = Report.objects.filter(user=CustomUser.objects.get(email=request.user.email))
    reports = reports.order_by('-pub_date_report')
    return render(request, 'my_reports.html', {'reports': reports})

def my_reports_new(request):
    if not request.user.is_authenticated:
        return redirect("index")
    reports = Report.objects.filter(user=CustomUser.objects.get(email=request.user.email))
    reports = reports.order_by('-pub_date_report')
    new_report = reports.filter(status = 0)
    return render(request, 'my_reports.html', {'reports': new_report})

def my_reports_in_progress(request):
    if not request.user.is_authenticated:
        return redirect("index")
    reports = Report.objects.filter(user=CustomUser.objects.get(email=request.user.email))
    reports = reports.order_by('-pub_date_report')
    in_progress_report = reports.filter(status = 1)
    return render(request, 'my_reports.html', {'reports': in_progress_report})

def my_reports_resolved(request):
    if not request.user.is_authenticated:
        return redirect("index")
    reports = Report.objects.filter(user=CustomUser.objects.get(email=request.user.email))
    reports = reports.order_by('-pub_date_report')
    resolved_report = reports.filter(status = 2)
    return render(request, 'my_reports.html', {'reports': resolved_report})
    
    
    # if not request.user.is_authenticated:
    #     return redirect("index")
    
    
    # user = CustomUser.objects.get(email=request.user.email)
    # new_reports = Report.objects.filter(user=user, status=0)
    # print(new_reports)
    # in_progress_reports = Report.objects.filter(user=user, status = 1)
    # print(in_progress_reports)
    # resolved_reports = Report.objects.filter(user=user, status = 2)
    # print(resolved_reports)
    # status = request.GET.get('status', 'new')

    # if status == 'new':
    #     filtered_objects = Report.objects.filter(status = 0)
    # elif status == "in_progress":
    #     filtered_objects = Report.objects.filter(status = 1)
    # else:
    #     filtered_objects = Report.objects.filter(status = 2)

    # context = {
    #     'new_reports' : new_reports, 
    #     'in_progresss_reports' : in_progress_reports, 
    #     'resolved_reports' : resolved_reports
    # }

    # return render(request, 'my_reports.html', context)


def user_full_report(request, report_id):
    if not request.user.is_authenticated:
        return redirect("index")
    report = get_object_or_404(Report, pk=report_id)
    report.date = convert_date(report.date)
    report.time = convert_time(report.time)
    return render(request, 'user_full_report.html', {'report': report})

def delete_report(request, report_id):
    if not request.user.is_authenticated:
        return redirect("index")
    report = get_object_or_404(Report, pk=report_id)
    if request.method == 'POST':
        with transaction.atomic():
            report_files = report.files.all()
            for report_file in report_files:
                report_file.delete()
            report.delete()
        return redirect("my_reports")
    report.date = convert_date(report.date)
    report.time = convert_time(report.time)
    return render(request, 'delete_report.html', {'report': report})


def admin_full_report(request, report_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not is_site_admin(request.user.email):
        return redirect("user_home")
    report = get_object_or_404(Report, pk=report_id)
    
    if report.status == 0:
        report.status = 1
        report.save()

    if request.method == 'POST':
        # updating function based on POST action (i.e., pressing resolved/in progress button)
        action = request.POST.get('action')
        if action == 'resolved':
            report.status = 2
            report.save()
            return redirect("admin_full_report", report_id=report.id)
        elif action == 'in_progress':
            report.status = 1
            report.save()
            return redirect("admin_full_report", report_id=report.id)

        # if button not pressed, process AdminForm
        form = AdminForm(request.POST)
        if form.is_valid():
            admin_note = form.cleaned_data["note"]
            report.note = admin_note
            # commenting out this line so that saving a note doesn't automatically change the status of the report
            # report.status = 2
            report.save()
            return redirect("admin_full_report", report_id=report.id)
        

    report.date = convert_date(report.date)
    report.time = convert_time(report.time)
    return render(request, 'admin_full_report.html', {'report': report})