- `docker run --rm -d -p 9411:9411 --name zipkin openzipkin/zipkin`
- `npm init`
- `npm i @opentelemetry/core @opentelemetry/node @opentelemetry/plugin-http @opentelemetry/plugin-https @opentelemetry/exporter-zipkin @opentelemetry/tracing @opentelemetry/plugin-express express`
- `npm install @opentelemetry/api @opentelemetry/node @opentelemetry/exporter-zipkin @opentelemetry/tracing @opentelemetry/resources @opentelemetry/semantic-conventions @opentelemetry/instrumentation-http express`

- Before running your server, rmb to init the tracing file FIRST!!
    - `node -r ./tracing.js app.js`

------------

- The above covers end to end tracing. Next, we want to aggregate metrics over time with Prometheus
    - Download from the webpage
- `docker run --rm -d -p 9090:9090 --name prometheus prom/prometheus`
- `npm i @opentelemetry/metrics`
- `npm i @opentelemetry/exporter-prometheus`
