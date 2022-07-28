const {frameHandler, init, saveImagesHandler} = require('./handler');

const routes = [
  {
    method: 'GET',
    path: '/init',
    handler: init,
  },
  {
    method: 'GET',
    path: '/frames',
    handler: frameHandler,
  },
  {
    method: 'POST',
    path: '/images',
    handler: saveImagesHandler,
  },
];

module.exports = {routes};
