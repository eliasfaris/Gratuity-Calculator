from django.shortcuts import render, redirect
from .forms import newForm, TipForm
from .models import Employee, Tip, Form
from datetime import datetime
from django.forms import modelformset_factory, formset_factory
import json
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth import logout
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required    
def home_view(request):
    title = 'Employee / New Form'
    page = "New Form"
    js_dict = sendEmployeeDataAsJSON()
    form = formset_factory(TipForm)
    if request.method == 'POST':
        print(request.POST)
        #checks to make sure we are not submitting any form for a existing date and time_frame
        date = request.POST['date']
        time_frame = request.POST['time_frame']
        if Form.objects.filter(date = date).filter(time_frame = time_frame).exists():
            error_message = "There is already a form for the date: " + date + " and timeframe: " + time_frame
            messages.error(request, error_message)
            return redirect("employee_home")

        form1 = form(request.POST)
        new_form= newForm(request.POST)
        if form1.is_valid() and form1.has_changed() and new_form.is_valid():
           
            for f in form1:
               
                new_instance = f.save(commit=False)
                new_instance.date = request.POST.get('date')
                new_instance.time_frame = request.POST.get('time_frame')
                new_instance.save()
                
            new_instance2 = new_form.save(commit = False)
            new_instance2.time = datetime.now().time()
            new_instance2.save()
            messages.success(request, "The Tips have been successfully saved!")
            messages.success(request, "The form has been successfully saved!")

            return redirect('employee_home')
                
        else:
            for error in form1.errors:
                messages.error(request, error)
            for error2 in new_form.errors:
                messages.error(request, error2)
            return render(request, 'employee_home.html', {'form':form1, 'new_form':new_form,
            'js_dict':js_dict, 'page': page })
        
        """if new_form.is_valid():
            new_instance2 = new_form.save(commit = False)
            new_instance2.time = datetime.now().time()
            new_instance2.save()
            messages.success(request, "The form has been successfully saved!")
            return redirect('employee_home')
        else:
            messages.error(request, new_form.errors)
            return render(request, 'employee_home.html',{'form':form1, 'new_form':new_form,
            'js_dict':js_dict, 'page': page})"""
            
            
        
    new_form = newForm()

    #form = tip_form_set(queryset = Tip.objects.none())
    context = {
        'title': title,
        'page': page,
        'new_form':new_form,
        'js_dict':js_dict,
        'form':form
    }
    return render(request, 'employee_home.html', context)

        #tip_form = TipForm(request.POST, prefix="form1")
        #new_form = newForm(request.POST, prefix="form2")
        #if new_form.is_valid():
         
            #new_form.save()
            #tip_form.save()
            

    #tip_form = TipForm(prefix="form1")
    #new_form = newForm(prefix="form2")
    """ date = request.POST.get('date')
        tip_amount = request.POST.get('tip_amount')
        time_frame = request.POST.get('time_frame')
        paid_later = request.POST.get('paid_later')
        point = request.POST.get('point')
        employee = request.POST.get('employee')
        e = Tip(date = date, tim_amount = tip_amount, time_frame = time_frame, paid_later = paid_later
        ,point = point, employee = employee)
        e.save()"""

def sendEmployeeDataAsJSON():
    query = Employee.objects.all()
    dict = {}
    for emp in query:
        dict[emp.id] = emp.point
    js_dict = json.dumps(dict)
    return js_dict

@login_required    
def logout_employee(request):
    if request.method=='POST':
        logout(request)
        return redirect ('login')

@login_required    
def weekly_report_view(request):
    title = "Weekly Reports BY Employee"

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
    #print(total_info)
    #for tip in tips:
     #   print(tip.employee.name , "  ", tip.date , tip.time_frame, tip.paid_later, tip.paid_today)
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
        'tips':tips,
        'employees':employees,
        'days_dates':days_dates,
        'all_info':all_info,
        'total_info': total_info
    }
    
    return render(request, 'weekly_reports_employee.html', context)