var path = require('path');

module.exports = {
  module: {
    rules: [
      {
        test: /\.js$/,
        // exclude: /node_modules/,
        include: [
          path.resolve(__dirname, 'src'),

          /\bxterm\b/,
        ],
        use: {
          loader: "babel-loader"
        }
      }
    ]
  }
};
