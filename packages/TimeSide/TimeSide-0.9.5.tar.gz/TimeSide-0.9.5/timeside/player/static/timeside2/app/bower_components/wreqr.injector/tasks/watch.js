/* global module*/
'use strict';

module.exports = {
  grunt: {
    files: '<%= jshint.grunt.src %>',
    tasks: ['jshint:grunt', 'jscs:grunt']
  },
  lib: {
    files: '<%= jshint.lib.src %>',
    tasks: ['jshint:lib', 'jscs:lib']
  }
};
