'use strict';

const { diag, DiagConsoleLogger, DiagLogLevel } = require('@opentelemetry/api');
const { NodeTracerProvider } = require('@opentelemetry/node');
const { ZipkinExporter } = require('@opentelemetry/exporter-zipkin');
const { SimpleSpanProcessor } = require('@opentelemetry/tracing');
const { Resource } = require('@opentelemetry/resources');
const { SEMRESATTRS_SERVICE_VERSION, SEMRESATTRS_SERVICE_NAME} = require('@opentelemetry/semantic-conventions');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');

// Set the global log level to DEBUG
diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.DEBUG);

const provider = new NodeTracerProvider({
  resource: new Resource({
    [SEMRESATTRS_SERVICE_NAME]: 'getting-started',
    [SEMRESATTRS_SERVICE_VERSION]: '1.0.0'
  }),
});

provider.addSpanProcessor(
  new SimpleSpanProcessor(
    new ZipkinExporter({
      serviceName: 'getting-started'
    })
  )
);

provider.register();

const httpInstrumentation = new HttpInstrumentation();
httpInstrumentation.setTracerProvider(provider);
