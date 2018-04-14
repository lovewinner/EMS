const debug = process.env.NODE_ENV !== "production";
const webpack = require('webpack');
const path = require('path');

module.exports = {
  context: path.join(__dirname, "src"),
  devtool: debug ? "inline-sourcemap" : false,
  entry: {
    app: "./js/index.jsx",
    login: "./js/Login.jsx",
  },
  module: {
    loaders: [
      {
        test: /\.(js|jsx)?$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel-loader',
        query: {
          presets: ['react', 'es2015', 'stage-0'],
          plugins: ['react-html-attrs', 'transform-decorators-legacy', 'transform-class-properties'],
        }
      },
      {
        test: /\.(css)(\?.*)?$/,
        loader: 'style-loader!css-loader'
      },
      {
        test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 10000,
              name: '/images/[name].[hash:8].[ext]'
            }
          }
        ]
      },
      {
        test: /\.(ttf|eot|woff|woff2)$/,
        loader: "file-loader",
        options: {
          name: '/fonts/[hash].[ext]',
        }
      }
    ]
  },
  output: {
    path: __dirname + "/static/",
    filename: "[name].min.js",
    chunkFilename: "[name].chunk.js",
    publicPath: '/static'
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css', '.sass']
  },
  plugins: debug ? [ ] : [
    new webpack.optimize.CommonsChunkPlugin({name: 'common', filename: 'common.bundle.js'}),
    new webpack.optimize.OccurrenceOrderPlugin(),
    new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
  ],
};
