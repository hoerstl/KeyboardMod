import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../logic/keyPicker/keyPicker.dart';

Widget main_ui({required BuildContext context, required sharedData, required setSharedData}){
  var keyboardMode = sharedData["keyboardMode"];
  return Center(
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
                  child: keyPicker(sharedData: sharedData, setSharedData: setSharedData)
                //   SvgPicture.asset("assets/svg/keyboard.svg", 
                //   height: 120,
                //   width: 312,
                //   fit: BoxFit.fill
                // )
                ),
              )),
              Expanded(flex: 1, child: Container()),
            ],
          ));
}