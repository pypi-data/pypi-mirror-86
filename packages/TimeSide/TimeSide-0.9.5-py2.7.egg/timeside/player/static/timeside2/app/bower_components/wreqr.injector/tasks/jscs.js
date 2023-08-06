/*global module*/
'use strict';

module.exports = {
  options: {
    config: '.jscs.json'
  },
  lib: ['lib/{,*/}*.js'],
  grunt: ['<%= jshint.grunt.src %>'],
  test: ['test/spec/{,*/}*.js']
};
