import 'package:flutter/material.dart' hide Key;
import 'package:xml/xml.dart';
import 'SvgElement.dart';

class Key extends SvgElement { // We need to extend this from a rectangle property
  late XmlDocument? xmlDocument;
  late String id;
  late String path;
  late String name;
  late double strokeWidth;
  late Color color;
  late Rect rect;
  
  Key(XmlElement element, [this.xmlDocument]) {
    id = element.getAttribute('id').toString();
    path = element.getAttribute('d').toString();
    name = element.getAttribute('name').toString();
    strokeWidth = double.parse(element.getAttribute("stroke-width")!);
    strokeWidth = 2.0; // Override since it's too thin
    color = Color(int.parse("FF${element.getAttribute('stroke')?.toString().substring(1) ?? 'FFFFFF'}", radix: 16));
    List<double> coordinates = getLTRBFromElement(element, xmlDocument);
    rect = Rect.fromLTRB(coordinates[0], coordinates[1], coordinates[2], coordinates[3]);
  }
}