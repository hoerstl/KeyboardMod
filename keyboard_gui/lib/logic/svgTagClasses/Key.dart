import 'package:flutter/material.dart' hide Key;
import 'package:xml/xml.dart';

class Key { // We need to extend this from a rectangle property
  late String id;
  late String path;
  late String name;
  late double strokeWidth;
  late Color color;
  late Rect rect;
  
  Key(XmlElement element) {
    id = element.getAttribute('id').toString();
    path = element.getAttribute('d').toString();
    name = element.getAttribute('name').toString();
    String? strokeWidthStr = element.getAttribute("stroke-width");
    strokeWidth = 2.0;
    color = Color(int.parse("FF${element.getAttribute('stroke')?.toString().substring(1) ?? 'FFFFFF'}", radix: 16));
    List<double> coordinates = extractLTRBFromRect(element);
    rect = Rect.fromLTRB(coordinates[0], coordinates[1], coordinates[2], coordinates[3]);
  }

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
    return [L, T, R, B];
  }
}