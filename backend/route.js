const {frameHandler} = require('./handler');

const routes = [
  {
    method: 'GET',
    path: '/frames/{frame}',
    handler: frameHandler,
  },
];

module.exports = {routes};
