from typing import TYPE_CHECKING, Dict, Optional, Sequence

from faststream.nats.prometheus.provider import settings_provider_factory
from faststream.prometheus.middleware import BasePrometheusMiddleware
from faststream.types import EMPTY

if TYPE_CHECKING:
    from prometheus_client import CollectorRegistry


class NatsPrometheusMiddleware(BasePrometheusMiddleware):
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
            settings_provider_factory=settings_provider_factory,
            registry=registry,
            app_name=app_name,
            metrics_prefix=metrics_prefix,
            received_messages_size_buckets=received_messages_size_buckets,
            use_faststream_version_label=use_faststream_version_label,
            extra_labels=extra_labels,
        )
