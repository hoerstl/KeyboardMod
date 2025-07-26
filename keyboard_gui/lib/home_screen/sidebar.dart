import 'package:flutter/material.dart';
import 'dart:io';
import 'package:file_picker/file_picker.dart';

class Sidebar extends StatefulWidget {
  final Map<String, dynamic> sharedData;
  final void Function(List<dynamic>, dynamic) setSharedData;
  const Sidebar({super.key, required this.sharedData, required this.setSharedData});

  @override
  State<Sidebar> createState() => _SidebarState();
}

class _SidebarState extends State<Sidebar> {

  /// Creates the file if it doesn't exist, then opens it in the default .py editor
  void openOrCreatePythonFile(String filePath) async {
    final file = File(filePath);

    // Step 1: Create the file if it doesn't exist
    if (!await file.exists()) {
      await file.create(recursive: true);  // Also creates parent folders if needed
      await file.writeAsString('# Python script ran when "${widget.sharedData["selectedKey"]}" is pressed in ${widget.sharedData["keyboardMode"]} mode\n');
    }

    // Step 2: Open the file using default associated editor (like VS Code, PyCharm, Notepad++)
    await Process.start('cmd', ['/c', 'start', '', filePath]);
  }

  void editKeyBinding(){
    var keyData = widget.sharedData["keyData"];
    var selectedKey = widget.sharedData["selectedKey"];
    var keyboardMode = widget.sharedData["keyboardMode"];

    if (keyData[keyboardMode]?[selectedKey]?["useDefaultFilepath"] ?? true) {
      final filePath = '..\\keyboardHook\\keybindings\\$keyboardMode\\$selectedKey.py';
      openOrCreatePythonFile(filePath);
    }
    else {  
      // TODO: Set up error handling for when someone enters a nonsense customFilepath or a filepath in our current directory (".")
      final filePath = keyData[keyboardMode]?[selectedKey]?["customFilepath"];
      openOrCreatePythonFile(filePath);
    }
  }

  Future<void> selectPythonFile() async {
    var keyData = widget.sharedData["keyData"];
    var selectedKey = widget.sharedData["selectedKey"];
    var keyboardMode = widget.sharedData["keyboardMode"];

    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['py'],
    );

    if (result != null && result.files.single.path != null) {
      final filePath = result.files.single.path!;

      final regex = RegExp(r'^[a-zA-Z]:\\');  // Matches "C:\", "D:\", etc.
      bool isAbsolutePath = regex.hasMatch(filePath);
      if (filePath.toLowerCase().endsWith('.py') && isAbsolutePath) {
        widget.setSharedData(["keyData", keyboardMode, selectedKey, "customFilepath"], filePath);
        // keyData[keyboardMode]?[selectedKey]?["customFilepath"] = filePath;
        // Proceed with open or edit logic
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Please select a valid .py file.', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            backgroundColor: Colors.red,
            duration: Duration(seconds: 3),
          ),
        );
      }
    }}

  @override
  Widget build(BuildContext context) {

    var keyData = widget.sharedData["keyData"];
    var selectedKey = widget.sharedData["selectedKey"];
    var keyboardMode = widget.sharedData["keyboardMode"];


    TextEditingController customFilepathController = TextEditingController(
        text: keyData[keyboardMode]?[selectedKey]?["customFilepath"]);
    TextStyle sidebarTextStyle = TextStyle(
          fontSize: 15.0, color: Theme.of(context).colorScheme.onSurface);

    return Container(
              padding: const EdgeInsets.all(20.0),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.surfaceContainer,
                border: Border(
                    left: BorderSide(
                        width: 2.0,
                        color: Theme.of(context).colorScheme.shadow)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Center(
                    child: Text(
                      'Binding $selectedKey',
                      style: const TextStyle(
                        fontSize: 25.0,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  Divider(
                    height: 20.0,
                    thickness: 2.0,
                    color: Theme.of(context).colorScheme.outline,
                  ),
                  Container(
                    margin: EdgeInsets.fromLTRB(0.0, 0.0, 0.0, 5.0),
                    child: Row(
                      children: [
                        Checkbox(
                            value: keyData[keyboardMode]?[selectedKey]?["Enabled"] ?? false,
                            onChanged: (val) {
                              if ((keyData.containsKey(keyboardMode) && keyData[keyboardMode].containsKey(selectedKey)) != null) {
                                widget.setSharedData(["keyData", keyboardMode, selectedKey, "Enabled"], val);
                                keyData[keyboardMode]![selectedKey]!["Enabled"] = val;
                              }
                            }),
                        Text("Enable", style: sidebarTextStyle)
                      ],
                    ),
                  ),
                  Row(
                    children: [
                      Radio(
                        value: true,
                        groupValue: keyData[keyboardMode]?[selectedKey]
                            ?["useDefaultFilepath"] ?? false,
                        onChanged: (val) {
                          setState(() {
                            keyData[keyboardMode]?[selectedKey]
                                ?["useDefaultFilepath"] = val;
                          });
                        },
                      ),
                      Text("Use Default Filepath", style: sidebarTextStyle),
                    ],
                  ),
                  Row(
                    children: [
                      Radio(
                        value: false,
                        groupValue: keyData[keyboardMode]?[selectedKey]
                            ?["useDefaultFilepath"] ?? false,
                        onChanged: (val) {
                          setState(() {
                            keyData[keyboardMode]?[selectedKey]
                                ?["useDefaultFilepath"] = val;
                          });
                        },
                      ),
                      Text("Use Custom Filepath", style: sidebarTextStyle),
                    ],
                  ),
                  SizedBox(height: 5.0),
                  Row(
                    children: [
                      const SizedBox(width: 40.0),
                      Expanded(
                        child: TextField(
                          enabled: !(keyData[keyboardMode]?[selectedKey]
                              ?["useDefaultFilepath"] ?? true),
                          readOnly: true,
                          onTap: selectPythonFile,
                          controller: customFilepathController,
                          decoration: InputDecoration(
                            hintText: 'Select File',
                            prefixIcon: IconButton(
                              icon: const Icon(Icons.folder),
                              onPressed: selectPythonFile
                            ),
                            border: const OutlineInputBorder(),
                          ),
                          onChanged: (text) {
                            keyData[keyboardMode]?[selectedKey]
                                ?["customFilepath"] = text;
                          },
                        ),
                      )
                    ],
                  ),
                  Expanded(child: Container()),
                  Container(
                    margin: const EdgeInsets.fromLTRB(0.0, 0.0, 0.0, 10.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        ElevatedButton(
                          onPressed: () => {editKeyBinding()},
                          style: ElevatedButton.styleFrom(
                              backgroundColor:
                                  Theme.of(context).colorScheme.onSurface,
                              foregroundColor:
                                  Theme.of(context).colorScheme.surface,
                              shape: const RoundedRectangleBorder(
                                borderRadius: BorderRadius.all(Radius.circular(5.0)),
                              )),
                          child: const Text("Edit",
                              style: TextStyle(
                                  fontSize: 25.0, letterSpacing: 1.0)),
                        ),
                        const SizedBox(height: 3.0)
                      ],
                    ),
                  ),
                ],
              ),
            );
  }
}




