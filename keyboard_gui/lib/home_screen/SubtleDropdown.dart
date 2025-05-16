import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class SubtleDropdown extends StatefulWidget {
  final String value;
  final List<String> options;
  final TextStyle style;
  final void Function(String) onChanged;

  const SubtleDropdown({
    super.key,
    required this.value,
    required this.options,
    required this.style,
    required this.onChanged,
  });

  @override
  State<SubtleDropdown> createState() => _SubtleDropdownState();
}

class _SubtleDropdownState extends State<SubtleDropdown> {
  bool _isHovering = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovering = true),
      onExit: (_) => setState(() => _isHovering = false),
      child: PopupMenuButton<String>(
        onSelected: widget.onChanged,
        itemBuilder: (context) => widget.options.map((option) {
          return PopupMenuItem(
            value: option,
            child: Text(option, style: GoogleFonts.butterflyKids(textStyle: TextStyle(
                              fontSize: widget.style.fontSize! * .5,
                            ))),
          );
        }).toList(),
        padding: EdgeInsets.zero,
        offset: Offset(0, widget.style.fontSize! * 1.1),
        // Prevents the default button splash on hover/click
        splashRadius: 0,
        tooltip: '',
        child: Text(
          widget.value,
          style: widget.style
          // TextStyle(
          //   fontSize: 16,
          //   color: _isHovering ? Colors.blue : Colors.white,
          //   decoration: _isHovering ? TextDecoration.underline : null,
          // ),
        ),
      ),
    );
  }
}
