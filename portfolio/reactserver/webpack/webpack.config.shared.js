const path = require('path');

module.exports = argv => ({
  mode: argv.mode,
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx', '.css', '.scss'],
    alias: {
      styles: path.resolve(__dirname, '../src/styles'),
      components: path.resolve(__dirname, '../src/components'),
      store: path.resolve(__dirname, '../src/store'),
      utils: path.resolve(__dirname, '../src/utils')
    }
  },
  output: {
    path: path.resolve(__dirname, '../dist')
  },
  watch: argv.mode === 'development'
});