from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.duration_pb2 import Duration
from enum import Enum
import trace_pb2 as tracepb
import uuid
import os
import sys
from provider.AWSFact import AWSFact


class Provider(Enum):
    AWS = 0  # AWS Lambda
    ICF = 1  # IBM Cloud Functions
    GCF = 2  # Google Cloud Functions
    ACF = 3  # Azure Cloud Functions
    OWk = 4  # OpenWhisk
    Dok = 5  # Docker
    UND = 6  # UNDEFINED


class Fact:
    _ContainerID = uuid.uuid4()
    _RuntimeString = "{} {} Python {}".format(os.uname()[0], os.uname()[2], sys.version.split(' ')[0])
    config = {}
    _trace = tracepb.Trace()
    _provider = None
    start_time = 0
    base = None

    PHASE = ["provisioned", "start", "update", "done"]

    @staticmethod
    def readFile(path):
        return

    @staticmethod
    def fingerprint(trace, context):
        aws_key = os.getenv("AWS_LAMBDA_LOG_STREAM_NAME")
        gcf_key = os.getenv("X_GOOGLE_FUNCTION_NAME")
        ow_key = os.getenv("__OW_ACTION_NAME")
        acf_key = os.getenv("WEBSITE_HOSTNAME")

        if aws_key:
            AWSFact.get_instances().init(trace, context)
            Fact._provider = Provider.AWS
        elif gcf_key:
            Fact._provider = Provider.GCF
        elif acf_key:
            Fact._provider = Provider.ACF
        elif ow_key:
            if os.path.isfile("/sys/hypervisor/uuid"):
                Fact._provider = Provider.ICF
            else:
                Fact._provider = Provider.OWk

        else:
            Fact._provider = Provider.UND

        return

    @staticmethod
    def boot(configuration):
        Fact.config = configuration
        trace = tracepb.Trace()
        Fact._trace = trace
        now = datetime.now()
        print()
        timestamp = Timestamp()
        timestamp.FromDatetime(now)
        if "inlcudeEnvironment" in configuration and configuration["inlcudeEnvironment"]:
            trace.Env.update(os.environ)
        trace.BootTime.CopyFrom(timestamp)
        trace.ContainerID = str(Fact._ContainerID)
        trace.Runtime = Fact._RuntimeString
        trace.Timestamp.CopyFrom(Fact._trace.BootTime)
        if "lazy_loading" not in configuration or not configuration["lazy_loading"]:
            Fact.load(None)
            if "send_on_update" in configuration and configuration["send_on_update"]:
                Fact.send("provisioned")
        Fact.base = trace

    @staticmethod
    def send(phase):
        if phase not in Fact.PHASE:
            raise ValueError("{} is not a defined phase".format(phase))
        try:
            Fact.config["io"].send(phase, Fact._trace)
        except IOError as e:
            print("failed to send {}:{} - {}\n".format(phase, Fact._trace, e))

    @staticmethod
    def now():
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.now())
        return timestamp

    @staticmethod
    def load(context):
        Fact.fingerprint(Fact._trace, context)
        Fact.config["io"].connect(os.environ)

    @staticmethod
    def start(context, event):
        trace = tracepb.Trace()
        trace.MergeFrom(Fact.base)
        Fact._trace = trace
        Fact._trace.StartTime.CopyFrom(Fact.now())
        trace.ID = str(uuid.uuid4())
        if Fact._provider is None:
            Fact.load(context)
        assert Fact._provider is not None

        if Fact._provider is Provider.AWS:
            AWSFact.getInstances().collect(Fact._trace, context)

        if "send_on_update" in Fact.config and Fact.config["send_on_update"]:
            Fact.send("start")

    @staticmethod
    def update(context, message, tags):

        assert Fact._provider is not None
        assert Fact.config["io"].connected
        key = int(datetime.now().timestamp() * 1000)
        Fact._trace.Logs[key] = message
        Fact._trace.Logs.update(tags)

        if Fact._provider is Provider.AWS:
            AWSFact.getInstances().collect(Fact._trace, context)

        if "send_on_update" in Fact.config and Fact.config["send_on_update"]:
            Fact.send("update")

    @staticmethod
    def done(context, message, args):
        assert Fact._provider is not None
        assert Fact.config["io"].connected

        Fact._trace.EndTime.CopyFrom(Fact.now())
        key = int(datetime.now().timestamp() * 1000)
        Fact._trace.Logs[key] = message
        Fact._trace.Args.extend(args)
        duration = Duration()
        exec_time = Fact._trace.EndTime.seconds - Fact._trace.StartTime.seconds
        duration.FromSeconds(exec_time)
        Fact._trace.ExecutionLatency.CopyFrom(duration)

        if Fact._provider is Provider.AWS:
            AWSFact.getInstances().collect(Fact._trace, context)

        if "send_on_update" in Fact.config and Fact.config["send_on_update"]:
            Fact.send("done")
