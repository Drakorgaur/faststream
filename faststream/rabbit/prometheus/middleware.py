from typing import TYPE_CHECKING, Dict, Optional, Sequence

from faststream.prometheus.middleware import BasePrometheusMiddleware
from faststream.rabbit.prometheus.provider import RabbitMetricsSettingsProvider
from faststream.types import EMPTY

if TYPE_CHECKING:
    from prometheus_client import CollectorRegistry


class RabbitPrometheusMiddleware(BasePrometheusMiddleware):
    def __init__(
        self,
        *,
        registry: "CollectorRegistry",
        app_name: str = EMPTY,
        metrics_prefix: str = "faststream",
        received_messages_size_buckets: Optional[Sequence[float]] = None,
        use_faststream_version_label: bool = False,
        extra_labels: Dict[str, str] = EMPTY,
    ) -> None:
        super().__init__(
            settings_provider_factory=lambda _: RabbitMetricsSettingsProvider(),
            registry=registry,
            app_name=app_name,
            metrics_prefix=metrics_prefix,
            received_messages_size_buckets=received_messages_size_buckets,
            use_faststream_version_label=use_faststream_version_label,
            extra_labels=extra_labels,
        )
