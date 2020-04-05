const merge = require('webpack-merge');
const sharedConfig = require('./webpack.config.shared.js');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = (env, argv) => merge(sharedConfig(argv), {
  entry: './src/App.js',
  devtool: argv.mode === 'development' ? 'inline-source-map' : 'none',
  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader:'css-loader',
            options: {
              url: false,
              sourceMap: true,
              importLoaders: 2,
              modules: {
                localIdentName: '[path][name]__[local]--[hash:base64:5]'
              },
            }
          },
          {loader:'sass-loader', options: { sourceMap: true }},
        ],
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "bundle.css",
      chunkFilename: "bundle.css"
    })
  ],
  output: {
    filename: 'client.bundle.js',
  },
});