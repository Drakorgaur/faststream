from types import MappingProxyType
from typing import Dict, Final

from faststream.prometheus.container import MetricsContainer
from faststream.prometheus.types import ProcessingStatus, PublishingStatus
from faststream.types import EMPTY


class MetricsManager:
    """Metrics Manager for Prometheus metrics.

    Updates Prometheus metrics using the provided container.

    Attributes:
        _container (MetricsContainer): The container to update.
        _app_name (str): The application name to use in the labels.
        _extra_labels (MappingProxyType[str, str]): Extra labels to add to the metrics.
            (MappingProxyType[str, str]: A read-only mapping of str keys to str values.)
    """

    __slots__ = ("_container", "_app_name", "_extra_labels")

    def __init__(
        self,
        container: MetricsContainer,
        *,
        app_name: str = "faststream",
        extra_labels: Dict[str, str] = EMPTY,
    ):
        """Initializes the MetricsManager.

        Args:
            container (MetricsContainer): The container to update.
            app_name (str): The application name to use in the labels.
            extra_labels (dict[str, str]): Extra labels to add to the metrics.
                if not provided but `use_faststream_version_label` is set to true,
                `extra_labels` will contain only the faststream version.
        """
        self._container = container
        self._app_name = app_name

        self._extra_labels: Final[MappingProxyType[str, str]] = MappingProxyType(
            extra_labels if isinstance(extra_labels, dict) else {}
        )

    def add_received_message(self, broker: str, handler: str, amount: int = 1) -> None:
        self._container.received_messages_total.labels(
            app_name=self._app_name,
            broker=broker,
            handler=handler,
            **self._extra_labels,
        ).inc(amount)

    def observe_received_messages_size(
        self,
        broker: str,
        handler: str,
        size: int,
    ) -> None:
        self._container.received_messages_size_bytes.labels(
            app_name=self._app_name,
            broker=broker,
            handler=handler,
            **self._extra_labels,
        ).observe(size)

    def add_received_message_in_process(
        self,
        broker: str,
        handler: str,
        amount: int = 1,
    ) -> None:
        self._container.received_messages_in_process.labels(
            app_name=self._app_name,
            broker=broker,
            handler=handler,
            **self._extra_labels,
        ).inc(amount)

    def remove_received_message_in_process(
        self,
        broker: str,
        handler: str,
        amount: int = 1,
    ) -> None:
        self._container.received_messages_in_process.labels(
            app_name=self._app_name,
            broker=broker,
            handler=handler,
            **self._extra_labels,
        ).dec(amount)

    def add_received_processed_message(
        self,
        broker: str,
        handler: str,
        status: ProcessingStatus,
        amount: int = 1,
    ) -> None:
        self._container.received_processed_messages_total.labels(
            app_name=self._app_name,
            broker=broker,
            handler=handler,
            status=status.value,
            **self._extra_labels,
        ).inc(amount)

    def observe_received_processed_message_duration(
        self,
        duration: float,
        broker: str,
        handler: str,
    ) -> None:
        self._container.received_processed_messages_duration_seconds.labels(
            app_name=self._app_name,
            broker=broker,
            handler=handler,
            **self._extra_labels,
        ).observe(duration)

    def add_received_processed_message_exception(
        self,
        broker: str,
        handler: str,
        exception_type: str,
    ) -> None:
        self._container.received_processed_messages_exceptions_total.labels(
            app_name=self._app_name,
            broker=broker,
            handler=handler,
            exception_type=exception_type,
            **self._extra_labels,
        ).inc()

    def add_published_message(
        self,
        broker: str,
        destination: str,
        status: PublishingStatus,
        amount: int = 1,
    ) -> None:
        self._container.published_messages_total.labels(
            app_name=self._app_name,
            broker=broker,
            destination=destination,
            status=status.value,
            **self._extra_labels,
        ).inc(amount)

    def observe_published_message_duration(
        self,
        duration: float,
        broker: str,
        destination: str,
    ) -> None:
        self._container.published_messages_duration_seconds.labels(
            app_name=self._app_name,
            broker=broker,
            destination=destination,
            **self._extra_labels,
        ).observe(duration)

    def add_published_message_exception(
        self,
        broker: str,
        destination: str,
        exception_type: str,
    ) -> None:
        self._container.published_messages_exceptions_total.labels(
            app_name=self._app_name,
            broker=broker,
            destination=destination,
            exception_type=exception_type,
            **self._extra_labels,
        ).inc()
