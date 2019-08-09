const webpack = require('webpack');
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');


const config = {
    entry: './src/theme.js',
    output: {
        path: path.resolve(__dirname, 'sphinx_dg_theme/static'),
        filename: 'js/theme.js'
    },
    module: {
        rules: [
            {
                test: /\.svg$/,
                use: 'file-loader'
            },
            {
                test: /\.js$/,
                use: 'babel-loader',
                exclude: /node_modules/
            },
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader
                    },
                    'css-loader',
                    'sass-loader'
                ]
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // all options are optional
            filename: 'css/theme.css'
        }),
    ]
};

module.exports = config;
