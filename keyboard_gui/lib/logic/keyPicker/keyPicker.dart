import 'package:flutter/material.dart' hide Key;
import 'package:xml/xml.dart';
import 'dart:math';

import '../customPainters/keyboardPainter.dart';

import '../svgTagClasses/Key.dart';
import 'package:keyboard_gui/logic/svgTagClasses/SvgPathElement.dart';
import '../svgTagClasses/SvgTextElement.dart';


class KeyPicker extends StatefulWidget {
  final Map<String, dynamic> sharedData;
  final void Function(List<dynamic>, dynamic) setSharedData;
  late final List<Key> keys;
  late final List<SvgPathElement> pathElements;
  late final List<SvgTextElement> textElements;
  KeyPicker({super.key, required this.sharedData, required this.setSharedData});

  @override
  State<KeyPicker> createState() => _KeyPickerState();
}

class _KeyPickerState extends State<KeyPicker> {
  @override
  Widget build(BuildContext context) {
    final XmlDocument keyboardSVG = widget.sharedData["keyboardSVG"];
    widget.keys = keyboardSVG.findAllElements("rect").map((e) => Key(e, keyboardSVG)).toList();

    // Extract lists of all path and text elements from the svg document
    widget.pathElements = keyboardSVG.findAllElements("path").map((e) => SvgPathElement(e, keyboardSVG)).toList();
    widget.textElements = keyboardSVG.findAllElements("text").map((e) => SvgTextElement(e, keyboardSVG)).toList();
    // Turn each tag into its standardized class representation

    // Pass in the necessary lists of standardized SVG class elements 
    return LayoutBuilder(
        builder: (context, constraints) {
          // Get the rendered size of the SVG.
          final double maxWidth = constraints.maxWidth;
          final double maxHeight = constraints.maxHeight;

          // Original SVG dimensions.
          const double originalWidth = 312;
          const double originalHeight = 120;

          // Calculate scaling factor
          final double scale = min(maxWidth / originalWidth, maxHeight / originalHeight);


          final double renderedWidth = originalWidth * scale;
          final double renderedHeight = originalHeight * scale;
  

          return GestureDetector(
            onTapDown: (TapDownDetails details) {
              // Raw tap position relative to the widget.
              final Offset rawPosition = details.localPosition;

              // Scale the coordinates to match the original SVG dimensions.
              final double scaledX = rawPosition.dx / scale;
              final double scaledY = rawPosition.dy / scale;

              handleTap(scaledX, scaledY);
            },
            child: SizedBox(
              width: renderedWidth,
              height: renderedHeight,
              child: CustomPaint(
            painter: KeyboardPainter(scaleX: scale, scaleY: scale, keys: widget.keys, pathElements: widget.pathElements, textElements: widget.textElements, sharedData: widget.sharedData, context: context),
            child: Container())
          ));

        });
  }


  void handleTap(double x, double y){
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


