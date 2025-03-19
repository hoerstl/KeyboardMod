import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:xml/xml.dart';

class Key { // We need to extend this from a rectangle property
  final String id;
  final String path;
  final String name;
  final String color;
  final Rect rect;
  
  Key({required this.id, required this.path, required this.name, required this.color, required this.rect});
}
// Load the SVG string
// Parse the string and extract all the text, rects, and paths into separate lists
// Pass those to the customPainter which has the keyData hash map
// Return a canvas using the customPainter which colors all elements based on the keyData

List<double> extractLTRBFromRect(var element){
  final regex = RegExp(r'translate\(([^,]+),\s*([^)]+)\)');
  final match = regex.firstMatch(element.getAttribute('transform'));

  if (match == null) {
    throw FormatException("This element's transform property does not match the expected format: $element.getAttribute('transform')");
  } 
  // Parse the numbers and return them as a list
  final L = double.parse(match.group(1)!);
  final T = double.parse(match.group(2)!);
  final R = L + double.parse(element.getAttribute("width"));
  final B = T + double.parse(element.getAttribute("height"));

  return [T, L, R, B];
}


Future<List<Key>> loadKeysFromKeyboardSVG({required XmlDocument keyboardSVG}) async {
   List<Key> keys = [];
   
   final keyboardRects = keyboardSVG.findAllElements('rect');

   for (var element in keyboardRects) {
     String partId = element.getAttribute('id').toString();
     String partPath = element.getAttribute('d').toString();
     String name = element.getAttribute('name').toString();
     String color = element.getAttribute('color')?.toString() ?? 'D7D3D2';
     List<double> coordinates = extractLTRBFromRect(element);
     Rect rect = Rect.fromLTRB(coordinates[0], coordinates[1], coordinates[2], coordinates[3]);

     keys.add(Key(id: partId, path: partPath, color: color, name: name, rect: rect));
   }

   return keys;
 }

String correctSvgColors(String svgString) {
    // Parse the SVG XML.
    final XmlDocument svgDocument = XmlDocument.parse(svgString);

    // Modify the 'fill' attribute of all elements with a `fill` attribute.
    for (XmlElement element in svgDocument.findAllElements('*')) {
      element.setAttribute('fill', '#FFFFFF');
      // if (element.getAttribute('fill') != null) {
      //   // Change the color to purple.
      //   element.setAttribute('fill', 'purple');
      // }
    }

    // Return the modified SVG string.
    return svgDocument.toXmlString();
  }




Future<Widget> keyPicker() async {  // Add Context here so we can build with the correct colors

  String svgString = await rootBundle.loadString("assets/keyboard.svg");
  XmlDocument keyboardSVG = XmlDocument.parse(svgString);
  List<Key> keys = await loadKeysFromKeyboardSVG(keyboardSVG: keyboardSVG);

  // Extract lists of all text, rect, and path elements from the svg string
  // Turn each tag into its standardized class representation

  CustomPainter keyboardSVGPainter = KeyboardPainter(); // Pass in the necessary lists of standardized SVG class elements

  return CustomPaint(
    painter: keyboardSVGPainter,
    child: Container()
  );
}


// Use this to get the scaled coordinates from the rendered SVG file. We can get the scaled size from the constraints argument of the LayoutBuilder.
// LayoutBuilder(
//         builder: (context, constraints) {
//           // Get the rendered size of the SVG.
//           final double renderedWidth = constraints.maxWidth;
//           final double renderedHeight = constraints.maxHeight;

//           // Original SVG dimensions.
//           const double originalWidth = 200;
//           const double originalHeight = 200;

//           // Calculate scaling factors.
//           final double scaleX = renderedWidth / originalWidth;
//           final double scaleY = renderedHeight / originalHeight;

//           return GestureDetector(
//             onTapDown: (TapDownDetails details) {
//               // Raw tap position relative to the widget.
//               final Offset rawPosition = details.localPosition;

//               // Scale the coordinates to match the original SVG dimensions.
//               final double scaledX = rawPosition.dx / scaleX;
//               final double scaledY = rawPosition.dy / scaleY;

//               print("Raw Tap at: ${rawPosition.dx}, ${rawPosition.dy}");
//               print("Scaled Tap at: $scaledX, $scaledY");

//               handleTap(scaledX, scaledY);
//             },
//             child: SizedBox(
//               width: renderedWidth,
//               height: renderedHeight,
//               child: SvgPicture.string(
//                 svgContent,
//                 fit: BoxFit.contain, // Scales the SVG to fit the container.
//               ),
//             ),
//           );

