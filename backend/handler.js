const {N_PER_BLOCK, framesExprs, myEventEmitter,
  writeImages,
  FRAME_COUNT} = require('./fileHandler');

const frameHandler = (request, h) => {
  const {frame} = request.query;
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

const init = (request, h) => {
  return h.response({
    status: 'success',
    message: 'Berhasil membuat koneksi dengan server',
    data: {
      frame_count: FRAME_COUNT,
    },
  })
      .type('application/json')
      .code(200);
};

const saveImagesHandler = (request, h) => {
  // Front end will send a data URI in base64
  console.log('Data received');
  console.log(request.payload);
  const {data: {uri}} = request.payload;
  const {frame} = request.query;

  try {
    const data = uri.split(',')[1];
    const buf = Buffer.from(data, 'base64');
    writeImages(buf, frame);
  } catch (e) {
    console.log(e);
    return h.response({
      status: 'fail',
      message: 'Error',
    })
        .type('application/json')
        .code(500);
  }

  return h.response({
    status: 'success',
    message: `Berhasil menyimpan frame ${frame}`,
  })
      .type('application/json')
      .code(201);
};

module.exports = {frameHandler, init, saveImagesHandler};
