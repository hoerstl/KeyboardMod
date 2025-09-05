import 'package:bitsdojo_window/bitsdojo_window.dart';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:keyboard_gui/logic/settingsMenu/exportProfile.dart';
import 'package:keyboard_gui/logic/settingsMenu/importProfile.dart';
import 'package:xml/xml.dart';
import 'dart:io';
import 'package:system_tray/system_tray.dart';

class settingsMenu extends StatefulWidget {
  final Map<String, dynamic> sharedData;
  final void Function(List<dynamic>, dynamic) setSharedData;

  const settingsMenu({super.key, required this.sharedData, required this.setSharedData});

  @override
  State<settingsMenu> createState() => _settingsMenuState();
}

class _settingsMenuState extends State<settingsMenu> {
  @override
  Widget build(BuildContext context) {
    return AnimatedPositioned(
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
      left: widget.sharedData["isSettingsVisible"] ? 0 : -250, // Adjust width here
      top: 0,
      bottom: 0,
      child: Container(
        width: 250,
        color: Colors.blueGrey[800],
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 20),
            Align(
              alignment: Alignment.topRight,
              child: IconButton(
                icon: const Icon(Icons.settings, color: Colors.white, size: 30),
                onPressed: () {
                  setState(() {
                    widget.setSharedData(["isSettingsVisible"], false);
                  });
                },
              ),
            ),
            const Padding(
              padding: EdgeInsets.all(16.0),
              child: Text(
                'Settings',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            const Divider(color: Colors.white54),
            ListTile(
              leading: const Icon(Icons.file_download, color: Colors.white),
              title: const Text('Import Profile', style: TextStyle(color: Colors.white)),
              onTap: () {importKeyboardProfile();},
            ),
            ListTile(
              leading: const Icon(Icons.file_upload, color: Colors.white),
              title: const Text('Export Profile', style: TextStyle(color: Colors.white)),
              onTap: () {exportKeyboardProfile();},
            ),
            ListTile(
              leading: const Icon(Icons.settings, color: Colors.white),
              title: const Text('TBD', style: TextStyle(color: Colors.white)),
              onTap: () {},
            ),
          ],
        ),
      ),
    );
  }
}

