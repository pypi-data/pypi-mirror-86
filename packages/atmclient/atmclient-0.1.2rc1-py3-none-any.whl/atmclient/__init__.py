"""
    Copyright 2020 LXPER Inc.
    REFERENCE: Engine(공통함수)
    DESIGNER: LXPER Development Team
    TECHNICAL WRITER: LXPER Development Team
    VERSION: 2.0

    ATM v2 API Protocol Compliant Client
    
    This script is designed to communicate with 
    the ATM Code Standard(Chan Woo Kim, Jung Jung Ho) compliant ATM v2 API
    Developers can use this module to conveniently utilize the various engines 
    and shared functions in the LXPER Kubernetes on-premises environment.
    It is distributed without requiring the installation of dependencies.

    >>> from atmclient import client
    >>> client.<tab>
    
"""

__version__ = "0.1.2-rc.1"

# python standard libraries
import os
import json
import warnings
import urllib.request
from urllib.error import URLError, HTTPError
from typing import (List, Dict, Optional, Any)

# contrib libraries
from .contrib.easydict import EasyDict

################################################################################
# Section A. Utility Classes
################################################################################
class ATMResult(EasyDict):
    """Result container for server responses"""
    pass

################################################################################
# Section B. Base Classes
################################################################################

class BaseRequest:
    """Base class for urllib requests.

    This is callable, which get urllib.request.Request from property 'request' 
    and execute it. Therefore, the subclasses have responsibility
    to implement property 'request' so that it returns urllib.request.Request.

    When subclasses need to adapt the response json data into desired format,
    please implement method 'postprocess' which defaults to identity transformation.
    """
    def __call__(self):
        """
        First, send the request as specified in urllib.request.Request.
        Second, convert response as json format.
        Third, post process the json data into desired format. 
        """
        try:
            res = urllib.request.urlopen(self.request)
            data = json.loads(res.read().decode('utf-8'))
            data = self.postprocess(data)
            return data
        except HTTPError as exc:
            message = "[{code}] {sent_message}".format(
                code=exc.code,
                sent_message=exc.read().decode('utf-8')
            )
            raise ValueError(message)
        except URLError as exc:
            raise ValueError("[-] Unable to reach server.")

    @property
    def request(self) -> urllib.request.Request:
        """The subclasses should implement this property 
        to return the instance of urllib.request.Request"""
        raise NotImplementedError("You should implement the request property"
                                  "to inherit the class.")

    def postprocess(self, data: Dict) -> Any:
        """Transform response json data into desired format.
        
        Args:
            data(dict): response from the request.

        Returns:
            Any: desired format. defaults to identity transformation.
        """
        return data

class BaseGETRequest(BaseRequest):
    """Specialized for the GET request using urllib. 
    
    Note:
        Contrary to the POST request, GET request does not require any payload.
    """
    def __init__(self, 
                 url: str):
        super().__init__()
        self._url = url

    @property
    def request(self) -> urllib.request.Request:
        url = self._url
        req = urllib.request.Request(url, 
                                     headers={'content-type': 'application/json'})
        return req

class BasePOSTRequest(BaseRequest):
    """Specialized for the POST request using urllib. 
    
    Note: 
        Every POST requests requires the payload and url, 
        Therefore this class needs to be initialized with the two positional arguments.
    """
    def __init__(self, 
                 url: str, 
                 payload: Dict):
        super().__init__()
        self._url = url
        self._payload = payload

    @property
    def request(self) -> urllib.request.Request:
        url = self._url
        payload = json.dumps(self._payload).encode('utf-8')
        req = urllib.request.Request(url, 
                                     data=payload, 
                                     headers={'content-type': 'application/json'})
        return req

class BaseDiscoveryRequest(BaseGETRequest):
    """To discover the possible parameters on the LXPER endpoint."""
    def postprocess(self, data: Dict) -> List[Dict]:
        """Transforms the response json into the parameter listing format.

        Args:
            data (dict): Response json from the engine which implements 
                         the LXPER code-standard interface.
                         (Other keys are omitted for the brevity.) 

                            { 
                                ...
                            "request_json":{
                                            "title":"requestJSON",
                                            "type":"object",
                                            "properties":{
                                                "passage":{
                                                    "title":"Passage",
                                                    "type":"string"
                                                }
                                            },
                                            "required":[
                                                "passage"
                                            ]
                                            }
                            }

        Returns:
            params: List[Dict]

                [
                    {"name": "passage", "type": "string", "description": "", "required": True}
                ]
        """
        params_properties = data['request_json']['properties']
        params_required = data['request_json'].get('required', [])
        params = []
        for param_name, param_info in params_properties.items():
            # In the example above, 'param_name' is 'passage' 
            # while 'param_info' is {'title': 'x', 'type': 'x'}
            param = {'name': param_name, 
                     'type': param_info.get("type", ""), 
                     'description': param_info.get("description", ""),
                     'required': param_name in params_required}
            params.append(param)
        
        return params

