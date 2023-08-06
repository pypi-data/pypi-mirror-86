module.exports = {
  release: [
    'clean',
    'build',
    'release-it'
  ],
  build: [
    'jshint',
    'jscs',
    'umd',
    'concat',
    'uglify'
  ],
  distro: [
    'build',
    'changelog'
  ],
  default: ['build']
};
