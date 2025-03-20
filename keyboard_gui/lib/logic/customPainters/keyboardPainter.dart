import 'package:flutter/material.dart' hide Key;
import '../svgTagClasses/Key.dart';

class KeyboardPainter extends CustomPainter {
  final double scaleX;
  final double scaleY;
  final List<Key> keys;
  final List<Path> paths;
  final List<SvgTextElement> textElements;
  final Map<String, dynamic> sharedData;
  final BuildContext context;

  KeyboardPainter({
    required this.scaleX,
    required this.scaleY,
    required this.keys,
    required this.paths,
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
      ..strokeWidth = 2.0;

    // Draw rectangles
    for (Key key in keys) {
      rectPaint.strokeWidth = key.strokeWidth;
      rectPaint.color = Theme.of(context).colorScheme.onPrimary; // Replace this with color determining logic that uses sharedData
      if (key.name == sharedData["selectedKey"]){
        rectPaint.color = Theme.of(context).colorScheme.primary;
      }
      canvas.drawRect(Rect.fromLTRB(key.rect.left * scaleX,
         key.rect.top * scaleY,
         key.rect.right * scaleX,
         key.rect.bottom * scaleY), rectPaint);
    }

    // Draw paths
    for (Path path in paths) {
      canvas.drawPath(path, pathPaint);
    }

    // Draw text
    for (SvgTextElement textElement in textElements) {
      final TextSpan textSpan = TextSpan(
        text: textElement.content,
        style: TextStyle(
          color: Colors.black,
          fontSize: textElement.fontSize,
        ),
      );
      final TextPainter textPainter = TextPainter(
        text: textSpan,
        textDirection: TextDirection.ltr,
      )..layout();
      textPainter.paint(canvas, Offset(textElement.x, textElement.y));
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true; // Always repaint for now. Optimize as needed.
  }
}

class SvgTextElement {
  final double x; // Extracted from the transform property
  final double y; // Extracted from the transform property and the dy property on the spans
  final double fontSize;
  final String fill;
  final String name;
  final String content;

  SvgTextElement({
    required this.x,
    required this.y,
    required this.fontSize,
    required this.fill,
    required this.name,
    required this.content,
  });
}