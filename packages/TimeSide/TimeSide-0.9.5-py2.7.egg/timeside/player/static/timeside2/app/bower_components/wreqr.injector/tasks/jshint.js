/*global module*/
'use strict';

module.exports = {
  options: {
    jshintrc: '.jshintrc',
    reporter: require('jshint-stylish')
  },
  grunt: {
    src: ['Gruntfile.js', 'tasks/{,*/}*.js']
  },
  lib: {
    src: ['lib/{,*/}*.js']
  },
  test: {
    src: ['test/spec/{,*/}*.js']
  }
};
