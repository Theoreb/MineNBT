import nbt

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

data = nb.build() # Returns bytes of NBT

print(nb.dict()) # Returns a JSON-compatible list format

# Print NBT into a Tree view on the console
nb.show()

# Save NBT into file
nb.save("hello_world.nbt", gzip=False)