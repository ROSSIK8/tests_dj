from random import randint, choice

import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


# проверка получения первого курса
@pytest.mark.django_db
def test_retrieve_course(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    first_course = Course.objects.first()
    assert first_course.id == 1


# проверка получения списка курсов
@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    assert type(courses) == list


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_id_course(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    first_id = courses[0].id
    last_id = courses[-1].id
    # first_id = Course.objects.first().id
    # last_id = Course.objects.last().id
    course_id = randint(first_id, last_id)
    filter_id_course = Course.objects.get(id=course_id)
    assert course_id == filter_id_course.id


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_name_course(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    names = [course.name for course in courses]
    course_name = choice(names)
    filter_id_name = Course.objects.get(name=course_name)
    assert course_name == filter_id_name.name


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    response = client.post('/api/v1/courses/', data={'name': 'Python'})
    assert response.status_code == 201


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    course = course_factory(_quantity=1)
    student = student_factory(_quantity=1)
    response = client.patch(f'/api/v1/courses/{course[0].id}/', data={'name': course[0].name, 'students': [student[0].id]})
    assert response.status_code == 200


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.delete(f'/api/v1/courses/{course[0].id}/')
    assert response.status_code == 204






