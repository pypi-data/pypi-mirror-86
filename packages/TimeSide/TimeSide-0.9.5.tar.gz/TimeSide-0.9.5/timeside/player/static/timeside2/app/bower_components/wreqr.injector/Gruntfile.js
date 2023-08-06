/*global module:false*/
'use strict';

module.exports = function (grunt) {
  // show elapsed time at the end
  require('time-grunt')(grunt);

  var path = require('path');

  function loadConfig (path) {
    var glob = require('glob');
    var object = {};
    var key;

    glob.sync('*', {cwd: path}).forEach(function (option) {
      key = option.replace(/\.js$/,'');
      var req;
      try {
        req = require(path + option);
        object[key] = typeof req === 'function' ? req(grunt) : req;
      }
      catch (e) {}
    });

    return object;
  }

  // Project configuration.
  var config = {
    // Metadata.
    pkg: grunt.file.readJSON('package.json'),
    banner: '/*! <%= pkg.title || pkg.name %> - v<%= pkg.version %> - ' +
      '<%= grunt.template.today("yyyy-mm-dd") %>\n' +
      ' * \n' +
      ' * Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>\n' +
      ' * Distributed under <%= pkg.license %> LICENSE \n' +
      ' * \n' +
      ' * <%= pkg.homepage %>\n' +
      ' */\n'
  };

  grunt.util._.extend(config, loadConfig('./tasks/'));

  grunt.initConfig(config);

  require('load-grunt-config')(grunt, {
    configPath: path.join(process.cwd(), 'tasks'),
    init: false,
    config: config
  });
};