class BaseJobRequest(BasePOSTRequest):
    """Every Job Request should implement this class. 
    
    JobRequest is the request sent to ATM API to make actual work done.

    Any subclasses should implement __init__ and be adapted into the specific purpose. 
    Inside the __init__, you need to instantialize with 
    super().__init__(url), where url is the destination to make the call.

    This does not have any differences from BasePOSTRequest. However, in order to maintain
    the naming consistency, we provide this as base class."""


################################################################################
# Section C. Job / Discovery / List Request Classes
################################################################################

ATM_GATEWAY_URL = os.getenv("ATM_GATEWAY_URL", "http://atm-api-gateway.atm.svc.cluster.local:8080")

class EndpointDiscoveryRequest(BaseDiscoveryRequest):
    """Request sent to Endpoint API to discover the possible parameters and availability"""
    def __init__(self, 
                 endpoint_id: str):
        url = f"{ATM_GATEWAY_URL}/{endpoint_id}"
        super().__init__(url)

class EndpointJobRequest(BaseJobRequest):
    """Request sent to Endpoint API to make the actual work done"""
    def __init__(self, 
                 endpoint_id: str, 
                 payload: Dict):
        url = f"{ATM_GATEWAY_URL}/{endpoint_id}/generate"
        super().__init__(url, payload)

class EndpointListRequest(BaseGETRequest):
    """To discover the possible endpoints on the LXPER atm v2 api"""
    def __init__(self):
        url = f"{ATM_GATEWAY_URL}/actuator/gateway/routes"
        super().__init__(url)

    def postprocess(self, data: Dict) -> List[Dict]:
        """Transforms the response json into the parameter listing format.

        Args:
            data (dict): Response json from the api gateway.
                         (Other keys are omitted for the brevity.) 

            [
                {
                    "predicate":"Paths: [/engine-blank-finder/**], match trailing slash: true",
                    "metadata":{
                        "type":"atm-library",
                        "kubectl.kubernetes.io/last-applied-configuration":"{"apiVersi...,
                        "port.web":"8000"
                    },
                    "route_id":"ReactiveCompositeDiscoveryClient_atm-engine-blank-finder",
                    "filters":[
                        "[[RewritePath /proc(?<segment>[^/]*)(/)?(?<remaining>.*)? = '/proc${segment}/${remaining}'], order = 1]",
                        "[[RewritePath /task(?<segment>[^/]*)(/)?(?<remaining>.*)? = '/${remaining}'], order = 2]",
                        "[[RewritePath /engine(?<segment>[^/]*)(/)?(?<remaining>.*)? = '/${remaining}'], order = 3]"
                    ],
                    "uri":"http://atm-engine-blank-finder:8000",
                    "order":0
                }, ...
            ]

        Returns:
            endpoints: Dict

                {
                    'endpoints': ['proc-translate', ...]
                }
        """
        endpoint_ids = []
        for route in data:
            predicate = route['predicate']
            start_position = predicate.find("/") + 1
            end_position = predicate.find("/**")
            endpoint_id = predicate[start_position:end_position]
            
            if '-' not in endpoint_id:
                continue
            endpoint_ids.append(endpoint_id)
            
        endpoints = {'endpoints': endpoint_ids}
        
        return endpoints


################################################################################
# Section D. Function and Client Classes
#
#    Client is the mediator between user and the ATMFunction class.
#    When user tries to access the member of client, client looks up the
#    related ATMFunction from its own internal dictionary.
################################################################################

