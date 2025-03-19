import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:xml/xml.dart';
import '../customPainters/keyboardPainter.dart';


class keyPicker extends StatefulWidget {
  final Map<String, dynamic> sharedData;
  final void Function(List<dynamic>, dynamic) setSharedData;
  const keyPicker({super.key, required this.sharedData, required this.setSharedData});

  @override
  State<keyPicker> createState() => _keyPickerState();
}

class _keyPickerState extends State<keyPicker> {
  @override
  Widget build(BuildContext context) {
    final XmlDocument keyboardSVG = widget.sharedData["keyboardSVG"];
    List<Key> keys = loadKeysFromKeyboardSVG(keyboardSVG: keyboardSVG);

    // Extract lists of all text and path elements from the svg document
    // Turn each tag into its standardized class representation

    // Pass in the necessary lists of standardized SVG class elements
    CustomPainter keyboardSVGPainter = KeyboardPainter(rectangles: keys, paths: [], textElements: []); 

    return CustomPaint(
      painter: keyboardSVGPainter,
      child: Container() // Wrap this in a gestureDetector which will grab click events and check if you clicked in a key
    );
  }
}



class Key { // We need to extend this from a rectangle property
  String id;
  String path;
  String name;
  double strokeWidth;
  Color color;
  Rect rect;
  
  Key(XmlElement element) {
    this.id = element.getAttribute('id').toString();
    this.path = element.getAttribute('d').toString();
    String name = element.getAttribute('name').toString();
    Color color = Color(int.parse("FF${element.getAttribute('stroke')?.toString().substring(1) ?? 'FFFFFF'}", radix: 16));
    List<double> coordinates = extractLTRBFromRect(element);
    Rect rect = Rect.fromLTRB(coordinates[0], coordinates[1], coordinates[2], coordinates[3]);
  };





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


List<Key> loadKeysFromKeyboardSVG({required XmlDocument keyboardSVG}) {
   List<Key> keys = [];
   
   final keyboardRects = keyboardSVG.findAllElements('rect');

   for (XmlElement element in keyboardRects) {
     keys.add(Key(element));
   }

   return keys;
 }

void correctSvgColors(XmlDocument svgDocument) {
    // Modify the 'fill' attribute of all elements with a `fill` attribute.
    for (XmlElement element in svgDocument.findAllElements('*')) {
      element.setAttribute('fill', '#FFFFFF');
      // if (element.getAttribute('fill') != null) {
      //   // Change the color to purple.
      //   element.setAttribute('fill', 'purple');
      // }
    }
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

