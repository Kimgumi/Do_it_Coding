from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase):
    def setUp(self):# 기본 설정
        self.client = Client()

    def test_post_list(self):
        # 테스트할 내용 나열 후 코드 작성
        #1. 목록 페이지 가져오기
        response = self.client.get('/blog/')
        #2. 페이지 로드
        self.assertEqual(response.status_code, 200)

        #3. 페이지 타이틀: Blog
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        #4. 내비게이션바
        navbar = soup.nav
        #5. 내비게이션 바에 있는 문구 확인
        self.assertIn('About Me', navbar.text)

        # 6. 포스트 게시물이 없다면
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        # 7. 게시물이 1개 존재
        post_001 = Post.objects.create(
            title='첫번째',
            content='첫번째 포스트',
        )
        self.assertEqual(Post.objects.count(), 1)

        # 8. 새로고침
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

    def test_post_detail(self):
        # 1.포스트가 있다
        post_001 = Post.objects.create(
            title = '첫번째',
            content = '첫번째 포스트',
        )
        # 2.그 포스트의 url
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 포스트의 상세 페이지 테스트
        # 1. url로 접근하면 정상 작동
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2. 탭 타이틀
        self.assertIn(post_001.title, soup.title.text)
        # 3. 포스트의 제목
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        # 4. 포스트의 작성자

        # 5. 포스트의 내용
        self.assertIn(post_001.content, post_area.text)