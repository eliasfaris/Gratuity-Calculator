from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Employee
from Employees.models import Tip, Form
from django.contrib import messages
from .form import EmployeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime, timedelta
from Employees.forms import *
from django.forms import modelformset_factory, formset_factory
from Employees.views import sendEmployeeDataAsJSON

# Create your views here.
@login_required
def home_view(request):
    if request.user.manager == False:
        return redirect('/employee/')
    title = 'Manager / Home'
    page = 'Home'
    if request.method == 'POST':
        start_date = request.POST['start_date_input']
        end_date = request.POST['end_date_input']
        forms = Form.objects.filter(date__gte=start_date).filter(date__lte=end_date).order_by('-date')
        return render(request, 'home.html', {'allForms':forms, 'start_date': start_date, 'end_date':end_date})
    
    today_date = datetime.today().date()
    week_ago = today_date - timedelta(days=7)
    allForms = Form.objects.filter(date__gte = week_ago).order_by('-date')
    #fetch all the forms submitted between week ago and today. 
    context = {
        'title': title,
        "page": page,
        'allForms':allForms
    }
    return render(request, 'home.html', context)

#login_required is functional, just commented out for development process
@login_required
def add_employee_view(request):
    if request.user.manager == False:
        return redirect('/employee/')
    title = 'Manager / Add Employee'
    page = 'Add Employee'
    if request.method == 'POST':
        
        form = EmployeeForm(request.POST)
        if request.POST.get('cancel_button') == '':
            return redirect('home')
        if form.is_valid():
             
            name = request.POST['name']
            if Employee.objects.filter(name=name).exists():
                messages.error(request, 'Employee was already Added')
                return redirect('add_employee')
            else:   
                form.save()
                messages.success(request, 'Employee Successfully Added')
                return redirect('add_employee')
        else:
            messages.error(request, 'The form is invalid.')
            return redirect('add_employee')


        context = {
            'title': title,
            'page': page,
            'form': form
        }
        return render(request, 'employee.html', context)
    
    form = EmployeeForm()
    context = {
        'title': title,
        'page': page,
        'form': form
    }
    return render(request, 'employee.html', context)
    
def list_employee_view(request):
    if request.user.manager == False:
        return redirect('/employee/')
    title = 'Manager / Edit Employee'
    page = "Edit Employee"
    queryset = Employee.objects.all()
    context = {
        "list": queryset,
        "title": title,
        "page": page
    }
    return render (request,'list.html', context)
@login_required
def update_employee_view(request, id=id):
    if request.method == "POST":
        print(request.POST)
    if request.user.manager == False:
        return redirect('/employee/')
    title = 'Update Employee Information'
    employee = get_object_or_404(Employee, id=id)
    form = EmployeeForm(request.POST or None, instance = employee)
    if request.POST.get('cancel_button') == '':
        return redirect('list_employee')
    if form.is_valid():
        if request.POST.get('save_button') == '':
            form.save()
            return redirect('list_employee')
        
        elif request.POST.get('delete_button') == '':
            employee.delete()
            return redirect('list_employee')

    context = {
        'form':form,
        'title':title
    }
    return render(request,'edit_employee.html', context)
@login_required
def update_form_view(request, id = id):
    if request.user.manager == False:
        return redirect('/employee/')
    js_dict = sendEmployeeDataAsJSON()
    title = "Editing Form"
    
            
    form = get_object_or_404(Form, id = id)
    tipFormSet = modelformset_factory(Tip, exclude=(), form = TipForm, extra = 0, can_delete=True)
    editForm = newForm(request.POST or None, instance = form)
    queryset = Tip.objects.filter(date = form.date).filter(time_frame = form.time_frame)
    tips = tipFormSet(queryset = queryset)

    if request.method == 'POST' and editForm.is_valid():
        if request.POST.get('cancel_button') == 'Cancel':
            return redirect ('home')
        if request.POST.get('delete_button') == 'Delete':
            Tip.objects.filter(date = form.date).filter(time_frame = form.time_frame).delete()
            form.delete()
            return redirect('home')
        
        else:
            date = request.POST['date']
            time_frame = request.POST['time_frame']
            if Form.objects.filter(date = date).filter(time_frame = time_frame).exists():
                existing_form_query = Form.objects.filter(date = date).filter(time_frame = time_frame)
                if existing_form_query[0].id != id:
                    error_message = "There is already a form for the date: " + date + " and timeframe: " + time_frame
                    messages.error(request, error_message)
                    return redirect("update_form", id = id)
            
            tipForms = tipFormSet(request.POST)
    
            if tipForms.is_valid() and editForm.is_valid():
                for tip in tipForms:
                    new_tip_instance = tip.save(commit = False)
                    new_tip_instance.date = request.POST['date']
                    new_tip_instance.time_frame = request.POST['time_frame']
                    new_tip_instance.save()
                
                new_form_instance = editForm.save(commit = False)
                new_form_instance.time = datetime.now().time()
                new_form_instance.save()
                
                messages.success(request, "The changes have been successfully submitted!")
                return redirect('home')
            else:
                for error in tipForms.errors:
                    print(error)
            """
           
            for tip in tips:
                tip.save(commit = False)
                tip.date = request.POST.get('date')
                tip.time_frame = request.POST.get('time_frame')
                tip.save()

            """
                
    
    context = {
        'form':tips,
        'new_form': editForm,
        'title': title,
        'js_dict':js_dict
    }

    return render(request, 'edit_form.html', context)

@login_required
def weekly_report_view(request):
    title = "Manager / Weekly Reports"
    page = "Weekly Reports, Manager"
    if request.method == 'POST':
        print(request.POST)
        today_date_str = request.POST['date_input']
        today_date = datetime.strptime(today_date_str, '%Y-%m-%d').date()

        today_day = today_date.weekday()
    else:
        today_day = datetime.today().weekday()
        today_date = datetime.today().date()

    #print(today_date)
    
    first_date_of_week = today_date - timedelta(today_day)
    last_date_of_week = first_date_of_week + timedelta(7)
    days_dates=[]
    for i in range(0,7):
        days_dates.append(first_date_of_week+timedelta(i))

    tips = Tip.objects.filter(date__lte = last_date_of_week).filter(date__gte=first_date_of_week).order_by('date')
    employees = Employee.objects.all().order_by('name')
    
    all_info = {}
    total_info = {}
    for employee in employees:
        all_info[employee.name] = {}
        total_info[employee.name] = 0
        for day in days_dates:
            all_info[employee.name][day]=['','']
    for tip in tips:
        if tip.time_frame == 'AM':
            all_info[tip.employee.name][tip.date][0] = tip.paid_later
            total_info[tip.employee.name] += tip.paid_later
        else:
            all_info[tip.employee.name][tip.date][1] = tip.paid_later
            total_info[tip.employee.name] += tip.paid_later
    print(total_info)
    for tip in tips:
        print(tip.employee.name , "  ", tip.date , tip.time_frame, tip.paid_later, tip.paid_today)
#    print(all_info)


    """all_info = {}
    for employee in employees:
        all_info[employee.name] = []
        for tip in tips:
            if tip.employee == employee:
                all_info[employee.name].append({tip.date:[{tip.time_frame:tip.paid_later}]})
    for key in all_info:
        for i in range(0, 7):"""
            

                
    
    context = {
        'title':title,
        'page': page,
        'tips':tips,
        'employees':employees,
        'days_dates':days_dates,
        'all_info':all_info,
        'total_info': total_info
    }
    
    return render(request, 'weekly_reports.html', context)
@login_required    
def logout_view(request):
    if request.method=='POST':
        logout(request)
        return redirect ('login')
