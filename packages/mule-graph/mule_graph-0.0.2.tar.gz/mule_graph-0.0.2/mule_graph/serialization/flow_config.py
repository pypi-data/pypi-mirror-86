# constants

FLOW_XML_TAG = "{http://www.mulesoft.org/schema/mule/core}flow"


FLOW_XML_TAG = "{http://www.mulesoft.org/schema/mule/core}flow"

APIKIT_XML_TAG = "{http://www.mulesoft.org/schema/mule/mule-apikit}router"
APIKIT_CONFIG_XML_TAG = "{http://www.mulesoft.org/schema/mule/mule-apikit}config"
ERROR_HANDLER_XML = "{http://www.mulesoft.org/schema/mule/core}error-handler"


# this should go to a yaml file
FLOW_CONTROLS = [
    "{http://www.mulesoft.org/schema/mule/core}round-robin",
    "{http://www.mulesoft.org/schema/mule/core}choice",
    "{http://www.mulesoft.org/schema/mule/core}first-successful",
    "{http://www.mulesoft.org/schema/mule/core}scatter-gather",
    "{http://www.mulesoft.org/schema/mule/core}try",
]
