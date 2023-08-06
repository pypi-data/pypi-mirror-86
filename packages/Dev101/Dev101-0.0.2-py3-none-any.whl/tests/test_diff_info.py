import unittest

from diffs import get_diff_info, \
    convert_commit_message_to_filename
from .helpers import read_file

class TestConvertCommitMessageToFilename(unittest.TestCase):

    def test_step_0(self):
        commit_message = 'Step 0: Setup for the tutorial'
        expected = 'Step0_Setup-for-the-tutorial.md'

        actual = convert_commit_message_to_filename(commit_message)

        self.assertEqual(actual, expected)

    def test_step_1(self):
        commit_message = 'Step 1: Create layout component'
        expected = 'Step1_Create-layout-component.md'

        actual = convert_commit_message_to_filename(commit_message)

        self.assertEqual(actual, expected)

class TestDockerizeProject(unittest.TestCase):

    def setUp(self):
        self.expected = self._get_expected()
        self.actual = self._get_actual()

    def test_contains_dockerfile_filename(self):
        self.assertTrue('filename' in self.actual[0])
        self.assertEqual(self.actual[0]['filename'], self.expected[0]['filename'])
        
    def test_contains_dockerfile_content(self):
        self.assertTrue('content' in self.actual[0])
        self.assertEqual(self.actual[0]['content'], self.expected[0]['content'])

    def test_contains_dockerfile_action(self):
        self.assertTrue('action' in self.actual[0])
        self.assertEqual(self.actual[0]['action'], self.expected[0]['action'])

    def test_contains_docker_yml_filename(self):
        self.assertTrue('filename' in self.actual[1])
        self.assertEqual(self.actual[1]['filename'], self.expected[1]['filename'])

    def test_contains_docker_yml_content(self):
        self.assertEqual(self.actual[1]['content'], self.expected[1]['content'])

    def _get_expected(self):
        expected = [
            {
                'filename': 'Dockerfile.dev',
                'content': [
                    '+FROM node:alpine',
                    '+',
                    '+WORKDIR /app',
                    '+',
                    '+COPY package.json /app',
                    '+',
                    '+RUN yarn install',
                    '+',
                    '+COPY . /app',
                    '+',
                    '+CMD ["yarn", "run", "start"]'
                ],
                'action': 'CREATE'
            },
            {
                'filename': 'docker-compose.yml',
                'content': [
                    '+version: "3.8"',
                    '+services:',
                    '+  client:',
                    '+    stdin_open: true',
                    '+    build:',
                    '+      context: .',
                    '+      dockerfile: Dockerfile.dev',
                    '+    environment:',
                    '+      CHOKIDAR_USEPOLLING: "true"',
                    '+    ports:',
                    '+      - "3000:3000"',
                    '+    volumes:',
                    '+      - "/app/node_modules"',
                    '+      - "./:/app"'
                ],
                'action': 'CREATE'
            }
        ]
        return expected
        
    def _get_actual(self):
        filename = 'dockerize-project.txt'
        diff_info = read_diff_info(filename)

        return diff_info

def read_diff_info(filename):
    raw_diff = read_file(filename)
    diff_info = get_diff_info(raw_diff)
    
    return diff_info 
