import 'dart:ffi';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:flutter/services.dart' show rootBundle;


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
      title: 'Keyboard Mod',
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
  
  var keyData;

  late Map<String, dynamic> sharedData;

  Future<void> loadKeyData() async {
    final String jsonString = await rootBundle.loadString('data/keyData.json');
    var data = jsonDecode(jsonString);
    keyData = data; 
    print("loaded keyData:");
    print(keyData); 
  }

  void setSharedData(List keys, var value ){
    setState(() {
      dynamic data = sharedData;
      for (int i = 0; i < keys.length; i++){
        if (data.containsKey(keys[i])){
          if (i == keys.length - 1){
            data[keys[i]] = value;
          }
          data = data[keys[i]];
        } else {
          throw StateError('KeyError: The key "${keys[i]}" does not exist in the map.');
        }
      }
    });
  }

  Future<void> loadSharedData() async {
    await loadKeyData();
    sharedData = {
      "selectedKey": "W",
      "keyboardMode": "Default",
      "keyData": keyData
    };
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return FutureBuilder(
      future: loadSharedData(), // The async method that loads your data
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          // Show a loading indicator while waiting for the future
          return const Scaffold(
            body: Center(
              child: CircularProgressIndicator(),
            ),
          );
        } else if (snapshot.hasError) {
          // Handle errors gracefully
          return Scaffold(
            body: Center(
              child: Text('Error loading data: ${snapshot.error}'),
            ),
          );
        } else {
          // Once the data is loaded, build the main UI
          return buildMainUI();
        }
      },
    );
  }

  Widget buildMainUI(){
    var keyboardMode = sharedData["keyboardMode"];
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
            child: Sidebar(sharedData: sharedData, setSharedData: setSharedData)),
      ],
    ));
  }
}





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
                            value: keyData[keyboardMode]?[selectedKey]?["Enabled"] ?? false,
                            onChanged: (val) {
                              if (keyData.containsKey(keyboardMode) && keyData[keyboardMode]?.containsKey(selectedKey) != null) {
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
                              style: const TextStyle(
                                  fontSize: 30.0, letterSpacing: 1.0)),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            );
  }
}
