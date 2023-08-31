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
