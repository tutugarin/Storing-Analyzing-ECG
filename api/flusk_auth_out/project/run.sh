export FN_AUTH_REDIRECT_URI=http://localhost:5000/google/auth
export FN_BASE_URI=http://localhost:5000/table
export FN_CLIENT_ID='433488219494-pskhdk5jvej4f11kt8a6svtqb5qnts05.apps.googleusercontent.com'
export FN_CLIENT_SECRET='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'
export OAUTHLIB_INSECURE_TRANSPORT=1
export FLASK_APP=project
export FLASK_DEBUG=1
export FN_FLASK_SECRET_KEY='secret-key-goes-here'

 {
  "dataSource": [ # A previously created data source.
    { # Definition of a unique source of sensor data. Data sources can expose raw data coming from hardware sensors on local or companion devices. They can also expose derived data, created by transforming or merging other data sources. Multiple data sources can exist for the same data type. Every data point inserted into or read from this service has an associated data source. The data source contains enough information to uniquely identify its data, including the hardware device and the application that collected and/or transformed the data. It also holds useful metadata, such as the hardware and application versions, and the device type. Each data source produces a unique stream of data, with a unique identifier. Not all changes to data source affect the stream identifier, so that data collected by updated versions of the same application/device can still be considered to belong to the same data stream.
      "application": { # Information about an application which feeds sensor data into the platform.
        "detailsUrl": "A String", # An optional URI that can be used to link back to the application.
        "name": "A String", # The name of this application. This is required for REST clients, but we do not enforce uniqueness of this name. It is provided as a matter of convenience for other developers who would like to identify which REST created an Application or Data Source.
        "packageName": "A String", # Package name for this application. This is used as a unique identifier when created by Android applications, but cannot be specified by REST clients. REST clients will have their developer project number reflected into the Data Source data stream IDs, instead of the packageName.
        "version": "A String", # Version of the application. You should update this field whenever the application changes in a way that affects the computation of the data.
      },
      "dataQualityStandard": [ # DO NOT POPULATE THIS FIELD. It is never populated in responses from the platform, and is ignored in queries. It will be removed in a future version entirely.
        "A String",
      ],
      "dataStreamId": "A String", # A unique identifier for the data stream produced by this data source. The identifier includes: - The physical device's manufacturer, model, and serial number (UID). - The application's package name or name. Package name is used when the data source was created by an Android application. The developer project number is used when the data source was created by a REST client. - The data source's type. - The data source's stream name. Note that not all attributes of the data source are used as part of the stream identifier. In particular, the version of the hardware/the application isn't used. This allows us to preserve the same stream through version updates. This also means that two DataSource objects may represent the same data stream even if they're not equal. The exact format of the data stream ID created by an Android application is: type:dataType.name:application.packageName:device.manufacturer:device.model:device.uid:dataStreamName The exact format of the data stream ID created by a REST client is: type:dataType.name:developer project number:device.manufacturer:device.model:device.uid:dataStreamName When any of the optional fields that make up the data stream ID are absent, they will be omitted from the data stream ID. The minimum viable data stream ID would be: type:dataType.name:developer project number Finally, the developer project number and device UID are obfuscated when read by any REST or Android client that did not create the data source. Only the data source creator will see the developer project number in clear and normal form. This means a client will see a different set of data_stream_ids than another client with different credentials.
      "dataStreamName": "A String", # The stream name uniquely identifies this particular data source among other data sources of the same type from the same underlying producer. Setting the stream name is optional, but should be done whenever an application exposes two streams for the same data type, or when a device has two equivalent sensors.
      "dataType": { # The data type defines the schema for a stream of data being collected by, inserted into, or queried from the Fitness API.
        "field": [ # A field represents one dimension of a data type.
          { # In case of multi-dimensional data (such as an accelerometer with x, y, and z axes) each field represents one dimension. Each data type field has a unique name which identifies it. The field also defines the format of the data (int, float, etc.). This message is only instantiated in code and not used for wire comms or stored in any way.
            "format": "A String", # The different supported formats for each field in a data type.
            "name": "A String", # Defines the name and format of data. Unlike data type names, field names are not namespaced, and only need to be unique within the data type.
            "optional": True or False,
          },
        ],
        "name": "A String", # Each data type has a unique, namespaced, name. All data types in the com.google namespace are shared as part of the platform.
      },
      "device": { # Representation of an integrated device (such as a phone or a wearable) that can hold sensors. Each sensor is exposed as a data source. The main purpose of the device information contained in this class is to identify the hardware of a particular data source. This can be useful in different ways, including: - Distinguishing two similar sensors on different devices (the step counter on two nexus 5 phones, for instance) - Display the source of data to the user (by using the device make / model) - Treat data differently depending on sensor type (accelerometers on a watch may give different patterns than those on a phone) - Build different analysis models for each device/version. # Representation of an integrated device (such as a phone or a wearable) that can hold sensors.
        "manufacturer": "A String", # Manufacturer of the product/hardware.
        "model": "A String", # End-user visible model name for the device.
        "type": "A String", # A constant representing the type of the device.
        "uid": "A String", # The serial number or other unique ID for the hardware. This field is obfuscated when read by any REST or Android client that did not create the data source. Only the data source creator will see the uid field in clear and normal form. The obfuscation preserves equality; that is, given two IDs, if id1 == id2, obfuscated(id1) == obfuscated(id2).
        "version": "A String", # Version string for the device hardware/software.
      },
      "name": "A String", # An end-user visible name for this data source.
      "type": "A String", # A constant describing the type of this data source. Indicates whether this data source produces raw or derived data.
    },
  ],
}