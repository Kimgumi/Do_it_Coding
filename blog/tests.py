from django.test import TestCase

# Create your tests here.
class TestView(TestCase):
    def test_post_list(self):
        self.assertEqual(2,2)
        # self.assertEqual(2,3) => 둘은 같지 않으니 TEST를 하면 Failed와 함께 실패라고 뜬다
        