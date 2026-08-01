from django.shortcuts import render

def login_view(request):
    return render(request, 'accounts/login.html')

def register_selection_view(request):
    return render(request, 'accounts/register_selection.html')

def register_student_view(request):
    return render(request, 'accounts/register_student.html')

def register_company_view(request):
    return render(request, 'accounts/register_company.html')
