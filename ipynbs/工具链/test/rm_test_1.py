from rm import rm
from unittest import mock
from unittest import TestCase

class RmTestCase(TestCase):

    @mock.patch('rm.os.path')
    @mock.patch('rm.os')
    def test_rm(self, mock_os, mock_path):
        # mock_path就是patch过后的`os.path`,mock_os就是patch过后的`os`
        #需要注意顺序
        #指定`mock_path.isfile`的返回值False
        mock_path.isfile.return_value = False

        rm("any path")        
        #测试mock_os.remove有没有被调用
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present.")        
        # 指定`mock_path.isfile`的返回值为True
        mock_path.isfile.return_value = True

        rm("any path")

        mock_os.remove.assert_called_with("any path")