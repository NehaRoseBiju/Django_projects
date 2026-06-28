from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Instructor
from .forms import CourseForm, InstructorForm


# -------------------- COURSE CRUD --------------------
def home(request):
    return redirect('course_list')

# Create Course
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(request, 'course_form.html', {'form': form})


# View Courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


# Update Course
def course_update(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'course_form.html', {'form': form})


# Delete Course
def course_delete(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        course.delete()
        return redirect('course_list')

    return render(request, 'course_delete.html', {'course': course})


# -------------------- INSTRUCTOR CRUD --------------------

# Create Instructor
def instructor_create(request):
    if request.method == "POST":
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instructor_list')
    else:
        form = InstructorForm()

    return render(request, 'instructor_form.html', {'form': form})


# View Instructors
def instructor_list(request):
    instructors = Instructor.objects.all()
    return render(request, 'instructor_list.html', {'instructors': instructors})


# Update Instructor
def instructor_update(request, id):
    instructor = get_object_or_404(Instructor, id=id)

    if request.method == "POST":
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            return redirect('instructor_list')
    else:
        form = InstructorForm(instance=instructor)

    return render(request, 'instructor_form.html', {'form': form})


# Delete Instructor
def instructor_delete(request, id):
    instructor = get_object_or_404(Instructor, id=id)

    if request.method == "POST":
        instructor.delete()
        return redirect('instructor_list')

    return render(request, 'instructor_delete.html', {'instructor': instructor})