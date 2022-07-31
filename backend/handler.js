const {N_FRAMES, framesExprs, myEventEmitter,
  writeImages, FRAME_COUNT, START_FRAMES} = require('./fileHandler');

let CURR_FRAMES_BOTTOM = START_FRAMES;

const frameHandler = (request, h) => {
  let {frame} = request.query;
  frame = Number(frame);

  if (frame < CURR_FRAMES_BOTTOM || frame > CURR_FRAMES_BOTTOM + N_FRAMES - 1) {
    return h.response({
      status: 'fail',
      // eslint-disable-next-line max-len
      message: `Frame request is below ${CURR_FRAMES_BOTTOM} or exceed ${CURR_FRAMES_BOTTOM + N_FRAMES - 1} `,
    })
        .type('application/json')
        .code(500);
  }
  if (frame > FRAME_COUNT) {
    return h.response({
      status: 'fail',
      message: 'Accessing frame that does not exist',
    })
        .type('application/json')
        .code(500);
  }

  const temp = framesExprs.slice();
  framesExprs.splice(0, framesExprs.length);

  // Send response
  const response = h.response({
    status: 'Success',
    data: {
      N_FRAMES,
      framesExprs: temp,
    },
  });
  response.type('application/json');
  response.code(200);

  CURR_FRAMES_BOTTOM = frame + N_FRAMES;
  if (CURR_FRAMES_BOTTOM <= FRAME_COUNT) {
    // if there still data to be read
    setTimeout(() => {
      myEventEmitter.emit('used', CURR_FRAMES_BOTTOM);
    }, 5000);
  }

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
