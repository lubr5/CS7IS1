please read for changes ive made to example instances

## Parks
I took IRI from ObjectID rather than park_name so park/3 rather than CabinTeelyPark -> safer
I will probably do this rather than
park has label in english and irish, altLabel as previous name, address as address, parkType as type (parkType must be defined all others are general)
we must remove whitespace from data - done here but not original data

we currently only have 7 classes, i think we should just do area ill make a simple mapping here, then make parkclassification a class instead of string - that way a query could be like count parks of this type in this area blahablahblah