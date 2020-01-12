from django.test import TestCase
from blog.models import Post, Profile,Comment, TotalViews, Images, TotalViews
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
from django.core.files import File





     
class TestPostModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='rex', email='vij@gmail', password='123456')
    
        self.post = Post.objects.create(
            title = 'this is post',
            slug = 'this-is-post',

            author = self.user,
            body = 'this is my post',
            created = datetime.now(),
            updated = datetime.now(),
            status = 'published'
        )
    def test_created_user_is_author_of_post(self):
        
        self.assertEquals(self.post.author.username, 'rex')
                       
    def test_str_method_is_working_properly(self):
        self.assertEquals(str(self.post.title), self.post.title)
    


    def test_get_absolute_url(self):

        self.assertIsNotNone(self.post.get_absolute_url())

class TestProfileModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='rex', email='vij@gmail', password='123456')
        self.profile = Profile.objects.create(
            user = self.user,
            description = "this is my profile",
            dob = '2000-08-20',
            country = 'India',     
            city = 'new delhi',
            website = 'http://www.ignou.in.ac',
            mobile = 1234567890



        )
    def  test__str__(self):
        
        self.assertEqual(str(self.profile.user), self.user.username)    

            
        
class TestCommentModel(TestCase):
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
            content= 'This is cool post.',
            date = datetime.now()
            

        )
     def test__str__(self):
        print(self.comment)
        self.assertEqual(str(self.comment), '{}-{}'.format(self.post.title, str(self.comment.user.username)))
    



class TestTotalViewsModel(TestCase):
    def setUp(self ):

        self.user = get_user_model().objects.create(username='rex', email='vij@gmail', password='123456')
    
        self.post = Post.objects.create(
            title = 'this is post',
            slug = 'this-is-post',

            author = self.user,
            body = 'this is my post',
            created = datetime.now(),
            updated = datetime.now(),
            status = 'published'
        )
        self.view = TotalViews.objects.create(
            post = self.post,
            
            session =self.client.session.session_key
    
            

        )

    def test__str__(self):
        self.assertEqual(str(self.view.post.title), "this is post")
        self.assertTrue(self.view.session)
        
                   





class TestImageModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='rex', email='vij@gmail', password='123456')

        self.post = Post.objects.create(
            title = 'this is post',
            slug = 'this-is-post',

            author = self.user,
            body = 'this is my post',
            created = datetime.now(),
            updated = datetime.now(),
            status = 'published'
        )
        m1 = Images()
        m1.post=self.post
        m1.image=File(open(r"blog/media/images/avtor.png", 'rb'))
        m1.save()
         
    def test(self):
        p = Images.objects.get(id=1).image.path
        self.failUnless(open(p), "file not found")
        
    


        



























 








        
         


