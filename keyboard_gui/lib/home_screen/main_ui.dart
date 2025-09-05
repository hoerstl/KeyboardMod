import 'dart:math';

import 'package:flutter/material.dart';
import '../logic/keyPicker/keyPicker.dart';
import 'package:google_fonts/google_fonts.dart';
import 'SubtleDropdown.dart';

Widget main_ui(
    {required BuildContext context,
    required sharedData,
    required setSharedData}) {
  var keyboardMode = sharedData["keyboardMode"];
  return Center(
      child: Column(
    children: [
      Expanded(
        flex: 1,
        child: LayoutBuilder(
          builder: (context, constraints) {
            final double maxWidth = constraints.maxWidth;
            final double maxHeight = constraints.maxHeight;
            

            final double scale = min((maxWidth / 998), (maxHeight / 167));

            TextStyle modeStyle = GoogleFonts.butterflyKids(textStyle: TextStyle(
                              fontSize: 80.0 * scale,
                            ));

            return Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                SubtleDropdown(
                    value: keyboardMode,
                    options: const ["Default", "Caps Lock", "Shift", "Ctrl", "Alt"],
                    style: modeStyle.copyWith(decoration: TextDecoration.underline),
                    onChanged: (newValue) {
                      setSharedData(["keyboardMode"], newValue);
                    }),
                SizedBox(width: 30 * scale),
                Text("Mode",
                    style: modeStyle),
              ],
            );
          })),
      Expanded(
          flex: 2,
          child: Center( child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 50),
              child: KeyPicker(
                  sharedData: sharedData, setSharedData: setSharedData)))),
      Expanded(flex: 1, child: Container()),
    ],
  ));
}
