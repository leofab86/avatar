const merge = require('webpack-merge');
const sharedConfig = require('./webpack.config.shared.js');

module.exports = (env, argv) => merge(sharedConfig(argv), {
  entry: './src/server.js',
  target: 'node',
  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          'isomorphic-style-loader',
          {
            loader:'css-loader',
            options: {
              url: false,
              sourceMap: false,
              importLoaders: 2,
              modules: {
                localIdentName: '[path][name]__[local]--[hash:base64:5]'
              },
            }
          },
          {loader:'sass-loader', options: { sourceMap: false }},
        ],
      }
    ]
  },
  plugins: [],
  output: {
    filename: 'server.bundle.js',
  },
});