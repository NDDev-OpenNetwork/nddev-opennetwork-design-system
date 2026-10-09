import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:nddev_opennetwork_design_system/opennetwork_design_system.dart';

void main() {
  test('exposes the OpenNetwork dark theme and core tokens', () {
    expect(OpenNetworkTheme.dark().brightness, Brightness.dark);
    expect(OpenNetworkColors.accentCyan.toARGB32(), 0xFF58D6FF);
  });
}
