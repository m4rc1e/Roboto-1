from designSpaceDocument import DesignSpaceDocument, SourceDescriptor, InstanceDescriptor, AxisDescriptor
import os

###

designSpacePath = "Roboto-min.designspace"
familyName = "Roboto"

sources = [
	dict(path="master_ufo/Roboto-Thin.ufo", name="Roboto-Thin.ufo", location=dict(weight=-1), styleName="Thin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/Roboto-Regular.ufo", name="Roboto-Regular.ufo", location=dict(weight=-0.1, width=1.0, slant=0), styleName="Regular", familyName=familyName, copyInfo=True),
	dict(path="master_ufo/Roboto-Black.ufo", name="Roboto-Black.ufo", location=dict(weight=1.125), styleName="Black", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/Roboto-ThinItalic.ufo", name="Roboto-ThinItalic.ufo", location=dict(weight=-1, slant=12), styleName="Thin Italic", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/Roboto-Italic.ufo", name="Roboto-Italic.ufo", location=dict(slant=12), styleName="Italic", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/Roboto-BlackItalic.ufo", name="Roboto-BlackItalic.ufo", location=dict(weight=1.125, slant=12), styleName="Black Italic", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoCondensed-Light.ufo", name="RobotoCondensed-Light.ufo", location=dict(weight=-0.55, width=0.87), styleName="Condensed Light", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoCondensed-Regular.ufo", name="RobotoCondensed-Regular.ufo", location=dict(width=0.87), styleName="Condensed Regular", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoCondensed-Bold.ufo", name="RobotoCondensed-Bold.ufo", location=dict(weight=0.75, width=0.87), styleName="Condensed Bold", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoCondensed-LightItalic.ufo", name="RobotoCondensed-LightItalic.ufo", location=dict(weight=-0.55, width=0.87, slant=12), styleName="Condensed Light Italic", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoCondensed-Italic.ufo", name="RobotoCondensed-Italic.ufo", location=dict(width=0.87, slant=12), styleName="Condensed Italic", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoCondensed-BoldItalic.ufo", name="RobotoCondensed-BoldItalic.ufo", location=dict(weight=0.75, width=0.87, slant=12), styleName="Condensed Bold Italic", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoWide-Regular.ufo", name="RobotoWide-Regular.ufo", location=dict(width=1.21), styleName="Wide Regular", familyName=familyName, copyInfo=False),
]
axes = [
	dict(minimum=-1, maximum=1.125, default=-0.1, name="weight", tag="wght", labelNames={"en": "Weight"}, map=[]),
	dict(minimum=0.87, maximum=1.21, default=1.0, name="width", tag="wdth", labelNames={"en": "Width"}, map=[]),
	dict(minimum=0, maximum=12, default=0, name="slant", tag="slnt", labelNames={"en": "Slant"}, map=[]),
]

instances = []
for source in sources:
	instances.append(dict(location=source["location"], styleName=source["styleName"], familyName=source["familyName"]))

#Thin
instances.insert(1, dict(location=dict(weight=-0.55), styleName="Light", familyName=familyName))
#Regular
instances.insert(3, dict(location=dict(weight=0.35), styleName="Medium", familyName=familyName))
instances.insert(4, dict(location=dict(weight=0.73), styleName="Bold", familyName=familyName))
#Bold
#Thin Italic
instances.insert(7, dict(location=dict(weight=-0.55, slant=12), styleName="Light Italic", familyName=familyName))
#Italic
instances.insert(9, dict(location=dict(weight=0.35, slant=12), styleName="Medium Italic", familyName=familyName))
instances.insert(10, dict(location=dict(weight=0.73, slant=12), styleName="Bold Italic", familyName=familyName))
#Black Italic

instances.pop(2) # fix bug with 2 regular?

doc = DesignSpaceDocument()

for source in sources:
	s = SourceDescriptor()
	s.path = source["path"]
	s.name = source["name"]
	s.copyInfo = source["copyInfo"]
	s.location = source["location"]
	s.familyName = source["familyName"]
	s.styleName = source["styleName"]
	doc.addSource(s)

for instance in instances:
	i = InstanceDescriptor()
	i.location = instance["location"]
	i.familyName = instance["familyName"]
	i.styleName = instance["styleName"]
	doc.addInstance(i)

for axis in axes:
	a = AxisDescriptor()
	a.minimum = axis["minimum"]
	a.maximum = axis["maximum"]
	a.default = axis["default"]
	a.name = axis["name"]
	a.tag = axis["tag"]
	for languageCode, labelName in axis["labelNames"].items():
		a.labelNames[languageCode] = labelName
	a.map = axis["map"]
	doc.addAxis(a)

#doc.checkAxes()

#doc.checkDefault()

doc.write(designSpacePath)
