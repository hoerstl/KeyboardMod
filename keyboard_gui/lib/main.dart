import 'package:bitsdojo_window/bitsdojo_window.dart';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:keyboard_gui/home_screen/settingsMenu.dart';
import 'package:xml/xml.dart';
import 'home_screen/main_ui.dart';
import 'home_screen/sidebar.dart';
import 'dart:io';
import 'package:system_tray/system_tray.dart';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await _MyHomePageState.loadAsyncData();
  WidgetsFlutterBinding.ensureInitialized();
  await initSystemTray();

  runApp(const MyApp());
  // Ensure minimum window size after the app starts
  doWhenWindowReady(() {
    const initialSize = Size(1300, 700);
    appWindow.minSize = initialSize;
    appWindow.size = initialSize;
    appWindow.alignment = Alignment.center;
    // appWindow.title = "keyboard mod";
    appWindow.show();
  });
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  bool isSidebarVisible = false; // TODO: Rename this variable to isSettingsVisible
  
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Keyboard Mod',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Color.fromARGB(255, 241, 0, 253),
          brightness: Brightness.dark,
        ).copyWith(),
        useMaterial3: true,
      ),
      home: Scaffold(
          body: WindowBorder(
              color: Colors.white,
              width: 1,
              child: Column(children: [
                WindowTitleBarBox(
                    child: Row(children: [
                  Expanded(child: MoveWindow()),
                  WindowButtons()
                ])),
                Expanded(
                  child: MyHomePage(),
                )
                ]))),
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
    XmlDocument keyboardSVG = XmlDocument.parse(
        await rootBundle.loadString("assets/svg/keyboard.svg"));

    sharedData = {
      "selectedKey": "W",
      "keyboardMode": "Default",
      "keyData": keyData,
      "keyboardSVG": keyboardSVG,
      "isSettingsVisible": false,
    };
  }

  void setSharedData(List keys, var value) {
    setState(() {
      dynamic data = sharedData;
      for (int i = 0; i < keys.length; i++) {
        if (data.containsKey(keys[i])) {
          if (i == keys.length - 1) {
            data[keys[i]] = value;
          }
          data = data[keys[i]];
        } else {
          throw StateError(
              'KeyError: The key "${keys[i]}" does not exist in the map.');
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
          Scaffold(
            body: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Expanded(
                flex: 10,
                child: main_ui(
                    context: context,
                    sharedData: sharedData,
                    setSharedData: setSharedData)),
            Expanded(
                flex: 3,
                child:
                    Sidebar(sharedData: sharedData, setSharedData: setSharedData)),
          ],
        )),
        // Settings Menu
        settingsMenu(sharedData: sharedData, setSharedData: setSharedData),
        // Settings Icon
        if (!sharedData["isSettingsVisible"])
          Positioned(
            top: 20,
            left: 20,
            child: IconButton(
              icon: const Icon(Icons.settings, color: Colors.white, size: 30),
              onPressed: () {
                setState(() {
                  setSharedData(["isSettingsVisible"], true);
                });
              },
            ),
          ),
      ],
    );
  }
}

final buttonColors = WindowButtonColors(
    iconNormal: const Color(0xFF805306),
    mouseOver: const Color(0xFFF6A00C),
    mouseDown: const Color(0xFF805306),
    iconMouseOver: const Color(0xFF805306),
    iconMouseDown: const Color(0xFFFFD500));

final closeButtonColors = WindowButtonColors(
    mouseOver: const Color(0xFFD32F2F),
    mouseDown: const Color(0xFFB71C1C),
    iconNormal: const Color(0xFF805306),
    iconMouseOver: Colors.white);

class WindowButtons extends StatelessWidget {
  const WindowButtons({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        MinimizeWindowButton(colors: buttonColors),
        MaximizeWindowButton(colors: buttonColors),
        CloseWindowButton(colors: closeButtonColors, onPressed: () => {appWindow.hide()}),
      ],
    );
  }
}

Future<void> initSystemTray() async {
  String path = 'assets/icon/icon.ico'; //TODO: Replace this icon with one I've made myself

  final AppWindow appWindow = AppWindow();
  final SystemTray systemTray = SystemTray();

  // We first init the systray menu
  await systemTray.initSystemTray(
    title: "system tray",
    iconPath: path,
  );

  // create context menu
  final Menu menu = Menu();
  await menu.buildFrom([
    // MenuItemLabel(label: 'Keyboard Mod', enabled: false),
    // MenuSeparator(),
    MenuItemLabel(label: 'Show', onClicked: (menuItem) => appWindow.show()),
    MenuItemLabel(label: 'Hide', onClicked: (menuItem) => appWindow.hide()),
    MenuItemLabel(label: 'Exit', onClicked: (menuItem) => appWindow.close()),
  ]);

  // set context menu
  await systemTray.setContextMenu(menu);

  // handle system tray event
  systemTray.registerSystemTrayEventHandler((eventName) {
    if (eventName == kSystemTrayEventClick) {
       Platform.isWindows ? appWindow.show() : systemTray.popUpContextMenu();
    } else if (eventName == kSystemTrayEventRightClick) {
       Platform.isWindows ? systemTray.popUpContextMenu() : appWindow.show();
    }
  });
}

