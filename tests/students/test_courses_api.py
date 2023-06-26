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
    response = client.get(f'/api/v1/courses/{courses[0].id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1


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
    first_id = courses[0].id
    last_id = courses[-1].id
    course_id = randint(first_id, last_id)
    response = client.get('/api/v1/courses/', {'id': course_id})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == course_id

# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_name_course(client, course_factory):
    courses = course_factory(_quantity=10)
    names = [course.name for course in courses]
    course_name = choice(names)
    response = client.get(f'/api/v1/courses/?name={course_name}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course_name


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'Python'})
    assert response.status_code == 201
    assert count + 1 == Course.objects.count()


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    course = course_factory(_quantity=1)
    student = student_factory(_quantity=1)
    response_1 = client.get(f'/api/v1/courses/{course[0].id}/')
    response_2 = client.patch(f'/api/v1/courses/{course[0].id}/', data={'name': course[0].name, 'students': [student[0].id]})
    assert response_2.status_code == 200
    data_1 = response_1.json()
    data_2 = response_2.json()
    assert data_1 != data_2


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.delete(f'/api/v1/courses/{course[0].id}/')
    assert response.status_code == 204






