/* eslint-disable require-jsdoc */
/* Read Frames Latex Expressions from Files */

const fs = require('fs');
const {EventEmitter} = require('events');
const {exit} = require('process');


let IN_PATH = '';
let IMAGES_OUT_PATH = '';

let N_PER_BLOCK = 0;
let FRAME_COUNT = 0;

const myEventEmitter = new EventEmitter();
const framesExprs = [];

class ArgumentError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ArgumentError';
  }
};

const readArgument = () => {
  try {
    process.argv.splice(0, 2);
    if (process.argv.length === 4) {
      [IN_PATH, IMAGES_OUT_PATH, frameMax, N_PER_BLOCK] = process.argv;
      FRAME_COUNT += parseInt(frameMax);
      N_PER_BLOCK = parseInt(N_PER_BLOCK);
      console.log(`Input path: ${IN_PATH}; Output path: ${IMAGES_OUT_PATH}`);
      console.log(`Total frames: ${FRAME_COUNT}`);
      return;
    }
    // eslint-disable-next-line max-len
    throw new ArgumentError('You need to give the necessary arguments when running the server. node ./backend/server.js <in_path> <out_path> <total_frames> <batch_size>');
  } catch (err) {
    console.log(err.name);
    console.log(err.message);
    exit(1);
  };
};

const readNFiles = (start) => {
  console.log(start);
  // eslint-disable-next-line max-len
  for (let i = start; i <= start + Math.min(N_PER_BLOCK, (FRAME_COUNT - start)); i++) {
    const exprs = [];
    readFrameExpression(i, exprs);
    // eslint-disable-next-line max-len
    framesExprs.push(exprs);
  }
};

const readFrameExpression = (frame, exprs) => {
  const content = fs.readFileSync(IN_PATH + `/out${frame}.txt`).toString();
  exprs.push(...content.split('\n'));
};

const writeImages = (buffer, frame) => {
  console.log(frame);
  fs.writeFileSync(IMAGES_OUT_PATH + `Render${frame}.png`, buffer);
};

// Read Argument
readArgument();
// Before starting the server, read the first 100 block of images
module.exports = {readNFiles, N_PER_BLOCK, framesExprs, myEventEmitter,
  writeImages, FRAME_COUNT};
