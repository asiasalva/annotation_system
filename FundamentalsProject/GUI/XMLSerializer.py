import xml.etree.ElementTree as ET
from datetime import datetime

class XMLSerializer(object):
	def __init__(self, *args, **kwargs):
		return super().__init__(*args, **kwargs)

	

	def readXML(self, filePath):
		print("readXML")

	def writeXML(self, filePath, fileName, videoPath, listOfAnnotations):
		print("writeXML")

		root = ET.Element("project")
		root.attrib["name"] = fileName
		root.attrib["date"] = str((datetime.now()).strftime("%d/%m/%Y %H:%M:%S"))

		video = ET.SubElement(root, "video")
		video.text = filePath

		list_annotations = ET.SubElement(root, "list_annotations")

		for item in listOfAnnotations:
			annotation = ET.SubElement(list_annotations, "annotation")
			
			frame_start = ET.SubElement(annotation, "frame_start")
			frame_start.text = str((item.getFrameRange())[0])
			frame_end = ET.SubElement(annotation, "frame_end")
			frame_end.text = str((item.getFrameRange())[1])

			second_start = ET.SubElement(annotation, "second_start")
			second_start.text = str((item.getSecRange())[0])
			second_end = ET.SubElement(annotation, "second_end")
			second_end.text = str((item.getSecRange())[1])

			position = ET.SubElement(annotation, "position")
			x = ET.SubElement(position, "x")
			x.text = str((item.getPosition()).x())
			y = ET.SubElement(position, "y")
			y.text = str((item.getPosition()).y())

			dimensions = ET.SubElement(annotation, "dimensions")
			width = ET.SubElement(dimensions, "width")
			width.text = str((item.getDimensions())[0])
			height = ET.SubElement(dimensions, "height")
			height.text = str((item.getDimensions())[1])

			child = ET.SubElement(annotation, "child")
			child.attrib['type'] = item.annotationType

			if item.annotationType == "QPlainTextEdit":
				text = ET.SubElement(child, "text")
				text.text = item.getTextboxText()

				background_opacity = ET.SubElement(child, "background_opacity")
				background_opacity.text = str(item.getTextboxBackgroundOpacity())

				font_color = ET.SubElement(child, "font_color")
				font_color.text = item.getTextboxFontColor()

				font_size =  ET.SubElement(child, "font_size")
				font_size.text = str(item.getTextboxFontSize())

			elif item.annotationType == "QSvgWidget":
				is_arrow = ET.SubElement(child, "is_arrow")
				is_arrow.text = str(item.isArrow)

				color = ET.SubElement(child, "color")
				color.text = item.getSvgColor()

				extra = ET.SubElement(child, "extra")
				extra.text = item.getSvgExtraAttribute()

				transform = ET.SubElement(child, "transform")
				transform.text = item.getSvgTransform()


		tree = ET.ElementTree(root)
		tree.write(filePath + "/" + fileName)


		# TO PRETTY XML
		#from xml.dom import minidom
		#reparsed = minidom.parseString(s)
		#print(reparsed.toprettyxml(indent="  "))


	'''
	XML STRUCTURE

	<project name="name_project" date="date_modified">
		<video>video_path</video>
		<list_annotations>
			<annotation>
				<frame_start>n°</frame_start>
				<frame_end>n°</frame_end>
				<second_start>n°</second_start>
				<second_end>n°</second_end>
				<position>n°,n°</position>
				<width>n°</width>
				<height>n°</height>

				<child type="annotation_type">
					IF TYPE=QPLAINTEXTEDIT
					<text>textbox_text</text>
					<background_opacity>n°</background_opacity>
					<font_color>#000000</font_color>
					<font_size>n°</font_size>

					IF TYPE=QSVGWIDGET
					<is_arrow>bool</is_arrow>
					<color>#000000</color>
					<extra>n°</extra>
					<transform>n°</transform>

					IF TYPE=BREAKPOINT
					EMPTY
				</child>

			</annotation>
		</list_annotations>
	</project>
	'''