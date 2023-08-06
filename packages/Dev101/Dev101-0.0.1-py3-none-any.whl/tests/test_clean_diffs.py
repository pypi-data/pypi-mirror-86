import unittest
from .helpers import read_file
from diffs import clean_diff

class TestTrivialCases(unittest.TestCase):

    def test_add_first_line(self):
        filename = 'add-first-line.txt'
        raw_diff = read_file(filename)
        expected = [['+Do not go gentle into that good night']]
        actual = clean_diff(raw_diff)

        self.assertEqual(actual, expected)

    def test_add_two_lines(self):
        filename = 'add-two-lines.txt'
        raw_diff = read_file(filename)
        expected = [
            [
                '-Do not go gentle into that good night',
                '+Do not go gentle into that good night',
                '+Old age should burn and rave at close of day;',
                '+Rage, rage against the dying of the light.',
            ]
        ]
        actual = clean_diff(raw_diff)

        self.assertEqual(actual, expected)

    def test_remove_one_line(self):
        filename = 'remove-one-line.txt'
        raw_diff = read_file(filename)
        expected = [
            [
                ' Do not go gentle into that good night',
                '-Old age should burn and rave at close of day;',
                ' Rage, rage against the dying of the light.'
            ]
        ]
        actual = clean_diff(raw_diff)
        
        self.assertEqual(actual, expected)


class TestDockerizeFile(unittest.TestCase):

    maxDiff = None

    def test_equal_lengths(self):
        actual = self._get_actual()
        expected = self._get_expected()

        self.assertEqual(len(actual), len(expected))

    def test_diff_1(self):
        actual = self._get_actual()
        expected = self._get_expected()

        self.assertEqual(actual[0], expected[0])

    def test_diff_2(self):
        actual = self._get_actual()
        expected = self._get_expected()

        self.assertEqual(actual[1], expected[1])
        

    def _get_actual(self):
        filename = 'dockerize-project.txt'
        raw_diff = read_file(filename)

        actual = clean_diff(raw_diff)

        return actual

    def _get_expected(self):
        expected = [
            [
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
            [
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
            ]
        ]

        return expected

class TestCreateStartAndStopScripts(unittest.TestCase):

    def test_diffs_match(self):
        filename = 'create-start-and-stop-scripts.txt'
        raw_diff = read_file(filename)
        expected = [
            ['+docker-compose up -d'],
            ['+docker-compose down']
        ]
        actual = clean_diff(raw_diff)

        self.assertEqual(actual, expected)

class TestCreateLayoutComponent(unittest.TestCase):

    maxDiff = None

    def test_app_js_diff(self):
        expected = [
            "-import logo from './logo.svg';",
            "-import './App.css';",
            "+import React, { Component } from 'react';",
            ' ',
            '-function App() {',
            '-  return (',
            '-    <div className="App">',
            '-      <header className="App-header">',
            '-        <img src={logo} className="App-logo" alt="logo" />',
            '-        <p>',
            '-          Edit <code>src/App.js</code> and save to reload.',
            '-        </p>',
            '-        <a',
            '-          className="App-link"',
            '-          href="https://reactjs.org"',
            '-          target="_blank"',
            '-          rel="noopener noreferrer"',
            '-        >',
            '-          Learn React',
            '-        </a>',
            '-      </header>',
            '-    </div>',
            '-  );',
            "+import Layout from './components/Layout/Layout';",
            '+',
            '+class App extends Component {',
            '+  render() {',
            '+    return (',
            '+      <div>',
            '+        <Layout>',
            '+          <p>Test</p>',
            '+        </Layout>',
            '+      </div>',
            '+    );',
            '+  }',
            ' }',
            ' ',
            '+',
            ' export default App;',
        ]
        actual = self.get_actual()[0]

        self.assertEqual(actual, expected)

    def test_layout_js_diff(self):
        expected = [
            "+import React from 'react';",
            "+",
            "+import Helper from '../../hoc/Helper';",
            "+",
            "+const layout = ( props ) => (",
            "+    <Helper>",
            "+        <div>Toolbar, SideDrawer, Backdrop</div>",
            "+        <main>",
            "+            {props.children}",
            "+        </main>",
            "+    </Helper>",
            "+);",
            "+",
            "+export default layout;"
        ]
        actual = self.get_actual()[1]

        self.assertEqual(actual, expected)

    def test_helper_js_diff(self):
        expected = [
            "+const helper = (props) => props.children;",
            "+",
            "+export default helper;"
        ]
        actual = self.get_actual()[2]

        self.assertEqual(actual, expected)

    def get_actual(self):
        filename = 'create-layout-component.txt'
        raw_diff = read_file(filename)
        actual = clean_diff(raw_diff)
        
        return actual

class TestImplementationOfBurgerBuilderContainer(unittest.TestCase):

    def test_app_js_diff(self):
        expected = [
            " import React, { Component } from 'react';",
            " ",
            " import Layout from './components/Layout/Layout';",
            "+import BurgerBuilder from './containers/BurgerBuilder/BurgerBuilder';",
            " ",
            " class App extends Component {",
            "   render() {",
            "     return (",
            "       <div>",
            "         <Layout>",
            "-          <p>Test</p>",
            "+          <BurgerBuilder />",
            "         </Layout>",
            "       </div>",
            "     );",
        ]
        actual = self.get_actual()[0]

        self.assertEqual(actual, expected)

    def get_actual(self):
        filename = 'start-implementation-of-burger-builder-container.txt'
        return get_actual(filename)

class TestAddPropTypeValidation(unittest.TestCase):

    def test_burger_ingredient_js_diff_part_1(self):
        expected = [
            "-import classes from '*.module.css';",
            " import React from 'react';",
            "+import PropTypes from 'prop-types'",
            " ",
            " import './BurgerIngredient.css';",
            " ",
            "-const burgerIngredient = (props) => {",
            "+function BurgerIngredient(props) {",
            "     let ingredient = null;",
            " ",
            "     switch (props.type) {",
            "...",
            "     return ingredient;",
            " };",
            " ",
            "-export default burgerIngredient;",
            "+",
            "+BurgerIngredient.propTypes = {",
            "+    type: PropTypes.string.inRequired",
            "+};",
            "+",
            "+",
            "+export default BurgerIngredient;"
        ]
        actual = self.get_actual()[-1]

        # print(actual)

        self.assertEqual(actual, expected)

    def get_actual(self):
        filename = 'add-prop-type-validation.txt'
        return get_actual(filename)

def get_actual(filename):
    raw_diff = read_file(filename)
    actual = clean_diff(raw_diff)

    return actual

if __name__ == '__main__':
    unittest.main()