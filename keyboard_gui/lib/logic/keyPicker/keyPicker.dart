import 'package:flutter/material.dart' hide Key;
import 'package:xml/xml.dart';
import '../customPainters/keyboardPainter.dart';

import '../svgTagClasses/Key.dart';


class KeyPicker extends StatefulWidget {
  final Map<String, dynamic> sharedData;
  final void Function(List<dynamic>, dynamic) setSharedData;
  late List<Key> keys;
  KeyPicker({super.key, required this.sharedData, required this.setSharedData});

  @override
  State<KeyPicker> createState() => _KeyPickerState();
}

class _KeyPickerState extends State<KeyPicker> {
  @override
  Widget build(BuildContext context) {
    final XmlDocument keyboardSVG = widget.sharedData["keyboardSVG"];
    widget.keys = keyboardSVG.findAllElements("rect").map((e) => Key(e)).toList();

    // Extract lists of all text and path elements from the svg document
    // Turn each tag into its standardized class representation

    // Pass in the necessary lists of standardized SVG class elements 
    return LayoutBuilder(
        builder: (context, constraints) {
          // Get the rendered size of the SVG.
          final double renderedWidth = constraints.maxWidth;
          final double renderedHeight = constraints.maxHeight;

          // Original SVG dimensions.
          const double originalWidth = 312;
          const double originalHeight = 120;

          // Calculate scaling factors.
          final double scaleX = renderedWidth / originalWidth;
          final double scaleY = renderedHeight / originalHeight;

          return GestureDetector(
            onTapDown: (TapDownDetails details) {
              // Raw tap position relative to the widget.
              final Offset rawPosition = details.localPosition;

              // Scale the coordinates to match the original SVG dimensions.
              final double scaledX = rawPosition.dx / scaleX;
              final double scaledY = rawPosition.dy / scaleY;

              handleTap(scaledX, scaledY);
            },
            child: SizedBox(
              width: renderedWidth,
              height: renderedHeight,
              child: CustomPaint(
            painter: KeyboardPainter(scaleX: scaleX, scaleY: scaleY, keys: widget.keys, paths: [], textElements: [], sharedData: widget.sharedData),
            child: Container())
          ));

        });
  }


  void handleTap(double x, double y){
    print("handling click at $x $y");
    for (Key key in widget.keys){
      if (key.rect.contains(Offset(x, y))){
        widget.setSharedData(["selectedKey"], key.name);
        break;
      }
    }
  }
}






// void correctSvgColors(XmlDocument svgDocument) {
//     // Modify the 'fill' attribute of all elements with a `fill` attribute.
//     for (XmlElement element in svgDocument.findAllElements('*')) {
//       element.setAttribute('fill', '#FFFFFF');
//       // if (element.getAttribute('fill') != null) {
//       //   // Change the color to purple.
//       //   element.setAttribute('fill', 'purple');
//       // }
//     }
//   }




// Use this to get the scaled coordinates from the rendered SVG file. We can get the scaled size from the constraints argument of the LayoutBuilder.


