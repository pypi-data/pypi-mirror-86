/*global module*/
'use strict';

module.exports = {
  options: {
    banner: '<%= banner %>',
    stripBanners: true
  },
  dist: {
    src: ['dist/<%= pkg.name %>.js'],
    dest: 'dist/<%= pkg.name %>.js'
  }
};
