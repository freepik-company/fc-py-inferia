from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider

_exporter = PrometheusMetricReader()
_meter_provider = MeterProvider(metric_readers=[_exporter])
metrics.set_meter_provider(_meter_provider)

_meter = metrics.get_meter("cogito.metrics")

request_histogram = _meter.create_histogram(
    name="request_histogram", description="Number of requests", unit="1"
)
inference_duration_histogram = _meter.create_histogram(
    name="inference_duration_histogram", description="Inference duration", unit="ms"
)
