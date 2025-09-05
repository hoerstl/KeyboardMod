import 'dart:convert';
import 'dart:io';
import 'package:path/path.dart' as p;
import 'package:file_picker/file_picker.dart';

/// Hard‑coded base path where you want your .py files written.
/// e.g. '/Users/you/projects/keyboardHook/keybindings'
const String baseFolder = '../keyboardHook/keybindings';

Future<void> importKeyboardProfile() async {
  // 1) Let user pick a .json file
  final result = await FilePicker.platform.pickFiles(
    dialogTitle: 'Select keyboard profile JSON',
    type: FileType.custom,
    allowedExtensions: ['json'],
  );
  if (result == null || result.files.single.path == null) {
    print('User cancelled import.');
    return;
  }
  final jsonPath = result.files.single.path!;
  
  // 2) Read & decode
  final jsonString = await File(jsonPath).readAsString();
  final Map<String, dynamic> profile = jsonDecode(jsonString);

  // 3) Iterate
  for (final subfolderEntry in profile.entries) {
    final String subfolderName = subfolderEntry.key;
    final dynamic fileMapDynamic = subfolderEntry.value;
    if (fileMapDynamic is! Map<String, dynamic>) continue;

    // 4) Ensure the subfolder exists under your base
    final targetDir = Directory(p.join(baseFolder, subfolderName));
    if (!await targetDir.exists()) {
      await targetDir.create(recursive: true);
    }

    // 5) Write each file
    for (final fileEntry in fileMapDynamic.entries) {
      final String fileNameNoExt = fileEntry.key;
      final dynamic fileData = fileEntry.value;
      if (fileData is! Map<String, dynamic> || fileData['code'] is! String) {
        continue;
      }
      final String code = fileData['code'];
      if (code == "") {
        continue;
      }

      final outFile =
          File(p.join(targetDir.path, '$fileNameNoExt.py'));
      await outFile.writeAsString(code);
      print('Wrote ${outFile.path}');
    }
  }

  print('Import complete!');
}
