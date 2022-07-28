const Hapi = require('@hapi/hapi');
const {readNFiles, myEventEmitter} = require('./fileHandler');
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
  myEventEmitter.emit('used', 1);
};


init();
myEventEmitter.on('used', readNFiles);


