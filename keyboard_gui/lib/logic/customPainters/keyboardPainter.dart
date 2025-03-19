import 'package:flutter/material.dart' hide Key;
import 'package:xml/xml.dart';
import '../keyPicker/keyPicker.dart';

class KeyboardPainter extends CustomPainter {
  final List<Key> rectangles;
  final List<Path> paths;
  final List<SvgTextElement> textElements;

  KeyboardPainter({
    required this.rectangles,
    required this.paths,
    required this.textElements,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final Paint rectPaint = Paint()..color = Colors.blue.withOpacity(0.5);
    final Paint pathPaint = Paint()
      ..color = Colors.green
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    // Draw rectangles
    for (Key key in rectangles) {
      canvas.drawRect(key.rect, rectPaint);
    }

    // Draw paths
    for (Path path in paths) {
      canvas.drawPath(path, pathPaint);
    }

    // Draw text
    for (_TextElement textElement in textElements) {
      final TextSpan textSpan = TextSpan(
        text: textElement.text,
        style: TextStyle(
          color: Colors.black,
          fontSize: textElement.fontSize,
        ),
      );
      final TextPainter textPainter = TextPainter(
        text: textSpan,
        textDirection: TextDirection.ltr,
      )..layout();
      textPainter.paint(canvas, textElement.position);
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