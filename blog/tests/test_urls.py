from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import (post_list,
 post_detail,
like_post,
post_create,
post_delete,
post_update,
user_register,
user_login,
user_logout,
display_profile,
edit_profile,
user_post_history,
archive,
about_post_user,
follow,
tagged,
followers_following_list

)
class TestUrls(SimpleTestCase):
    def test_post_list_url_is_resolved(self):
        url = reverse('post_list')
    
        self.assertEqual(resolve(url).func, post_list)


    def test_post_detail_url_is_resolved(self):
        url = reverse('blog:post_detail', args=[2, 'pattern'])   
        self.assertEquals(resolve(url).func, post_detail)
        
    def test_post_like_url_is_resolved(self):
        url = reverse('like_post')
        self.assertEquals(resolve(url).func, like_post)
    

    def test_post_create_url_is_resolved(self):
        url = reverse('blog:post_create')
        self.assertEquals(resolve(url).func, post_create)



    def test_post_delete_url_is_resolved(self):
        url = reverse('blog:delete', args=[1])
        self.assertEquals(resolve(url).func, post_delete)
        
    def test_post_update_url_is_resolved(self):
        url = reverse('blog:post_update', args=[1])
        self.assertEquals(resolve(url).func, post_update)

    def test_register_user_url_is_resolved(self):
        url = reverse("user_register")
        self.assertEquals(resolve(url).func, user_register)

    def test_login_url_is_resolved(self):
        url = reverse("user_login")
        
        self.assertEquals(resolve(url).func, user_login)


    def test_logout_url_is_resolved(self):
        url = reverse("user_logout")
        self.assertEquals(resolve(url).func, user_logout)
    
    


    def test_user_display_profile_url_is_resolved(self):
        url = reverse("blog:display_profile")
        self.assertEquals(resolve(url).func, display_profile)


    def test_edit_user_profile_url_is_resolved(self):
        url = reverse("edit_profile")
        self.assertEquals(resolve(url).func, edit_profile)
    
    def test_user_post_history_url_is_resolved(self):
        url = reverse("blog:user_post_history", args=[1])
        self.assertEquals(resolve(url).func, user_post_history)
    

    def test_post_archive_history_url_is_resolved(self):
        url = reverse("blog:archive", args=[1])
        self.assertEquals(resolve(url).func, archive)
    
    def test_about_post_user_url_is_resolved(self):
        url = reverse("about_post_user", args=[1])
        self.assertEquals(resolve(url).func, about_post_user)



    def test_follow_url_is_resolved(self):
        url = reverse("blog:user_follow")
        print(resolve(url))
        self.assertEquals(resolve(url).func, follow)



    def test_tagged_url_is_resolved(self):
        url = reverse("tagged", args=['this-is-tagged'])
        self.assertEquals(resolve(url).func, tagged)    

         
    def test_followers_following_list_url_is_resolved(self):
        url = reverse("blog:followers_following_list")        
        self.assertEquals(resolve(url).func, followers_following_list)


           




























