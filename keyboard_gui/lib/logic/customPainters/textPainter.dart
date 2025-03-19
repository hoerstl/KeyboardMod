import 'package:flutter/material.dart';
import 'package:xml/xml.dart';

class SvgTextPainter extends CustomPainter {
  final List<SvgTextElement> textElements;

  SvgTextPainter(this.textElements);

  @override
  void paint(Canvas canvas, Size size) {
    for (final element in textElements) {
      final textSpan = TextSpan(
        text: element.content,
        style: TextStyle(
          color: Color(int.parse("0xFF$element.fill.substring(1)", radix: 16)),
          fontSize: element.fontSize,
        ),
      );

      final textPainter = TextPainter(
        text: textSpan,
        textDirection: TextDirection.ltr,
      );

      textPainter.layout();

      final offset = Offset(element.x, element.y - textPainter.height);
      textPainter.paint(canvas, offset);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true; // Repaint every time, if needed.
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