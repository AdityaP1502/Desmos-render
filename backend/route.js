const {frameHandler, init} = require('./handler');

const routes = [
  {
    method: 'GET',
    path: '/init',
    handler: init,
  },
  {
    method: 'GET',
    path: '/frames/{frame}',
    handler: frameHandler,
  },
];

module.exports = {routes};
