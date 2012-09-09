import unittest
import os
from fhp.models.user import User
from fhp.models.photo import Photo
from fhp.helpers.json_finder import _parse_json

class Test_retrieve_user(unittest.TestCase):
    def setUp(self):
        self.zachaysan = User(403022)
        with open(os.path.join('fhp', 'config', 'test_settings.json')) as f:
            self.test_settings = _parse_json(f.read())
        if self.test_settings['oauth']:
            self.auth_zach = User(403022, authorize=True)

    def test_init(self):
        self.assertEqual(self.zachaysan.id, 403022)
        
    def test_username(self):
        self.assertEqual(self.zachaysan.username, 'zachaysan')

    def test_init_with_username(self):
        zachaysan = User(username='zachaysan')
        self.assertEqual(zachaysan.id, self.zachaysan.id)

    def test_init_with_username_ensure_same_object_as_id_lookup(self):
        zachaysan = User(username='zachaysan')
        self.assertEqual(zachaysan.__hash__(),
                         self.zachaysan.__hash__())

    def test_init_with_username_first_then_id(self):
        arragorn = User(username='arragorn')
        arragorn_again = User(1354783)
        self.assertEqual(arragorn.__hash__(),
                         arragorn_again.__hash__())

    def test_auth_without_oauth(self):
        self.assertFalse(hasattr(self.zachaysan, 'auth'))
        
    def test_oauth_with_auth(self):
        if self.test_settings['oauth']:
            api_test_user = self.auth_zach
            self.assertTrue(hasattr(api_test_user, 'auth'))
            
    def test_friends(self):
        evgenys_id = 1
        evgenys_username = 'tchebotarev'
        friend_evgeny = self.zachaysan.find_friend(id=evgenys_id)
        self.assertEqual(evgenys_id, friend_evgeny.id)
        friend_evgeny = self.zachaysan.find_friend(username=evgenys_username)
        self.assertEqual(evgenys_username, friend_evgeny.username)
    
    def test_friends_is_same_object_when_before(self):
        evgenys_id = 1
        friend_evgeny = self.zachaysan.find_friend(id=evgenys_id)
        self.assertEqual(evgenys_id, friend_evgeny.id)
        evgeny = User(evgenys_id)
        self.assertEqual(friend_evgeny.__hash__(),
                         evgeny.__hash__())

    def test_friends_is_same_object_when_after(self):
        evgenys_id = 1
        evgeny = User(evgenys_id)
        zachaysan = User(username='zachaysan')
        friend_evgeny = self.zachaysan.find_friend(id=evgenys_id)
        self.assertEqual(friend_evgeny.__hash__(),
                         evgeny.__hash__())

    def test_stories(self):
        olegs_id = 2
        oleg = User(olegs_id)
        oleg.blog_posts
        self.assertTrue(hasattr(oleg, 'blog_posts'))
        """ Oleg wrote the first blog post :) """
        self.assertIn(1, oleg.blog_posts)

    def test_story_retrival_in_proper_order(self):
        pass

    def test_friends_auto_build_needed_data(self):
        """ Since less data is sent from the api when 
        pulling a list of friends, we need the user
        model to update itself if we request an attribute
        that it should have automatically.
        """
        self.assertTrue(hasattr(self.zachaysan, 'friends'))
        evgenys_id = 1
        self.assertTrue('affection' in dir(self.zachaysan.friends[evgenys_id]))
        self.assertTrue(self.zachaysan.friends[evgenys_id].affection > 5)
        
    def test_followers(self):
        evgenys_id = 1
        evgenys_username = 'tchebotarev'
        self.assertTrue(hasattr(self.zachaysan, 'followers'))
        follower_evgeny = self.zachaysan.find_follower(id=evgenys_id)
        self.assertEqual(evgenys_id, follower_evgeny.id)
        follower_evgeny = self.zachaysan.find_follower(username=evgenys_username)
        self.assertEqual(evgenys_username, follower_evgeny.username)

    def test_friends_auto_build_needed_data(self):
        """ Since less data is sent from the api when 
        pulling a list of friends, we need the user
        model to update itself if we request an attribute
        that it should have automatically.
        """
        evgenys_id = 1
        friend_evgeny = self.zachaysan.find_friend(id=evgenys_id)
        self.assertTrue('affection' in dir(friend_evgeny))
        self.assertTrue(friend_evgeny > 5)
    
    def test_collection_pulling(self):
        if not self.test_settings['ignore_known_failing_tests']:
            evgenys_id = 1
            evgeny = User(evgenys_id)
            self.assertTrue(evgeny.collections)
 
    def test_self_collection_pulling_with_oauth(self):
        if self.test_settings['oauth']:
            zachaysan = self.auth_zach
            zachaysan.collections
            self.assertTrue(hasattr(zachaysan, 'collections'))
            self.assertIn(383355, zachaysan.collections)
            
    def test_user_favorites(self):
        """ Normally I would split these into their own tests, but 
        they need to proceed sequentially or I may get an error due
        to trying to "unfavorite" a photo I've already unfavorited.
        """
        if self.test_settings['oauth']:
            photo_id = 10005987
            self.assertTrue(self.auth_zach.favorite(photo_id))
            self.assertTrue(self.auth_zach.unfavorite(photo_id))
            photo = Photo(photo_id)
            self.assertTrue(self.auth_zach.favorite(photo))
            self.assertTrue(self.auth_zach.unfavorite(photo))

    def test_asking_for_an_oauth_only_resource_from_a_nonowned_user_id(self):
        pass

    def test_auto_photo_creation(self):
        pass

    def test_user_search(self):
        pass
    
    def test_follow_user(self):
        pass

    def test_unfollow_user(self):
        pass

    def test_super_amounts_of_magic_in_user_dont_interfere_with_force_fn_call(self):
        pass
