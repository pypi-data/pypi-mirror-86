/*global module*/
'use strict';

module.exports = {
  options: {
    pkgFiles: ['package.json', 'bower.json'],
    commitMessage: 'bump version %s',
    tagName: '%s',
    tagAnnotation: 'Release %s',
    publish: false,
    buildCommand: 'grunt distro'
  }
};
