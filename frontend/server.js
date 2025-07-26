const express = require('express');
const path = require('path');

const app = express();

app.use(express.static('./dist/frontend'));

app.get('/*', (req, res) =>
  res.sendFile('index.html', { root: 'dist/frontend/' }),
);

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`Servidor ejecutándose en el puerto ${port}`);
});
