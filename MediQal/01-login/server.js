const express = require("express");
const morgan = require("morgan");
const helmet = require("helmet");
const jwt = require("express-jwt");
const jwksRsa = require("jwks-rsa");
const { join } = require("path");
const authConfig = require("./auth_config.json");
const axios = require("axios");
const app = express();

const quantumServer = "http://2e5b-3-81-125-211.ngrok.io"

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

app.get("/api/external/:x/:y", checkJwt, jwtUser, async (req, res) => {
  // find user email
  console.log(req.params)
  const resp = await axios.post(quantumServer + "/test", {
    position: req.params,
    email: req.user
  })

  res.send({
    msg: "Your access token was successfully validated!",
    data: resp.data
  });
});


app.get("/api/graph", checkJwt, jwtUser, async (req, res) => {
  const graph = await axios.get(quantumServer + "/api/graph")
  return res.json(graph.data)
})

app.get("/api/markers", checkJwt, jwtUser, async (req, res) => {
  const markers = await axios.get(quantumServer + "/api/markers")
  return res.json(markers.data)
})

app.post("/api/graph", checkJwt, jwtUser, async (req, res) => {
  const newGraph = req.body.graph
  const updating = await axios.post(quantumServer + "/api/graph", {
    graph: newGraph
  })
  return res.json(updating.data)
})

app.post("/api/markers", checkJwt, jwtUser, async (req, res) => {
  const newMarker = req.body.marker
  const updating = await axios.post(quantumServer + "/api/markers", {
    marker: newMarker
  })
  return res.json(updating.data)
})

app.get("/api/vehicles", async (req, res) => {
  return res.json({
    "vehicles": [[24.474, 54.368], [23.474, 55.368], [24.2, 54.01]]
  })
})

app.get("/auth_config.json", (req, res) => {
  res.sendFile(join(__dirname, "auth_config.json"));
});

app.get("/", (req, res) => {
  res.sendFile(join(__dirname, "index.html"));
});

app.get("/map", (req, res) => {
  res.sendFile(join(__dirname, "index.html"));
});

app.get("/request", (req, res) => {
  res.sendFile(join(__dirname, "index.html"));
});

app.get("/api/path", async (req, res) => {
  // console.log(req.body)
  const response = await axios.get(quantumServer + "/test")
  console.log(response.data)
  res.json(response.data)
})


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
