import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:xml/xml.dart';
import 'home_screen/main_ui.dart';
import 'home_screen/sidebar.dart';


void main() async{
  WidgetsFlutterBinding.ensureInitialized();
  await _MyHomePageState.loadAsyncData();
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

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  
  static late Map<String, dynamic> sharedData;

  static Future<void> loadAsyncData() async {
    final String jsonString = await rootBundle.loadString('data/keyData.json');
    var keyData = jsonDecode(jsonString);
    XmlDocument keyboardSVG = XmlDocument.parse(await rootBundle.loadString("assets/svg/keyboard.svg"));

    sharedData = {
      "selectedKey": "W",
      "keyboardMode": "Default",
      "keyData": keyData,
      "keyboardSVG": keyboardSVG
    };
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Expanded(
          flex: 10,
          child: main_ui(context: context, sharedData: sharedData, setSharedData: setSharedData)
        ),
        Expanded(
            flex: 3,
            child: Sidebar(sharedData: sharedData, setSharedData: setSharedData)),
      ],
    ));
  }
}


