import http from 'http'
import express from 'express'
import bodyParser from'body-parser'
import ReactDOMServer from 'react-dom/server'
import React from 'react'
import App from './App'

const ENV = process.env.NODE_ENV;
const ADDRESS = process.env.NODE_HOST || '127.0.0.1'
const PORT = process.env.NODE_PORT || '8001'
const developmentMode = ENV === 'development'

const app = express()
const server = http.Server(app)

// I've increased the limit of the max payload size in case a huge page
// needs to be rendered
app.use(bodyParser.json({ limit: '100mb' }))

developmentMode && (
  app.use(function logger (req, res, next) {
    console.log(`REACTSERVER request: ${req.method} ${req.originalUrl}`)
    // console.log(req.body)
    next()
  })
)

app.post('/render-react', function renderHome (req, res) {
  const body = req.body;
  const data = {};
  for(const key in body) {
      try {
          data[key] = JSON.parse(body[key])
      } catch (e) {
          data[key] = body[key]
      }
  }

  const staticRouterProps = {
    location: data.path,
    context: {}
  };

  res.json({
    html: ReactDOMServer.renderToString(<App store={data} staticRouterProps={staticRouterProps}/>),
    data: JSON.stringify(data),
    title: body.title,
  })
})

server.listen(PORT, ADDRESS, function () {
  console.log('Render server listening at http://' + ADDRESS + ':' + PORT)
})