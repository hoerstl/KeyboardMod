import 'dart:math';

import 'package:flutter/material.dart' hide Key;
import '../svgTagClasses/Key.dart';
import '../svgTagClasses/SvgPathElement.dart';
import '../svgTagClasses/SvgTextElement.dart';
import 'package:path_drawing/path_drawing.dart';

class KeyboardPainter extends CustomPainter {
  final double scaleX;
  final double scaleY;
  final List<Key> keys;
  final List<SvgPathElement> pathElements;
  final List<SvgTextElement> textElements;
  final Map<String, dynamic> sharedData;
  final BuildContext context;

  KeyboardPainter({
    required this.scaleX,
    required this.scaleY,
    required this.keys,
    required this.pathElements,
    required this.textElements,
    required this.sharedData,
    required this.context
  });

  @override
  void paint(Canvas canvas, Size size) {
    final Paint rectPaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.stroke;
    final Paint pathPaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.0 * scaleX / 2.8;
    
    // Draw rectangles
    for (Key key in keys) {
      rectPaint.strokeWidth = key.strokeWidth;
      rectPaint.color = Theme.of(context).colorScheme.onPrimary; // Replace this with color determining logic that uses sharedData
      if (key.name == sharedData["selectedKey"]){
        rectPaint.color = Theme.of(context).colorScheme.primary;
      }
      final rect = Rect.fromLTRB(key.rect.left * scaleX,
         key.rect.top * scaleY,
         key.rect.right * scaleX,
         key.rect.bottom * scaleY);
      final RRect roundedRect = RRect.fromRectAndRadius(rect, const Radius.circular(3));
      canvas.drawRRect(roundedRect, rectPaint);
    }

    // Draw paths
    for (SvgPathElement pathElement in pathElements) {
      // Compose scale and SVG matrix together correctly
      final Matrix4 transform = Matrix4.identity()
        ..scale(scaleX, scaleY)
        ..multiply(pathElement.matrixTransform);

      // Apply combined transform to the path
      final Path transformedPath = pathElement.path.transform(transform.storage);

      // Draw the path
      canvas.drawPath(transformedPath, pathPaint);
    }



    // Draw text
    for (SvgTextElement textElement in textElements) {
      final fontSize = textElement.fontSize * min(scaleX, scaleY);
      final TextSpan textSpan = TextSpan(
        text: textElement.content,
        style: TextStyle(
          color: Colors.white,
          fontSize: fontSize,
          fontFamily: textElement.fontFamily,
          fontStyle: textElement.italicized ? FontStyle.italic : FontStyle.normal,
          fontWeight: textElement.bold ? FontWeight.bold : FontWeight.normal, 
        ),
      );
      final TextPainter textPainter = TextPainter(
        text: textSpan,
        textAlign: TextAlign.center,
        textDirection: TextDirection.ltr,
      )..layout();
      
      // SVG readers display text from bottom left
      // Paint paints from top left so we need to convert with an offset of the height of the fontsize
      textPainter.paint(canvas, Offset(textElement.x * scaleX, textElement.y * scaleY - (fontSize * 1.15)));
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true; // Always repaint for now. Optimize as needed.
  }
}
