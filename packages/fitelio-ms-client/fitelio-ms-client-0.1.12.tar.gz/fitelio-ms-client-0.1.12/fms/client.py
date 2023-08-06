import grpc
import structlog
from fms import settings
from fms.pb import fms_pb2 as pb, fms_pb2_grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc

logger = structlog.getLogger(__name__)


def health_check():
    channel = grpc.insecure_channel(settings.MS_SERVER_URL)
    stub = health_pb2_grpc.HealthStub(channel)
    response = stub.Check(health_pb2.HealthCheckRequest(service="fms-server"), timeout=10)
    logger.info(f"response: {response}")


class FMSError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class FMSClient:
    def __init__(self, raise_exception=False, timeout=10):
        self.client = fms_pb2_grpc.MessagingServiceAPIStub(grpc.insecure_channel(settings.MS_SERVER_URL))
        self.raise_exception = raise_exception
        self.timeout = timeout
        self.log = logger

    @classmethod
    def _build_message(
        cls,
        recipients,
        text,
        uid="",
        tag="",
        method=None,
        provider=None,
        alpha_name="",
        topic=None,
        title="",
        action=None,
        data=None,
        image=None,
        start_time=None,
        ttl=30,
    ):

        if method:
            method = pb.SendMethod.Value(method)
        if provider:
            provider = pb.Provider.Value(provider)

        return pb.Message(
            recipients=recipients,
            text=text,
            uid=uid,
            tag=tag,
            method=method,
            provider=provider,
            alpha_name=alpha_name,
            topic=topic,
            title=title,
            action=action,
            data=data,
            image=image,
            start_time=start_time,
            ttl=ttl,
        )

    def _handle_error(self, message, code=""):
        self.log.error(code=code, status=message)
        if self.raise_exception:
            raise FMSError(code, message)
        return None

    def send_message(
        self,
        recipients,
        text,
        uid="",
        tag="",
        method=None,
        provider=None,
        alpha_name="",
        topic="",
        title="",
        action="",
        data=None,
        image=None,
        start_time=None,
        ttl=30,
    ):
        self.log = self.log.bind(
            message={
                str(recipients),
                text,
                uid,
                tag,
                method,
                provider,
                alpha_name,
                topic,
                title,
                action,
                data,
                image,
                start_time,
                ttl,
            }
        )

        message = self._build_message(
            recipients,
            text,
            uid=uid,
            tag=tag,
            method=method,
            provider=provider,
            alpha_name=alpha_name,
            topic=topic,
            title=title,
            action=action,
            data=data,
            image=image,
            start_time=start_time,
            ttl=ttl,
        )
        try:
            response = self.client.Send(pb.MessageRequest(message=message), timeout=self.timeout)
        except grpc.RpcError as e:
            return self._handle_error(f"RPC call failed: {e}")
        except Exception as e:
            return self._handle_error(f"RPC call failed: {e}")
        if response.error.code:
            return self._handle_error(message=response.error.message, code=response.error.code)

        result = [
            {"code": res.code, "status": res.status, "recipient": res.recipient, "message_id": res.message_id}
            for res in response.results
        ]
        self.log.info(result=result)
        return result


__all__ = ["FMSError", "FMSClient", "health_check"]
