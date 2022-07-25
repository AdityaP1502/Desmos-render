const {N_PER_BLOCK, framesExprs, myEventEmitter} = require('./frameRead');

const frameHandler = (request, h) => {
  const {frame} = request.params;

  const temp = framesExprs.slice();
  framesExprs.splice(0, framesExprs.length);

  // Send response
  const response = h.response({
    status: 'Success',
    data: {
      N_FRAMES: N_PER_BLOCK,
      framesExprs: temp,
    },
  });
  response.type('application/json');
  response.code(200);

  setTimeout(() => {
    myEventEmitter.emit('used', Number(frame) + N_PER_BLOCK + 1);
  }, 5000);

  return response;
};

module.exports = {frameHandler};
