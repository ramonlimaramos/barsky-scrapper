import os
from os.path import exists, abspath, dirname, join


__all__ = ['BucketMixin']


here = abspath(dirname(__file__))


class BucketMixin:
    bucket = 'bucket'

    def bucket_set_up(self):
        if not exists(self.bucket):
            os.makedirs(self.bucket)

    def given_file_on_bucket(self, filename, content='somecontent'):
        with open(join(here, '..', '..', '..', self.bucket, filename), 'w') as f:
            f.write(content)

    def given_file_not_on_bucket(self, filename):
        path = join(here, '..', '..', '..', self.bucket, filename)
        if exists(path):
            os.remove(path)

    def given_bucket_empty(self):
        for path in os.listdir(join(here, '..', '..', '..', self.bucket)):
            filepath = join(here, '..', '..', '..', self.bucket, path)
            os.unlink(filepath)

    def assert_file_not_in_bucket(self, filename):
        filepath = self.get_bucket_path(filename)
        self.assertFalse(exists(filepath))

    def assert_file_in_bucket(self, filename):
        filepath = self.get_bucket_path(filename)
        self.assertTrue(exists(filepath))

    def assert_bucket_file_count(self, count):
        self.assertEqual(len(os.listdir(self.bucket)), 1)

    def assert_file_content(self, file, content):
        filepath = self.get_bucket_path(file)
        with open(filepath, 'r') as f:
            actual = f.read()

        self.assertEqual(content, actual)

    def get_bucket_path(self, filename):
        return abspath(join(here, '..', '..', '..', self.bucket, filename))
