import unittest

from app import create_app, db
from config import TestingConfig
from app.models import User, Article
from flask_login import current_user
from flask_testing import TestCase
from werkzeug.security import generate_password_hash


class TestCase(TestCase):

    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        db.create_all()
        db.session.add(User(username='Admin', email='Admin@mail.ru',
                            password=generate_password_hash('Admin')))
        db.session.add(Article(title="title", intro="intro", text="text", user_id=1))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_db_user(self):
        user = User(username='test', email='test@mail.ru',
                    password='test')
        db.session.add(user)
        db.session.commit()
        result_user = User.query.get(user.id)
        self.assertIsInstance(result_user, User)
        self.assertEqual(result_user.username, 'test')
        self.assertEqual(result_user.email, 'test@mail.ru')
        self.assertEqual(result_user.password, 'test')
        article = Article(title='title', intro='intro', text='text', user_id=user.id)
        db.session.add(article)
        db.session.commit()
        result_article = Article.query.get(article.id)
        self.assertIsInstance(result_article, Article)
        self.assertEqual(result_article.title, 'title')
        self.assertEqual(result_article.intro, 'intro')
        self.assertEqual(result_article.text, 'text')
        self.assertEqual(result_article.user_id, user.id)

    def test_user_registeration(self):
        with self.client:
            response = self.client.post('/reg', data=dict(
                username='Michael', email='michael@realpython.com',
                password='python', confirm='python'
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(User.query.filter_by(
                username='Michael',
                email='michael@realpython.com', ).first())

    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/aut',
                data=dict(username='Admin', password='Admin'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.username == "Admin")
            self.assertTrue(current_user.is_active)
            response = self.client.post(
                '/post_create',
                data=dict(title="Test post", intro="This is a test. Only a test.", text="Test text", user_id=1),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(Article.query.filter_by(
                title="Test post",
                intro="This is a test. Only a test.", text="Test text", user_id=1).first())

    def test_logout(self):
        with self.client:
            self.client.post(
                '/aut',
                data=dict(username="Admin", password="Admin"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertFalse(current_user.is_active)
            self.assertEqual(response.status_code, 200)

    def test_main(self):
        with self.client:
            self.client.post(
                '/',
                data=dict(title="title", intro="intro", text="text", user_id=1),
                follow_redirects=True
            )
            response = self.client.get('/')
            self.assertIn(b'title', response.data)
            self.assertIn(b'intro', response.data)


if __name__ == '__main__':
    unittest.main()
