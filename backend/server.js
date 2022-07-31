const Hapi = require('@hapi/hapi');
const {readNFiles, myEventEmitter, START_FRAMES} = require('./fileHandler');
const {routes} = require('./route');

const init = async () => {
  const server = Hapi.server({
    port: 5000,
    host: 'localhost',
    routes: {
      cors: true,
    },
  });
  server.route(routes);

  await server.start();

  console.log(`Server berjalan pada ${server.info.uri}`);
  myEventEmitter.emit('used', START_FRAMES);
};


init();
myEventEmitter.on('used', readNFiles);


