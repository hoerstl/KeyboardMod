import 'package:flutter/material.dart' hide Key;
import 'package:xml/xml.dart';
import 'dart:io';
import 'package:flutter/services.dart' show rootBundle;
import 'package:file_picker/file_picker.dart';
import 'dart:convert';


Future<void> exportKeyboardProfile() async {
  print("Export Profile Selected!!!");

  final String jsonString = await rootBundle.loadString("data/exportTemplate.json");
  Map<String, dynamic> keyboardProfile = jsonDecode(jsonString);



  final root = Directory('../keyboardHook/keybindings'); // Replace with your path

  await for (var entity in root.list(recursive: true, followLinks: false)) {
    if (entity is File && entity.path.endsWith('.py')) {
      String fileName = entity.uri.pathSegments.last.replaceAll(RegExp(r'\.py$'), '');
      String fileContent = await entity.readAsString();
      String fullPath = entity.path;

      // Get the parent directory name
      String parentDir = Directory(fullPath).parent.uri.pathSegments
          .where((s) => s.isNotEmpty)
          .toList()
          .last;

      
      keyboardProfile[parentDir]![fileName]!["code"] = fileContent;
    }
  }

  await saveProfile(keyboardProfile);
}



Future<void> saveProfile(Map<String, dynamic> keyboardProfile) async {
  final outputPath = await FilePicker.platform.saveFile(
    dialogTitle: 'Save keyboard profile',
    fileName: 'keyboardProfile.json',
    type: FileType.custom,
    allowedExtensions: ['json'],
  );

  if (outputPath == null) {
    print('User canceled the save dialog.');
    return;
  } 
  final jsonString = jsonEncode(keyboardProfile);
  final file = File(outputPath);
  await file.writeAsString(jsonString);
  print('Saved JSON to $outputPath');
}



