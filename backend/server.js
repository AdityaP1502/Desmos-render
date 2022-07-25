const Hapi = require('@hapi/hapi');

const init = async () => {
  const server = Hapi.server({
    port: 5000,
    host: 'localhost',
    routes: {
      cors: true,
    },
  });

  await server.start();

  console.log(`Server berjalan pada ${server.info.uri}`);
};

init();
