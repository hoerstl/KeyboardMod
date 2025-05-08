import 'package:xml/xml.dart';

abstract class SvgElement {
  List<double> getLTRBFromElement(XmlElement element, [XmlDocument? xmlDocument]){
    double ancestorX = 0;
    double ancestorY = 0;
    if (xmlDocument != null){
      XmlElement? parentGroup = getParentGroup(xmlDocument, element);
      if (parentGroup != null){
        List<double> groupLTRB = getLTRBFromElement(parentGroup, xmlDocument);
        ancestorX += groupLTRB[0];
        ancestorY += groupLTRB[1];
      }
    }
    

    final transform = element.getAttribute('transform');
    double x = 0.0;
    double y = 0.0;
    if (transform != null){
      RegExp regex = RegExp(r'translate\(([^,]+),\s*([^)]+)\)');
      RegExpMatch? match = regex.firstMatch(transform);
      if (match == null) {
        regex = RegExp(r'matrix\([-\d.eE\s,]*?([-\d.eE]+)[\s,]+([-\d.eE]+)\)');
        match = regex.firstMatch(transform);
        if (match == null){
          throw FormatException("This element's transform property does not match either expected format: '${element.getAttribute('transform')}'");
        }
      }  
      x = double.parse(match.group(1)!);
      y = double.parse(match.group(2)!);
    }
    
    // Parse the numbers and return them as a list
    final L = x + ancestorX;
    final T = y + ancestorY;
    final R = L + double.parse(element.getAttribute("width") ?? "0");
    final B = T + double.parse(element.getAttribute("height") ?? "0");
    return [L, T, R, B];
  }

  XmlElement? getParentGroup(XmlDocument svgXml, XmlElement element) {
    final elementID = element.getAttribute("id");
    if (elementID == null){
      throw const FormatException("This element does not have an id attribute to use in finding any parent groups");
    }
    List<XmlElement> ancestorGroups = svgXml.findAllElements('g').where((gElement) {
        return gElement.descendants.whereType<XmlElement>().any((path) =>
          path.getAttribute('id') == elementID
        );
      }).toList();
    
    if (ancestorGroups.isNotEmpty){
      return ancestorGroups[0];
    }
    return null;
  }
}