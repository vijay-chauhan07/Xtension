from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from blog.models import Post, Profile, Comment, TotalViews, Images
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files import File
from django.http import HttpRequest
class HomePageTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='vijay')
    def test_post_entry(self):
        Post.objects.create(
            title = 'this is post',
            slug = 'this-is-post',

            author = self.user,
            body = 'this is my post',
            created = datetime.now(),
            updated = datetime.now(),
            status = 'published'
        )
        response = self.client.get('/')
        self.assertContains(response, 'this-is-post')
        self.assertContains(response, 'this is my post')
    def test_view_is_rendering_on_correct_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200 )
        self.assertTemplateUsed(response, 'blog/post_list.html')

class PostViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='vijay')
        self.post=Post.objects.create(

            title = 'this is my',
            slug = 'this-is-my',
            author = self.user,
            body = 'this is my post',
            created = datetime.now(),
            updated = datetime.now(),
            status = 'published'

            )
        
    def test_basic_view(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
    
    def test_post_title(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, self.post.title)
    def test_post_body(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, self.post.body)
         
        
        
class TestGetProfileView(TestCase):
    def setUp(self):
    
        self.user = get_user_model().objects.create_user(username='rex', email='vij@gmail', password='123456')
        self.profile = Profile.objects.create(
            user = self.user,
            description = "this is my profile",
            dob = '2000-08-20',
            country = 'India',     
            city = 'new delhi',
            website = 'http://www.ignou.in.ac',
            mobile = 1234567890
            



        )
        self.login = self.client.login(username='rex', password='123456')

        



    def test_status_code(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertTrue(self.login)
        self.assertEqual(response.status_code, 200)

    def test_get_user_profile(self):
        #login = self.client.login(username='rex', password='123456')
        response = self.client.get(reverse('blog:display_profile'))
        
        self.assertContains(response, self.profile.user.username)
        self.assertContains(response, self.profile.website)

        
class TestCommentView(TestCase):
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
    def  test_status_code(self):
        #Only logged in user can comment
        login=self.client.login(username='neha', password='123456')
        self.assertTrue(login)
        response = self.client.get((self.comment.post.get_absolute_url()))
        self.assertEqual(response.status_code, 200)
        
        
        

class TestViewCount(TestCase):
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
        

    def test(self):
        response = self.client.get(self.view.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
          
    

class TestImageView(TestCase):
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
        self.view = TotalViews.objects.create(
            post = self.post,
            
            session =self.client.session.session_key
    
            

        )
        
        self.m1 = Images()
        self.m1.post=self.post
        self.m1.image=File(open(r"blog/media/images/avtor.png", 'rb'))
        self.m1.save()
    

    def test_whether_view_is_returning_image_or_not(self):
        image = self.m1
        response = self.client.get(image.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, image.image)
    
    def tearDown(self):
        del self.post
        del self.m1
        del self.view
        
      
    






    
    
        

        
            


                
            