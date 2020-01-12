from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from blog.models import Post, Comment
from blog.forms import (
    CommentForm,
    PostCreateForm,
    EMPTY_BODY,
    PostUpdateForm,
    EMPTY_USERNAME,
    UserRegistrationForm,
    UserLoginForm
)
from datetime import datetime
class CommentFormTest(TestCase):


    def setUp(self):
        
        self.user1 = User.objects.create_user(username='amit', email='amit@gmail.com', password='12345')
        self.user2 = User.objects.create_user(username='neha', email='neha@gmail.com', password='123456')

        self.post = Post.objects.create(
            title = 'this is post',
            slug = 'this-is-post',

            author = self.user1, 
            body = 'this is my post',
            created = datetime.now(),
                 updated = datetime.now(),
            status = 'published'
        )
        self.comment = Comment.objects.create(
            post = self.post,
            user = self.user2,
            content = "Hi, there.",
            date = datetime.now()

        )


    def comment_form_with_valid_data(self):
        form = CommentForm(data={'content': "Hi, there."})
        self.assertTrue(form.is_valid()) 


    def comment_form_with_invalid_data(self):
        form = CommentForm(data={'content': ""})
        self.assertFalse(form.is_valid())








class PostCreateFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='rex', email='rex@gmail.com', password=123456)
        self.post = Post.objects.create(
            title = 'What is the Python ?',
            slug = 'What-is-the-python-?',
            author =self.user,
            body = "Python is a dynamic programming language.",
            created = datetime.now(),
            updated = datetime.now(),
            status  = "published",
            tags ="python",

            
        )



    def test_post_create_form_with_valid_data(self):
        form = PostCreateForm(data={
            'title':self.post.title,
            'body': self.post.body,
            'tags':self.post.tags,
            'status': self.post.status})   
        self.assertTrue(form.is_valid())



    def test_post_create_form_with_Invalid_data(self):
        form = PostCreateForm(data={
            'title': self.post.title,
            'body': '',
            'tags':'',
            'status': 'draft'})   
        self.assertFalse(form.is_valid())   
     

 


class PostUpdateFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='rex', email='rex@gmail.com', password=123456)
        self.post = Post.objects.create(
            title = 'What is the Python ?',
            slug = 'What-is-the-python-?',
            author =self.user,
            body = "Python is a dynamic programming language.",
            created = datetime.now(),
            updated = datetime.now(),
            status  = "published",
            tags ="python",

            
        )

    def test_postUpdateForm_with_valid_data(self):
        data={
            'title':self.post.title,
            'body': self.post.body,
            'tags':self.post.tags,
            'status': self.post.status
            }
        form = PostUpdateForm(data=data)
        self.assertTrue(form.is_valid())
         



    def test_postUpdateForm_with_invalid_data(self):
        data={
            'title':self.post.title,   
            'body': '', 
            'tags':self.post.tags,
            'status': self.post.status
            }
        form = PostUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['body'], [EMPTY_BODY]
        )


        

        

class TestUserRegistrationForm(TestCase):
    def setUp(self):
        data={
            'username': 'vijay123',
            'first_name': 'vijay',
            'last_name': 'rajput',
            'email':'vijay123@gmail.com',
            'password':'123445',
            'confirm_password':'123445'
            
        }
        
        self.form = UserRegistrationForm(data=data)
    def test_valid_data(self):
        
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data['username'], 'vijay123')
        self.assertEqual(self.form.cleaned_data['first_name'], 'vijay')
        self.assertEqual(self.form.cleaned_data['last_name'], 'rajput')
        self.assertEqual(self.form.cleaned_data['email'], 'vijay123@gmail.com')
        self.assertEqual(self.form.cleaned_data['password'], '123445')
        self.assertEqual(self.form.cleaned_data['confirm_password'], '123445')






    
    def test_invalid_data(self):
        data={
            'username': '',
            'first_name': 'vijay',
            'last_name': 'rajput',
            'email':'vijay123@gmail.com',
            'password':'123445',
            'confirm_password':'123445'
            
        }
        
        form = UserRegistrationForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'],[EMPTY_USERNAME]
        )




class TestUserLoginForm(TestCase):
    def  setUp(self):

        self.user = get_user_model().objects.create_user(username='rex', email='rex@gmail.com', password=123456)
    
    def tearDown(self):
         
        self.user = None 



    def test_form_with_valid_data(self):
        
        data={
            'username': 'rex',
            'password': '12345'
        }
        form = UserLoginForm(data)

        self.assertTrue(form.is_valid())

    def test_form_with_Invalid_data_password(self):
    
        data={
            'username': 'rex',
            'password': ''
        }
        form = UserLoginForm(data)

        self.assertFalse(form.is_valid())

    def test_form_with_valid_data_username(self):
        data={
            'username': '',
            'password': '12345'
        }
        form = UserLoginForm(data)

        self.assertFalse(form.is_valid())

    

    



                         
