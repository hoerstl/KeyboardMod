import 'dart:ffi';

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_svg/flutter_svg.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // TRY THIS: Try running your application with "flutter run". You'll see
        // the application has a purple toolbar. Then, without quitting the app,
        // try changing the seedColor in the colorScheme below to Colors.green
        // and then invoke "hot reload" (save your changes or press the "hot
        // reload" button in a Flutter-supported IDE, or press "r" if you used
        // the command line to start the app).
        //
        // Notice that the counter didn't reset back to zero; the application
        // state is not lost during the reload. To reset the state, use hot
        // restart instead.
        //
        // This works for code too, not just values: Most code changes can be
        // tested with just a hot reload.
        colorScheme: ColorScheme.fromSeed(
          seedColor: Color.fromARGB(255, 241, 0, 253),
          brightness: Brightness.dark,
        ).copyWith(),

        // ColorScheme.dark(
        //   primary: Color.fromARGB(255, 112, 112, 112),
        //   secondary: Color.fromARGB(255, 82, 82, 82),
        //   background: Color.fromARGB(255, 72, 72, 72),
        //   surface: Color.fromARGB(255, 72, 72, 72),
        //   inversePrimary: Color.fromARGB(255, 200, 200, 200),
        //   outline: Colors.grey[200],
        // ),
        useMaterial3: true,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;
  String selectedKey = "W";
  String keyboardMode = "Default";
  bool recentlyDeleted = false;

  Map<String, Map<String, Map<String, dynamic>>> keyData = {
    "Default": {
      "W": {
        "Enabled": true,
        "useDefaultFilepath": true,
        "customFilepath": "",
      },
    },
    "Caps Lock": {},
    "Shift": {},
    "Ctrl": {},
    "Alt": {},
  };

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.



    TextEditingController customFilepathController = TextEditingController(
        text: keyData[keyboardMode]?[selectedKey]?["customFilepath"]);
    TextStyle sidebarTextStyle = TextStyle(
        fontSize: 15.0, color: Theme.of(context).colorScheme.onSurface);

    return Scaffold(
        body: Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Expanded(
          flex: 10,
          child: Center(
            child: Column(
            children: [
              Expanded(
                flex: 1,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(keyboardMode,
                        style: const TextStyle(
                          fontSize: 40.0,
                          fontWeight: FontWeight.bold,
                        )),
                    const Text("Mode",
                        style: TextStyle(
                          fontSize: 40.0,
                          fontWeight: FontWeight.bold,
                        )),
                  ],
                ),
              ),
              Expanded(flex: 2, child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 50),
                child: FittedBox(
                  child: SvgPicture.asset("assets/svg/keyboard.svg", 
                  height: 120,
                  width: 312,
                  fit: BoxFit.fill
                )
                        ,),
              )),
              Expanded(flex: 1, child: Container()),
            ],
          )),
        ),
        Expanded(
            flex: 3,
            child: Container(
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
                      'Binding $selectedKey in $keyboardMode',
                      style: const TextStyle(
                        fontSize: 30.0,
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
                            value: keyData[keyboardMode]?[selectedKey]
                                    ?['Enabled'] ??
                                false,
                            onChanged: (val) {
                              setState(() {
                                if (keyData.containsKey(keyboardMode) &&
                                    keyData[keyboardMode]
                                            ?.containsKey(selectedKey) !=
                                        null) {
                                  keyData[keyboardMode]![selectedKey]![
                                      'Enabled'] = val;
                                }
                              });
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
                            ?["useDefaultFilepath"],
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
                            ?["useDefaultFilepath"],
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
                              ?["useDefaultFilepath"],
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
                    margin: EdgeInsets.fromLTRB(0.0, 0.0, 0.0, 10.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        ElevatedButton(
                          onPressed: () => {print("Editing")},
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
                                  fontSize: 30.0, letterSpacing: 1.0)),
                        ),
                        const SizedBox(width: 10.0),
                        ElevatedButton(
                          onPressed: () => {setState(() {
                            print("Deleted");
                            recentlyDeleted = ! recentlyDeleted;
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
                          child: Text(recentlyDeleted ? "Undo" : "Delete",
                              style: TextStyle(
                                  fontSize: 30.0, letterSpacing: 1.0)),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            )),
      ],
    ));
  }
}
