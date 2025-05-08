import 'package:flutter/material.dart';

class Sidebar extends StatefulWidget {
  final Map<String, dynamic> sharedData;
  final void Function(List<dynamic>, dynamic) setSharedData;
  const Sidebar({super.key, required this.sharedData, required this.setSharedData});

  @override
  State<Sidebar> createState() => _SidebarState();
}

class _SidebarState extends State<Sidebar> {
  bool recentlyDeleted = false;



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
                          enabled: !keyData[keyboardMode]?[selectedKey]
                              ?["useDefaultFilepath"] ?? false,
                          controller: customFilepathController,
                          decoration: InputDecoration(
                            hintText: 'enter filepath to .py file...',
                            prefixIcon: IconButton(
                              icon: Icon(Icons.folder),
                              onPressed: () {
                                print("Selecting a file");
                              },
                            ),
                            border: OutlineInputBorder(),
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
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Expanded(child:ElevatedButton(
                          onPressed: () => {print("Editing")}, // TODO: Make this open the correct python file for editing
                          style: ElevatedButton.styleFrom(
                              backgroundColor:
                                  Theme.of(context).colorScheme.onSurface,
                              foregroundColor:
                                  Theme.of(context).colorScheme.surface,
                              shape: const RoundedRectangleBorder(
                                borderRadius: BorderRadius.only(
                                    topLeft: Radius.circular(10.0),
                                    bottomLeft: Radius.circular(10.0)),
                              )),
                          child: const Text("Edit",
                              style: TextStyle(
                                  fontSize: 25.0, letterSpacing: 1.0)),
                        )),
                        const SizedBox(width: 10.0),
                        Expanded(child: ElevatedButton(
                          onPressed: () => {setState(() {
                            recentlyDeleted = !recentlyDeleted;
                          })},
                          style: ElevatedButton.styleFrom(
                              backgroundColor:
                                  Theme.of(context).colorScheme.onSurface,
                              foregroundColor:
                                  Theme.of(context).colorScheme.surface,
                              shape: const RoundedRectangleBorder(
                                borderRadius: BorderRadius.only(
                                    topRight: Radius.circular(10.0),
                                    bottomRight: Radius.circular(10.0)),
                              )),
                          // minimumSize: Size(150, 50),
                          child: Text(recentlyDeleted ? "Undo" : "Delete",
                              style: TextStyle(
                                  fontSize: recentlyDeleted ? 25.0 : 20.0, letterSpacing: 1.0)),
                        )),
                      ],
                    ),
                  ),
                ],
              ),
            );
  }
}
