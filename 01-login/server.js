const express = require("express");
const morgan = require("morgan");
const helmet = require("helmet");
const jwt = require("express-jwt");
const jwksRsa = require("jwks-rsa");
const { join } = require("path");
const authConfig = require("./auth_config.json");
const axios = require("axios");

const app = express();

if (!authConfig.domain || !authConfig.audience) {
  throw "Please make sure that auth_config.json is in place and populated";
}

app.use(morgan("dev"));
app.use(helmet());
app.use(express.static(join(__dirname, "public")));

app.use(
  express.urlencoded({
    extended: true
  })
)

app.use(express.json())

const checkJwt = jwt({
  secret: jwksRsa.expressJwtSecret({
    cache: true,
    rateLimit: true,
    jwksRequestsPerMinute: 5,
    jwksUri: `https://${authConfig.domain}/.well-known/jwks.json`
  }),

  audience: authConfig.audience,
  issuer: `https://${authConfig.domain}/`,
  algorithms: ["RS256"]
});

const jwtUser = async (req, res, next) => {
  const response = await axios.get(req.user.aud[1], { headers: { 'Authorization': req.headers.authorization } });
  req.user = response.data.email;
  next()
};

app.post("/api/external", checkJwt, jwtUser, async (req, res) => {

  // find user email
  const resp = await axios.post("http://localhost:5000/test", {
    position: req.body.position,
    email: req.user
  })

  res.send({
    msg: "Your access token was successfully validated!",
    status: resp.data.status,
    email: resp.data.email
  });
});

app.get("/auth_config.json", (req, res) => {
  res.sendFile(join(__dirname, "auth_config.json"));
});

app.get("/*", (req, res) => {
  res.sendFile(join(__dirname, "index.html"));
});

app.use(function (err, req, res, next) {
  if (err.name === "UnauthorizedError") {
    return res.status(401).send({ msg: "Invalid token" });
  }

  next(err, req, res);
});

process.on("SIGINT", function () {
  process.exit();
});

module.exports = app;
