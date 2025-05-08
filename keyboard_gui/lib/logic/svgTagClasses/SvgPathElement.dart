import 'package:flutter/material.dart' hide Key;
import 'package:xml/xml.dart';
import 'SvgElement.dart';
import 'package:path_drawing/path_drawing.dart';


class SvgPathElement extends SvgElement {
  late final XmlDocument? xmlDocument;
  late final double x;
  late final double y;
  late final Path path;
  late final Color stroke;
  late final Matrix4 matrixTransform;

  SvgPathElement(XmlElement element, [this.xmlDocument]) {
    List<double> pathltrb = getLTRBFromElement(element, xmlDocument);
    x = pathltrb[0];
    y = pathltrb[1];
    path = getPath(element);
    stroke = Color(int.parse("FF${element.getAttribute('stroke')?.toString().substring(1) ?? 'FFFFFF'}", radix: 16));
    matrixTransform = parseSvgMatrixTransform(element);
  }

  Path getPath(XmlElement element){
    final String? d = element.getAttribute("d");
    if (d == null){
      throw "This path tag doesn't have a path data ('d') attribute";
    }
    return parseSvgPathData(d);
  }

  Matrix4 parseSvgMatrixTransform(XmlElement element) {
    Matrix4 ancestorMatrix = Matrix4.identity();
    if (xmlDocument != null) {
      XmlElement? parentGroup = getParentGroup(xmlDocument!, element);
      if (parentGroup != null){
        ancestorMatrix = parseSvgMatrixTransform(parentGroup);
      }
    }

    final transform = element.getAttribute("transform");
    if (transform == null || !transform.contains("matrix")) {
      Matrix4 matrix = Matrix4.identity();
      if (transform != null){
        RegExp regex = RegExp(r'translate\(([^,]+),\s*([^)]+)\)');
        RegExpMatch? match = regex.firstMatch(transform);
        if (match != null) {
          matrix.setEntry(0, 3, double.parse(match.group(1)!)); // m03 = translate X
          matrix.setEntry(1, 3, double.parse(match.group(2)!)); // m13 = translate Y
        }  
      }
      
      return ancestorMatrix.multiplied(matrix);
    }

    final match = RegExp(r'matrix\(([^)]+)\)').firstMatch(transform);
    if (match == null) return Matrix4.identity();

    final values = match.group(1)!
        .split(RegExp(r'[ ,]+'))
        .map(double.parse)
        .toList();

    if (values.length != 6) {
      throw FormatException('Expected 6 values in matrix(), got: $values');
    }

    final a = values[0]; // scale X or flip X
    final b = values[1]; // skew Y
    final c = values[2]; // skew X
    final d = values[3]; // scale Y or flip Y
    final e = values[4]; // translate X
    final f = values[5]; // translate Y

    final matrix = Matrix4.identity();

    // Populate the matrix correctly
    matrix.setEntry(0, 0, a); // m00
    matrix.setEntry(0, 1, c); // m01 (skew X)
    matrix.setEntry(1, 0, b); // m10 (skew Y)
    matrix.setEntry(1, 1, d); // m11
    matrix.setEntry(0, 3, e); // m03 = translate X
    matrix.setEntry(1, 3, f); // m13 = translate Y

    Matrix4 combinedMatrix = ancestorMatrix.multiplied(matrix);

    return combinedMatrix;
  }


}


