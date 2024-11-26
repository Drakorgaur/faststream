from typing import TYPE_CHECKING, Iterable, Optional, Sequence, Union, cast

from prometheus_client import Counter, Gauge, Histogram

if TYPE_CHECKING:
    from prometheus_client import CollectorRegistry
    from prometheus_client.registry import Collector


class MetricsContainer:
    __slots__ = (
        "_registry",
        "_user_labels",
        "_metrics_prefix",
        "received_messages_total",
        "received_messages_size_bytes",
        "received_processed_messages_duration_seconds",
        "received_messages_in_process",
        "received_processed_messages_total",
        "received_processed_messages_exceptions_total",
        "published_messages_total",
        "published_messages_duration_seconds",
        "published_messages_exceptions_total",
    )

    DEFAULT_SIZE_BUCKETS = (
        2.0**4,
        2.0**6,
        2.0**8,
        2.0**10,
        2.0**12,
        2.0**14,
        2.0**16,
        2.0**18,
        2.0**20,
        2.0**22,
        2.0**24,
        float("inf"),
    )

    def __init__(
        self,
        registry: "CollectorRegistry",
        *,
        metrics_prefix: str = "faststream",
        received_messages_size_buckets: Optional[Sequence[float]] = None,
        extra_labels: Iterable[str] = (),
    ):
        self._registry = registry
        self._metrics_prefix = metrics_prefix
        self._user_labels = extra_labels

        self.received_messages_total = cast(
            Counter,
            self._get_registered_metric(f"{metrics_prefix}_received_messages_total"),
        ) or Counter(
            name=f"{metrics_prefix}_received_messages_total",
            documentation="Count of received messages by broker and handler",
            labelnames=["app_name", "broker", "handler", *self._user_labels],
            registry=registry,
        )

        self.received_messages_size_bytes = cast(
            Histogram,
            self._get_registered_metric(
                f"{metrics_prefix}_received_messages_size_bytes"
            ),
        ) or Histogram(
            name=f"{metrics_prefix}_received_messages_size_bytes",
            documentation="Histogram of received messages size in bytes by broker and handler",
            labelnames=["app_name", "broker", "handler", *self._user_labels],
            registry=registry,
            buckets=received_messages_size_buckets or self.DEFAULT_SIZE_BUCKETS,
        )

        self.received_messages_in_process = cast(
            Gauge,
            self._get_registered_metric(
                f"{metrics_prefix}_received_messages_in_process"
            ),
        ) or Gauge(
            name=f"{metrics_prefix}_received_messages_in_process",
            documentation="Gauge of received messages in process by broker and handler",
            labelnames=["app_name", "broker", "handler", *self._user_labels],
            registry=registry,
        )

        self.received_processed_messages_total = cast(
            Counter,
            self._get_registered_metric(
                f"{metrics_prefix}_received_processed_messages_total"
            ),
        ) or Counter(
            name=f"{metrics_prefix}_received_processed_messages_total",
            documentation="Count of received processed messages by broker, handler and status",
            labelnames=["app_name", "broker", "handler", "status", *self._user_labels],
            registry=registry,
        )

        self.received_processed_messages_duration_seconds = cast(
            Histogram,
            self._get_registered_metric(
                f"{metrics_prefix}_received_processed_messages_duration_seconds"
            ),
        ) or Histogram(
            name=f"{metrics_prefix}_received_processed_messages_duration_seconds",
            documentation="Histogram of received processed messages duration in seconds by broker and handler",
            labelnames=["app_name", "broker", "handler", *self._user_labels],
            registry=registry,
        )

        self.received_processed_messages_exceptions_total = cast(
            Counter,
            self._get_registered_metric(
                f"{metrics_prefix}_received_processed_messages_exceptions_total"
            ),
        ) or Counter(
            name=f"{metrics_prefix}_received_processed_messages_exceptions_total",
            documentation="Count of received processed messages exceptions by broker, handler and exception_type",
            labelnames=[
                "app_name",
                "broker",
                "handler",
                "exception_type",
                *self._user_labels,
            ],
            registry=registry,
        )

        self.published_messages_total = cast(
            Counter,
            self._get_registered_metric(f"{metrics_prefix}_published_messages_total"),
        ) or Counter(
            name=f"{metrics_prefix}_published_messages_total",
            documentation="Count of published messages by destination and status",
            labelnames=[
                "app_name",
                "broker",
                "destination",
                "status",
                *self._user_labels,
            ],
            registry=registry,
        )

        self.published_messages_duration_seconds = cast(
            Histogram,
            self._get_registered_metric(
                f"{metrics_prefix}_published_messages_duration_seconds"
            ),
        ) or Histogram(
            name=f"{metrics_prefix}_published_messages_duration_seconds",
            documentation="Histogram of published messages duration in seconds by broker and destination",
            labelnames=["app_name", "broker", "destination", *self._user_labels],
            registry=registry,
        )

        self.published_messages_exceptions_total = cast(
            Counter,
            self._get_registered_metric(
                f"{metrics_prefix}_published_messages_exceptions_total"
            ),
        ) or Counter(
            name=f"{metrics_prefix}_published_messages_exceptions_total",
            documentation="Count of published messages exceptions by broker, destination and exception_type",
            labelnames=[
                "app_name",
                "broker",
                "destination",
                "exception_type",
                *self._user_labels,
            ],
            registry=registry,
        )

    def _get_registered_metric(self, metric_name: str) -> Union["Collector", None]:
        return self._registry._names_to_collectors.get(metric_name)
