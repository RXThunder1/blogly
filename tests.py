import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test_db'
    db.create_all()
    yield app.test_client()
    db.drop_all()

def test_list_users(client):
    response = client.get('/users')
    assert b'User List' in response.data

def test_new_user(client):
    response = client.post('/users/new', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'image_url': 'http://example.com/image.jpg'
    })
    assert User.query.count() == 1
    assert User.query.first().first_name == 'John'

def test_user_detail(client):
    user = User(first_name='Jane', last_name='Doe', image_url='http://example.com/image.jpg')
    db.session.add(user)
    db.session.commit()
    response = client.get(f'/users/{user.id}')
    assert b'Jane Doe' in response.data

def test_edit_user(client):
    user = User(first_name='Jack', last_name='Smith', image_url='http://example.com/image.jpg')
    db.session.add(user)
    db.session.commit()
    response = client.post(f'/users/{user.id}/edit', data={
        'first_name': 'Jackie',
        'last_name': 'Smith',
        'image_url': 'http://example.com/new_image.jpg'
    })
    db.session.refresh(user)
    assert user.first_name == 'Jackie'
    assert user.image_url == 'http://example.com/new_image.jpg'