import 'package:flutter/material.dart' hide Key;
import 'package:xml/xml.dart';
import 'SvgElement.dart';

// TODO: add italics and bold styling options to text elements
class SvgTextElement extends SvgElement {
  late final XmlDocument? xmlDocument;
  late final double x; // Extracted from the transform property
  late final double y; // Extracted from the transform property and the dy property on the spans
  late final double fontSize;
  late final String fontFamily;
  late final bool italicized;
  late final bool bold;
  late final Color fill;
  late final String name;
  late final String content;

  SvgTextElement(XmlElement element, [this.xmlDocument]) {
    List<double> ltrb = getLTRBFromElement(element, xmlDocument);
    x = ltrb[0];
    y = ltrb[1];
    fontSize = getFontSizeFromElement(element);
    fontFamily = getFontFamilyFromElement(element);
    italicized = RegExp(r'font-style: italic;').firstMatch(element.getAttribute('style')!) != null;
    bold = RegExp(r'font-weight: bold;').firstMatch(element.getAttribute('style')!) != null;
    fill = Color(int.parse("FF${element.getAttribute('fill')?.toString().substring(1) ?? 'FFFFFF'}", radix: 16));
    name = element.getAttribute("name")!;
    content = getTextFromElement(element);
  }

  static double getFontSizeFromElement(XmlElement element){
    final match = RegExp(r'font-size:\s*([^;^\s]*)').firstMatch(element.getAttribute('style')!);

    if (match == null) {
      throw FormatException("This element's style property does not match the expected format: '${element.getAttribute('style')}'");
    } 
    // Parse the numbers and return them as a list
    return double.parse(match.group(1)!);
  }

  static String getFontFamilyFromElement(XmlElement element){
    final match = RegExp(r'font-family:\s*([^;^\s]*)').firstMatch(element.getAttribute('style')!);

    if (match == null) {
      throw FormatException("This element's style property does not match the expected format: '${element.getAttribute('style')}'");
    } 
    // Parse the numbers and return them as a list
    return match.group(1)!;
  }

  static String getTextFromElement(XmlElement element){
    // Get all child <tspan> nodes
    var tspanNodes = element.findAllElements("tspan");

    // Extract and combine the text content
    var displayedText = List.from(tspanNodes)
      .map((e) => e.text.trim()) // Get and clean text content
      .join("\n"); // Combine all into a single string
    return displayedText;
  }
}