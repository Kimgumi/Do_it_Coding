from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag

# Create your tests here.
class TestView(TestCase):
    def setUp(self):# 기본 설정
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password="minkado813@")
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')

        self.user_obama.is_staff = True
        self.user_obama.save()
        self.tag_python_kr = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/single_page/')

    def test_post_list(self):
        # 테스트할 내용 나열 후 코드 작성
        #1. 목록 페이지 가져오기
        response = self.client.get('/single_page/')
        #2. 페이지 로드
        self.assertEqual(response.status_code, 200)

        #3. 페이지 타이틀: Blog
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        #4. 내비게이션바
        #navbar = soup.nav
        #5. 내비게이션 바에 있는 문구 확인
        #self.assertIn('About Me', navbar.text)
        self.navbar_test(soup)

        # 6. 포스트 게시물이 없다면
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        # 7. 게시물이 1개 존재
        self.post_001 = Post.objects.create(
            title='첫번째',
            content='첫번째 포스트',
            author=self.user_obama,
        )
        self.post_001.tags.add(self.tag_hello)
        self.post_001.tags.add(self.tag_python_kr)
        self.assertEqual(Post.objects.count(), 1)

        # 8. 새로고침
        response = self.client.get('/single_page/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        # 9. 작성자
        self.assertIn(self.user_obama.username.upper(), main_area.text)

    def test_post_detail(self):
        # 1.포스트가 있다
        post_001 = Post.objects.create(
            title = '첫번째',
            content = '첫번째 포스트',
        )
        # 2.그 포스트의 url
        self.assertEqual(post_001.get_absolute_url(), '/single_page/1/')

        # 포스트의 상세 페이지 테스트
        # 1. url로 접근하면 정상 작동
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 포스트의 네비게이션바 테스트
        self.navbar_test(soup)

        # 2. 탭 타이틀
        self.assertIn(post_001.title, soup.title.text)

        # 3. 포스트의 제목
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        # 4. 포스트의 작성자

        # 5. 포스트의 내용
        self.assertIn(post_001.content, post_area.text)

    def test_create_post(self):
        response = self.client.get('/single_page/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='trump', password='minkado813@')

        response = self.client.get('/single_page/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id="main-area")
        self.assertIn('Create New Post', main_area.text)


        self.client.post(
            '/single_page/create_post/',
            {
                'title': 'Post form 만들기',
                'content': 'Post form 페이지를 만듭니다',
            }
        )
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, "Post form 만들기")
        self.assertEqual(last_post.author.username, 'trump')