/* Read Frames Latex Expressions from Files */

const N_PER_BLOCK = 10;
const fs = require('fs');
const path = require('path');
const {EventEmitter} = require('events');

const IN_PATH = path.resolve('out_latex/video1');
const myEventEmitter = new EventEmitter();

const framesExprs = [];

const readNFiles = (start) => {
  console.log(start);
  for (let i = start; i <= start + N_PER_BLOCK; i++) {
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

// Before starting the server, read the first 100 block of images
module.exports = {readNFiles, N_PER_BLOCK, framesExprs, myEventEmitter};