class ATMFunction:
    """Callable which executes the request to the API using JobRequest.
    
    This class also performs parameter discovery using DiscoveryRequest.
    When the class is initialized, the test is done to check whether the function is
    able to work, and determines how the parameters are defined in the API side.

    It does not catch the exceptions. raised exception will propagate into parent code.
    """
    def __init__(self, 
                 endpoint_id: str, 
                 job_request_cls: BaseJobRequest, 
                 discovery_request_cls: BaseDiscoveryRequest):
        self._endpoint_id = endpoint_id
        self._job_request_cls = job_request_cls
        self._discovery_request_cls = discovery_request_cls

        # Initially, _discovered_params is None 
        # When the property 'self.params' is called,
        # and 'self._discovered_params' found to be None,
        # the _discovery_request_cls is fired to set 'self._discovered_params'
        self._discovered_params = None

        # to check this function is in work 
        self._test()

    def _test(self):
        # test by look up self.params.
        # Note that self.params has logic to check the availability.
        assert len(self.params) > 0, f"Test failed for {self._endpoint_id}."

    @property
    def params(self) -> List[Dict]:
        """list parameters that API accepts.
        
        If the self._discovered_params is not set, the _discovery_request_cls is called
        to get the parameter information from the API

        This property will raise the error when the API side does not respond.
        """
        if self._discovered_params is None:
            req = self._discovery_request_cls(self._endpoint_id)
            params = req()
            self._discovered_params = params
        return self._discovered_params

    def __repr__(self) -> str:
        """Support visual repretation in the IDE
        
        Returns:
            str: <ATMFunction(parameter_name: parameter_type, ...)>
        """
        repr_param = ", ".join(f"{param['name']}: {param['type']}" 
                               for param in self.params)
        repr_clsname = type(self).__name__
        return f"<{repr_clsname}({repr_param})>"

    @property
    def __doc__(self) -> str:
        # TODO: Support for `Returns:` section
        docstring_args = "Args:"
        docstring_kwargs = "Keyword Arguments:"
        docstring_param_tpl = "{name}({type}): {description}"
        
        params_args, params_kwargs = [], []

        for param in self.params:
            if param['required']:
                params_args.append(param)
            else:
                params_kwargs.append(param)
        
        docstring = f"Calls API for {self._endpoint_id}"
        docstring += "\n"
        docstring += "\n"
        
        if params_args:
            docstring += docstring_args + "\n"

            for param in params_args:
                docstring_param = \
                docstring_param_tpl.format(name=param['name'], 
                                           type=param['type'], 
                                           description=param["description"])
                docstring += "\t" + docstring_param + "\n"

        if params_kwargs:
            docstring += docstring_kwargs + "\n"

            for param in params_kwargs:
                docstring_param = \
                docstring_param_tpl.format(name=param['name'], 
                                           type=param['type'], 
                                           description=param["description"])
                docstring += "\t" + docstring_param + "\n"

        return docstring
       
    def __call__(self, *args, **kwargs):
        # This builds the payload from the given args and kwargs, 
        # and the params that ATM API supports
        payload = {}

        # When kwargs is set twice, we will raise error.
        param_name_set = set()

        # In PEP8, 'if args' is completely acceptable and the recommended way, 
        # because the empty sequence is evaluated as False.
        # However, explicitly stating the comparison with zero
        # makes the another technical writers infer the data type easily.
        if len(args) > 0:
            # user gave args. this means we need to fill the parameters in order.
            for param, value in zip(self.params, args):
                param_name = param['name']
                payload[param_name] = value
                # occupied parameters are inserted into the set 'param_name_set'
                param_name_set.add(param_name)
            
        if len(kwargs) > 0:
            for param_name, value in kwargs.items():
                if param_name in param_name_set:
                    # This line is executed when the keyword argument is
                    # provided for the same position argument which is
                    # already occupied. 
                    raise TypeError("got multiple valus for argument"
                                    f"'{param_name}'")
                payload[param_name] = value
                param_name_set.add(param_name)

        req = self._job_request_cls(self._endpoint_id, payload)
        # request is evaluated(fired, called) in the following line.
        data = req()
        
        # we can support dot notation for easier access for data
        try:
            data = ATMResult(data)
            return data
        except:
            # if the data isn't dictionary type, it may raise exception.
            return data
    

class Client:
    """ATM v2 API Protocol Compliant Client

    Example usage:
        - List available endpoints
        >>> client.<tab>

    """
    def __init__(self):
        # container for storing the ATMFunction object with the key 'endpoint-id'
        # atm-endpoints are lazily loaded when __dir__ or __getattr__ is called.
        self._endpoints = {}        
        
    def __dir__(self) -> List[str]:
        """Discovered endpoints as well as the original possible attributes 
        are presented here.
        
        It is intended for supporting IPython, jupyter notebook tab completion
        """
        # lazily loading for the available endpoints
        if len(self._endpoints) == 0:
            self.proc_list()
            
        possible_attrs = [endpoint_id.replace("-", "_") 
                          for endpoint_id in self._endpoints] + \
                          object.__dir__(self)
        return possible_attrs

    def proc_list(self):
        """List possible endpoints in the ATM v2 API"""
        req = EndpointListRequest()
        data = req()
        endpoint_ids = data['endpoints']
        
        # reset endpoints
        self._endpoints = {}
        for endpoint_id in endpoint_ids:
            try:
                func = ATMFunction(endpoint_id, EndpointJobRequest, EndpointDiscoveryRequest)
                self._endpoints[endpoint_id] = func
                # when ATMFunction is initialized, AssertionError is raised if the target endpoint_id is invalid.
            except Exception as exc:
                exc_type, exc_msg = type(exc).__name__, exc.args[0] if len(exc.args) else ""
                msg = f"Ignored '{endpoint_id}' since it does not exist.({exc_type}: {exc_msg})"
                warnings.warn(msg)
        return {'endpoints': self._endpoints.keys()}

    def __getattr__(self, attr):
        """__getattr__ is called when the given attribute is not found in the object.
        
        This method allows us to access custom functions dynamically.
        When a user tries accessing attributes, for instance, 
        'client.engine_xxx_xxx', 
        this method is called with positional argument 'attr' as 'engine_xxx_xxx'. 
        """
        # This line ensures the attribute the user is looking for is converted to
        # dash-style conforming. e.g. 'engine_xxx' -> 'engine-xxx'
        endpoint_id = attr.replace("_", "-")
        
        # if current endpoint_id is not listed in the self._endpoints,
        # we renew the endpoint listings.
        if endpoint_id not in self._endpoints:
            self.proc_list()
        
        func = self._endpoints.get(endpoint_id, None)
        
        # if initialization of function failures, we should raise Exception
        if func is None:
            raise AttributeError(f"No endpoint exists for '{endpoint_id}'. "
                                      "Did you put it correctly?")
        return func
            


################################################################################
# Section E. Initializing Classes
#
#    Initialize the client when imported
################################################################################


client = Client()
