
# MineNBT
MineNBT is a lightweight, efficient Python library designed to read and write Minecraft's Named Binary Tag (NBT) data. This library aims to provide a simple interface for manipulating NBT data, which is used extensively in Minecraft for storing item, block, and world information.

## Features

-  **Read and Write NBT Files**: Load and save NBT data with full support for Minecraft's data formats.
-   **Support for Various Data Types**: Handle all NBT data types used in Minecraft.
-   **Automatic Handling of Compression**: Seamlessly manage compressed and uncompressed NBT files.
-   **Pure Python Implementation**: No external dependencies, easy to integrate with other projects.

## Installation

Install MineNBT using pip:

    pip install minenbt

## NBT Tag Types
MineNBT supports a variety of tag types defined in the NBT specification. Each tag type has a unique identifier and a specific data format. Below is a detailed listing of all supported NBT tag types along with their descriptions:

- **TAG_End**: (Tag ID: *0x00*) Marks the end of a TAG_Compound, contains no data.
- **TAG_Byte**: (Tag ID: *0x01*) A single signed byte (8-bit).
- **TAG_Short**: (Tag ID: *0x02*) A single signed, big endian 16-bit integer.
- **TAG_Int**: (Tag ID: *0x03*) A single signed, big endian 32-bit integer.
- **TAG_Long**: (Tag ID: *0x04*) A single signed, big endian 64-bit integer.
- **TAG_Float**: (Tag ID: *0x05*) A single, big endian IEEE-754 single-precision float.
- **TAG_Double**: (Tag ID: *0x06*) A single, big endian IEEE-754 double-precision float.
- **TAG_Byte_Array**: (Tag ID: *0x07*) A length-prefixed array of signed bytes.
- **TAG_String**: (Tag ID: *0x08*) A length-prefixed modified UTF-8 string.
- **TAG_List**: (Tag ID: *0x09*) A list of nameless tags, all of the same type.
- **TAG_Compound**: (Tag ID: *0x0A*) A complex tag containing a set of named tags.
- **TAG_IntArray**: (Tag ID: *0x0B*) A length-prefixed array of signed 32-bit integers.
- **TAG_LongArray**: (Tag ID: *0x0C*) A length-prefixed array of signed 64-bit longs.

## Important Update

> **Warning**: As of Minecraft version 1.20.2 (Protocol 764), NBT data sent over the network has been updated to exclude the name from the root TAG_COMPOUND. Ensure your implementations take this change into account to avoid compatibility issues.## Important Update

## Usage Examples

### Reading NBT Data

    from minenbt import NBT
    
    nbt_data = NBT.load('path_to_nbt_file.nbt')
    print(nbt_data)
    
### Saving NBT Data

    nbt_data.save('path_to_modified_nbt_file.nbt')
    
###  Exemples
   
	import  nbt
    
    # Load NBT file
    nb = nbt.NBT.load("test/hello_world.nbt", gzip=False)
    
    # Build NBT
    nb = nbt.NBT()
    nb.add(nbt.TagCompound("compoundTest", {
	    nbt.TagString("key", "value"),
	    nbt.TagFloat("floatTest", 1.0),
	    nbt.TagDouble("doubleTest", 1.0),
	    nbt.TagInt("intTest", 1),
	    nbt.TagLong("longTest", 1),
	    nbt.TagByteArray("byteArrayTest", [
		    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07
	    ]),
	    nbt.TagList("listTest", [
		    nbt.TagInt("intTest", 1),
	    	nbt.TagInt("intTest", 2),
	    ]),
	    nbt.TagIntArray("intArrayTest", [1, 2, 3]),
	    nbt.TagLongArray("longArrayTest", [1, 2, 3]),
	    nbt.TagList("listTest", [
		    nbt.TagCompound(None, {
			    nbt.TagString("key", "value")
		    }),
		    nbt.TagCompound(None, {
			    nbt.TagString("key", "value")
		    })
	    ])
	}))
	
	data  =  nb.build() # Returns bytes of NBT
	json  =  nb.json() # Returns NBT in a custom JSON format
	
	# Print NBT into a Tree view on the console
	nb.show()
	
	# Save NBT into file
	nb.save("hello_world.nbt", gzip=False)

### Output examples:

##### NBT.show()

    [NBT]
    TAG_Compound('compoundTest') (entries: 10)
    [
	    TAG_List('listTest') (entries: 2)
	    [
	      TAG_Int(intTest): 1
	      TAG_Int(intTest): 2
	    ]
	    TAG_Int(intTest): 1
	    TAG_IntArray('intArrayTest') (entries: 3)
		    [1, 2, 2]
	    TAG_Long(longTest): 1
	    TAG_List('listTest') (entries: 2)
	    [
	      TAG_Compound(None) (entries: 1)
	      [
	         TAG_String(key): 'value'
	      ]
	      TAG_Compound(None) (entries: 1)
	      [
	         TAG_String(key): 'value'
	      ]
	    ]
	    TAG_Double(doubleTest): 1.0
	    TAG_LongArray('longArrayTest') (entries: 3)
		    [1, 2, 2]
	    TAG_ByteArray('byteArrayTest') (entries: 8)
		    [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x6]
	    TAG_Float(floatTest): 1.0
	    TAG_String(key): 'value'
	]

##### NBT.json()

    [
	    {
		    "type":"TAG_Compound",
		    "name":"compoundTest",
		    "payload":[
			    {
				    "type":"TAG_Long",
				    "name":"longTest",
				    "payload":1
			    },
			    {
				    "type":"TAG_List",
				    "name":"listTest",
				    "data_type":"TAG_Compound",
				    "payload":[
					    [
						    {
							    "type":"TAG_String",
							    "name":"key",
							    "payload":"value"
						    }
					    ],
					    [
						    {
							    "type":"TAG_String",
							    "name":"key",
							    "payload":"value"
						    }
					    ]
				    ]
			    },
			    {
				    "type":"TAG_Double",
				    "name":"doubleTest",
				    "payload":1.0
			    },
			    {
				    "type":"TAG_LongArray",
				    "name":"longArrayTest",
				    "payload":[
					    1,2,3
				    ]
			    },
			    {
				    "type":"TAG_ByteArray",
				    "name":"byteArrayTest",
				    "payload":[
					    0,1,2,3,4,5,6,7
				    ]
			    },
			    {
				    "type":"TAG_Float",
				    "name":"floatTest",
				    "payload":1.0
			    },
			    {
				    "type":"TAG_Int",
				    "name":"intTest",
				    "payload":1
			    },
			    {
				    "type":"TAG_List",
				    "name":"listTest",
				    "data_type":"TAG_Int",
				    "payload":[1,2]
			    },
			    {
				    "type":"TAG_String",
				    "name":"key",
				    "payload":"value"
			    },
			    {
				    "type":"TAG_IntArray",
				    "name":"intArrayTest",
				    "payload":[1,2,3]
			    }
		    ]
	    }
    ]

## License
MineNBT is licensed under the MIT License - see the [LICENSE.md](https://github.com/Theoreb/MineNBT/LICENSE.md) file for details.

## Authors

 - **Theoreb**-  _Initial work_

