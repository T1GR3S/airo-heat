var config = {};

config.web = {};

config.web.port = process.env.WEB_PORT || 3000;
config.web.db = process.env.WEB_DATABASE || "database2.db";

module.exports = config;
